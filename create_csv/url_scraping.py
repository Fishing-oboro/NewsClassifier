# ニュース記事の取得
from bs4 import BeautifulSoup
import requests
import time
import csv


class LiveDoorScraping:
    def __init__(self, header, categories=None):
        if categories is None:
            categories = ['dom', 'world', 'eco', 'ent', 'sports', 'gourmet', 'love', 'trend']
        self.categories = categories
        self.base_url = 'https://news.livedoor.com/topics/category/'
        self.headers = header

    def soup(self, url):
        time.sleep(3)
        html = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(html.content, 'html.parser')
        return soup

    def get_url(self, page=1):
        url_list = []
        for i, category in enumerate(self.categories):
            category_url = self.base_url + category + '/'
            urls = [topic_soup.find('a').attrs["href"].replace('topics', 'article') for topic_soup in
                    self.soup(category_url).findAll('li', {'class': 'hasImg'})]
            # 1のときは無し、2から追加
            n = 2
            while page >= n:
                next_url = category_url + '?p=' + str(n)
                a_urls = [topic_soup.find('a').attrs["href"].replace('topics', 'article') for topic_soup in
                          self.soup(next_url).findAll('li', {'class': 'hasImg'})]
                urls.extend(a_urls)
                n += 1
            url_list.append(urls)
        return url_list

    def get_data(self, url_list=get_url):
        d = {'\u3000': None, '\n': None, ' ': None, '\xa0': None}
        trans = str.maketrans(d)

        articles = []
        for number, urls in enumerate(url_list):
            print(self.categories[number])
            for url in urls:
                try:
                    soup_obj = self.soup(url)
                    if soup_obj.original_encoding == 'windows-1252':
                        print('error')
                        continue

                    title = soup_obj.find('h1', {'class': 'articleTtl'}).text.translate(trans)

                    paragraph_list = [p.text for p in soup_obj.find('span', {'itemprop': 'articleBody'}).find_all('p')]
                    paragraph = ''.join(paragraph_list).translate(trans)

                    article = {
                        'category': self.categories[number],
                        'title': title,
                        'url': url,
                        'sentence': paragraph
                    }
                    print(article)  # log
                    articles.append(article)
                except AttributeError:
                    print("error")
                    continue
        return articles

    def create_csv(self, url='./sample.create_csv', articles=None):
        if articles is None:
            articles = self.get_data
        with open(url, mode='w', encoding='utf-8') as f:
            writer = csv.DictWriter(f, ['category', 'title', 'url', 'sentence'])
            writer.writeheader()
            writer.writerows(articles)
