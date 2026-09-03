import pytest

from page_loader.url_utils import build_file_name


@pytest.mark.parametrize('url, expected', [
    ('https://ru.hexlet.io/courses', 'ru-hexlet-io-courses.html'),
    ('https://ru.hexlet.io/courses/', 'ru-hexlet-io-courses.html'),
    ('http://example.com', 'example-com.html'),
])
def test_build_file_name(url, expected):
    assert build_file_name(url) == expected
