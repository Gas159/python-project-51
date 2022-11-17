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


def test_connection(requests_mock, tmpdir):
    with pytest.raises(requests.exceptions.RequestException):
        requests_mock.get(URL, exc=requests.exceptions.ConnectionError)
        download(URL, tmpdir)


LIST_OF_FILES = {
    'https://gas159.github.io/images/poster.jpg': 'gas159-github-io-images-poster.jpg',
    'https://gas159.github.io/assets/css/style.css': 'gas159-github-io-assets-css-style.css',
    'https://gas159.github.io/assets/scripts.js': 'gas159-github-io-assets-scripts.js'

}


def generate_fixtures_path(name='', direct=''):
    dir_name = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(dir_name, 'fixtures', direct, name)


def reader(path, mode='r'):
    with open(path, mode) as f:
        return f.read()


@pytest.mark.parametrize('original_html, expected_html ',
                         [(generate_fixtures_path('original.html'),
                           generate_fixtures_path('expected.html', 'expected'))])
def test_download1(requests_mock, tmpdir, original_html, expected_html):
    for url, value, in LIST_OF_FILES.items():
        file = reader(generate_fixtures_path(value, 'images'), mode='rb')
        requests_mock.get(url, content=file)
        requests_mock.get(URL, text=reader(original_html))

    result = download(URL, tmpdir)
    assert reader(result) == reader(expected_html)

    expect_file = reader(generate_fixtures_path
                         ('gas159-github-io-images-poster.jpg', 'images'), mode='rb')
    current_file = reader(
        os.path.join(
            tmpdir, "gas159-github-io_files/gas159-github-io-images-poster.jpg"), mode='rb')

    assert expect_file == current_file

    expect_files = generate_fixtures_path(direct='images')
    current_files = os.path.join(tmpdir, "gas159-github-io_files")
    assert len(os.listdir(expect_files)) == len(os.listdir(current_files))
