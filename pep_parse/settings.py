# Scrapy settings for pep_parse project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings in the documentation.

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RESULTS_DIR = BASE_DIR / 'results'

# Spiders
SPIDER_MODULES = ['pep_parse.spiders']
NEWSPIDER_MODULE = 'pep_parse.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure item pipelines
ITEM_PIPELINES = {
    'pep_parse.pipelines.PepParsePipeline': 300,
}

# Configure feeds
FEEDS = {
    'results/pep_%(time)s.csv': {
        'format': 'csv',
        'fields': ['number', 'name', 'status'],
        'encoding': 'utf-8',
    },
}
