import os
import re
import bisect
import pathlib
import dataclasses
from urllib.request import urlopen

from bs4 import BeautifulSoup


@dataclasses.dataclass
class Company:
    company_name: str
    company_link: str
    logo_link: str


class CompanyStorage:
    def __init__(self, path):
        self.file_path = path
        self.content = self.__load_content()

    def __del__(self):
        self.__save_content()

    def is_visited_page(self, url):
        i = bisect.bisect_left(self.content, url)
        return i != len(self.content) and self.content[i] == url

    def store_url(self, url):
        if not self.is_visited_page(url):
            bisect.insort(self.content, url)

    def __load_content(self):
        content = []
        with open(self.file_path, mode='r') as f:
            for line in f.readline():
                bisect.insort(content, line.strip())
        return content

    def __save_content(self):
        with open(self.file_path, mode='w') as f:
            for url in self.content:
                f.write(url + '\n')


class WebCrawler:
    def __init__(self, start_with_company):
        self.base_url = 'https://career.habr.com/companies'
        self.start_with_company = start_with_company
        # self.urls_storage = CompanyStorage(
        #     os.path.join(self.working_data_dir_path, 'parsed_urls.txt')
        # )
        # self.__create_working_dir_if_needs()

    @property
    def working_data_dir_path(self):
        return os.path.join(os.path.dirname(__file__), 'working-data')

    def __create_working_dir_if_needs(self):
        try:
            pathlib.Path(self.working_data_dir_path).mkdir()
        except FileExistsError:
            pass
        except FileNotFoundError as e:
            print(e)

    def crawl(self):
        company_name = self.start_with_company
        html = urlopen(f'{self.base_url}/{company_name}').read()

        soup = BeautifulSoup(html, 'html.parser')

        src = self.extract_companies(soup, 'Откуда приходят в компанию')
        dst = self.extract_companies(soup, 'В какие компании уходят')

        print('src', src)
        print('dst', dst)

        # Сохранение страницы для дальнейшей работы
        # company_file_abs_path = os.path.join(self.working_data_dir_path, f'{company_name}.html')
        # with open(company_file_abs_path, mode='wb') as f:
        #     f.write(html)

    @staticmethod
    def extract_companies(soup, text):
        companies = []
        section = soup.find('div', text=re.compile(text)).parent
        for company_item in section.find_all('div', class_='company_item'):
            company_style = company_item.find('a', class_='logo').get('style')
            company_logo_url = company_style[
                company_style.index('(') + 1:company_style.index(')')
            ]
            company_title_block = company_item.find('a', class_='title')
            company_name = company_title_block.getText().strip()
            company_link = company_title_block.get('href')

            companies.append(Company(company_name, company_link, company_logo_url))
        return companies


def main():
    web_crawler = WebCrawler('webimru')
    web_crawler.crawl()


if __name__ == '__main__':
    main()
