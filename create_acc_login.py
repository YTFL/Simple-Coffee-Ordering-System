from req_mods import *

def login(cursor, mydb):
    while True:
        choice = input("Do you want to login (L) or create a new account (C)? \n").upper()
        if choice in ["L", "C"]:
            break
        else:
            print("\nInvalid choice. Please enter L or C.")

    if choice == "L":
        while True:
            login_info = input("\nEnter your phone number or email address: ")

            cursor.execute(
                "SELECT * FROM cust WHERE (phone_no = %s OR email_id = %s) AND (phone_no IS NOT NULL OR email_id IS NOT NULL)",
                (login_info, login_info)
            )
            result = cursor.fetchone()

            if result:
                while True:
                    password = input("Enter your password: ")
                    if password == result[4]:
                        print("Login successful!")
                        cust_info = get_customer_info(cursor, login_info)
                        print(f"\nWelcome, {cust_info[1]} \nWhat would you like to have today?")
                        return cust_info
                    else:
                        print("Incorrect password\n")
                        pass_wr = input("Would you like to try again (T) or reset (R) your password?: ").upper()

                        while pass_wr not in ["T", "R"]:
                            print("Invalid Input.")
                            pass_wr = input("Please enter T to try again or R to reset password: ").upper()

                        if pass_wr == "T":
                            continue
                        elif pass_wr == "R":
                            reset_password(cursor, mydb)
                            return login(cursor, mydb)  # Reattempt login after reset
            else:
                print("Account not found.")
                while True:
                    retry = input("Do you want to try again (Y) or create a new account (C)? ").upper()
                    if retry in ["Y", "C"]:
                        break
                    else:
                        print("Invalid Input.")
                if retry == "C":
                    return create_account(cursor, mydb)
                else:
                    continue

    elif choice == "C":
        return create_account(cursor, mydb)

def create_account(cursor, mydb):
    phone_number = None
    email = None
    name = input("Enter Your Name: \n")
    customer_id = generate_customer_id()

    while True:
        choice = input("Do you want to use phone number (P) or email address (E)? \n").upper()

        if choice == "P":
            while True:
                phone_number = input("Enter your phone number: ")
                if len(phone_number) == 10 and phone_number.isdigit():
                    cursor.execute("SELECT * FROM cust WHERE phone_no = %s", (phone_number,))
                    result = cursor.fetchone()
                    if result:
                        print("\nAccount with this phone number already exists. Please Login.")
                        return login(cursor, mydb)
                    break
                else:
                    print("Invalid phone number. Please enter a valid 10-digit phone number.")
            break

        elif choice == "E":
            while True:
                email = input("Enter your email address: ")
                if "@" in email and "." in email and email.index("@") < email.rindex("."):
                    cursor.execute("SELECT * FROM cust WHERE email_id = %s", (email,))
                    result = cursor.fetchone()
                    if result:
                        print("\nAccount with this email address already exists. Please Login.")
                        return login(cursor, mydb)
                    break
                else:
                    print("Invalid email address. Please enter a valid email address.")
            break

        else:
            print("\nInvalid choice. Please enter E or P.")

    while True:
        password = input("Enter your password: ")
        password_re = input("Please Re-enter your password for confirmation: ")
        if password == password_re:
            pass_qn = input("Enter a question that allows you to reset your password when you forget: ")
            pass_ans = input("Enter the answer to the question in a single word: ")

            print("You will be asked this question when requested to reset your password when you forget. "
                  "You can reset the password when you answer the question correctly.")
            break
        else:
            print("Passwords do not match. Please try again.\n")

    try:
        cursor.execute(
            "INSERT INTO cust (cust_id, cust_name, phone_no, email_id, password, pass_qn, pass_ans) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (customer_id, name, phone_number, email, password, pass_qn, pass_ans)
        )
        mydb.commit()
        print("Account created successfully!\n")

        cursor.execute("SELECT * FROM cust WHERE cust_id = %s", (customer_id,))
        cust_info = cursor.fetchone()
        print(f"\nWelcome, {cust_info[1]} \nWhat would you like to have today?")
        return cust_info
    except Exception as err:
        print("Error creating account:", err)
        return create_account(cursor, mydb)


def reset_password(cursor, mydb):
    while True:
        ph_ei = input("Enter your phone number or email address: ")
        query = "SELECT * FROM cust WHERE phone_no = %s OR email_id = %s"
        cursor.execute(query, (ph_ei, ph_ei))
        result = cursor.fetchone()

        if result:
            break
        else:
            print("No matching record found. Please try again.\n")

    print(f"Security Question: {result[5]}")
    while True:
        qn_ans = input("Enter the answer to the security question: ").strip()
        if qn_ans.lower() == result[6].lower():
            print("Identity Verified")
            break
        else:
            print("Incorrect answer. Please try again.")

    while True:
        password_reset = input("Enter a new password: ")
        password_reset_re = input("Please Re-enter the new password for confirmation: ")

        if password_reset == password_reset_re:
            cursor.execute(
                "UPDATE cust SET password = %s WHERE CAST(phone_no AS CHAR) = %s OR email_id = %s",
                (password_reset, ph_ei, ph_ei)
            )
            mydb.commit()
            print("Password reset successful!")
            return  # Control goes back to login after reset
        else:
            print("Passwords do not match. Please try again.")
