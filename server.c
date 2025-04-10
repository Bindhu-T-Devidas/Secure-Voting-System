#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <openssl/aes.h>
#include <openssl/pem.h>
#include <openssl/rsa.h>
#include <openssl/err.h>
#include <openssl/bio.h>
#include <mysql/mysql.h>

#define PORT 8080
#define MAX_CLIENTS 10
#define AES_BLOCK_SIZE 16

pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;
MYSQL *conn;

RSA *load_private_key(const char *filename) {
    FILE *fp = fopen(filename, "r");
    if (!fp) {
        perror("Cannot open private.pem");
        exit(1);
    }
    RSA *rsa = PEM_read_RSAPrivateKey(fp, NULL, NULL, NULL);
    fclose(fp);
    return rsa;
}

char *base64_encode(const unsigned char *input, int length) {
    BIO *bmem = NULL, *b64 = NULL;
    BUF_MEM *bptr;
    b64 = BIO_new(BIO_f_base64());
    bmem = BIO_new(BIO_s_mem());
    b64 = BIO_push(b64, bmem);
    BIO_set_flags(b64, BIO_FLAGS_BASE64_NO_NL);
    BIO_write(b64, input, length);
    BIO_flush(b64);
    BIO_get_mem_ptr(b64, &bptr);
    char *buff = malloc(bptr->length + 1);
    memcpy(buff, bptr->data, bptr->length);
    buff[bptr->length] = '\0';
    BIO_free_all(b64);
    return buff;
}

void *handle_client(void *client_socket) {
    int sock = *(int *)client_socket;
    free(client_socket);

    RSA *rsa = load_private_key("private.pem");
    unsigned char encrypted_key[256];
    read(sock, encrypted_key, sizeof(encrypted_key));

    unsigned char session_key[16];
    int decrypted_len = RSA_private_decrypt(256, encrypted_key, session_key, rsa, RSA_PKCS1_OAEP_PADDING);
    if (decrypted_len == -1) {
        ERR_print_errors_fp(stderr);
        RSA_free(rsa);
        close(sock);
        return NULL;
    }

    unsigned char encrypted_vote_raw[16];
    int valread = read(sock, encrypted_vote_raw, 16);
    if (valread == 16) {
        char username[50] = {0};
        read(sock, username, sizeof(username));

        char query[256];
        sprintf(query, "SELECT id FROM users2 WHERE username='%s'", username);
        mysql_query(conn, query);
        MYSQL_RES *res = mysql_store_result(conn);
        MYSQL_ROW row = mysql_fetch_row(res);
        int user_id = row ? atoi(row[0]) : -1;
        mysql_free_result(res);

        if (user_id != -1) {
            char *encoded_vote = base64_encode(encrypted_vote_raw, 16);
            char *encoded_key = base64_encode(session_key, 16);

            pthread_mutex_lock(&lock);
            sprintf(query, "INSERT INTO votes3 (encrypted_vote, user_id, session_key) VALUES ('%s', %d, '%s')", encoded_vote, user_id, encoded_key);
            mysql_query(conn, query);
            pthread_mutex_unlock(&lock);

            printf("✅ Vote from %s stored.\n", username);
            free(encoded_vote);
            free(encoded_key);
        }
    }

    RSA_free(rsa);
    close(sock);
    return NULL;
}

int main() {
    int server_fd, new_socket, *new_sock;
    struct sockaddr_in address;
    int addrlen = sizeof(address);

    conn = mysql_init(NULL);
    if (!mysql_real_connect(conn, "localhost", "root", "", "votingDB", 0, NULL, 0)) {
        fprintf(stderr, "❌ MySQL Connection Failed\n");
        exit(1);
    }

    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) {
        perror("❌ Socket failed");
        exit(1);
    }

    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);

    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0) {
        perror("❌ Bind failed");
        exit(1);
    }

    if (listen(server_fd, MAX_CLIENTS) < 0) {
        perror("❌ Listen failed");
        exit(1);
    }

    printf("🚀 Secure Voting Server Started on port %d...\n", PORT);

    while ((new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t*)&addrlen))) {
        pthread_t thread;
        new_sock = malloc(sizeof(int));
        *new_sock = new_socket;
        pthread_create(&thread, NULL, handle_client, (void *)new_sock);
        pthread_detach(thread);
    }

    mysql_close(conn);
    return 0;
}
