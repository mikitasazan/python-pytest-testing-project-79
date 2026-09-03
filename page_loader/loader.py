import logging
import os

import requests

from page_loader.resources import download_resources
from page_loader.url_utils import build_file_name

logger = logging.getLogger(__name__)


def download(url, output=None):
    output = output or os.getcwd()
    logger.info('requested url: %s', url)
    logger.info('output path: %s', output)

    if not os.path.isdir(output):
        raise FileNotFoundError(f'output directory does not exist: {output}')

    response = requests.get(url)
    logger.debug('response status: %s', response.status_code)
    response.raise_for_status()

    html = download_resources(response.text, url, output)

    file_path = os.path.join(output, build_file_name(url))
    logger.info('write html file: %s', file_path)
    with open(file_path, 'w', encoding='utf-8') as html_file:
        html_file.write(html)

    return file_path
