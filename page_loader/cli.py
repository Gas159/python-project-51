import argparse
import os


def parse():
    parse = argparse.ArgumentParser(description='Download  web page.')
    parse.add_argument('url', type=str, help='url for page')
    parse.add_argument('-o', '--output', dest='path', default=os.getcwd(),
                       type=str,
                       help='path to download page, default = os.getcwd()')
    return parse.parse_args()
