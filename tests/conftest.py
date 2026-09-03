import os

import pytest

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), 'fixtures')


def read_fixture(name):
    with open(os.path.join(FIXTURES_DIR, name), encoding='utf-8') as f:
        return f.read()


@pytest.fixture
def page_content():
    return read_fixture('simple_page.html')


@pytest.fixture
def page_with_image():
    return read_fixture('page_with_image.html')


@pytest.fixture
def image_content():
    path = os.path.join(FIXTURES_DIR, 'python.png')
    with open(path, 'rb') as f:
        return f.read()


@pytest.fixture
def page_with_resources():
    return read_fixture('page_with_resources.html')


@pytest.fixture
def css_content():
    return read_fixture('application.css')


@pytest.fixture
def js_content():
    return read_fixture('runtime.js')
