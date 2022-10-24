from page_loader import download
import tempfile

def test_download():
    # with open('fixtures', 'r') as file:
    #     assert download('url','path').text == file
    with tempfile.TemporaryDirectory() as tmpdirname:
        print('created temporary directory', tmpdirname)

test_download()

