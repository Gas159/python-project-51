import os.path

from page_loader import download
import tempfile

def test_download():
    # with open('fixtures', 'r') as file:
    #     assert download('url','path').text == file
    with tempfile.TemporaryDirectory() as tmpdirname:
        print('created temporary directory', tmpdirname)

def generate_fixtures_path(name):
    dir_name = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(dir_name, 'fixtures', name)

