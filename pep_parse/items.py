"""
Модели данных для спайдера PEP.

Определяет структуру элементов, которые извлекает спайдер
и передаёт в пайплайн для обработки.
"""
import scrapy


class PepParseItem(scrapy.Item):
    """
    Элемент данных о PEP (Python Enhancement Proposal).

    Содержит основную информацию о каждом документе PEP:
        number: Номер PEP (целое число или строка)
        name: Название PEP (строка)
        status: Статус документа (строка, например "Active", "Draft")
    """

    number = scrapy.Field()
    name = scrapy.Field()
    status = scrapy.Field()
