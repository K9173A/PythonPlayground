"""
Сервер, основная задача которого получать от пользователей запросы на сорти-
ровку последовательности чисел и возвращении полученного результата обратно
пользователю. Алгоритм сортировки выбирается пользователем и передаётся в
виде словаря:
{
    'algorithm': 'bubble_sort',
    'sequence': [5, 2, 5, 1, 6, 8]
}
"""
import asyncio
import json

from sort import sort


class Server:
    def __init__(self, address, port):
        """
        Создаёт event loop и устанавливает нужные настройки для своей работы.
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
        print('[SERVER] Stopped')
        self.event_loop.stop()

    def run(self):
        """
        Запускает сокет-сервер. Колбэк-функция receive вызывается каждый раз
        при коннекте нового пользователя. Колбэк должен иметь два параметра
        StreamReader и StreamWriter, соответствующие потоку для чтения и
        записи данных.
        :return: None.
        """
        print('[SERVER] Started')
        coro = asyncio.start_server(
            client_connected_cb=self.handle,
            host=self.address,
            port=self.port,
            loop=self.event_loop,
        )
        asyncio.ensure_future(coro, loop=self.event_loop)
        try:
            self.event_loop.run_forever()
        except KeyboardInterrupt:
            self.stop()

    @asyncio.coroutine
    def handle(self, reader, writer):
        """
        Колбэк-функция, которая вызывается каждый раз, когда устанавливается
        новое соединение с пользователем. Принимает два обязательных
        параметра.
        :param reader: StreamReader - объект для чтения данных из IO потока.
        :param writer: StreamWriter - объект для записи данных в IO поток.
        :return: None.
        """
        data = yield from reader.read(self.data_chunk_size)
        if not data:
            return None
        message = json.loads(data.decode(), encoding='utf-8')
        print('[SERVER] Received task')

        sorted_data = sort(message['algorithm'], message['sequence'])
        print('[SERVER] Sorted sequence')

        message = json.dumps({'sequence': sorted_data}).encode('utf-8')
        writer.write(message)
        print('[SERVER] Sent answer')

        yield from writer.drain()


if __name__ == '__main__':
    server = Server('localhost', 8888)
    server.run()
