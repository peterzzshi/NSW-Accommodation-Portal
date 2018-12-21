import re

def change_to_db(text):
    return re.sub(r'\'', '+++++', text)

def change_to_front(text):
    return re.sub(r'\+\+\+\+\+', '\'', text)


def change_list_to_set_format(text):
    if not text:
        return '{}'
    if type(text[0]) is int:
        return "{" + ",".join(list(map(str, text))) + "}"
    return "{" + ",".join("{" + ",".join(list(map(str, x))) + "}" for x in text) + "}"

if __name__ == '__main__':
    text1 = [[1,2], [4]]
    text = [1,2,3]

    print(change_list_to_set_format(text1))
    print(change_list_to_set_format(text))