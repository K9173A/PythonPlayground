import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr


def compose_message():
    msg = MIMEText('Message content example...')
    msg['To'] = formataddr(('Recipient', 'recipient@example.com'))
    msg['From'] = formataddr(('Author', 'author@example.com'))
    msg['Subject'] = 'Test test tess...'
    return msg.as_string()


def main():
    client = smtplib.SMTP('127.0.0.1', 1025)
    client.set_debuglevel(True)

    try:
        client.sendmail('sender@example.com', ['recipient@example.com'], compose_message())
    finally:
        client.quit()


if __name__ == '__main__':
    main()
