# coding=utf-8
import urllib2
import re
from bs4 import BeautifulSoup

response = urllib2.urlopen('https://www.iana.org/domains/root/db')
parsed_html = BeautifulSoup(response.read(), features='html.parser')

spans = parsed_html.find_all(
    lambda tag: tag.name == 'span' and tag.get('class') == ['domain', 'tld']
)

pattern = re.compile(ur'^\.[\u0410-\u042F\u0430-\u044F\u0451\u0401\d_]+$', re.UNICODE)
matched = []
for span in spans:
    domain = span.find('a').getText()
    # А-Яа-яёЁ
    if pattern.match(domain):
        matched.append(domain[1:])
