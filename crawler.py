import re
from typing import Iterable
from bs4 import BeautifulSoup
import requests
import urllib



def is_link(url: str) -> bool:
    last = url.split('/')[-1]
    if last.endswith('.html'):
        return True
    if '.' in last:
        return False
    return True


class Crawler:
    def __init__(self, regex: str, base_url: str, ignored_urls: Iterable[str]):
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
        if not is_link(url):
            return False
        return True

    def get_urls(self, soup: BeautifulSoup) -> set[str]:
        urls = soup.find_all('a', href=True)
        rel_urls: set[str]  = set()
        for u in urls:
            u: str = u['href']
            if u.startswith('/'):
                u = urllib.parse.urljoin(self.base_url, u)
            if not self.is_valid(u):
                continue
            rel_urls.add(u)
        return rel_urls