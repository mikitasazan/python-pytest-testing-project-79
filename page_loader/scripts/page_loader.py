import argparse
import logging
import os
import sys

from page_loader import download


def build_parser():
    parser = argparse.ArgumentParser(
        prog='page-loader',
        description='Downloads a page from the network and saves it locally',
    )
    parser.add_argument('url', help='page address')
    parser.add_argument(
        '-o', '--output',
        default=os.getcwd(),
        help='output directory (default: current directory)',
    )
    return parser


def main():
    logging.basicConfig(level=logging.INFO)
    args = build_parser().parse_args()

    try:
        file_path = download(args.url, args.output)
    except Exception as error:
        print(f'Error: {error}', file=sys.stderr)
        sys.exit(1)

    print(f"Page was downloaded as '{file_path}'")


if __name__ == '__main__':
    main()
