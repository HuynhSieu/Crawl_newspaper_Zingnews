import logging
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO)

class Zing:
    def __init__(self, links=[]):
        self.subject_links = []
        self.links_of_subject = links

    def get_url(self, url):
        return requests.get(url).text

    def get_linked_links(self, url, html):
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a'):
            path = link.get('href')
            if path and path.startswith('/'):
                path = urljoin(url, path)
            return path

    def add_url_to_list(self, url):
        if url not in self.subject_links and url not in self.links_of_subject:
            self.links_of_subject.append(url)
        print(self.links_of_subject)

    def crawl(self, url):
        html = self.get_url(url)
        for url in self.get_linked_links(url, html):
            self.add_url_to_list(url)

    def run(self):
        while self.links_of_subject:
            url = self.links_of_subject.pop(0)
            logging.info(f'Crawling: {url}')
            try:
                lambda x: x not in self.crawl(url), url
            except Exception:
                logging.exception(f'Failed to crawl: {url}')
            finally:
                self.subject_links.append(url)

if __name__ == '__main__':
    Zing(links=['https://zingnews.vn/']).run()
