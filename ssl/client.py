import socket
import ssl


class Client:
    def __init__(self):
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        self.context.load_verify_locations(cafile='certchain.crt')
        self.context.verify_mode = ssl.CERT_REQUIRED
        self.context.check_hostname = False

    def run(self, host, port):
        # Создание обычного TCP сокета
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Привязка сокета к SSL контексту
        ssl_sock = self.context.wrap_socket(sock)

        # Коннект к серверу по указанному адресу (хосту и порту)
        ssl_sock.connect((host, port))

        # Принять не более 1024 байтов данных
        received_data = ssl_sock.recv(1024)

        # Получить SSL-сертификат собеседника (того, кто на другой стороне)
        print(ssl_sock.getpeercert())

        # Закрытие соединения с сервером
        ssl_sock.close()

        print('Текущее время: {}'.format(received_data.decode('ascii')))

        # todo: https://www.makethenmakeinstall.com/2014/05/ssl-client-authentication-step-by-step/


def main():
    client = Client()
    client.run('localhost', 8888)


if __name__ == '__main__':
    main()
