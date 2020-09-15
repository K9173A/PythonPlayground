"""
Простая реализация Шифра Цезаря.
"""


def cycle_text(text: str, n: int) -> str:
    """
    Циклически сдвигает текст `text` на заданное количество позиций `n`.

    >>> cycle_text('asdf', 1)
    'sdfa'

    >>> cycle_text('asdf', -1)
    'fasd'

    :param text: текст
    :param n: число позиций, на которое нужно сдвинуть текст.
    - Больше нуля - сдвиг влево.
    - Меньше нуля - сдвиг вправо.
    :return: текст, сдвинутый на заданное количество позиций.
    """
    return text[n:] + text[:n]


class CaesarCipher:
    """
    Шифр цезаря.
    Ширования осуществляется путём сдвига на заданное количество символов
    исходного алфавита и замена на эти символы исходного текста. Получателю
    в качестве ключа нужно знать в какую сторону сдвигать алфавит.
    """
    def __init__(self, alphabet: str):
        """
        :param alphabet: строка с алфавитом. Все буквы записаны слитно в той
        последовательности, в которой они идут стандартно.
        """
        self.alphabet = alphabet

    def encrypt(self, text: str, key: int) -> str:
        """
        Зашифровывает текст `text` с помощью ключа `key`.

        >>> cc.encrypt('привет', 1)
        'рсйгёу'

        :param text: исходный текст, который необходимо зашифровать.
        :param key: ключ-число для сдвига алфавита.
        :return: зашифрованный текст.
        """
        return self._cipher(text, key)

    def decrypt(self, text: str, key: int) -> str:
        """
        Расшифровывает текст `text` с помощью ключа `key`. Так как ключ `key`
        для зашифровки - то умножением на -1  получится ключ для расшифровки.

        >>> cc.decrypt('рсйгёу', 1)
        'привет'

        :param text: текст, который необходимо расшифровать.
        :param key: ключ-число для сдвига алфавита.
        :return: зашифрованный текст.
        """
        return self._cipher(text, key * -1)

    def _cipher(self, text: str, key: int) -> str:
        """
        Производит сам алгоритм шифровки/дешифровки текста `text` путём
        сопоставления исходного и целевого алфавитов и замены символов в тексте.
        :param text: текст, который необходимо зашифровать/расшифровать.
        :param key: ключ-число для сдвига алфавита.
        :return: обработанный текст.
        """
        target_alphabet = cycle_text(self.alphabet, key)
        encrypted_text = ''

        for char in text:
            i = self.alphabet.find(char)
            replacer_char = target_alphabet[i]
            encrypted_text += replacer_char

        return encrypted_text


if __name__ == '__main__':
    import doctest
    doctest.testmod(extraglobs={'cc': CaesarCipher('абвгдеёжзийклмнопрстуфхцчшщьыъэюя')})
