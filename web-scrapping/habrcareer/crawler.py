import re
import queue

import requests
from bs4 import BeautifulSoup

from .models import Company, Transition
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
        response = requests.get(
            f'{self.base_url}/{company}', headers={'User-Agent': 'mozilla/5.0'}
        )

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
        else:
            raise requests.HTTPError(response.status_code)

        company_search_text = {
            'src': 'Откуда приходят в компанию',
            'dst': 'В какие компании уходят'
        }

        for key, text in company_search_text.items():
            section = soup.find('div', text=re.compile(text)).parent

            for company_item in section.find_all('div', class_='company_item'):
                style = company_item.find('a', class_='logo').get('style')
                title = company_item.find('a', class_='title')

                link = title.get('href').split('/')[-1]

                if not self.storage.get_company(link):
                    self.storage.save_company(Company(
                        name=title.getText().strip(),
                        logo=style[style.index('(') + 1:style.index(')')],
                        link=link
                    ))

                    self.storage.save_transition(Transition(
                        src=link if key is 'src' else company,
                        dst=company if key is 'src' else link,
                        n=int(company_item.find('a', class_='count').getText().split()[0])
                    ))

                    self.companies_queue.put(link)

