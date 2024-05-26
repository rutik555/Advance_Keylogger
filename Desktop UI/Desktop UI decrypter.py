import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.fernet import Fernet
import os

# Define encryption key
encryption_key = b"LDtGBp9DMpHh7CROYmkhaEx5Dt9VhW-dVijLS4oBmrw="

# Function to decrypt the file
def decrypt_file(file_path):
    try:
        with open(file_path, 'rb') as f:
            encrypted_data = f.read()
            fernet = Fernet(encryption_key)
            decrypted_data = fernet.decrypt(encrypted_data)
            return decrypted_data
    except Exception as e:
        messagebox.showerror("Error", f"Failed to decrypt file: {str(e)}")

# Function to handle file selection and decryption
def decrypt_file_dialog():
    file_path = filedialog.askopenfilename(title="Select Encrypted File")
    if file_path:
        decrypted_data = decrypt_file(file_path)
        if decrypted_data:
            directory = os.path.dirname(file_path)
            filename = os.path.basename(file_path)
            if filename.endswith('.encrypted'):
                filename = filename[:-len('.encrypted')]  # Remove the '.encrypted' extension
            output_file = os.path.join(directory, "decrypted_" + filename)
            with open(output_file, 'wb') as f:
                f.write(decrypted_data)
            messagebox.showinfo("Success", f"File decrypted successfully and saved as {output_file}!")

# Create GUI
root = tk.Tk()
root.title("File Decryptor")
root.geometry("400x300")
root.configure(bg="#f0f0f0")

# Header Label
header_label = tk.Label(root, text="File Decryptor", font=("Arial", 24, "bold"), bg="#f0f0f0", fg="#333")
header_label.pack(pady=20)

# Decrypt Button
decrypt_button = tk.Button(root, text="Select Encrypted File", command=decrypt_file_dialog, font=("Arial", 14), bg="#007bff", fg="white", relief="flat", activebackground="#0056b3", activeforeground="white")
decrypt_button.pack(pady=20, padx=20, ipadx=20, ipady=10)

# Footer Label
footer_label = tk.Label(root, text="© 2024 File Decryptor. All rights reserved.", font=("Arial", 10), bg="#f0f0f0", fg="#555")
footer_label.pack(side="bottom", pady=10)

root.mainloop()
