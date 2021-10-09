import asyncio
import time


JOB_COUNT = 200
WORKER_COUNT = 4


async def heartbeat():
    """
    Выводим в консоль смещение от запланированного выполнения heartbeat.
    Типа сколько нам пришлось лишнего времени ждать, пока heartbeat снова запустится.
    """
    while True:
        start_ts = time.time()
        await asyncio.sleep(1)
        end_ts = time.time()
        delay = end_ts - start_ts - 1
        print(f'headtbeat delay = {delay:.5f}s')


async def process():
    """
    Используем синхронный sleep, т.к. это эмуляция реальной работы CPU.
    В течении этих 10nms никакие другие корутины не могут быть запланированы,
    т.к. наша программа однопотточная.
    """
    time.sleep(0.01)


async def process3():
    await asyncio.sleep(0.01)
    time.sleep(0.01)
    await asyncio.sleep(0.01)


async def main():
    # Запускаем корутину heartbeat в задаче. Корутина будет "прогрессировать",
    # независимо, т.к. мы запихнули её в задачу. И задача ждёт корутину, поэтому
    # она (корутина) не будет простаивать без дела.
    asyncio.create_task(heartbeat())

    # Имитация процесса ожидания, например, запроса к БД или Интернету
    await asyncio.sleep(2.5)

    print('begin processing')

    # Мы запланировали 200 тасок, каждая из которых делает задержку в 10ms.
    # Однако корутина heartbeat была запущена только после 1.5s. Что произошло?
    # Python выполняет запланированные таски через event loop. Каждая таска выполняется
    # по принципу round robin - один за другим в том порядке, в котором таски поступают.
    # 200 тасок планируются ДО heartbeat, поэтому heartbeat не планируется до тех пор,
    # пока каждая из этих 200 тасок не завершится, либо прервётся с помощью await.
    # ВЫВОД: не спавнить большое количество тасок, если задержка является важным фактором.
    for _ in range(JOB_COUNT):
        asyncio.create_task(process())

    await asyncio.sleep(5)


async def main_with_semaphore():
    asyncio.create_task(heartbeat())

    await asyncio.sleep(2.5)

    # Первая идея: использовать семафоры для блокировки количества активных тасок в
    # момент времени. Когда heartbeat sleep завершится, около половины тасок завершится
    # а другая половина будет заблокирована семафором. Однако... семафор не помог, т.к.
    # каждая таска занимает своё место в event loop'е. Даже уменьшение количества воркеров
    # до 1 не поможет. Как только таска завершается, она освобождает запуск следующей
    # таски. Семафор не может сделать тут ничего.
    sem = asyncio.Semaphore(WORKER_COUNT)

    async def process2():
        # Семафор уменьшает счётчик каждый раз, когда вызывается acquire
        await sem.acquire()
        time.sleep(0.1)
        # и увеличивает счётчик каждый раз, когда вызывается release
        sem.release()

    print('begin processing')

    for _ in range(200):
        asyncio.create_task(process2())

    await asyncio.sleep(5)


async def main_with_queue():
    asyncio.create_task(heartbeat())

    await asyncio.sleep(2.5)

    # Job queue - заполняется корутинами, а не тасками! Для GO разработчиков
    # это будет похоже на unbuffered channel, т.к. maxsize=1 - самый типичный channel.
    # Этот канал служит синхронизирующим резеруаром между продьюсером (put()) и
    # консьюмером (get()).  Продьюсер ждёт в очереди с задачей, пока таска не
    # освободится, чтобы забрать её. Таска ждёт в очереди до тех пор, пока не придёт
    # продьюсер и не даст задачу для неё.
    queue = asyncio.Queue(maxsize=1)

    async def worker():
        while True:
            coro = await queue.get()
            await coro
            # Синхронизация: таска выполнена
            queue.task_done()

    workers = [asyncio.create_task(worker()) for _ in range(WORKER_COUNT)]

    print('begin processing')

    # На выходе мы получили минимальную задержку heartbeat - heartbeat продолжал
    # выполнение, пока таски обрабатывались. Чем больше конкурентности - тем больше
    # тасок воркеров запущено в очереди - тем больше задержка.
    # Замечание: увеличение WORKER_COUNT не повлияет на задержку, т.к. задачи на самом
    # деле не конкурентные. Они запускаются, выполняются и завершаются перед тем как
    # другие таски воркеров извлекаются из очереди.
    for _ in range(JOB_COUNT):
        # Добавление пары await'ов в process3() позволяет делать конкурентность.
        # await queue.put(process())
        await queue.put(process3())

    # Так как тасок много, а воркеров мало - мы вернулись к первоначальной проблеме.
    # Уменьшение WORKER_COUNT приводит к увеличению дарежки heartbeat.

    await queue.join()

    print('end processing')

    # Убиваем воркеров. На самом деле их можно было бы оставить как есть.
    # в заблокированном состоянии в очереди - это нормально. Они будут собраны
    # GC. Однако CPython жалуется на GC'ing запущенных тасок, т.к. это выглядит как
    # бага - и это действительно обычно так и есть (смысл удалять таски, если мы
    # ещё с ними работаем?).
    for w in workers:
        w.cancel()

    await asyncio.sleep(2)


async def producer_consumer():
    # Никогда не используйте unbound queues! На самом деле asyncio.Queue()
    # без лимита - это баг. Это дефект API, который позволяет создавать
    # unbounded queues. По умолчанию значение maxsize должно быть 0 (unbuffered),
    # а не inf. Так как unbounded - выбран дефолтном, в каком-то смысле все примеры
    # из официальной документации немного сломаны. Важные выводы:
    # 1. Дефолтная asyncio.Queue() - это баг
    # 2. asyncio.sleep(0) - обычно всегда используется некорректно (это не решает проблему)
    # 3. Используйте maxsize=1 вместо спавна большого количества одинаковых тасок
    # Не стоит путать несколько концепций:
    # - data structure queues
    # - concurrent communication infrastructure queues
    # Последняя обычно называется каналом. unbounded queue (collections.deque) необходима,
    # а вот unbounded channel (asyncio.Queue) - это ошибка.
    queue = asyncio.Queue(maxsize=1)

    # Асинхронный аналог threading.Condition(). Реализует Condition Variable Object.
    # Позволяет одной и более корутине ждать, пока они не будут оповещены другой корутиной.
    done = asyncio.Condition()

    async def producer():
        for i in range(100):
            print(i)
            await queue.put(i)
        # Блокируется до тех пор, пока все элементы очереди не будут обработаны
        await queue.join()
        async with done:
            # По дефолту, возобновляет одну корутину, которая ожидает этого условия
            # (если таковы имеются). Если вызывающая корутина на захватила lock,
            # когда этот метод вызывается, RuntimeError выкидывается. Этот метод
            # возобновляет максимум n корутинг, ожидающих condition variable;
            # Метод нефункционален, если нет ожидающих корутин.
            # Важно: возобновлённая корутина на самом деле не return'ится из wait()
            # до тех пор, пока она не завладеет lock'ом. notify() не снимает lock,
            # этим должна заниматься вызывающая сторона.
            done.notify()

    async def consumer():
        while True:
            await queue.get()
            print(f'qsize = {queue.qsize()}')
            # Используется консьюмерами. Для каждого get() используется для извлечения
            # таска, последующий вызов task_done() уже говорит, что обработка таска завершена.
            # Если join() в настоящий момент блокирует, он возобновится, когда все элементы
            # будут обработаны (что означает, что task_done() будет получен для каждого элемента
            # который был помещён в очередь).
            queue.task_done()

    asyncio.create_task(producer())
    asyncio.create_task(consumer())

    async with done:
        await done.wait()


# asyncio.run(main())
# asyncio.run(main_with_semaphore())
# asyncio.run(main_with_queue())
asyncio.run(producer_consumer())
