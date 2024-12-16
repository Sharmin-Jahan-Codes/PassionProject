
import mysql.connector
import csv

# MySQL Database configuration
db_config = {
    'host': 'localhost',  # Change this if you're using a different host
    'user': 'sharmin',  # Replace with your MySQL username
    'password': 'thisistheway',  # Replace with your MySQL password
    'database': 'food_choices_db'  # Replace with your desired database name
}

# Connect to MySQL
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Step 1: Create the table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS food_info (
    user_id INT NOT NULL,
    user_name VARCHAR(100) NOT NULL,
    food_category VARCHAR(100) NOT NULL,
    food_choice VARCHAR(100) NOT NULL,
    PRIMARY KEY (user_id, food_category, food_choice)
);
''')

# Step 2: Path to the CSV file
csv_file = "src/food_info.csv"  # Make sure the CSV file is in the correct location

# Step 3: Read the CSV file and insert the data into the table
with open(csv_file, "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        user_id = int(row["user_id"])
        user_name = row["user_name"]
        food_category = row["food_category"]
        food_choice = row["food_choice"]

        # Insert data into the food_info table
        cursor.execute('''
        INSERT INTO food_info (user_id, user_name, food_category, food_choice)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE 
            user_name = VALUES(user_name),
            food_category = VALUES(food_category),
            food_choice = VALUES(food_choice);
        ''', (user_id, user_name, food_category, food_choice))

# Commit changes and close the connection
conn.commit()
conn.close()

print(f"Data from {csv_file} has been successfully imported into MySQL database!")

