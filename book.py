from amazon.api import AmazonException

def fetch_books(amazon_api, keyword='', num=1):
    """
    fetch three books using amazon api
    
    :param amazon_api: 
    :param keyword: 
    :return: books object
    """
    try:
        books = amazon_api.search_n(num, Keywords=keyword,
                                    SearchIndex='Books')
        return books
    except AmazonException:
        return None


def trim_str_60(s):
    if len(s) < 60:
        return s
    else:
        l = []
        suffix = '...'
        for i, value in enumerate(s):
            if i < 55:
                l.append(value)
        result = ''.join(l)
        result = result + suffix
        return result


if __name__ == '__main__':
    s = 'ハロプロ スッペシャ~ル ~ハロー! プロジェクト×CDジャーナルの全インタビューを集めちゃいました! ~ (CDジャーナルムック)'
    result = trim_str_60(s)
    print(len(result))
    print(result)
