import re
from urllib.parse import urlparse

NON_ALNUM_RE = re.compile(r'[^a-zA-Z0-9]')


def build_file_name(url):
    parsed = urlparse(url)
    address = f'{parsed.netloc}{parsed.path}'
    slug = NON_ALNUM_RE.sub('-', address).strip('-')
    return f'{slug}.html'
