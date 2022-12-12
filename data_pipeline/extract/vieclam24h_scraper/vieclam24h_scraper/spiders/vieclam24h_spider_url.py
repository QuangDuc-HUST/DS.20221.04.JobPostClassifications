from .vieclam24h_spider import *


class Vieclam24HURLSpider(Vieclam24hSpider):
    name = 'vieclam24hurl'

    def __init__(self, **kwargs):
        self.crawl_url = json.load(open('./error/error.json', 'r'))

    def start_requests(self):
        for u in self.crawl_url:
            yield scrapy.Request(u['url'], callback=self._get_javascript_data, meta={
                        "download_timeout": 10,
                        "max_retry_time": 1,
                        'job_type_id': u['job_type_id']
                    })