"""
Search info about book from web. 
"""
from pprint import pprint
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup as bs


def fetch_books(keyword, number_of_books=1):
    """
    Honya Clubから本のタイトル、詳細リンク、画像リンクを取得する
    :param keyword: str (book title what you want search) 
    :param number_of_books: int
    :return: 3 list's tuple (title, image_link, detail_link)  
    """
    search_url = 'http://www.honyaclub.com/shop/goods/search.aspx?'
    main_url = 'https://www.honyaclub.com'
    encode_word = keyword.encode('Shift-JIS')

    payload = {
        'search': 'x',
        'keyw': encode_word,
    }

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
    try:
        books_title, books_image_url, books_detail_url = fetch_books('ねこ', number_of_books=3)
    except TypeError:
        print('本はありません')
    print(books_detail_url)
