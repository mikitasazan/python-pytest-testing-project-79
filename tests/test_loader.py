import os

import pytest
import requests
import requests_mock

from page_loader import download

URL = 'https://ru.hexlet.io/courses'
EXPECTED_FILE_NAME = 'ru-hexlet-io-courses.html'


def test_download_saves_file(tmp_path, page_content):
    with requests_mock.Mocker() as mock:
        mock.get(URL, text=page_content)
        file_path = download(URL, str(tmp_path))

    expected_path = tmp_path / EXPECTED_FILE_NAME
    assert file_path == str(expected_path)
    assert expected_path.read_text(encoding='utf-8') == page_content


def test_download_returns_absolute_path(tmp_path, page_content):
    with requests_mock.Mocker() as mock:
        mock.get(URL, text=page_content)
        file_path = download(URL, str(tmp_path))

    assert os.path.isabs(file_path)


def test_download_defaults_output_to_cwd(tmp_path, page_content, monkeypatch):
    monkeypatch.chdir(tmp_path)
    with requests_mock.Mocker() as mock:
        mock.get(URL, text=page_content)
        file_path = download(URL)

    assert file_path == str(tmp_path / EXPECTED_FILE_NAME)


def test_download_raises_on_http_error(tmp_path):
    with requests_mock.Mocker() as mock:
        mock.get(URL, status_code=404)
        with pytest.raises(requests.exceptions.HTTPError):
            download(URL, str(tmp_path))
