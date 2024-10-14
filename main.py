import re
from bs4 import BeautifulSoup
import requests
from urllib import parse


class Crawler:
    def __init__(self, regex: str, base_url: str, ignored_urls: list[str]):
        self.visited_urls: set[str] = set()
        self.emails_set:set[str] = set()
        self.regex = regex
        self.base_url = base_url
        self.ignored_urls = set(ignored_urls)

    def visit(self, current_url: str):
        if current_url in self.visited_urls:
            return
        print(current_url)
        self.visited_urls.add(current_url)
        try:
            r = requests.get(current_url)
            soup = BeautifulSoup(r.content, "html.parser")
        except Exception as e:
            print(f"failed to get {current_url}\n Exception: {e}")
            return
        
        emails :list[str] = re.findall(self.regex, r.text)
        urls = self.get_urls(soup)
        for e in emails:  
            self.emails_set.add(e)
        for url in urls:
            self.visit(url)
    
    def is_valid(self, url: str) -> bool:
        if url in self.ignored_urls:
            return False
        if not url.startswith(self.base_url):
            return False
        if not self.is_link(url):
            return False
        return True
    


    @staticmethod
    def is_link(url: str) -> bool:
        last = url.split('/')[-1]
        if last.endswith('.html'):
            return True
        if '.' in last:
            return False
        return True

    def get_urls(self, soup: BeautifulSoup) -> set[str]:
        urls = soup.find_all('a', href=True)
        rel_urls: set[str]  = set()
        url_strings: list[str] = [u['href'] for u in urls]
        for u in url_strings:
            if u.startswith('/'):
                u = parse.urljoin(self.base_url, u)
            if not self.is_valid(u):
                continue
            rel_urls.add(u)
        return rel_urls
    

BASE_URL = 'https://ccis.ksu.edu.sa'
EMAIL_REGEX = r'[\w_.-]+@ksu.edu.sa'
IGNORED = [
    'https://ccis.ksu.edu.sa/ar/samllogin',
    'https://ccis.ksu.edu.sa/en/samllogin',
]

def main():
    crawler = Crawler(
        EMAIL_REGEX,
        BASE_URL,
        IGNORED
    )
    url = f'{BASE_URL}/en'
    crawler.visit(url)

    with open('emails.txt', 'w') as f:
        f.write('\n'.join(crawler.emails_set))

    with open('visited_urls.txt', 'w') as f:
        f.write('\n'.join(crawler.visited_urls))


if __name__ == "__main__":
    main()
