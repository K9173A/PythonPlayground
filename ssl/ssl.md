### Генерация SSL пары на Windows
1. Запустить `cmd.exe` как администратор.
2. OpenSSL поставляется с Git, удобно использовать его. Следующая команда сгененирует certificate authority (CA) кертификаты: 
    ```bash
    cd C:\Program Files\Git\usr\bin
    openssl req -x509 -nodes
      -days 365
      -newkey rsa:2048
      -keyout private.key
      -out certchain.crt
    ```
3. Будет получено 2 файла с приватным и публичным ключом.