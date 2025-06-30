import mysql.connector
from create_acc_login import *
from order import *
from rating_feedback import *
from profile import *
import sys

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="db_name"
)
cursor = mydb.cursor()

print('Welcome to Caffo! \n')

cust_info = login(cursor, mydb)
if cust_info is None:
    print("Login failed. Exiting application.")
    sys.exit(1)
    
cust_id = cust_info[0]

print("Continue with choosing an option")
print("1. Order\n2. Profile\n3. Order History\n4. Exit")

while True:
    choice = input("Enter your option: ")
    match choice:
        case "1":
            order(cursor, cust_id)
            break

        case "2":
            profile(cursor, cust_id, mydb)
            continue

        case "3":
            order_history(cursor, cust_id)
            break

        case "4":
            print("Thank you for using Caffo")
            sys.exit()
        case _:
            print("\nInvalid choice. Please try again.")

rating_feedback(cursor, cust_id)

print('\nThank You for visiting us today, make sure you visit us again!\nHave a Nice Day')
time.sleep(10)
print("---")

mydb.commit()
mydb.close()