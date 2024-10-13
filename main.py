from crawler import Crawler

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