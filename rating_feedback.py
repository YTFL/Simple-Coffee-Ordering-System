def rating_feedback(cursor, cust_id):
    while True:
        try:
            rating = int(input('\nPlease Rate your Experience with us Today on a Scale of 1 to 10: '))
            if 1 <= rating <= 10:
                break
            else:
                print("Please enter a valid Rating between 1 and 10.")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 10.")


    if rating >= 7:
        print('Thank you so much for your rating!')
        print('We are extremely happy that you are satisfied with us today!')
        rev = input("Please provide any feedback if you have:\n")
    else:
        print('\nWe are very sorry that you aren\'t happy with us.')
        rev = input('\nPlease let us know what went wrong and how we can improve:\n')
        print('\nThank you for your feedback! We look forward to improving next time.')

    cursor.execute(
        "INSERT INTO customer_review (cust_id, rating, feedback) VALUES (%s, %s, %s)",
        (cust_id, rating, rev)
    )
