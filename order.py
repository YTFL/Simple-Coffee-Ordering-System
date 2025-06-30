from prettytable import PrettyTable
from req_mods import *
from decimal import Decimal, ROUND_HALF_UP

def order(cursor, cust_id):
    order_number = generate_order_number()
    item_no = []
    addon_no = []
    milk_no = []
    total_price = []
    qty = []

    main_loop_flag = True

    while main_loop_flag:
        price = Decimal("0.00")

        print("\nHere's Our Menu")

        cursor.execute("SELECT * FROM items")
        menu_sql = cursor.fetchall()

        menu = PrettyTable()
        menu.field_names = [i[0] for i in cursor.description]

        for row in menu_sql:
            menu.add_row(row)

        print(menu)

        while True:
            item_number = input('Enter the item number to order: ')
            if item_number.isdigit():
                cursor.execute(
                    "SELECT item_name, price, item_no FROM items WHERE item_no = %s",
                    (int(item_number),)
                )
                item_result = cursor.fetchone()
                if item_result:
                    print(f"You selected: {item_result[0]}")
                    price += Decimal(str(item_result[1]))
                    item_no.append(item_result[2])
                    break
            print("\nInvalid item number. Enter Again.")

        cursor.execute("SELECT * FROM add_ons")
        addons_sql = cursor.fetchall()
        addons = PrettyTable()
        addons.field_names = [i[0] for i in cursor.description]
        for row in addons_sql:
            addons.add_row(row)
        print("\nSelect an Addon to add")
        print(addons)

        while True:
            addon_number = input("Enter your Addon Number: ")
            if addon_number.isdigit():
                cursor.execute(
                    "SELECT addon_name, price, addon_no FROM add_ons WHERE addon_no = %s",
                    (int(addon_number),)
                )
                addon_result = cursor.fetchone()
                if addon_result:
                    print(f"You Selected: {addon_result[0]}")
                    price += Decimal(str(addon_result[1]))
                    addon_no.append(addon_result[2])
                    break
            print("\nInvalid addon number. Enter Again.")

        cursor.execute("SELECT * FROM milk")
        milk_sql = cursor.fetchall()
        milk = PrettyTable()
        milk.field_names = [i[0] for i in cursor.description]
        for row in milk_sql:
            milk.add_row(row)
        print("\nSelect the milk you want")
        print(milk)

        while True:
            milk_number = input("Enter the Milk Number: ")
            if milk_number.isdigit():
                cursor.execute(
                    "SELECT milk_type, price, milk_no FROM milk WHERE milk_no = %s",
                    (int(milk_number),)
                )
                milk_result = cursor.fetchone()
                if milk_result:
                    print(f"You Selected: {milk_result[0]}")
                    price += Decimal(str(milk_result[1]))
                    milk_no.append(milk_result[2])
                    break
            print("\nInvalid milk number. Enter Again.")

        while True:
            qty_str = input("\nEnter your order Quantity here: ")
            if qty_str.isdigit() and 1 <= int(qty_str) <= 4:
                qty_int = int(qty_str)
                qty.append(qty_int)
                price *= qty_int
                price = price.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                total_price.append(price)
                break
            print("Please enter a Valid Quantity of up to 4")

        while True:
            mi = input("\nWould you Like to Order more items? (Y/N): ").upper()
            if mi == "Y":
                print()
                break
            elif mi == "N":
                main_loop_flag = False
                break
            print("Invalid Input. Please enter Y for yes and N for no")

    cursor.execute("INSERT INTO order_info (order_no, cust_id) VALUES (%s, %s)", (order_number, cust_id))

    for i in range(len(item_no)):
        cursor.execute(
            "INSERT INTO orders (order_no, item_no, addon_no, milk_no, qty, total_price) VALUES (%s, %s, %s, %s, %s, %s)",
            (order_number, item_no[i], addon_no[i], milk_no[i], qty[i], total_price[i])
        )

    cursor.execute(
        "SELECT item_no, item_name FROM items WHERE item_no IN ({})".format(", ".join(["%s"] * len(item_no))),
        item_no
    )
    items_details = cursor.fetchall()

    cursor.execute(
        "SELECT addon_no, addon_name FROM add_ons WHERE addon_no IN ({})".format(", ".join(["%s"] * len(addon_no))),
        addon_no
    )
    addons_details = cursor.fetchall()

    cursor.execute(
        "SELECT milk_no, milk_type FROM milk WHERE milk_no IN ({})".format(", ".join(["%s"] * len(milk_no))),
        milk_no
    )
    milk_details = cursor.fetchall()

    bill_table = PrettyTable()
    bill_table.field_names = ["S.No", "Item", "Addon", "Milk", "Quantity", "Price"]

    total_amount = 0
    for i in range(len(item_no)):
        item_name = next(item[1] for item in items_details if item[0] == item_no[i])
        addon_name = next(addon[1] for addon in addons_details if addon[0] == addon_no[i])
        milk_type = next(milk[1] for milk in milk_details if milk[0] == milk_no[i])
        total_amount += total_price[i]
        bill_table.add_row([i + 1, item_name, addon_name, milk_type, qty[i], total_price[i]])

    print("\nBill Details:")
    print(bill_table)
    print(f"Total amount to be paid: ${total_amount}")

    countdown(sum(qty) * 5)

    print("\nPlease pay using Cash, Card or EPay")


def order_history(cursor, cust_id):
    cursor.execute("SELECT cust_name FROM cust WHERE cust_id = %s", (cust_id,))
    result = cursor.fetchone()

    if not result:
        print("No customer found with that ID.")
        return

    cust_name = result[0]
    print(f"\nOrder history for: {cust_name} (Customer ID: {cust_id})")

    cursor.execute("SELECT order_no FROM order_info WHERE cust_id = %s", (cust_id,))
    order_nos = cursor.fetchall()

    if not order_nos:
        print("No orders found.")
        return

    history_table = PrettyTable()
    history_table.field_names = ["Order No", "Item", "Addon", "Milk", "Quantity", "Total Price"]

    for (order_no,) in order_nos:
        cursor.execute("SELECT item_no, addon_no, milk_no, qty, total_price FROM orders WHERE order_no = %s", (order_no,))
        order_items = cursor.fetchall()

        for item_no, addon_no, milk_no, qty, price in order_items:
            # Fetch item names
            cursor.execute("SELECT item_name FROM items WHERE item_no = %s", (item_no,))
            item_name = cursor.fetchone()[0]

            cursor.execute("SELECT addon_name FROM add_ons WHERE addon_no = %s", (addon_no,))
            addon_name = cursor.fetchone()[0]

            cursor.execute("SELECT milk_type FROM milk WHERE milk_no = %s", (milk_no,))
            milk_type = cursor.fetchone()[0]

            history_table.add_row([order_no, item_name, addon_name, milk_type, qty, price])

    print(history_table)