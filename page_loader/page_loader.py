import os # https://browser-info.ru/
import requests

def download(url, cli_path):
    if not os.path.exists(cli_path):
        raise IsADirectoryError('Directory not found')

    response = requests.get(url)
    file_name = set_name(url)
    file_dir = set_path(cli_path)
    file_path = os.path.join(file_dir, file_name)

    with open(file_path, 'w') as file:
        file.write(response.text)
        print('it\'s full path: ', os.path.abspath(file_path))
        return os.path.abspath(file_path)


def set_name(path_name):
    name = path_name.lstrip('https:').strip('/')
    res = ''
    for i in name:
        if i.isdigit() or i.isalpha():
            res += i
        elif i == '.':
            break
        else:
            res += '-'
    res += '.html'
    return res


def set_path(path):
    return os.path.abspath(path)

