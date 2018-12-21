import re

def change_to_db(text):
    return re.sub(r'\'', '+++++', text)

def change_to_front(text):
    return re.sub(r'\+\+\+\+\+', '\'', text)