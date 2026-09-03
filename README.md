# Тестирование загрузчика страниц (Python)

[![hexlet-check](https://github.com/mikitasazan/python-pytest-testing-project-79/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/mikitasazan/python-pytest-testing-project-79/actions)

Загрузчик страниц – библиотека, которая умеет скачивать страницы по сети и сохранять их на локальном диске. Акцент в проекте делается на ее тестировании. Из-за обилия побочных эффектов, здесь придется правильно работать с их подавлением, стабами/моками и возможными ошибками.

Учебный проект Хекслета: https://ru.hexlet.io/programs/python-pytest-testing

## Стек

- Python 3.10+
- requests — HTTP-запросы
- BeautifulSoup4 (html.parser) — разбор и переписывание HTML
- logging — журналирование (INFO/DEBUG/WARNING/ERROR)
- pytest, pytest-cov, requests-mock — тесты и покрытие
- ruff — линтер
- uv + hatchling — сборка и управление зависимостями

## Установка

```bash
git clone https://github.com/mikitasazan/python-pytest-testing-project-79.git
cd python-pytest-testing-project-79
make install
```

## Использование

Как утилита командной строки:

```bash
page-loader --output /var/tmp https://ru.hexlet.io/courses
```

скачивает страницу и все её локальные ресурсы (картинки, стили, скрипты) в указанную директорию, переписывая ссылки в HTML на локальные пути, и печатает путь к загруженному файлу.

Как библиотека:

```python
from page_loader import download

file_path = download('https://ru.hexlet.io/courses', '/var/tmp')
print(file_path)  # => '/var/tmp/ru-hexlet-io-courses.html'
```

Установка собранного пакета в систему:

```bash
make build
make package-install
```

Тесты, линтер, отладочные логи:

```bash
make test        # pytest
make lint         # ruff
make test-log     # pytest с --log-cli-level=DEBUG — видно debug/warning-сообщения
```

### Записи в терминале

Файлы записей лежат в [`docs/casts/`](docs/casts/) — воспроизвести локально: `asciinema play docs/casts/download.cast`.

- [Скачивание страницы и её ресурсов](https://asciinema.org/a/Q5TzzZ0DoqVjigGJ) — установка, `page-loader`, полученные файлы (картинки, стили, скрипты).
- [Отладочные и предупреждающие логи](https://asciinema.org/a/ul0UdLKLa3ww7tC5) — `make test-log`: видно `DEBUG`-сообщения о каждом скачиваемом ресурсе.
- [Обработка ошибки](https://asciinema.org/a/B968WrjR1iOouZdj) — запуск с несуществующей директорией: сообщение в STDERR и код возврата 1.

---

<details>
<summary>Автоматические тесты Хекслета</summary>

Тесты запускаются на каждый коммит. За запуск отвечает файл `.github/workflows/hexlet-check.yml` — не удаляйте и не переименовывайте ни его, ни репозиторий.

</details>

## О Хекслете

[Хекслет](https://ru.hexlet.io/) — школа программирования: авторские программы обучения с практикой, поддержкой наставников и реальными проектами, которые остаются в резюме. Этот репозиторий — один из таких проектов.
