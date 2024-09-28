def is_valid_email(email):
    return ('@' in email) and ('.' in email)
user_email = input("Enter your e-mail address: ")
if is_valid_email(user_email):
    print("This is a valid e-mail address")
else:
    print("This is not a valid e-mail address")