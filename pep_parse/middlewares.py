"""
Модули промежуточной обработки (middleware) для спайдера и загрузчика.

Содержит классы для обработки запросов и ответов на уровне спайдера
и загрузчика. Позволяет модифицировать запросы/ответы и обрабатывать
исключения.
"""

from scrapy import signals


class PepParseSpiderMiddleware:
    """
    Промежуточный слой для обработки входных и выходных данных спайдера.

    Методы этого класса вызываются при прохождении ответов через спайдер
    и позволяют модифицировать или фильтровать результаты.
    """

    @classmethod
    def from_crawler(cls, crawler, spider):
        """
        Создаёт экземпляр middleware и подключает сигналы.

        Args:
            crawler: Экземпляр Crawler для доступа к сигналам
            spider: Экземпляр спайдера

        Returns:
            Экземпляр PepParseSpiderMiddleware
        """
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        """
        Обрабатывает входящий ответ перед передачей спайдеру.

        Args:
            response: Ответ от загрузчика
            spider: Экземпляр спайдера

        Returns:
            None — ответ передаётся спайдеру без изменений
        """
        return None

    def process_spider_output(self, response, result_request, spider):
        """
        Обрабатывает выходные данные спайдера (items и requests).

        Args:
            response: Ответ, который обработал спайдер
            result: Генератор с результатами (items/requests)
            spider: Экземпляр спайдера

        Yields:
            Каждый элемент из результата без модификаций
        """
        for element in result_request:
            yield element

    def process_spider_exception(self, response, exception, spider):
        """
        Обрабатывает исключения при парсинге ответа.

        Args:
            response: Ответ, вызвавший исключение
            exception: Объект исключения
            spider: Экземпляр спайдера

        Returns:
            None — исключение обрабатывается стандартным способом
        """

    def process_start_requests(self, start_requests, spider):
        """
        Обрабатывает стартовые запросы спайдера.

        Args:
            start_requests: Генератор стартовых запросов
            spider: Экземпляр спайдера

        Yields:
            Каждый стартовый запрос без модификаций
        """
        for psr in start_requests:
            yield psr

    def spider_opened(self, spider):
        """
        Обработчик сигнала открытия спайдера.

        Args:
            spider: Открывшийся спайдер
        """
        spider.logger.info('Spider opened: %s' % spider.name)


class PepParseDownloaderMiddleware:
    """
    Промежуточный слой для обработки запросов и ответов загрузчика.

    Позволяет модифицировать HTTP-запросы и ответы на уровне загрузчика
    до передачи их спайдеру.
    """

    @classmethod
    def from_crawler(cls, crawler, spider):
        """
        Создаёт экземпляр middleware и подключает сигналы.

        Args:
            crawler: Экземпляр Crawler для доступа к сигналам
            spider: Экземпляр спайдера

        Returns:
            Экземпляр PepParseDownloaderMiddleware
        """
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        """
        Обрабатывает каждый HTTP-запрос перед отправкой.

        Args:
            request: Объект запроса
            spider: Экземпляр спайдера

        Returns:
            None — запрос отправляется без изменений
        """
        return None

    def process_response(self, request, response, spider):
        """
        Обрабатывает полученный HTTP-ответ.

        Args:
            request: Исходный запрос
            response: Полученный ответ
            spider: Экземпляр спайдера

        Returns:
            response: Ответ без модификаций
        """
        return response

    def process_exception(self, request, exception, spider):
        """
        Обрабатывает исключения при загрузке запроса.

        Args:
            request: Запрос, вызвавший исключение
            exception: Объект исключения
            spider: Экземпляр спайдера

        Returns:
            None — исключение обрабатывается стандартным способом
        """
        return None

    def spider_opened(self, spider):
        """
        Обработчик сигнала открытия загрузчика.

        Args:
            spider: Спайдер, для которого открылся загрузчик
        """
        spider.logger.info('Downloader opened: %s' % spider.name)
