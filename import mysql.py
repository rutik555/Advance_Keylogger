import mysql.connector

# Establish MySQL connection
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Rutik@5555",
    database="keylogger"
)
    
if connection.is_connected():
    print("Connected to MySQL!")
    cursor = connection.cursor()

    # Query to retrieve files from the database
    select_query = "SELECT * FROM files"
    cursor.execute(select_query)

    # Fetch all rows from the result set
    rows = cursor.fetchall()

    if rows:
        print("Downloading files from the database:")
        for row in rows:
            filename = row[1]
            file_content = row[2]  # Assuming the file content is in the third column

            # Write the file content to a local file
            with open(filename, 'wb') as file:
                file.write(file_content)

            print(f"Downloaded: {filename}")
    else:
        print("No files found in the database")

    # Close cursor and connection
    cursor.close()
    connection.close()
else:
    print("Failed to connect to MySQL database")
