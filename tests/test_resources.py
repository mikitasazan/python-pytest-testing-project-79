from pathlib import Path

import pytest
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


CSS_URL = 'https://ru.hexlet.io/assets/application.css'
JS_URL = 'https://ru.hexlet.io/packs/js/runtime.js'
CSS_FILE = 'ru-hexlet-io-assets-application.css'
JS_FILE = 'ru-hexlet-io-packs-js-runtime.js'
CANONICAL_FILE = 'ru-hexlet-io-courses.html'


@pytest.fixture
def mocked_resources(
    page_with_resources, image_content, css_content, js_content,
):
    with requests_mock.Mocker() as mock:
        mock.get(URL, text=page_with_resources)
        mock.get(IMAGE_URL, content=image_content)
        mock.get(CSS_URL, text=css_content)
        mock.get(JS_URL, text=js_content)
        yield mock


def test_download_saves_link_and_script_resources(
    tmp_path, mocked_resources, css_content, js_content, page_with_resources,
):
    download(URL, str(tmp_path))

    resource_dir = tmp_path / RESOURCE_DIR
    assert (resource_dir / CSS_FILE).read_text(encoding='utf-8') == css_content
    assert (resource_dir / JS_FILE).read_text(encoding='utf-8') == js_content
    # The canonical <link href="/courses"> points at the page's own address,
    # with no extension of its own, so it falls back to a saved .html copy.
    canonical_path = resource_dir / CANONICAL_FILE
    assert canonical_path.read_text(encoding='utf-8') == page_with_resources


def test_download_rewrites_link_and_script_src_leaving_remote_ones_alone(
    tmp_path, mocked_resources,
):
    file_path = download(URL, str(tmp_path))

    saved_html = Path(file_path).read_text(encoding='utf-8')
    soup = BeautifulSoup(saved_html, 'html.parser')
    links = soup.find_all('link')
    scripts = soup.find_all('script')

    assert links[0]['href'] == 'https://cdn2.hexlet.io/assets/menu.css'
    assert links[1]['href'] == f'{RESOURCE_DIR}/{CSS_FILE}'
    assert links[2]['href'] == f'{RESOURCE_DIR}/{CANONICAL_FILE}'
    assert scripts[0]['src'] == 'https://js.stripe.com/v3/'
    assert scripts[1]['src'] == f'{RESOURCE_DIR}/{JS_FILE}'

    # The <a> tag is not a resource tag: its link must stay untouched.
    assert soup.find('a')['href'] == '/professions/python'
