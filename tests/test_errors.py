import logging
import os
import stat

import pytest
import requests
import requests_mock

from page_loader import download
from page_loader.scripts.page_loader import main

URL = 'https://ru.hexlet.io/courses'


def test_download_raises_on_missing_output_directory(tmp_path):
    missing_dir = tmp_path / 'does-not-exist'

    # No mock is registered: the directory check must happen before any
    # network call, or an unmocked request would blow up with a different
    # exception (requests_mock.NoMockAddress) and fail this test loudly.
    with requests_mock.Mocker():
        with pytest.raises(FileNotFoundError):
            download(URL, str(missing_dir))


def test_download_raises_on_unwritable_output_directory(tmp_path):
    readonly_dir = tmp_path / 'readonly'
    readonly_dir.mkdir()
    os.chmod(readonly_dir, stat.S_IREAD | stat.S_IEXEC)
    try:
        with requests_mock.Mocker() as mock:
            mock.get(URL, text='<html><body></body></html>')
            with pytest.raises(PermissionError):
                download(URL, str(readonly_dir))
    finally:
        os.chmod(readonly_dir, stat.S_IRWXU)


def test_download_raises_on_network_error(tmp_path):
    with requests_mock.Mocker() as mock:
        mock.get(URL, exc=requests.exceptions.ConnectionError)
        with pytest.raises(requests.exceptions.ConnectionError):
            download(URL, str(tmp_path))


def test_download_raises_on_http_error_status(tmp_path):
    with requests_mock.Mocker() as mock:
        mock.get(URL, status_code=500)
        with pytest.raises(requests.exceptions.HTTPError):
            download(URL, str(tmp_path))


def test_cli_exits_with_nonzero_code_and_prints_nothing_to_stdout(
    tmp_path, capsys, caplog,
):
    caplog.set_level(logging.ERROR)
    missing_dir = tmp_path / 'does-not-exist'

    with requests_mock.Mocker():
        with pytest.raises(SystemExit) as exc_info:
            main([URL, '--output', str(missing_dir)])

    assert exc_info.value.code == 1
    assert capsys.readouterr().out == ''
    error_messages = [r.message for r in caplog.records]
    assert any('does not exist' in m for m in error_messages)
