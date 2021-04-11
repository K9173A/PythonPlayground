import os
import datetime
import pathlib
import functools

from PIL import Image


class ImageEditor:
    def __init__(self, img_path):
        p = pathlib.Path(img_path)
        self.dir_path = p.parent
        name, ext = p.name.split('.')
        self.name = name
        self.ext = ext
        self.img = Image.open(img_path)
        self.width = self.img.size[0]
        self.height = self.img.size[1]
        self.pixel_map = self.img.load()

    def apply(self, f):
        for i in range(self.width):
            for j in range(self.height):
                self.pixel_map[i, j] = f(*self.pixel_map[i, j])
        return self

    def __del__(self):
        out_img = self.img.copy()

        suffix = datetime.datetime.now().strftime('%H-%M-%S')
        new_img_name = f'{self.name}-{suffix}.{self.ext}'
        new_img_path = os.path.join(self.dir_path, new_img_name)

        out_img.save(new_img_path)


def build_filter(f, *args):
    return functools.partial(f, *args)


def limit_channel_value(channel):
    if channel < 0:
        return 0
    if channel > 255:
        return 255
    return channel


def modify_channel(channel, delta, condition, r, g, b):
    if channel == 'r':
        if condition(r):
            r = limit_channel_value(r + delta)
    elif channel == 'g':
        if condition(g):
            g = limit_channel_value(g + delta)
    elif channel == 'b':
        if condition(b):
            b = limit_channel_value(b + delta)
    else:
        raise ValueError('Incorrect channel value!')
    return r, g, b


def custom_inversion(*channels):
    """
    Кастомный эффект "негатива". Битовая инверсия каждого канала.
    Весьма странный эффект.
    :param channels: каналы RGB.
    :return: RGB с применённой битовой инверсией.
    """
    rgb = []
    for channel in channels:
        bin_channel = bin(channel)[2:]
        inverted = ''
        for c in bin_channel:
            inverted += '0' if c == '1' else '1'
        rgb.append(int(inverted, 2))
    return tuple(rgb)


def inversion(r, g, b):
    """
    Эффект негатива.
    :param r: значение канала Red.
    :param g: значение канала Green.
    :param b: значение канала Blue.
    :return: RBG с эффектом негатива.
    """
    return 255 - r, 255 - g, 255 - b


def contrast(low, high, *channels):
    """
    Эффект пониженной контрастности.
    :param low: нижнаяя граница.
    :param high: верхняя граница.
    :param channels: RGB каналы.
    :return: RGB c эффектом кпониженной контрастности.
    """
    rgb = []
    for channel in channels:
        if channel < low:
            rgb.append(low)
        elif channel > high:
            rgb.append(high)
        else:
            rgb.append(channel)
    return tuple(rgb)


def black_and_white(f, *channels):
    """
    Делает картинку чёрно-белой.
    :param f: функция сравнения каналов для выбора значения, должна
    возвращать одно из значений канала.
    :param channels: RGB каналы.
    :return: RBG с чёрно-белым эффектом.
    """
    return (f(channels),) * 3


def sepia(r):
    """
    Применяет эффект сепии - коричнево-оранжевые тона.
    В данном варианте учитывается только красный канал.
    Он берётся за 100% и от него выстраивается отношение других каналов.
    На Википедии указано соотношение RGB: (112. 66. 20), соответственно
    выведены соотношения:
    g: 66 / 112 = 0.5892
    b: 20 / 112 = 0.1785
    :param r:
    :return: RBG с эффектом сепии.
    """
    return r, int(r * 0.5892), int(r * 0.1785)


def main():
    img_name = 'photo.jpg'
    img_dir = os.path.dirname(__file__)
    img_path = os.path.join(img_dir, img_name)

    image_editor = ImageEditor(img_path)

    # Простые фильтры с подкручиванием конкретных каналов
    # min_red = build_filter(modify_channel, 'r', -255, lambda channel: channel > 0)
    # max_green = build_filter(modify_channel, 'b', 255, lambda channel: True)
    # image_editor.apply(min_red).apply(max_green)

    # Негатив
    # image_editor.apply(inversion)

    # Инверсия (неудачная попытка написания негатива), но прикольно
    # image_editor.apply(custom_inversion)

    # Контрастность
    # contrast_filter = build_filter(contrast, 100, 150)
    # image_editor.apply(contrast_filter)

    # Чёрно-белая картинка по разным функциям (максимальное, минимальное и среднее значения)
    # min_black_and_white_filter = build_filter(black_and_white, min)
    # max_black_and_white_filter = build_filter(black_and_white, max)
    # avg_black_and_white_filter = build_filter(black_and_white, lambda channels: int(sum(channels) / 3))

    # Более чёрный вариант
    # image_editor.apply(min_black_and_white_filter)
    # Более белый вариант
    # image_editor.apply(max_black_and_white_filter)
    # Усреднённый вариант
    # image_editor.apply(avg_black_and_white_filter)

    # Сепия
    # image_editor.apply(sepia)


if __name__ == '__main__':
    main()
