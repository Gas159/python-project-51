#!/urs/bin/env python3
from page_loader.page_loader import download
from page_loader.cli import parse


def main():
    args = parse()
    download(args.url, args.path)


if __name__ == '__main__':
    main()
