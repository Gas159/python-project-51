import requests
from page_loader import download
import tempfile
import pytest
import os
from page_loader.exceptions import KnownError, AllErrors
from page_loader.requests_and_response import generate_path

URL = 'https://gas159.github.io/'


def test_dir_not_exist(requests_mock):
    with pytest.raises(KnownError):
        requests_mock.get(URL, text='current_data')
        download(URL, 'wrong path')


def test_connection(requests_mock):
    with pytest.raises(AllErrors):
        requests_mock.get(URL, exc=requests.RequestException)
        with tempfile.TemporaryDirectory() as temp:
            download(URL, temp)


def test_download1(requests_mock):
    with tempfile.TemporaryDirectory() as tempdir:
        original_html = reader(generate_fixtures_path('original.html'))
        expected_html = reader(generate_fixtures_path('expected.html'))


        requests_mock.get(URL, text=original_html)
        exp_path =  generate_path(URL, )
        # requests_mock.get()
        result = download(URL, tempdir)
        assert reader(result) == expected_html


# def test_download(requests_mock):
#     with tempfile.TemporaryDirectory() as tempdir:
#
#         fix_link = 'expected.html'
#         expected = generate_fixtures_path(fix_link)
#
#         start_link = 'original.html'
#         fix_path = generate_fixtures_path(start_link)
#
#         current_data = reader(fix_path)
#         requests_mock.get(URL, text=current_data)
#
#         excpected_path_to_download_file = generate_fixtures_path('images/poster.jpg')
#         expected_download_file = reader(excpected_path_to_download_file, mode='rb')
#         requests_mock.get('https://gas159.github.io/images/poster.jpg',
#                           content=expected_download_file)
#
#         requests_mock.get(
#             'https://gas159.github.io/assets/css/style.css?v=f2efc96042b257cf424f7da88654fc7667380f0f',
#             text='111')
#         expected_data = reader(expected)
#         result = download(URL, tempdir)
#         result_data = reader(result)
#
#         current_path_to_download_file = os.path.join(tempdir,
#                                                      'gas159-github-io_files/gas159-github-io-images-poster.jpg')
#         current_download_file = reader(current_path_to_download_file, mode='rb')
#
#         assert result_data == expected_data
#         assert expected_download_file == current_download_file

# @pytest.mark.parametrize('URL, get_name, file_status, dir_status,', [
#     ('https://github.com/mrjonsonDD/python-project-lvl3',
#      'github-com-mrjonsonDD-python-project-lvl3.html', None, None),
#     ('https://github.com/mrjonsonDD/python-project-lvl3',
#      'github-com-mrjonsonDD-python-project-lvl3_files', None, True),
#     ('https://github.com/mrjonsonDD/python-project-lvl3.css',
#      'github-com-mrjonsonDD-python-project-lvl3.css', True, None)
# ])
# def test_get_name(URL, get_name, dir_status, file_status):
#     assert format_local_name(URL, file=file_status,
#                              dir=dir_status) == get_name

def generate_fixtures_path(name):
    dir_name = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(dir_name, 'fixtures', name)


def reader(path, mode='r'):
    with open(path, mode) as f:
        return f.read()
