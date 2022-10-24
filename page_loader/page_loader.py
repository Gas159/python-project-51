import os

import requests

url = 'https://browser-info.ru/'
cli_path = os.getcwd()
print(cli_path)


def download(url, cli_path):
    responce = requests.get(url)
    path_to_file = set_name(url)
    with open(path_to_file, 'w') as file:
        print('writening...')
        file.write(responce.text)


def set_name(path_name):
    name = path_name.lstrip('https://').replace('/', '')
    res = ''
    for i in name:
        if i.isdigit() or i.isalpha():
            res += i
        else:
            res += '-'
    res += '.html'
    return res


q = download(url, cli_path)
print(q)
