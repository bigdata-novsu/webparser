import urllib3
from urllib.parse import urljoin
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import api.utils as utils
import api.web_parser_api as parser

def get_domain(url):
    return '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(url))

def get_sub_pages(page):
    href_list = []

    http = urllib3.PoolManager()
    resp = http.request('GET', page)
    soup = BeautifulSoup(resp.data)
    urls = parser.get_all_links(soup)
    for a in urls:
        link = a.get('href')
        if not link.startswith('http'):
            link = urljoin(page, link)
        href_list.append(link)
    return href_list

def get_pages(url):
    domain = get_domain(main_page)
    pages = get_sub_pages(domain)
    pages.append(domain)
    return list(filter(lambda x: str(x).startswith(domain), pages))

main_page = 'http://www.fsb.ru'
pages = get_pages(main_page)
utils.dump_to_file('pages.txt', pages)
