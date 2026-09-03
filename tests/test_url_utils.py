import pytest

from page_loader.url_utils import build_file_name, build_resource_file_name


@pytest.mark.parametrize('url, expected', [
    ('https://ru.hexlet.io/courses', 'ru-hexlet-io-courses.html'),
    ('https://ru.hexlet.io/courses/', 'ru-hexlet-io-courses.html'),
    ('http://example.com', 'example-com.html'),
])
def test_build_file_name(url, expected):
    assert build_file_name(url) == expected


@pytest.mark.parametrize('url, expected', [
    (
        'https://ru.hexlet.io/assets/professions/python.png',
        'ru-hexlet-io-assets-professions-python.png',
    ),
    (
        'https://ru.hexlet.io/assets/application.css',
        'ru-hexlet-io-assets-application.css',
    ),
    (
        'https://ru.hexlet.io/packs/js/runtime.js',
        'ru-hexlet-io-packs-js-runtime.js',
    ),
    # A resource address with no extension of its own falls back to .html.
    ('https://ru.hexlet.io/courses', 'ru-hexlet-io-courses.html'),
])
def test_build_resource_file_name(url, expected):
    assert build_resource_file_name(url) == expected
