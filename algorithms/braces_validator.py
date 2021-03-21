

# Вариант 1. Самый простой вариант задачи, с одним типом скобок.
def validate_braces(text):
    counter = 0

    for brace in text:
        if brace == '(':
            counter += 1
        elif brace == ')':
            counter -= 1

        # Если вышли в отрицательные числа, значит закрывающаяся
        # скобка не имеет парной открывающейся скобки.
        if counter < 0:
            return False

    return counter == 0


def test_braces(func):
    braces_tests = [
        '(())()()(())',  # Всё ОК
        '(()))(',  # Неверная последовательность скобок, но равное их количество
        '((())',  # Не закрытая левая скобка
        '()()(',  # Не закрытая правая скобка
        '(()()())(()(())())'  # Всё OK
    ]

    for test in braces_tests:
        print('Result for test "{}" is: {}'.format(test, func(test)))


test_braces(validate_braces)
print('-' * 80)


# Вариант 2. Расширенный. Но тут не рассматриваются варианты с неправильными пересечениями
# скобок, т.е. "<((<>))[(()><)]>" даст положительный результат.
class BraceCounter:
    def __init__(self, open_brace: str, close_brace: str) -> None:
        self.open_brace = open_brace
        self.close_brace = close_brace
        self.counter = 0
        self.negative_counter_flag = False

    def process_brace(self, brace: str) -> None:
        if self.open_brace == brace:
            self.counter += 1
        elif self.close_brace == brace:
            self.counter -= 1
        if self.counter < 0:
            self.negative_counter_flag = True

    def is_valid_braces_sequence(self):
        return self.negative_counter_flag is False and self.counter == 0


class BracesValidationManager:
    def __init__(self) -> None:
        self.brace_counters = {}

    def add_braces(self, open_brace: str, close_brace: str):
        self.brace_counters[open_brace + close_brace] = BraceCounter(
            open_brace=open_brace,
            close_brace=close_brace
        )

    def is_valid_text(self, text):
        for char in text:
            for key in self.brace_counters.keys():
                if char in key:
                    self.brace_counters[key].process_brace(char)
                    break

        final_result = True
        for braces, brace_counter in self.brace_counters.items():
            final_result &= brace_counter.is_valid_braces_sequence()

        return final_result


braces_validation_manager = BracesValidationManager()
braces_validation_manager.add_braces(open_brace='(', close_brace=')')
braces_validation_manager.add_braces(open_brace='[', close_brace=']')
braces_validation_manager.add_braces(open_brace='<', close_brace='>')
print('<((<>))[(()><)]', braces_validation_manager.is_valid_text('<((<>))[(()><)]'))
print('-' * 80)


# Вариант 3. Правильный. С одним типом скобок.
def validate_braces2(text) -> bool:
    braces_stack = []

    for char in text:
        if char == '(':
            braces_stack.append(char)
        elif char == ')':
            if len(braces_stack) > 0 and braces_stack[-1] == '(':
                braces_stack.pop()
            else:
                return False

    return len(braces_stack) == 0


print(test_braces(validate_braces2))
print('-' * 80)


# Вариант 4. Правильный. С одним множеством типов скобок.
def validate_braces3(text, braces):
    braces_stack = []

    for char in text:
        for open_brace, close_brace in braces:
            if char == open_brace:
                braces_stack.append(open_brace)
                break
            elif char == close_brace:
                if len(braces_stack) > 0 and braces_stack[-1] == open_brace:
                    braces_stack.pop()
                    break
                else:
                    return False

    return len(braces_stack) == 0


braces_mapper = (
    ('(', ')'),
    ('{', '}'),
    ('<', '>'),
    ('[', ']')
)

test_braces3 = [
    '[(<{})]',
    '[(<{}>)]',
    '[({}>)]',
    '[(<{>})]',
    '((({{(}})))'
]

for t in test_braces3:
    print('Result for test "{}" is: {}'.format(t, validate_braces3(t, braces_mapper)))
