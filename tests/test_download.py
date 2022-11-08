import requests
from page_loader import download
import tempfile
import pytest
import os
from page_loader.exceptions import KnownError, AllErrors

URL = 'https://gas159.github.io/'


def test_dir_not_exist(requests_mock):
    with pytest.raises(KnownError):
        requests_mock.get(URL)
        download(URL, 'wrong path')


def test_connection(requests_mock):
    with pytest.raises(AllErrors):
        requests_mock.get(URL, exc=requests.RequestException)
        with tempfile.TemporaryDirectory() as temp:
            download(URL, temp)


LIST_OF_FILES = {
    'https://gas159.github.io/images/poster.jpg': 'gas159-github-io-images-poster.jpg',
    'https://gas159.github.io/assets/css/style.css': 'gas159-github-io-assets-css-style.css',
    'https://gas159.github.io/assets/scripts.js': 'gas159-github-io-assets-scripts.js'

}


def test_download1(requests_mock):
    with tempfile.TemporaryDirectory() as tempdir:
        original_html = reader(generate_fixtures_path('original.html', ))
        expected_html = reader(generate_fixtures_path('expected.html', 'expected'))

        for url, value, in LIST_OF_FILES.items():
            file = reader(generate_fixtures_path(value, 'images'), mode='rb')
            requests_mock.get(url, content=file)
            requests_mock.get(URL, text=original_html)

        result = download(URL, tempdir)
        assert reader(result) == expected_html
        expect_file = reader(generate_fixtures_path
                             ('gas159-github-io-images-poster.jpg', 'images'), mode='rb')

        current_file = reader(
            os.path.join(
                tempdir, "gas159-github-io_files/gas159-github-io-images-poster.jpg"), mode='rb')

        assert expect_file == current_file


def generate_fixtures_path(name, direct=''):
    dir_name = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(dir_name, 'fixtures', direct, name)


def reader(path, mode='r'):
    with open(path, mode) as f:
        return f.read()
