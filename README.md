# Secure Voting System - VoteGuard

A secure, encrypted electronic voting system built using a hybrid RSA + AES encryption model. The project uses a client-server architecture with multi-client support and ensures secure vote transmission, authentication, and real-time result decryption. 

---

## 🔐 Project Highlights

- 🔒 **Hybrid Encryption (AES + RSA)** for secure vote transmission
- 👥 **Multi-client Handling** using POSIX threads in C
- 🧑‍💻 **Client & Admin GUI** using Python’s Tkinter
- 🧾 **MySQL Database** to store encrypted votes & user credentials
- 🧠 **Password Hashing** using bcrypt for secure user login
- ✅ Real-time **vote decryption and counting** by admin
- 🖥️ Platform: macOS (localhost-based)

---

## 📁 Components

| File            | Description                                 |
|-----------------|---------------------------------------------|
| `client.py`     | GUI-based voting client (Python + Tkinter)  |
| `admin.py`      | GUI-based admin panel (Python + Tkinter)    |
| `server.c`      | Multi-threaded server (C + POSIX + OpenSSL) |
| `rsa_keygen.py` | Generates RSA public/private key pairs      |
| `database.sql`  | SQL schema for users and votes tables       |
| `README.md`     | This file                                   |

---

## 🔧 How It Works

1. **User Registration/Login**  
   Users register/login using a Tkinter GUI. Passwords are hashed using bcrypt.

2. **Vote Encryption**  
   - A random AES session key is generated.
   - The vote is encrypted using AES.
   - The AES key is encrypted using RSA (server's public key).

3. **Vote Transmission**  
   The client sends:
   - AES-encrypted vote
   - RSA-encrypted AES key to the server via TCP socket.

4. **Vote Decryption & Storage**  
   - The server decrypts the AES key using its private RSA key.
   - It uses the decrypted key to decrypt the vote.
   - Stores encrypted votes in MySQL.

5. **Admin Panel**  
   - Logs in using predefined credentials.
   - Displays encrypted and decrypted votes.
   - Real-time vote count.

---

## 💻 Technologies Used

### Python (3.11+)
- Tkinter (GUI)
- bcrypt
- pycryptodome
- socket
- mysql-connector-python

### C (GCC / Clang)
- POSIX Threads
- OpenSSL
- MySQL C API

### Database
- MySQL 8.0+

---

## 🔐 Security Features

- 🔐 **RSA (2048-bit)** for session key encryption
- 🛡️ **AES-128 (ECB Mode)** for vote encryption
- 🔏 **bcrypt** for password hashing
- 🔒 Secure key exchange & multi-client vote handling

---

## 📌 System Requirements

- **OS:** macOS
- **Python:** 3.11+
- **C Compiler:** GCC / Clang
- **Database:** MySQL Server 8+
- **Ports:** TCP Port `8080` open for localhost

---

## 📈 Future Enhancements

- 🌐 Shift to a cloud-based database (e.g., Supabase)
- 📊 Add vote analytics with charts
- 📧 Email confirmation after voting
- 🖥️ Upgrade frontend using React + TailwindCSS

---

## 👤 Author

**Bindu T D**  
School of Computer Science and Engineering | RV University  

---

## 📄 License

This project is for academic purposes only. Do not use in real-world elections without proper security audit and compliance.

