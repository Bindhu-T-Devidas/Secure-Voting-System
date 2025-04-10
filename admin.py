import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
import base64
from Crypto.Cipher import AES

# ---------- 🔐 Decryption Logic ----------
def decrypt_vote(b64, session_key):
    encrypted_bytes = base64.b64decode(b64)
    cipher = AES.new(session_key, AES.MODE_ECB)
    decrypted = cipher.decrypt(encrypted_bytes)
    return decrypted.decode(errors="ignore").rstrip('\x00')

# ---------- 🛡 Admin Login UI ----------
def admin_login():
    def check_admin():
        user = username_entry.get().strip()
        pwd = password_entry.get().strip()

        if not user or not pwd:
            messagebox.showwarning("Missing Fields", "Please enter both username and password.")
            return

        # Connect to DB to verify credentials
        conn = mysql.connector.connect(host="localhost", user="root", password="", database="votingDB")
        cursor = conn.cursor()
        cursor.execute("SELECT password_hash FROM users2 WHERE username=%s AND is_admin=TRUE", (user,))
        row = cursor.fetchone()
        conn.close()

        if row and pwd == "NSPROJECT":  # 🔁 Replace this later with bcrypt check
            login_window.destroy()
            load_results()
        else:
            messagebox.showerror("Access Denied", "Invalid credentials or not an admin.")

    # ---------- 🖼 Login Window ----------
    login_window = tk.Tk()
    login_window.geometry("300x200")
    login_window.title("Admin Login")

    frame = tk.Frame(login_window, bg="white")
    frame.pack(expand=True)

    tk.Label(frame, text="Admin Username:", bg="white").pack(pady=5)
    username_entry = tk.Entry(frame, bg="white", fg="black")
    username_entry.pack(pady=5)

    tk.Label(frame, text="Admin Password:", bg="white").pack(pady=5)
    password_entry = tk.Entry(frame, show="*", bg="white", fg="black")
    password_entry.pack(pady=5)

    tk.Button(frame, text="Login", command=check_admin).pack(pady=10)

    login_window.mainloop()

# ---------- 📊 Results Window ----------
def load_results():
    conn = mysql.connector.connect(host="localhost", user="root", password="", database="votingDB")
    cursor = conn.cursor()
    cursor.execute("SELECT u.username, v.encrypted_vote, v.session_key FROM votes3 v JOIN users2 u ON v.user_id = u.id")
    rows = cursor.fetchall()
    conn.close()

    root = tk.Tk()
    root.title("🛡️ Admin Panel – Secure Voting")

    tree = ttk.Treeview(root, columns=("Username", "Encrypted", "Decrypted"), show="headings")
    tree.heading("Username", text="Username")
    tree.heading("Encrypted", text="Encrypted Vote (Base64)")
    tree.heading("Decrypted", text="Decrypted Vote")
    tree.pack(fill=tk.BOTH, expand=True)

    counts = {"Python": 0, "Java": 0, "C": 0, "JavaScript": 0, "Invalid": 0}

    for username, enc_vote, b64key in rows:
        try:
            session_key = base64.b64decode(b64key)
            decrypted = decrypt_vote(enc_vote, session_key).strip()
            tree.insert("", "end", values=(username, enc_vote, decrypted))
            if decrypted in counts:
                counts[decrypted] += 1
            else:
                counts["Invalid"] += 1
        except Exception as e:
            tree.insert("", "end", values=(username, enc_vote, "❌ Error"))
            counts["Invalid"] += 1

    tk.Label(root, text="📊 Final Vote Counts", font=("Arial", 12, "bold")).pack(pady=10)
    for lang, count in counts.items():
        tk.Label(root, text=f"{lang:<15}: {count}", font=("Courier", 10)).pack()

    root.mainloop()

# 🔃 Start the login flow
admin_login()
