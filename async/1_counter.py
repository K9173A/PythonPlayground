"""
Пример, где создаются 3 таска на корутину, которая занимается инкрементом
числа и выводом его значения в консоль. Event loop по условию завершает
работу только после того, как все таски будут завершены.
"""
import asyncio


async def count(task_name, n, limit):
    """
    Простая корутина, которая делает инкремент n, пока не достигнет значения
    limit.
    :param task_name: Название таска (чтобы можно было различить их в консоли).
    :param n: число, которое будем инкрементировать.
    :param limit: верхний предел инкремента числа.
    :return: None.
    """
    while n < limit:
        print(f'task: {task_name} | n: {n} | limit: {limit}')
        await asyncio.sleep(1)
        n += 1


def main():
    """
    Основная функция, где создаются такски на счётчики и запускается event loop.
    :return: None.
    """
    # Создание event loop, наиболее подходящего для данной ОС.
    loop = asyncio.get_event_loop()
    # Список из тасков - обёрток для корутин count().
    # Начиная с версии Python 3.7 можно использовать asyncio.create_task().
    tasks_pool = [
        asyncio.ensure_future(count('Foo', 1, 17)),
        asyncio.ensure_future(count('Bar', 7, 12)),
        asyncio.ensure_future(count('Baz', 13, 25)),
    ]
    # event loop выполняет до тех пор, пока футуры не примут статус "завершены".
    loop.run_until_complete(
        # Запускает конкурентно таски и блокирует, пока условие return_when
        # не выполнится. В нашем случае используем значение по умолчанию:
        # функция вернётся, когда все футуры завершатся или будут прекращены.
        asyncio.wait(tasks_pool, return_when=asyncio.ALL_COMPLETED)
    )
    # Закрывает event loop. Любые callback'и в состоянии ожидания будут стёрты.
    # Этот метод очищает все очереди и удаляет executor, но не дожидается, пока
    # executor завершит работу. Никакие методоы не должны вызываться после него!
    loop.close()


if __name__ == '__main__':
    main()
