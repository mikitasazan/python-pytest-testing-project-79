from pathlib import Path

import requests_mock
from bs4 import BeautifulSoup

from page_loader import download

URL = 'https://ru.hexlet.io/courses'
IMAGE_URL = 'https://ru.hexlet.io/assets/professions/python.png'
RESOURCE_DIR = 'ru-hexlet-io-courses_files'
RESOURCE_FILE = 'ru-hexlet-io-assets-professions-python.png'


def test_download_saves_local_image(tmp_path, page_with_image, image_content):
    with requests_mock.Mocker() as mock:
        mock.get(URL, text=page_with_image)
        mock.get(IMAGE_URL, content=image_content)
        download(URL, str(tmp_path))

    resource_path = tmp_path / RESOURCE_DIR / RESOURCE_FILE
    assert resource_path.read_bytes() == image_content


def test_download_rewrites_image_src(tmp_path, page_with_image, image_content):
    with requests_mock.Mocker() as mock:
        mock.get(URL, text=page_with_image)
        mock.get(IMAGE_URL, content=image_content)
        file_path = download(URL, str(tmp_path))

    saved_html = Path(file_path).read_text(encoding='utf-8')
    soup = BeautifulSoup(saved_html, 'html.parser')
    img = soup.find('img')

    assert img['src'] == f'{RESOURCE_DIR}/{RESOURCE_FILE}'


def test_download_ignores_remote_image(tmp_path, page_content):
    remote_page = page_content.replace(
        '</body>',
        '<img src="https://other-domain.test/pic.png"></body>',
    )
    with requests_mock.Mocker() as mock:
        mock.get(URL, text=remote_page)
        download(URL, str(tmp_path))

    assert not (tmp_path / RESOURCE_DIR).exists()
