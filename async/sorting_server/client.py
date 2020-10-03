"""
Клиентская часть, которая занимается эмуляцией запросов. Интервал времени между
запросами варьируется случайным образом. Запросы состоят в сортировке
последовательности чисел произвольной длины с помоью заданного алгоритма.
"""
import asyncio
import random
import json


class Client:
    def __init__(self, address, port):
        """
        Создаёт event loop и устанавливает нужные настройки для работы с сервером.
        :param address: адрес сервера.
        :param port: порт сервера.
        """
        self.event_loop = asyncio.get_event_loop()
        self.address = address
        self.port = port
        self.data_chunk_size = 1024

    def stop(self):
        """
        Останавливает работу event loop.
        :return: None.
        """
        self.event_loop.stop()

    def run(self):
        """
        Запускает event loop, который работает до тех пор, пока пользователь
        не введёт Ctrl + C в консоли.
        :return: None.
        """
        print('[CLIENT] Started')
        asyncio.ensure_future(self.handle(), loop=self.event_loop)
        try:
            self.event_loop.run_forever()
        except KeyboardInterrupt:
            self.stop()

    @asyncio.coroutine
    def handle(self):
        """
        Главная корутина, которая занимается установление соедения с сервером
        с помощью сокета, и далее читает ответы и пишет и отправлят таски на
        обработку.
        :return: None.
        """
        while True:
            yield from asyncio.sleep(random.randint(1, 10))

            (reader, writer) = yield from asyncio.open_connection(
                host=self.address,
                port=self.port,
                loop=self.event_loop,
            )

            message = json.dumps({
                'algorithm': 'bubble_sort',
                'sequence': generate_random_sequence(1, 100, 20),
            }).encode('utf-8')
            writer.write(message)
            print('[CLIENT] Sent task')

            yield from writer.drain()

            data = yield from reader.read(self.data_chunk_size)
            print('[CLIENT] Got answer:', json.loads(data.decode('utf-8')))

            writer.close()


def generate_random_sequence(low, high, n=100):
    """
    Генерирует псевдослучайную последовательность из n чисел в диапазоне
    [low;high].
    :param low: нижний предел диапазноа генерации чисел.
    :param high: верхний предел диапазона генерации чисел.
    :param n: количество чисел, которые необходимо сгенерировать.
    :return:
    """
    return [random.randint(low, high) for _ in range(n)]


if __name__ == '__main__':
    client = Client('127.0.0.1', 8888)
    client.run()
