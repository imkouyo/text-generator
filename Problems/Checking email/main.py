import re
def check_email(string):
    return bool(re.match(r'[\w.]+@\w+\.\w*', string))