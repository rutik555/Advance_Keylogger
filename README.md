# Keylogger Project

## Introduction

This project is a keylogger that logs keystrokes, system information, clipboard data, audio recordings, and screenshots. The collected data is stored in a MySQL database and also sent via email.

## Prerequisites

- Python 3.x
- MySQL server
- Required Python packages (listed in `requirements.txt`)

## Setup

### MySQL Database Configuration

1. **Install MySQL Server**: If you don't have MySQL installed, download and install it from the [official MySQL website](https://dev.mysql.com/downloads/).

2. **Create the Database and Table**:

   Open the MySQL command line or a MySQL client (such as MySQL Workbench) and execute the following commands to create the database and the `files` table:

   ```sql
   CREATE DATABASE keylogger;
   USE keylogger;

   CREATE TABLE files (
       id INT AUTO_INCREMENT PRIMARY KEY,
       filename VARCHAR(255) NOT NULL,
       file_data LONGBLOB NOT NULL,
       upload_date DATE NOT NULL,
       upload_time TIME NOT NULL
   );

# Important Notes:

1. This code is a keylogger and is typically considered malicious. Use it responsibly and ensure you have explicit permission from the system owner. Misuse can lead to legal consequences.
