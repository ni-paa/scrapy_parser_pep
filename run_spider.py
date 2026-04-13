"""Скрипт для запуска парсера вне pytest."""
import sys
if sys.platform == 'win32':
    try:
        from twisted.internet import iocpreactor
        iocpreactor.install()
    except (ImportError, AttributeError):
        pass

# Monkeypatch для Windows — отключаем установку обработчиков сигналов
try:
    from scrapy.utils import ossignal
    ossignal.install_shutdown_handlers = lambda *args, **kwargs: None
except Exception:
    pass

from scrapy.crawler import CrawlerProcess
from pep_parse.spiders.pep import PepSpider

process = CrawlerProcess(settings={
    'LOG_ENABLED': True,
    'LOG_LEVEL': 'INFO',
    'ITEM_PIPELINES': {
        'pep_parse.pipelines.PepParsePipeline': 300,
    },
    'FEEDS': {
        'results/pep_%(time)s.csv': {
            'format': 'csv',
            'fields': ['number', 'name', 'status'],
            'encoding': 'utf-8',
        },
    },
})
process.crawl(PepSpider)
process.start()
