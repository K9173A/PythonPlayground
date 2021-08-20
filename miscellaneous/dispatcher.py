import abc
import dataclasses
import random
import threading
import time
import typing


@dataclasses.dataclass
class Event:
    name: str
    data: dict

    def __str__(self) -> str:
        return f'<Event: {self.name} Data: {self.data}>'


class Runnable:
    def __init__(self):
        self._runner = threading.Thread(target=self.run)
        self._is_running: bool = False

    @abc.abstractmethod
    def run(self) -> None:
        raise NotImplementedError

    def start(self) -> None:
        self._is_running = True
        self._runner.start()

    def stop(self) -> None:
        self._is_running = False


class EventsQueue:
    def __init__(self, length) -> None:
        self._length: int = length
        self.__lock: threading.Lock = threading.Lock()
        self._queue: typing.List[Event] = []

    def push(self, event: Event) -> None:
        if len(self._queue) < self._length:
            with self.__lock:
                self._queue.append(event)
        else:
            print('Exceeded queue maximum length!')

    def pop(self):
        if len(self._queue) > 0:
            with self.__lock:
                return self._queue.pop(0)
        else:
            return None


class Consumer:
    def __init__(self, name: str) -> None:
        self._name: str = name

    def consume_event(self, event: Event) -> None:
        print(f'Consumer {self._name} got event {event}!')


class Producer(Runnable):
    def __init__(self, name: str):
        super(Producer, self).__init__()
        self._name: str = name
        self._dispatcher: typing.Union['Dispatcher', None] = None
        self._runner = threading.Thread(target=self.run)

    def set_dispatcher(self, dispatcher: 'Dispatcher') -> None:
        self._dispatcher: 'Dispatcher' = dispatcher

    def run(self):
        while self._is_running:
            self.emit()
            time.sleep(random.randint(a=1, b=10))
            print(f'Running producer {self._name}...')

    def emit(self):
        self._dispatcher.push_event_to_queue(
            Event(name=f'{self._name}',
                  data={'foo': random.randint(a=1, b=10)})
        )


class Dispatcher(Runnable):
    def __init__(self):
        super(Dispatcher, self).__init__()
        self._producers: typing.List[Producer] = []
        self._consumers: typing.List[Consumer] = []
        self._queue: EventsQueue = EventsQueue(100)

    def run(self):
        while self._is_running:
            event = self._queue.pop()
            if event:
                self.__send_event_to_consumers(event)
            time.sleep(1)
            print('Running dispatcher...')

    def push_event_to_queue(self, event: Event) -> None:
        self._queue.push(event)

    def add_producer(self, producer: Producer) -> None:
        self._producers.append(producer)

    def add_consumer(self, consumer: Consumer) -> None:
        self._consumers.append(consumer)

    def __send_event_to_consumers(self, event: Event) -> None:
        for consumer in self._consumers:
            consumer.consume_event(event)


def main():
    dispatcher = Dispatcher()

    p1 = Producer('Foo')
    p2 = Producer('Bar')
    p3 = Producer('Baz')

    p1.set_dispatcher(dispatcher)
    p2.set_dispatcher(dispatcher)
    p3.set_dispatcher(dispatcher)

    dispatcher.add_producer(p1)
    dispatcher.add_producer(p2)
    dispatcher.add_producer(p3)

    dispatcher.add_consumer(Consumer('Kyle'))
    dispatcher.add_consumer(Consumer('Andrew'))
    dispatcher.add_consumer(Consumer('Luke'))

    dispatcher.start()

    p1.start()
    p2.start()
    p3.start()


if __name__ == '__main__':
    main()
