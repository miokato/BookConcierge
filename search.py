"""
Search info about book from web. 
"""
from pprint import pprint
import requests
from bs4 import BeautifulSoup as bs

url = 'http://www.honyaclub.com/shop/goods/search.aspx?'
url2 = 'http://www.honyaclub.com/shop/goods/search.aspx?cat_p=&search=x&keyw=%82%CB%82%B1&image.x=0&image.y=0'
keyword = 'ねこ'
encode_word = keyword.encode('Shift-JIS')

payload = {
    'search': 'x',
    'keyw': encode_word,
}

r = requests.get(url, params=payload)
soup = bs(r.content, 'html.parser')
# aタグ全部取得
links = soup.find_all('a')
# links > class : bs4.element.ResultSet
# aタグのhref属性を取得
urls = [link.get('href') for link in links]
pprint(links)
