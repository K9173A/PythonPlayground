

class Company:
    def __init__(self, name, link, logo):
        self.name = name
        self.link = link
        self.logo = logo

    def to_dict(self):
        return {'name': self.name,
                'link': self.link,
                'logo': self.logo}


class Transitions:
    def __init__(self, src, dst, n):
        self.src = src
        self.dst = dst
        self.n = n

    def to_dict(self):
        return {'src': self.src,
                'dst': self.dst,
                'n': self.n}
