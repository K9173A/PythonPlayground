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


def build_filter(channel, delta, condition):
    return functools.partial(modify_channel, channel, delta, condition)


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


def main():
    img_name = 'photo.jpg'
    img_dir = os.path.dirname(__file__)
    img_path = os.path.join(img_dir, img_name)

    image_editor = ImageEditor(img_path)

    min_red = build_filter('r', -255, lambda channel: channel > 0)
    max_green = build_filter('b', 255, lambda channel: True)

    image_editor \
        .apply(min_red) \
        .apply(max_green)


if __name__ == '__main__':
    main()
