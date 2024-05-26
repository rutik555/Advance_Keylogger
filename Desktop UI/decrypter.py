import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.fernet import Fernet
import os
from PIL import Image, ImageTk

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

# Load the background image and resize it to fit the screen
background_image = Image.open("C:\\Users\\Rutik\\Downloads\\back.jpeg")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
background_image = background_image.resize((screen_width, screen_height))
background_photo = ImageTk.PhotoImage(background_image)

# Create a label to display the background image
background_label = tk.Label(root, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Set the geometry of the window to fit the screen
root.geometry(f"{screen_width}x{screen_height}+0+0")

# Custom Fonts
header_font = ("Arial", 60, "bold")
button_font = ("Arial", 20, "bold")
footer_font = ("Arial", 14)

# Header Label
header_label = tk.Label(root, text="File Decryptor", font=header_font, bg="#3498DB", fg="#FFFFFF", bd=5, relief="raised", padx=30, pady=15)
header_label.place(relx=0.5, rely=0.2, anchor="center")

# Decrypt Button
decrypt_button = tk.Button(root, text="Select Encrypted File", command=decrypt_file_dialog, font=button_font, bg="#1ABC9C", fg="#FFFFFF", relief="flat", activebackground="#16A085", activeforeground="#FFFFFF", padx=20, pady=10, bd=3)
decrypt_button.place(relx=0.5, rely=0.5, anchor="center")

# Footer Label
footer_label = tk.Label(root, text="© 2024 File Decryptor. All rights reserved.", font=footer_font, bg="#3498DB", fg="#FFFFFF")
footer_label.pack(side="bottom", pady=10)

root.mainloop()
