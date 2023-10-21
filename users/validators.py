import re
from django.core.exceptions import ValidationError

def validate_email(email):
    if not email:
        raise ValidationError("Users must have an email address")
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        raise ValidationError("Invalid email format")
    return True

def validate_password(password):
    if not password:
        raise ValidationError("Users must have a password")
    if len(password) < 8:
        raise ValidationError("Password must have at least 8 characters")
    if not any(char.isupper() for char in password):
        raise ValidationError("Password must have at least one capital letter")
    if not any(char.isdigit() for char in password):
        raise ValidationError("Password must have at least one number")
    return True

def validate_phone(phone):
    if not phone:
        raise ValidationError("Users must have a phone number")
    if len(phone) < 10:
        raise ValidationError("Phone number must have at least 10 digits")
    if not phone.isdigit():
        raise ValidationError("Phone number must have only digits")
    return True

def validate_name(name):
    if not name:
        raise ValidationError("Users must have a name and a last name")
    if len(name) < 2:
        raise ValidationError("Name and last name must have at least 2 characters")
    if not name.isalpha():
        raise ValidationError("Name and last name must have only letters")
    return True

def validate_username(username):
    if not username:
        raise ValidationError("Users must have a username")
    if len(username) < 5:
        raise ValidationError("Username must have at least 5 characters")
    if not username.isalnum():
        raise ValidationError("Username must have only letters and numbers")
    return True