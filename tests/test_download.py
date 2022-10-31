import requests
from page_loader import download
import tempfile
import pytest
import os
from page_loader.page_loader import KnownError

URL = 'https://gas159.github.io/'


# def test_recursion_depth():
#     with pytest.raises(RuntimeError) as excinfo:
#         def f():
#             f()
#         f()
#     assert "maximum recursion" in str(excinfo.value)


def test_dir_not_exist(requests_mock):
    with pytest.raises(KnownError):
        requests_mock.get(URL, text='current_data')
        download(URL, 'wrong path')


def test_connection(requests_mock):
    with pytest.raises(KnownError):
        requests_mock.get(URL, exc=requests.RequestException)
        with tempfile.TemporaryDirectory() as temp:
            download(URL, temp)


# def test_


def test_download(requests_mock):
    with tempfile.TemporaryDirectory() as tempdir:
        # tempdir = creat_tempdir()

        fix_link = 'gas159-github-io.html'
        expected = generate_fixtures_path(fix_link)

        start_link = 'original.html'
        fix_path = generate_fixtures_path(start_link)

        current_data = reader(fix_path)
        requests_mock.get(URL, text=current_data)

        excpected_path_to_download_file = generate_fixtures_path('images/poster.jpg')
        expected_download_file = reader(excpected_path_to_download_file, mode='rb')
        requests_mock.get('https://gas159.github.io/images/poster.jpg',
                          content=expected_download_file)

        requests_mock.get(
            'https://gas159.github.io/assets/css/style.css?v=f2efc96042b257cf424f7da88654fc7667380f0f',
            text='111')
        expected_data = reader(expected)
        result = download(URL, tempdir)
        result_data = reader(result)

        current_path_to_download_file = os.path.join(tempdir,
                                                     'gas159-github-io_files/gas159-github-io-images-poster.jpg')
        current_download_file = reader(current_path_to_download_file, mode='rb')

        assert result_data == expected_data
        assert expected_download_file == current_download_file


def generate_fixtures_path(name):
    dir_name = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(dir_name, 'fixtures', name)


def reader(path, mode='r'):
    with open(path, mode) as f:
        return f.read()

# def creat_tempdir():
#     with tempfile.TemporaryDirectory() as temp:
#         return temp
