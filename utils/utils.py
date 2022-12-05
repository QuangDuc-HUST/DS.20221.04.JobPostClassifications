from itemloaders.processors import Join, MapCompose, TakeFirst
from w3lib.html import remove_tags
from datetime import datetime
from urllib.parse import urljoin


def preprocess(self, link):
        return urljoin(self.url, link)