from prettytable import PrettyTable
from create_acc_login import reset_password

def profile(cursor, cust_id, mydb):
    cursor.execute("SELECT * FROM cust WHERE cust_id = %s", (cust_id,))
    result = cursor.fetchone()

    if not result:
        print("User not found.")
        return

    def show_profile_table(data):
        table = PrettyTable()
        table.field_names = ["Field", "Information"]
        table.add_row(["Customer ID", data[0]])
        table.add_row(["Name", data[1]])
        table.add_row(["Phone Number", data[2]])
        table.add_row(["Gmail", data[3]])
        print("\n--- Profile Information ---")
        print(table)

    show_profile_table(result)

    while True:
        options = PrettyTable()
        options.field_names = ["Option", "Action"]
        options.add_row(["1", "Change Name"])
        options.add_row(["2", "Change Phone Number"])
        options.add_row(["3", "Change Gmail"])
        options.add_row(["4", "Change Reset Password Phrase"])
        options.add_row(["5", "Reset Password"])
        options.add_row(["6", "Exit Profile"])

        print("\nWhat would you like to do?")
        print(options)

        choice = input("Enter your choice (1-6): ")

        if choice == "6":
            print("Exiting profile...")
            break

        elif choice in ["1", "2", "3", "4"]:
            current_password = input("Enter your current password: ")
            if current_password != result[4]:
                print("Incorrect password.")
                continue

            if choice == "1":
                new_name = input("Enter new name: ")
                cursor.execute("UPDATE cust SET cust_name = %s WHERE cust_id = %s", (new_name, cust_id))
                print("Name updated successfully.")

            elif choice == "2":
                new_phone = input("Enter new phone number: ")
                cursor.execute("UPDATE cust SET phone_no = %s WHERE cust_id = %s", (new_phone, cust_id))
                print("Phone number updated successfully.")

            elif choice == "3":
                new_gmail = input("Enter new Gmail: ")
                cursor.execute("UPDATE cust SET email_id = %s WHERE cust_id = %s", (new_gmail, cust_id))
                print("Gmail updated successfully.")

            elif choice == "4":
                new_qn = input("Enter new reset password question: ")
                new_ans = input("Enter new reset password answer: ")
                cursor.execute("UPDATE cust SET pass_qn = %s, pass_ans = %s WHERE cust_id = %s",
                               (new_qn, new_ans, cust_id))
                print("Reset password phrase updated successfully.")

        elif choice == "5":
            reset_password(cursor, mydb)
            break

        else:
            print("Invalid choice. Please select from 1 to 6.")

        mydb.commit()
        cursor.execute("SELECT * FROM cust WHERE cust_id = %s", (cust_id,))
        result = cursor.fetchone()
        show_profile_table(result)