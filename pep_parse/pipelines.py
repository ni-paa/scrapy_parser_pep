"""
Пайплайн для обработки и агрегации данных о PEP.

Сохраняет сводную статистику по статусам PEP в CSV файл.
"""
import csv
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
RESULTS_DIR = BASE_DIR / 'results'


class PepParsePipeline:
    """
    Пайплайн для подсчёта количества PEP по каждому статусу.

    При закрытии спайдера создаёт CSV файл со сводной статистикой,
    включая общее количество обработанных записей.

    Атрибуты:
        status_counts: Словарь для подсчёта PEP по статусам
    """

    def __init__(self):
        """Инициализирует словарь для подсчёта статусов."""
        self.status_counts = {}

    def open_spider(self, spider):
        """
        Вызывается при открытии спайдера.

        Args:
            spider: Экземпляр спайдера, который был открыт
        """
        pass

    def process_item(self, item, spider):
        """
        Обрабатывает каждый элемент (PEP) и обновляет счётчик статусов.

        Args:
            item: Экземпляр PepParseItem с данными о PEP
            spider: Экземпляр спайдера, который вернул элемент

        Returns:
            item: Необработанный элемент для передачи следующему пайплайну
        """
        status = item.get('status', 'Unknown')
        if status in self.status_counts:
            self.status_counts[status] += 1
        else:
            self.status_counts[status] = 1
        return item

    def close_spider(self, spider):
        """
        Вызывается при закрытии спайдера.

        Создаёт CSV файл со сводной статистикой по статусам PEP
        в директории results/ с временной меткой в имени файла.

        Args:
            spider: Экземпляр закрывающегося спайдера
        """
        # Создаём директорию для результатов, если она не существует
        RESULTS_DIR.mkdir(exist_ok=True)

        # Формируем имя файла с временной меткой для уникальности
        timestamp = datetime.now().strftime('%Y-%m-%dT%H-%M-%S')
        filename = RESULTS_DIR / f'status_summary_{timestamp}.csv'

        # Вычисляем общее количество обработанных PEP
        total = sum(self.status_counts.values())

        # Записываем статистику в CSV файл
        with open(filename, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Статус', 'Количество'])
            for status, count in sorted(self.status_counts.items()):
                writer.writerow([status, count])
            writer.writerow(['Total', total])
