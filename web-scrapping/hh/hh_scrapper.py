import dataclasses

import requests
from bs4 import BeautifulSoup


class UrlBuilder:
    def __init__(self):
        self.protocol = None
        self.domain = None
        self.path = None
        self.args = []

    def set_protocol(self, protocol):
        self.protocol = protocol
        return self

    def set_path(self, path):
        self.path = path
        return self

    def set_domain(self, domain):
        self.domain = domain
        return self

    def set_arg(self, key, value):
        self.args.append(f'{key}={value}')
        return self

    def __str__(self):
        url = ''

        if self.protocol:
            url += f'{self.protocol}://'
        else:
            raise ValueError('Protocol was not set!')

        if self.domain:
            url += f'{self.domain}/'
        else:
            raise ValueError('Domain was not set!')

        if self.path:
            url += f'{self.path}'

        if self.args:
            url += '?'
            for arg in self.args:
                url += f'{arg}&'

        return url[:-1]


@dataclasses.dataclass
class Vacancy:
    employer_name: str
    link: str


class HhParser:
    def __init__(self):
        self.page = None

    def search(self, url):
        response = requests.get(url, headers={'User-Agent': 'mozilla/5.0'})
        if response.status_code == 200:
            self.page = BeautifulSoup(response.text, 'html.parser')
        else:
            raise requests.HTTPError(response.status_code)

    def extract_vacancies_info(self):
        vacancies = []
        for vacancy_block in self.page.find_all('div', class_='vacancy-serp-item'):
            v = Vacancy(
                vacancy_block.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).getText().strip(),
                vacancy_block.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'}).get('href')
            )
            vacancies.append(v)
        return vacancies


def main():
    # URL собирается с помощью класса, который реализует паттерн Builder.
    url_builder = UrlBuilder()
    url_builder \
        .set_protocol('https') \
        .set_domain('spb.hh.ru') \
        .set_path('search/vacancy') \
        .set_arg('area', '2') \
        .set_arg('st', 'searchVacancy') \
        .set_arg('text', 'Python') \
        .set_arg('fromSearch', 'true') \
        .set_arg('from', 'suggest_post')

    # Парсер вакансий (пока только первая странца)
    hh = HhParser()
    hh.search(str(url_builder))
    for v in hh.extract_vacancies_info():
        print(v)

    # todo: data-qa: skills-element


if __name__ == '__main__':
    main()


