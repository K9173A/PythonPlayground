import re


def replacer(match):
    """
    На вход поступает строка `match`, в которой идут последовательности вида `\\uXXXX`,
    поэтому делается следующая последовательность операций:
    1. Отрезаем первый backslash.
    2. Методом `.encode('utf-8')` превращаем строку в байты, не меняя изначальной сути.
    3. С помощью `.decode('unicode-escape')` превращаем в коды в читаемые символы.
    """
    return match.group()[1:].encode('utf-8').decode('unicode-escape')


with open('/home/k9173a/Downloads/57948_bot.log', mode='r') as f:
    content = f.read()

new_content = re.sub(r'\\\\u.{4}', replacer, content, flags=re.IGNORECASE)

with open('/home/k9173a/Downloads/57948_bot-2.log', mode='w') as f2:
    f2.write(new_content)
