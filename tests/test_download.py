import requests
from page_loader import download
import pytest
import os

URL = 'https://gas159.github.io/'


def test_dir_not_exist(requests_mock):
    with pytest.raises(FileNotFoundError):
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


def generate_fixtures_path(*args):
    dir_name = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(dir_name, 'fixtures', *args)


def reader(path, mode='r'):
    with open(path, mode) as f:
        return f.read()


@pytest.mark.parametrize('original_html, expected_html ',
                         [('original.html', 'expected/expected.html')])
def test_download(requests_mock, tmpdir, original_html, expected_html):
    for url, value, in LIST_OF_FILES.items():
        file = reader(generate_fixtures_path(os.path.join('images', value)), mode='rb')
        requests_mock.get(url, content=file)

    requests_mock.get(URL, text=reader(generate_fixtures_path(original_html)))
    result = download(URL, tmpdir)
    assert reader(result) == reader(generate_fixtures_path(expected_html))

    expect_content = reader(generate_fixtures_path
                         ('images/gas159-github-io-images-poster.jpg'), mode='rb')
    current_content = reader(
        os.path.join(
            tmpdir, "gas159-github-io_files/gas159-github-io-images-poster.jpg"), mode='rb')

    assert expect_content == current_content

    expect_files_path = generate_fixtures_path('images')
    current_files_path = os.path.join(tmpdir, "gas159-github-io_files")
    assert len(os.listdir(expect_files_path)) == len(os.listdir(current_files_path))
