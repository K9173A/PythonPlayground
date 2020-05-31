import smtpd
import asyncore


class Server(smtpd.SMTPServer):
    def __init__(self, address, port, *args, **kwargs):
        super(Server, self).__init__((address, port), None, *args, **kwargs)
        self.address = address
        self.port = port

    def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
        print(f'Sender: {peer}')
        print(f'From: {mailfrom}')
        print(f'To: {rcpttos}')
        print(f'Content: {data}')

    def run(self):
        try:
            asyncore.loop()
        except KeyboardInterrupt:
            pass


def main():
    server = Server('127.0.0.1', 1025)
    server.run()


if __name__ == '__main__':
    main()
