import time
import random

def countdown(t):
    while t >= 0:
        mins, secs = divmod(t, 60)
        timer = 'Countdown: {:02d}:{:02d}'.format(mins, secs)
        print(timer, end='\r')
        time.sleep(1)
        t -= 1
    print('\nCountdown finished!')

def generate_customer_id():
    return str(random.randint(100000, 999999))

def generate_order_number():
    return str(random.randint(10000000, 99999999))

def get_customer_info(cursor, login_info):
    cursor.execute(
        "SELECT * FROM cust WHERE (phone_no = %s OR email_id = %s) AND (phone_no IS NOT NULL OR email_id IS NOT NULL)",
        (login_info, login_info)
    )
    return cursor.fetchone()
