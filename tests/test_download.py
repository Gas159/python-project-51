from page_loader import download
import tempfile
import os

URL = 'https://gas159.github.io/'


def test_download(requests_mock):
    with tempfile.TemporaryDirectory() as tempdir:
        fix_link = 'gas159-github-io.html'
        expected = generate_fixtures_path(fix_link)

        start_link = 'original.html'
        fix_path = generate_fixtures_path(start_link)

        current_data = reader(fix_path)
        requests_mock.get(URL, text=current_data)

        excpected_path_to_download_file = generate_fixtures_path('images/poster.jpg')
        # print('```1`1`1``1', excpected_path_to_download_file)
        expected_download_file = reader(excpected_path_to_download_file, mode='rb')
        requests_mock.get('https://gas159.github.io/images/poster.jpg',
                                content=expected_download_file)



        requests_mock.get(
            'https://gas159.github.io/assets/css/style.css?v=f2efc96042b257cf424f7da88654fc7667380f0f',
            text='111')

        # current_path_to_download_file = os.path.join(tempdir,
        #                                              'gas159_github_io_files/gas159-github-io-images-poster.jpg')
        # print('```1`1`1``1', current_path_to_download_file)
        # current_download_file = reader(current_path_to_download_file, mode='rb')
        #
        # assert expected_download_file == current_download_file



        expected_data = reader(expected)
        result = download(URL, tempdir)
        result_data = reader(result)

        current_path_to_download_file = os.path.join(tempdir,
                                                     'gas159-github-io_files/gas159-github-io-images-poster.jpg')
        print('```1`1`1``1', current_path_to_download_file)
        current_download_file = reader(current_path_to_download_file, mode='rb')

        assert result_data == expected_data
        assert expected_download_file == current_download_file




def generate_fixtures_path(name):
    dir_name = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(dir_name, 'fixtures', name)


def reader(path, mode='r'):
    with open(path, mode) as f:
        return f.read()
