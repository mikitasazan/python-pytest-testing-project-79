import logging
import os
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

from page_loader.url_utils import (
    build_resource_dir_name,
    build_resource_file_name,
)

logger = logging.getLogger(__name__)

RESOURCE_TAGS = {
    'img': 'src',
    'link': 'href',
    'script': 'src',
}


def _is_local(resource_url, page_netloc):
    resource_netloc = urlparse(resource_url).netloc
    return resource_netloc in ('', page_netloc)


def download_resources(html, page_url, output):
    soup = BeautifulSoup(html, 'html.parser')
    page_netloc = urlparse(page_url).netloc
    resource_dir_name = build_resource_dir_name(page_url)
    resource_dir_path = os.path.join(output, resource_dir_name)
    dir_ready = False

    for tag_name, attr in RESOURCE_TAGS.items():
        for tag in soup.find_all(tag_name):
            src = tag.get(attr)
            if not src:
                continue

            resource_url = urljoin(page_url, src)
            if not _is_local(resource_url, page_netloc):
                logger.debug('skipping remote resource: %s', resource_url)
                continue

            logger.debug('downloading resource: %s', resource_url)
            try:
                response = requests.get(resource_url)
                response.raise_for_status()
            except requests.exceptions.RequestException as error:
                logger.warning(
                    'failed to download resource %s: %s', resource_url, error,
                )
                continue

            if not dir_ready:
                os.makedirs(resource_dir_path, exist_ok=True)
                dir_ready = True

            resource_file_name = build_resource_file_name(resource_url)
            resource_file_path = os.path.join(
                resource_dir_path, resource_file_name,
            )
            with open(resource_file_path, 'wb') as resource_file:
                resource_file.write(response.content)
            logger.debug('saved resource to: %s', resource_file_path)

            tag[attr] = os.path.join(resource_dir_name, resource_file_name)

    return soup.prettify()
