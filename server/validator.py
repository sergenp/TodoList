import re

def email_validator(email):
    return re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)

def password_validator(password):
    return re.match('^[a-zA-Z0-9]{8,32}$', password)
    