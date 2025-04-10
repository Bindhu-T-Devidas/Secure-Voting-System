import tkinter as tk
from tkinter import messagebox

def check_login():
    user = username_entry.get()
    pwd = password_entry.get()

    if user == "Bindu" and pwd == "NSPROJECT":
        messagebox.showinfo("Login Success", f"Welcome {user}!")
        print("✅ Logged in as:", user)
        root.destroy()
    elif user == "" or pwd == "":
        messagebox.showwarning("Missing Info", "Please fill both fields.")
    else:
        messagebox.showerror("Login Failed", "Invalid credentials.")

# ---- GUI Setup ----
root = tk.Tk()
root.title("Minimal Login")
root.geometry("300x200")
root.configure(bg="white")  # Set white background for macOS visibility

# Frame to hold everything (helps layout on Mac)
frame = tk.Frame(root, bg="white")
frame.pack(expand=True)

tk.Label(frame, text="Username:", bg="white", fg="black").pack(pady=5)
username_entry = tk.Entry(frame, bg="white", fg="black")
username_entry.pack(pady=5)

tk.Label(frame, text="Password:", bg="white", fg="black").pack(pady=5)
password_entry = tk.Entry(frame, show="*", bg="white", fg="black")
password_entry.pack(pady=5)

tk.Button(frame, text="Login", command=check_login).pack(pady=10)

root.update_idletasks()  # Helps force layout redraw
root.mainloop()
