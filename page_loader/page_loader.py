import os
from urllib.parse import urlparse
from bs4 import BeautifulSoup

import requests

link = 'https://browser-info.ru/'


# link = os.getcwd()


def download(url, cli_path):
    if not os.path.exists(cli_path):
        raise IsADirectoryError('Directory not found')

    response = requests.get(url)
    file_name = get_name(url)
    # file_dir = get_path(cli_path)
    page_path = os.path.join(cli_path, file_name)

    with open(page_path, 'w') as file:
        file.write(response.text)
        print('it\'s full path: ', page_path)

    return page_path


def get_name(path):
    parse_result = urlparse(os.path.splitext(path.strip('/'))[0])
    name = parse_result.netloc + parse_result.path
    print('parse name: ', name)
    res = ''
    for i in name:
        if i.isdigit() or i.isalpha():
            res += i
        else:
            res += '-'
    print('file name: ', res)
    return res + '.html'


# def get_path(path):
#     return os.path.abspath(path)


# link1 = 'https://docs.python.org/3/library/fda.txt'
# download(link, os.getcwd())
