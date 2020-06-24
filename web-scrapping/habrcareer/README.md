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

### Просмотр содержимого
```bash
# Проверить, работает ли MongoDB
sudo service mongodb status
# Зайти в командную строку MongoDB
mongo
# Зайти в БД `habrcareer`
use habrcareer
# Вывести все записи документа `company`
db.company.find({})
# Удалить конкретный документ со всем содержимым
db.company.remove({})
``
