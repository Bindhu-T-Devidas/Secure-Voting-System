import socket
import tkinter as tk
from tkinter import messagebox, simpledialog
import mysql.connector
import base64
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes
import bcrypt

SERVER_IP = "127.0.0.1"
PORT = 8080
session_key = None
logged_in_user = None
logged_in_user_id = None

# Connect to MySQL
db = mysql.connector.connect(host="localhost", user="root", password="", database="votingDB")
cursor = db.cursor()

# -------- Check user existence --------
def check_user_exists(username):
    cursor.execute("SELECT * FROM users2 WHERE username=%s", (username,))
    return cursor.fetchone()

# -------- Signup screen logic --------
def signup_screen():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Signup", font=("Helvetica", 16, "bold")).pack(pady=10)

    tk.Label(root, text="Full Name").pack()
    name_entry = tk.Entry(root)
    name_entry.pack()

    tk.Label(root, text="Username").pack()
    username_entry = tk.Entry(root)
    username_entry.pack()

    tk.Label(root, text="Password").pack()
    password_entry = tk.Entry(root, show="*")
    password_entry.pack()

    def complete_signup():
        name = name_entry.get()
        username = username_entry.get()
        password = password_entry.get()

        if not name or not username or not password:
            messagebox.showerror("Missing Info", "All fields are required.")
            return

        if check_user_exists(username):
            messagebox.showerror("Signup Failed", "Username already exists.")
            return

        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        cursor.execute("INSERT INTO users2 (username, password_hash, full_name, is_admin) VALUES (%s, %s, %s, %s)",
                       (username, hashed_pw, name, False))
        db.commit()
        messagebox.showinfo("Signup Success", "You can now log in!")
        show_login_screen()

    tk.Button(root, text="Signup", command=complete_signup).pack(pady=10)
    tk.Button(root, text="Back to Login", command=show_login_screen).pack()

# -------- Login logic --------
def login(username, password):
    global logged_in_user, logged_in_user_id
    row = check_user_exists(username)
    if row:
        user_id, db_username, pw_hash = row[0], row[1], row[2]
        if bcrypt.checkpw(password.encode(), pw_hash.encode('utf-8') if isinstance(pw_hash, str) else pw_hash):
            logged_in_user = db_username
            logged_in_user_id = user_id
            messagebox.showinfo("Login Success", f"Welcome {db_username}!")
            show_vote_screen()
        else:
            messagebox.showerror("Login Failed", "Incorrect password.")
    else:
        messagebox.showerror("Login Failed", "User does not exist. Please sign up.")

# -------- Send encrypted vote to server --------
def encrypt_and_send_vote(choice):
    global session_key, logged_in_user
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a new TCP/IP socket for communication
    client.connect((SERVER_IP, PORT)) # Connect the socket to the server at the specified IP address and port

    with open("public.pem", "rb") as f:      # Open the RSA public key file (public.pem) in binary read mode
        rsa_key = RSA.import_key(f.read())

    cipher_rsa = PKCS1_OAEP.new(rsa_key) # Create an RSA cipher object using the imported public key with OAEP padding
    session_key = get_random_bytes(16)  # Generate a random 16-byte session key for AES encryption
    encrypted_key = cipher_rsa.encrypt(session_key)  # Encrypt the session key using the RSA public key (asymmetric encryption)
    client.send(encrypted_key)  # Send the encrypted session key to the server

    cipher_aes = AES.new(session_key, AES.MODE_ECB)  # Create an AES cipher object using the session key in ECB mode
    padded = choice.ljust(16).encode()   # Pad the chosen vote string to 16 bytes to match the AES block size
    encrypted = cipher_aes.encrypt(padded)  # Encrypt the padded vote using the AES cipher
    client.send(encrypted)   # Send the encrypted vote to the server

    # Send username to server for vote tracking
    client.send(logged_in_user.encode())

    messagebox.showinfo("Vote", f"Vote for {choice} submitted securely!")
    client.close()  # Close the socket connection to the server

# -------- Login Screen UI --------
def show_login_screen():
    for widget in root.winfo_children():
        widget.destroy()
    tk.Label(root, text="Secure Voting System", font=("Helvetica", 16, "bold")).pack(pady=10)

    tk.Label(root, text="Username").pack()
    username_entry = tk.Entry(root)
    username_entry.pack()

    tk.Label(root, text="Password").pack()
    password_entry = tk.Entry(root, show="*")
    password_entry.pack()

    def try_login():
        login(username_entry.get(), password_entry.get())

    def try_signup():
        signup_screen()

    tk.Button(root, text="Login", command=try_login).pack(pady=5)
    tk.Button(root, text="Signup", command=try_signup).pack()

# -------- Voting UI --------
def show_vote_screen():
    for widget in root.winfo_children():
        widget.destroy()
    tk.Label(root, text=f"Welcome {logged_in_user}, vote your favorite language:").pack()
    for lang in ["Python", "Java", "C", "JavaScript"]:
        tk.Button(root, text=lang, command=lambda l=lang: encrypt_and_send_vote(l)).pack()

# -------- Launch app --------
root = tk.Tk()
root.geometry("300x350")
root.title("Secure Voting System")
show_login_screen()
root.mainloop()
