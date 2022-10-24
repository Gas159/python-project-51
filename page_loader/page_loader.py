import os
import requests


# url = 'https://browser-info.ru/'
# cli_path = os.getcwd()
# print(cli_path)
# # url = https://browser-info.ru/''

def download(url, cli_path):
    if not os.path.exists(cli_path):
        raise IsADirectoryError('Directory not found')
    response = requests.get(url)
    file_name = set_name(url)
    file_dir = set_path(cli_path)
    file_path = os.path.join(file_dir, file_name)

    # print('exist path:', os.path.exists(cli_path))
    # print('access path: ', os.access(cli_path, os.W_OK))
    with open(file_path, 'w') as file:
        # print('writing...')
        file.write(response.text)
        print('it\'s full path: ', os.path.abspath(file_path))


def set_name(path_name):
    name = path_name.lstrip('https:').strip('/')
    res = ''
    for i in name:
        if i.isdigit() or i.isalpha():
            res += i
        else:
            res += '-'
    res += '.html'
    return res


def set_path(path):
    q = os.path.abspath(path)
    return q
