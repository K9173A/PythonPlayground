import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr


def compose_message():
    msg = MIMEText('Message content example...')
    msg['To'] = formataddr(('Recipient', 'recipient@example.com'))
    msg['From'] = formataddr(('k9173a', 'k9173a@example.com'))
    msg['Subject'] = 'Test test tess...'
    return msg.as_string()


def main():
    # Создание соедининения с сервером
    # server = smtplib.SMTP('127.0.0.1', 1025)
    server = smtplib.SMTP('127.0.0.1', 587)
    # Позволяет выводить вспомогательную информацию в консоль
    server.set_debuglevel(True)
    # Идентификация себя на сервере (неявно вызывается sendmail)
    server.ehlo()
    # Проверка поддержки расширений сервером. в Python пока нет нативной поддержки AUTH, поэтому
    # для реализации собственного SMTP-сервера с аутентификацией придётся переопределять SMTPChannel,
    # Без проверки has_extn('AUTH') smtplib.SMTPNotSupportedError: SMTP AUTH extension not supported by server.
    if server.has_extn('AUTH'):
        server.login('k9173a@gmail.com', 'password')
    try:
        # Отправка сообщения на сервер
        server.sendmail('k9173a@example.com', ['recipient@example.com'], compose_message())
    finally:
        # Закрытие соединения с сервером
        server.quit()


if __name__ == '__main__':
    main()
