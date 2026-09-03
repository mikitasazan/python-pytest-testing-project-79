import os
import re
from urllib.parse import urlparse

NON_ALNUM_RE = re.compile(r'[^a-zA-Z0-9]')


def _address(url):
    parsed = urlparse(url)
    return f'{parsed.netloc}{parsed.path}'


def _slugify(text):
    return NON_ALNUM_RE.sub('-', text).strip('-')


def build_file_name(url):
    return f'{_slugify(_address(url))}.html'


def build_resource_dir_name(url):
    return f'{_slugify(_address(url))}_files'


def build_resource_file_name(url):
    base, ext = os.path.splitext(_address(url))
    return f'{_slugify(base)}{ext or ".html"}'
