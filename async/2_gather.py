"""
Аналог предыдущего примера, но вместо низкоуровневого asyncio.wait, который
позволяет более точно управлять тасками:
- определять таймауты.
- останавливать выполнение после определённого момента (напр. после
  завершения первого таска).
Здесь используется высокоуровневый asyncio.gather, в который сразу же
передаются таски. Удобством является возможность создавать группы из групп
тасков, используя один gather внутри другого. Также можно прекращать
выполнение необходимой группы: group.cancel().
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
    loop = asyncio.get_event_loop()
    # Стоит заметить, что таски сразу же передаются в функцию, без list()!
    group = asyncio.gather(
        asyncio.ensure_future(count('Foo', 1, 17)),
        asyncio.ensure_future(count('Bar', 7, 12)),
        asyncio.ensure_future(count('Baz', 13, 25)),
    )
    loop.run_until_complete(group)
    loop.close()


if __name__ == '__main__':
    main()
