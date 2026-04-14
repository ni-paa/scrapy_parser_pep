"""
Спайдер для парсинга PEP (Python Enhancement Proposals) с официального сайта.

Извлекает информацию о каждом PEP: номер, название и статус.
"""
import scrapy
from urllib.parse import urljoin
from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    """
    Спайдер для скрапинга индексной страницы PEP.

    Извлекает ссылки на отдельные документы и парсит их метаданные.

    Атрибуты:
        name: Имя спайдера для запуска через scrapy crawl
        allowed_domains: Список разрешённых доменов
        start_urls: Стартовые URL-адреса для парсинга
    """

    name = 'pep'
    # Если адреса делать в круглых кавчках, то тесты не проходит работа
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        """
        Парсит индексную страницу и извлекает ссылки на PEP.

        Находит все ссылки на PEP в таблицах, фильтрует по префиксу
        и переходит на каждую страницу для детального парсинга.

        Args:
            response: HTTP-ответ с индексной страницы PEP

        Yields:
            Request на страницу отдельного PEP
        """
        # Извлекаем ссылки на PEP из таблиц (lxml не всегда парсит tbody)
        pep_links = response.css(
            'table tr td:nth-child(2) a[href^="pep-"]::attr(href)'
        ).getall()
        for href in pep_links:
            url = urljoin(response.url, href)
            yield response.follow(url, callback=self.parse_pep)

    def parse_pep(self, response):
        """
        Парсит страницу отдельного PEP и извлекает метаданные.

        Логика:
        - Извлекает заголовок PEP из h1 тега
        - Парсит номер и название из заголовка
        - Определяет статус PEP из метаданных страницы

        Args:
            response: HTTP-ответ со страницы отдельного PEP

        Yields:
            PepParseItem с полями number, name, status
        """
        # Парсим страницу отдельного PEP
        item_page = PepParseItem()

        # Заголовок PEP вида "PEP 8 – Style Guide for Python Code"
        # Пытаемся найти заголовок в специальном элементе, иначе — в общем h1
        pep_header = response.css('h1.page-title::text').get('')
        if not pep_header:
            pep_header = response.css('h1::text').get('')

        # Извлекаем номер и название из заголовка
        # Формат: "PEP <номер> – <название>" или "PEP <номер> - <название>"
        pep_number = ''
        pep_title = ''
        if pep_header:
            if '–' in pep_header:
                # Длинное тире (en-dash)
                parts = pep_header.split('–', 1)
                pep_number = parts[0].strip().replace('PEP', '').strip()
                pep_title = parts[1].strip()
            elif '-' in pep_header:
                # Обычный дефис
                parts = pep_header.split('-', 1)
                pep_number = parts[0].strip().replace('PEP', '').strip()
                pep_title = parts[1].strip()
            else:
                # Если не удалось разделить, сохраняем весь заголовок как номер
                pep_number = pep_header.strip()

        # Статус PEP из метаданных страницы
        # HTML: <dt>Status:</dt><dd><abbr title="...">Active</abbr></dd>
        # Сначала ищем в abbr, затем — как обычный текст
        pep_status = response.xpath(
            '//dt[contains(., "Status")]/following-sibling::dd[1]/abbr/text()'
        ).get()
        if not pep_status:
            pep_status = response.xpath(
                '//dt[contains(., "Status")]/following-sibling::dd[1]/text()'
            ).get()
        pep_status = pep_status.strip() if pep_status else 'Unknown'

        # Номер в int, если это возможно, иначе — строка
        is_valid_number = pep_number and pep_number.isdigit()
        if is_valid_number:
            item_page['number'] = int(pep_number)
        else:
            item_page['number'] = pep_number
        item_page['name'] = pep_title
        item_page['status'] = pep_status

        yield item_page
