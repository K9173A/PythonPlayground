import queue

import requests
from bs4 import BeautifulSoup

from .models import Company
from .storage import Storage


class WebCrawler:
    def __init__(self):
        self.base_url = 'https://career.habr.com/companies'
        self.companies_queue = queue.Queue()
        self.storage = Storage()

    def run(self):
        self.visit_company_page('webimru')
        while not self.companies_queue.empty():
            company = self.companies_queue.get()
            # Если компания уже в БД, то пропускаем её
            if not self.storage.get_company(company):
                self.visit_company_page(company)

    def visit_company_page(self, company):
        response = requests.get(f'{self.base_url}/{company}',
                                headers={'User-Agent': 'mozilla/5.0'})

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
        else:
            raise requests.HTTPError(response.status_code)

        for src_company, n in self.extract_companies(soup, 'Откуда приходят в компанию'):
            if not self.storage.get_company(src_company.link):
                self.storage.save_company(src_company)
                self.storage.save_transition(Transition(
                    src=None,  # todo
                    dst=src_company.link,
                    n=n
                ))
                self.companies_queue.put(src_company.link)

        for dst_company, n in self.extract_companies(soup, 'В какие компании уходят'):
            if not self.storage.get_company(dst_company.link):
                self.storage.save_company(dst_company)
                self.storage.save_transition(Transition(
                    src=None,  # todo
                    dst=dst_company.link,
                    n=n
                ))
                self.companies_queue.put(dst_company.link)

    @staticmethod
    def extract_companies(soup, text):
        companies = []
        section = soup.find('div', text=re.compile(text)).parent

        for company_item in section.find_all('div', class_='company_item'):
            style = company_item.find('a', class_='logo').get('style')
            title = company_item.find('a', class_='title')
            count = int(company_item.find('a', class_='count').getText().split()[0])
            # Поле to будет заполнено только после посещения страницы компании?
            companies.append(Company(
                name=title.getText().strip(),
                logo=style[style.index('(') + 1:style.index(')')],
                link=title.get('href').split('/')[-1]
            ), count)

        return companies
