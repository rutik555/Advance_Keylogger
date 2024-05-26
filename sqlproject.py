import mysql.connector
import os

# Database connection details
config = {
    'user': 'your_database_user',
    'password': 'your_database_password',
    'host': 'your_database_host',
    'database': 'your_database_name'  # Use the name of your database
}

# Directory to save downloaded files
download_directory = 'downloaded_files'

# Ensure the download directory exists
if not os.path.exists(download_directory):
    os.makedirs(download_directory)

try:
    # Establish the connection
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    # Query to fetch all files from the table
    query = "SELECT filename, file_data FROM files"
    cursor.execute(query)

    # Fetch all rows
    rows = cursor.fetchall()

    if rows:
        # Process each row
        for row in rows:
            file_name = row[0]
            file_data = row[1]

            # Construct the full path to save the file
            file_path = os.path.join(download_directory, file_name)

            # Write the file data to the file
            with open(file_path, 'wb') as file:
                file.write(file_data)
            print(f"File {file_name} downloaded successfully.")
    else:
        print("No files found in the table.")

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
