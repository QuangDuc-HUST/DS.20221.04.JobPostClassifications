from itemloaders.processors import Join, MapCompose, TakeFirst
from w3lib.html import remove_tags
from datetime import datetime
from urllib.parse import urljoin
import json
import time
from datetime import date
from scrapy.loader import ItemLoader
import logging
from scrapy.utils.log import configure_logging

def preprocess(self, link):
        return urljoin(self.url, link)