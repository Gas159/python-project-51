from page_loader import download
import requests_mock
import tempfile
import pytest
import os


def test_download(requests_mock):
    with tempfile.TemporaryDirectory() as tempdir:
        fix_path = generate_fixtures_path('browser-info.html')
        with open(fix_path, 'r') as file:
            data = file.read()
            print('11111111', data)
            requests_mock.get('https://browser-info.ru/', text=data)
            q = download('https://browser-info.ru/', tempdir)
            receice = open(q).read()
            assert receice == data


def generate_fixtures_path(name):
    dir_name = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(dir_name, 'fixtures', name)
