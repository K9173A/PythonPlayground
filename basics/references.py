import gc
import sys
import weakref


# Выводит количество ссылок для объекта. Количество ссылок будет зависеть и от использования
# в стандартной библиотеке Python. Именно поэтому у `1` больше ссылок, чем у `102332`.
# Минимальное значение равно `3`, потому что сам `sys.getrefcount` создаёт временные ссылки,
# когда вызывается. В целом можно воспринимать `3`, как значение, что объект используется
# только в одном месте в коде, и нигде больше. И если импортировать `numpy` и `matplotlib`,
# то использование маленьких чисел ещё возрастёт - количество ссылок увеличится.
print(sys.getrefcount(1))  # 180
print(sys.getrefcount(2))  # 127
print(sys.getrefcount(3))  # 40
print(sys.getrefcount(4))  # 75
print(sys.getrefcount(5))  # 32
print(sys.getrefcount(102332))  # 3
print(sys.getrefcount(10231132))  # 3
print('-' * 80)


# Количество затрачиваемой памяти под каждый тип:
# Bytes  type        empty + scaling notes
# 24     int         NA
# 28     long        NA
# 37     str         + 1 byte per additional character
# 52     unicode     + 4 bytes per additional character
# 56     tuple       + 8 bytes per additional item
# 72     list        + 32 for first, 8 for each additional
# 232    set         sixth item increases to 744; 22nd, 2280; 86th, 8424
# 280    dict        sixth item increases to 1048; 22nd, 3352; 86th, 12568 *
# 120    func def    does not include default args and other attrs
# 64     class inst  has a __dict__ attr, same scaling as dict above
# 16     __slots__   class with slots has no dict, seems to store in
#                     mutable tuple-like structure.
# 904    class def   has a proxy __dict__ structure for class attrs
# 104    old class   makes sense, less stuff, has real dict though.
class Foo:
    def __init__(self):
        self.data = {str(i): i for i in range(1000)}

    def __del__(self):
        print(f'Deleting {self}')


def weak_ref_callback(reference):
    print(f'Reference: {reference}')


foo = Foo()
# Просто объект по адресу: `foo: <__main__.Foo object at 0x01D5B0D0>`
print('foo:', foo)

foo_weak_ref = weakref.ref(foo, weak_ref_callback)
# Слабая ссылка по адресу: `foo_weak_ref: <weakref at 0x03A41A00; to 'Foo' at 0x01D5B0D0>`
print(f'foo_weak_ref: {foo_weak_ref}')
# Получение объекта `foo` по слабой ссылке: `foo_weak_ref(): <__main__.Foo object at 0x01D5B0D0>`
print(f'foo_weak_ref(): {foo_weak_ref()}')

# Получение количества слабых ссылок на объект `foo`. Равно `1`.
print(weakref.getweakrefcount(foo))
# Удаление объекта. Так как мы используем слабую ссылку, GC удалит объект.
# Вначале вызывается метод `__del__`: `Deleting <__main__.Foo object at 0x0143B0D0>`
# Далее срабатывает `weak_ref_callback`: `Reference: <weakref at 0x03813988; dead>`
del foo

# Пытаемся получить объект по слабой ссылке, но возвращает `foo_weak_ref(): None`,
# так как мы удалили объект
print(f'foo_weak_ref(): {foo_weak_ref()}')

print('-' * 80)


# Вместо использования `weakref.ref` напрямую, лучше использовать прокси. Прокси можно использовать
# как-будто они являются оригинальными объектами (теми, на которые они ссылаются). В тамом случае не
# придётся вызывать `ref()` для доступа к объекту.
class Bar:
    def __init__(self):
        self.data = {str(i): i for i in range(1000)}

    def __del__(self):
        print(f'Deleting {self}')


bar = Bar()
bar_weak_ref = weakref.ref(bar)
bar_proxy = weakref.proxy(bar)

print('bar:', bar)
print('bar_weak_ref():', bar_weak_ref())  # bar_weak_ref(): <__main__.Bar object at 0x037CF6D0>
print('bar_proxy:', bar_proxy)  # bar_proxy: <__main__.Bar object at 0x037CF6D0>

# Если попытаться получить доступ к объекту через прокси, после того, как объекь был удалён,
# будет выкинуто исключение `ReferenceError: weakly-referenced object no longer exists`.
del bar  # print('bar_proxy:', bar_proxy.data)


# Кэширование объектов. `ref` и `proxy` считаются низкоуровневыми. Они полезны для создания слабых ссылок для
# отдельных объектов и позволяют создавать циклические ссылки, которые будут собраны GC. Если требуется создавать
# кэш нескольких объектов, самым подходящим API будет `WeakKeyDictionary` и `WeakValueDictionary`.

# Если нужно включить выведение адресов и объектов, которые удаляются GC, то раскомментировать.
# gc.set_debug(gc.DEBUG_LEAK)


class Baz:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'{Baz.__name__}({self.name})'

    def __del__(self):
        print(f'(Deleting {self})')


def demo(cache_storage_datatype):
    # Удерживает объекты, чтобы слабые ссылки не удалялись сразу же
    all_refs = {}

    print(f'CACHE TYPE: {cache_storage_datatype}')

    cache = cache_storage_datatype()

    # Заполняем и `cache` и `all_refs`, чтобы удерживать объекты от удаления.
    for name in ['one', 'two', 'three']:
        baz = Baz(name)
        cache[name] = baz
        all_refs[name] = baz
        del baz  # Эта ссылка нам больше не нужна

    print(f'all_refs={all_refs}')

    # Результат для `dict`: `['one', 'two', 'three']`
    # Результат для `WeakValueDictionary`: `['one', 'two', 'three']`
    print('Cache contains (before): {}'.format(list(cache.keys())))

    for name, value in cache.items():
        print(f'\t{name} = {value}')
        del value  # Уменьшаем количество ссылок на объект

    # Удаляем все ссылки на наши объекты за исключением тех, что хранятся в `cache`
    print('Cleanup')
    del all_refs

    # Активируем GC, чтобы он удалил все объекты, на которые нет ссылок. Для `dict`
    # ничего не будет удалено, а для `WeakValueDictionary` - всё удалится, т.к. это слабые ссылки.
    gc.collect()

    # Результат для `dict`: `['one', 'two', 'three']`
    # Результат для `WeakValueDictionary`: `[]`
    print('Cache contains (after): {}'.format(list(cache.keys())))
    for name, value in cache.items():
        print(f'\t{name} = {value}')


demo(dict)
print('---')
demo(weakref.WeakValueDictionary)


# todo: циклические ссылки
