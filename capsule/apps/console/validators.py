from django.core.exceptions import ValidationError
from django.core.validators import validate_email

import re


# Check mobile number format(Iran)
def mobile_format_check(some: str):
    mobile_regex = "^09(1[0-9]|3[1-9]|2[1-9])-?[0-9]{3}-?[0-9]{4}$"
    if re.search(mobile_regex, some):
        return True

    return False


# Check email format
def email_format_check(some: str):
    try:
        validate_email(some)
        return True
    except ValidationError:
        return False


def pass_difficulty(password: str) -> str:
    """ Get password as a string and return the difficulty label between (h:Hard, g:Good, w:Weak) """
    has_alpha = re.search("[a-zA-Z]", password)
    has_digit = re.search("[0-9]", password)
    has_punct = re.search("[!#$%&@()*+,^=></~|;'-]", password)

    if len(password) < 6:
        return "w"
    elif has_punct and has_alpha and has_digit:
        return "h"
    elif (has_alpha and has_punct) or (has_alpha and has_digit) and (len(password) >= 10):
        return "h"
    elif (has_alpha and has_punct) or (has_alpha and has_digit) or (has_digit and has_punct):
        return "g"

    return "w"


def account_type(username: str) -> str | None:
    """ Get username as a string and return the username type (e:Email, p:Phone) """
    if mobile_format_check(username):
        return "p"
    elif email_format_check(username):
        return "e"

    return None


def pass_difficulty_ave(passwords):
    """ Get a list of passwords and return the quality percent of all passwords """
    quality = 0
    for password in passwords:
        difficulty = pass_difficulty(password.password)
        if difficulty == "h":
            quality += 1
        elif difficulty == "g":
            quality += 0.5
        else:
            quality += 0.25

    return round((quality / len(passwords)) * 100)
