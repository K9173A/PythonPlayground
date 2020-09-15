import logging

# Название логгера
logger = logging.getLogger('my_logger')
# Уровень логирования
logger.setLevel(logging.INFO)

# Объект, который контролирует дескриптор файла для логирования.
loggerFileHandler = logging.FileHandler('test.log')
# Можно установить уровнерь логированя именно для файла.
loggerFileHandler.setLevel(logging.INFO)

# Объект, который контролирует дескриптор для вывода в консоль (stdout).
loggerStreamHandler = logging.StreamHandler()
# Можно установить уровнерь логированя для вывода в консоль.
loggerStreamHandler.setLevel(logging.INFO)

# Объект, который задаёт форматирование для объектов дескрипторов.
loggerFormatter = logging.Formatter('[%(levelname)s %(asctime)s %(filename)s:%(lineno)s @ %(funcName)s()] %(message)s')
# Необходимо задать форматтер для каждого дескриптора.
loggerFileHandler.setFormatter(loggerFormatter)
loggerStreamHandler.setFormatter(loggerFormatter)

# Затем необходимо добавить дескрипторы в объект логгера
logger.addHandler(loggerFileHandler)
logger.addHandler(loggerStreamHandler)


def func_info():
    logger.info('INFO!')


def func_warning():
    logger.warning('WARNING!')


def func_error():
    logger.error('ERROR!')


def func_critical():
    logger.critical('CRITICAL ERROR!')


def main():
    func_info()      # [INFO 2020-07-05 03:36:13,174 log.py:32 @ func_info()] INFO!
    func_warning()   # [WARNING 2020-07-05 03:36:13,174 log.py:36 @ func_warning()] WARNING!
    func_error()     # [ERROR 2020-07-05 03:36:13,175 log.py:40 @ func_error()] ERROR!
    func_critical()  # [CRITICAL 2020-07-05 03:36:13,175 log.py:44 @ func_critical()] CRITICAL ERROR!


if __name__ == '__main__':
    main()
