import mysql.connector

# Connect to the MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="db_name"
)
cursor = mydb.cursor()

#Items Table and Data
items_data = [
    (101, 'Arabica', 3),
    (102, 'Robusta', 2.50),
    (103, 'Excelsa', 4),
    (104, 'Liberica', 1)
]

cursor.execute("""
    CREATE TABLE items (
        item_no INT PRIMARY KEY,
        item_name VARCHAR(30),
        price DECIMAL(5,2)
    )
""")

insert_query = "INSERT INTO items (item_no, item_name, price) VALUES(%s, %s, %s)"
cursor.executemany(insert_query, items_data)

#Addons Table and Data
add_ons_data = [
    (201, 'Coco Fudge', 0.50),
    (202, 'Whip Cream', 0.10),
    (203, 'Vanilla Extract', 0.30),
    (204, 'Cinnamon and Nutmeg', 0.05),
    (205, 'None', 0)
]

cursor.execute("""
    CREATE TABLE add_ons (
        addon_no INT PRIMARY KEY,
        addon_name VARCHAR(30),
        price DECIMAL(5,2)
    )
""")

insert_query_add_ons = "INSERT INTO add_ons (addon_no, addon_name, price) VALUES (%s, %s, %s)"
cursor.executemany(insert_query_add_ons, add_ons_data)

#Milk Table and Data
milk_data =[
    (1001, 'Coconut', 0.10),
    (1002, 'Almond', 0.30),
    (1003, 'Regular', 0.05),
    (1004, 'Soy Milk', 0.20)
]

cursor.execute("""
    CREATE TABLE milk (
        milk_no INT PRIMARY KEY,
        milk_type VARCHAR(30),
        price DECIMAL(5,2)
    )
""")

insert_query_milk = "INSERT INTO milk (milk_no, milk_type, price) VALUES (%s, %s, %s)"
cursor.executemany(insert_query_milk, milk_data)

#Other Important Tables
cursor.execute("""
    CREATE TABLE cust (
        cust_id INT PRIMARY KEY,
        cust_name VARCHAR(50),
        phone_no BIGINT,
        email_id VARCHAR(50),
        password VARCHAR(50),
        pass_qn VARCHAR(255),
        pass_ans VARCHAR(50)
    )
""")

cursor.execute("""
    CREATE TABLE order_info (
        order_no INT PRIMARY KEY,
        cust_id INT,
        FOREIGN KEY (cust_id) REFERENCES cust (cust_id)
    )
""")

cursor.execute("""
    CREATE TABLE orders (
        order_no INT,
        item_no INT,
        addon_no INT,
        milk_no INT,
        qty INT,
        total_price INT,
        FOREIGN KEY (order_no) REFERENCES order_info (order_no),
        FOREIGN KEY (item_no) REFERENCES items (item_no),
        FOREIGN KEY (addon_no) REFERENCES add_ons (addon_no),
        FOREIGN KEY (milk_no) REFERENCES milk (milk_no)
    )
""")

# Create the customer_review table
cursor.execute("""
    CREATE TABLE customer_review (
        id INT AUTO_INCREMENT PRIMARY KEY,
        cust_id INT,
        rating INT,
        feedback TEXT,
        reviewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (cust_id) REFERENCES cust (cust_id)
    )
""")

#End Message
print("Successfully Installed Pre-requisites")

mydb.commit()
mydb.close()