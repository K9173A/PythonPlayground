### Установка MongoDB
```bash
sudo apt install -y mongodb
sudo systemctl status mongodb
# Проверка соединения
mongo --eval 'db.runCommand({ connectionStatus: 1 })'
```

### Установка пакетов
```bash
virtualenv -p /usr/bin/python3.8 venv-habrcareer
source venv-habrcareer/bin/activate
pip install -r requirements.txt
```
