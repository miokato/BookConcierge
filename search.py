"""
Search info about book from web. 
"""
from pprint import pprint
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup as bs


class BookScraper(object):
    search_url = 'http://www.honyaclub.com/shop/goods/search.aspx?'
    main_url = 'https://www.honyaclub.com'
    number_of_books = 1
    books_title = []
    books_image_url = []
    books_detail_url = []

    def fetch(self, keyword, number_of_books=1):
        self.number_of_books = number_of_books

        if self.number_of_books <= 0 or self.number_of_books > 5:
            return None

        if keyword == '':
            self.books_title = ''
            self.books_image_url = ''
            self.books_detail_url = ''

        encoded_keyword = keyword.encode('Shift-JIS')

        payload = {
            'search': 'x',
            'keyw': encoded_keyword,
        }

        r = requests.get(self.search_url, params=payload)
        soup = bs(r.content, 'html.parser')
        try:
            books_data = soup.find('div', class_='result-item')
            books_detail = books_data.find_all('div', class_='item-img',
                                               limit=self.number_of_books)

            self.books_title = [book.img.get('alt') for book in books_detail]

            books_image_elements = [book.img.get('src') for book in books_detail]
            self.books_image_url = [urljoin(self.main_url, path) for path in books_image_elements]

            books_detail_elements = [book.a.get('href') for book in books_detail]
            self.books_detail_url = [urljoin(self.main_url, path) for path in books_detail_elements]

            # get author data and url
            books_info = books_data.find_all('dl', class_='item-txt')
            books_author = [book.find('dd').find('a') for book in books_info]

        except AttributeError:
            return None

        return True

    def dump(self):
        return (self.books_title,
                self.books_image_url,
                self.books_detail_url)


def fetch_books(keyword, number_of_books=1):
    """
    Honya Clubから本のタイトル、詳細リンク、画像リンクを取得する
    :param keyword: str (book title what you want search) 
    :param number_of_books: int ( 1 <= books <= 5 )
    :return: 3 list's tuple (title, image_link, detail_link)  
    """
    search_url = 'http://www.honyaclub.com/shop/goods/search.aspx?'
    main_url = 'https://www.honyaclub.com'
    encode_word = keyword.encode('Shift-JIS')

    payload = {
        'search': 'x',
        'keyw': encode_word,
    }

    if number_of_books <= 0 or number_of_books > 5:
        return None

    r = requests.get(search_url, params=payload)
    soup = bs(r.content, 'html.parser')
    try:
        books_data = soup.find('div', class_='result-item')
        # それぞれの本を取得
        books_detail = books_data.find_all('div', class_='item-img', limit=number_of_books)
        # get alt elements
        books_title = [book.img.get('alt') for book in books_detail]
        # get src elements
        books_image_elements = [book.img.get('src') for book in books_detail]
        books_image_url = [urljoin(main_url, path) for path in books_image_elements]
        # get href elements
        books_detail_elements = [book.a.get('href') for book in books_detail]
        books_detail_url = [urljoin(main_url, path) for path in books_detail_elements]

        # get author data and url
        books_info = books_data.find_all('dl', class_='item-txt')
        books_author = [book.find('dd').find('a') for book in books_info]

    except AttributeError:
        return None

    return (books_title, books_image_url, books_detail_url)


if __name__ == '__main__':
    scraper = BookScraper('ねこ', number_of_books=2)
    try:
        scraper.fetch()
    except TypeError:
        print('本はありません')

    print(scraper.dump())
