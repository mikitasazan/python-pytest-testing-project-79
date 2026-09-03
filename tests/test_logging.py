import logging
from pathlib import Path

import requests_mock

from page_loader import download

URL = 'https://ru.hexlet.io/courses'
IMAGE_URL = 'https://ru.hexlet.io/assets/professions/python.png'


def test_download_logs_debug_messages(
    tmp_path, page_with_image, image_content, caplog,
):
    caplog.set_level(logging.DEBUG)
    with requests_mock.Mocker() as mock:
        mock.get(URL, text=page_with_image)
        mock.get(IMAGE_URL, content=image_content)
        download(URL, str(tmp_path))

    debug_messages = [
        r.message for r in caplog.records if r.levelno == logging.DEBUG
    ]
    assert any('downloading resource' in m for m in debug_messages)
    assert any('saved resource to' in m for m in debug_messages)


def test_download_warns_and_continues_on_broken_resource(
    tmp_path, page_with_image, caplog,
):
    caplog.set_level(logging.WARNING)
    with requests_mock.Mocker() as mock:
        mock.get(URL, text=page_with_image)
        mock.get(IMAGE_URL, status_code=500)
        file_path = download(URL, str(tmp_path))

    # A single broken resource must not abort the whole page download.
    assert Path(file_path).exists()

    warning_messages = [
        r.message for r in caplog.records if r.levelno == logging.WARNING
    ]
    assert any('failed to download resource' in m for m in warning_messages)
