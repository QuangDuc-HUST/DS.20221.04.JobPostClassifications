from itemloaders.processors import Join, MapCompose, TakeFirst
from w3lib.html import remove_tags
from datetime import datetime, date
from urllib.parse import urljoin
import json
import time
from scrapy.loader import ItemLoader
import logging
from scrapy.utils.log import configure_logging
import traceback

def preprocess(self, link):
        return urljoin(self.url, link)