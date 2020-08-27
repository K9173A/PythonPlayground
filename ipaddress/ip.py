# Добавлена в Python 3.3
# https://proglib.io/p/koncepciya-ip-adresov-na-primere-python-modulya-ipaddress-2020-08-07
import ipaddress


ip = ipaddress.IPv4Address('192.168.0.127')

print(int(ip))  # 3232235647 - в целочисленной форме
print(ip.packed)  # b'\xc0\xa8\x00\x7f' - в байтах
print(hash(ip))  # хэширование IP

result = ipaddress.IPv4Address('220.14.9.37') > ipaddress.IPv4Address('8.240.12.2')
print(result)  # Операции сравнения

ips = [
    ipaddress.IPv4Address("220.14.9.37"),
    ipaddress.IPv4Address("100.201.0.4"),
    ipaddress.IPv4Address("8.240.12.2")
]

print(sorted(ips))  # Отсортированный список IP адресов

network = ipaddress.IPv4Network('192.4.2.0/24')
print(network.num_addresses)  # Количество адресов, которые маска подсети позволяет выделить (CIDR)
print(network.prefixlen)  # CIRD (24)
print(network.netmask)  # Маска подсети

print(ip in network)  # Проверка, является ли адрес частью сети

# Широковещательный адрес - условный (не присвоенный никакому устройству в сети) адрес,
# который используется для передачи широковещательных пакетов в компьютерных сетях. Это
# единственный адрес, который может использоваться для связи со всеми хостами сети.
print(network.network_address)

# Перечисление всех допустимых адресов в данной сети
for address in ipaddress.IPv4Network('192.4.2.0/28'):
    print(address)

# Адреса, исключая сетевые и широковещательные
for address in ipaddress.IPv4Network('192.4.2.0/28').hosts():
    print(address)

# Является ли сеть подсетью
small_net = ipaddress.IPv4Network('192.0.2.0/28')
big_net = ipaddress.IPv4Network('192.0.0.0/16')
print(small_net.subnet_of(big_net))  # True
print(big_net.supernet_of(small_net))  # False

# Итерация через все подсети с заменой на новый CIDR 20
for subnet in ipaddress.IPv4Network('192.0.0.0/28').subnets(new_prefix=29):
    print(subnet)

# Является ли адрес приватным (попадает ли он в диапазон сети)?
result = ipaddress.IPv4Address("10.243.156.214") in ipaddress.IPv4Network("10.0.0.0/8")
print(result)

# Другой специальный тип адреса – это локальный адрес связи (169.254.0.0/16).
# Примером может служить Amazon Time Sync Service, доступный для инстансов
# AWS EC2 по адресу 169.254.169.123. Данный пул также использует Windows для
# выдачи адресов сетевым адаптерам при отсутствии интернета от провайдера.
timesync_addr = ipaddress.IPv4Address('169.254.169.123')
print(timesync_addr.is_link_local)

# Проверка, является ли адрес специальным
print([i for i in dir(ip) if i.startswith("is_")])

# Зарезервированные сети:
# 0.0.0.0/8 – адреса источников пакетов «своей» сети
# 127.0.0.0/8 – используется для локального хоста
# 169.254.0.0/16 – внутренние адреса
# 198.18.0.0/15 – для бенчмаркинга сетей
