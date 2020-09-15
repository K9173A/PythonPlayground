import textwrap


wrapper = textwrap.TextWrapper()
wrapper.initial_indent = '$$$'


text1 = textwrap.wrap(
    'a ' * 100,
    # Строка не может превышать заданное число символов. Лишняя часть отрезается и находится уже в индексе n + 1,
    # а если оставшаяся часть и туда не влезла, то записывается в n + 1.
    width=9,
    # Добавляет указанные символы в начало строки.
    initial_indent='$',
    # Если строка не влезне в width, то перед оставшейся частью будут поставлены эти символы (и в n + 1, и n + 2).
    # Если определён `max_lines` и `placeholder`, то не действует.
    subsequent_indent='#',
    # Удаляет пробелы в начале и в конце каждой строки (по умолчанию равно True).
    drop_whitespace=True,
    # Если строка была обрезана, то в конце строки будут указанные символы (по умолчанию '[...]')
    placeholder='^',
    # Максимальное количество строк (этот параметр нужен для параметра `placeholder`)
    max_lines=1
)

print(text1)

# Делает переносы в тексте (\n) в месте, где текст выходит за значение `width`.
# Аналог: "\n".join(wrap(text, ...))
text2 = textwrap.fill('Hello world!' * 3, width=10)

print(text2)

# Заменяет слишком длинный текст на `placeholder` (по умолчанию '[...]')
text3 = textwrap.shorten('Lorum ipsum sit amit', width=15, placeholder='...')  # Lorum ipsum...

print(text3)

# Добавляет префикс, последний параметр позволяет определять логику добавления префикса.
# В данном случае префикс добавляется даже для пустых строк, те вывод следующий:
# ***Hello
# ***
# ***world!
text4 = textwrap.indent('Hello\n\nworld!', '***', predicate=lambda line: True)

print(text4)
