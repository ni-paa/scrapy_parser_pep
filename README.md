# Scrapy Parser PEP

Парсер для сбора информации о PEP (Python Enhancement Proposals) с официального сайта [peps.python.org](https://peps.python.org/).

## Описание

Проект извлека данные о каждом PEP:
- **Номер** — уникальный идентификатор документа
- **Название** — краткое описание предложения
- **Статус** — текущее состояние (Draft, Active, Final, Withdrawn и др.)

Результаты сохраняются в формате CSV с временной меткой в имени файла. Дополнительно генерируется сводная статистика по количеству PEP в каждом статусе.

## Используемые технологии

| Технология | Назначение |
|---|---|
| [Python 3.12](https://www.python.org/) | Язык программирования |
| [Scrapy 2.5.1](https://scrapy.org/) | Фреймворк для веб-скрапинга |
| [Twisted](https://twistedmatrix.com/) | Асинхронная сетевая библиотека |
| [lxml](https://lxml.de/) | Парсинг HTML/XML документов |
| [parsel](https://github.com/scrapy/parsel) | Извлечение данных из HTML через CSS и XPath селекторы |
| [pytest](https://pytest.org/) | Фреймворк для тестирования |
| [flake8](https://flake8.pycqa.org/) | Линтер для проверки стиля кода |
| [cryptography](https://cryptography.io/) | Поддержка HTTPS запросов |

## Структура проекта

```
scrapy_parser_pep/
├── pep_parse/                 # Основной пакет проекта
│   ├── spiders/               # Спайдеры
│   │   └── pep.py             # Спайдер для парсинга PEP
│   ├── items.py               # Модели данных (Scrapy Item)
│   ├── pipelines.py           # Пайплайн обработки данных
│   ├── middlewares.py         # Промежуточная обработка
│   └── settings.py            # Настройки Scrapy
├── tests/                     # Модульные тесты
├── results/                   # Результаты парсинга (CSV)
├── run_spider.py              # Скрипт запуска парсера
├── scrapy.cfg                 # Конфигурация Scrapy
├── requirements.txt           # Зависимости проекта
├── pytest.ini                 # Настройки pytest
└── .flake8                    # Конфигурация flake8
```

## Установка

```bash
# Создание виртуального окружения
python -m venv venv
venv\Scripts\activate  # Windows

# Установка зависимостей
pip install -r requirements.txt
```

## Запуск парсера

```bash
# Через скрипт
python run_spider.py

# Через scrapy CLI
scrapy crawl pep
```

Результаты будут сохранены в директорию `results/`:
- `pep_<timestamp>.csv` — данные о каждом PEP
- `status_summary_<timestamp>.csv` — сводная статистика по статусам

## Запуск тестов

```bash
pytest
```

## Проверка кода

```bash
flake8 pep_parse/ run_spider.py
```

## Формат результатов

**pep_*.csv:**
| number | name | status |
|---|---|---|
| 8 | Style Guide for Python Code | Active |

**status_summary_*.csv:**
| Статус | Количество |
|---|---|
| Active | 15 |
| Draft | 42 |
| Total | 57 |

## Лицензия

MIT
