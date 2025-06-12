start_app: str = '''
    1. Login
    2. Register
    q. Quit
'''

inner_loop: str = """
    1. Check taxes
    2. Pay/Add tax
    q. Quit
    
    exit - close app 

    """

check_taxes: str = """
    Type name of tax to go into details of payment
    Type q or exit to leave
"""

payment_edit: str = """
    1. Edit payment
    2. Delete payment
    q. Quit
"""

edit_msg: str = """
    1. Edit date
    2. Edit price
    3. Edit tax
    4. Delete payment 
    a. Abandon changes
    q. Quit and save
"""

## admin messages
admin_dict: dict = {
        'tax': """
                1. Add tax
                2. Edit tax
                3. Delete tax
                4. Go to users
                5. Go to payments
                """,
        'payment': """
                1. Add payment
                2. Edit payment
                3. Delete payment
                4. Go to Taxes
                5. Go to Users
                """,
        'user': """
                1. Add new user
                2. Edit user
                3. Delete user
                4. Go to Taxes
                5. Go to Payments
                """
}
