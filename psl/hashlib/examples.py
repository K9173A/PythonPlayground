import hashlib
import binascii


# Объект, в котором будет производиться расчёт хэш-суммы.
hash_object = hashlib.md5()
# Загрузка в объект данных, хэш-сумму которых нужно вычислить.
hash_object.update(b'Hello')
# Получение хэш-суммы
hash_sum_1 = hash_object.hexdigest()
print(hash_sum_1)

# В этом варианте уже можно хранить хэш пароля - он надёжный
hash_sum_2 = hashlib.pbkdf2_hmac(
    hash_name='sha256',  # Название алгоритма
    password=b'password',  # Текст
    salt=b'salt',  # Соль
    iterations=100000,  # Количество итераций
    dklen=100,  # Длина значения на выходе
)
print(binascii.hexlify(hash_sum_2))
