import time
import socket
import ssl


class Server:
    def __init__(self):
        self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.context.load_cert_chain(certfile='certchain.crt',
                                     keyfile='private.key')
        self.context.verify_mode = ssl.CERT_REQUIRED
        self.context.check_hostname = False

    def run(self, host, port):
        # Создание обычного TCP сокета
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Сокет будет слушать приходящие запросы на соединение по указанному порту и хосту.
        sock.bind((host, port))

        # Максимальное количество запросов от климентов, которых можно обрабатывать одновременно.
        sock.listen(5)

        # Принимаем запрос на соединение, если такой имеется.
        # Функция возвращает сокет клиента и его адрес.
        client_connection, peer_address = sock.accept()

        print(f'Получен запрос на соединение от {peer_address}')

        connection_stream = self.context.wrap_socket(client_connection, server_side=True)

        print(f'SSL сертификат клиента: {connection_stream.getpeercert()}')

        # Отправка текущего времени клиенту
        connection_stream.send(f'{time.ctime(time.time())}\n'.encode('ascii'))

        # Закрытие соединения с клиентом
        connection_stream.close()


def main():
    server = Server()
    server.run('127.0.0.1', 8888)


if __name__ == '__main__':
    main()
