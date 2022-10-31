#!/urs/bin/env python3
import sys

from page_loader.page_loader import download, KnownError
from page_loader.cli import parse


def main():
    try:
        args = parse()
        download(args.url, args.path)
    except KnownError:
        sys.exit(1)


if __name__ == '__main__':
    main()
