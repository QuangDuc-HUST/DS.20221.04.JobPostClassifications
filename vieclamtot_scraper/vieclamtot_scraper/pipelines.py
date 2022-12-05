# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
from .items import *
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import re


class VieclamtotScraperPipeline:

    def __init__(self) -> None:
        self.first_item = True
        self.metadata = None
        self.data_job = []
        self.data_company = []

    def open_spider(self, spider):
        # print('---------- Opening Main Pipeline ----------')
        self.file_job = open('../vieclamtot_scraper/data/job.json', 'w')
        # self.file_job = open('/code/vieclamtot_scraper/data/job.json', 'w')

        self.file_company = open('../vieclamtot_scraper/data/company.json', 'w')
        # self.file_company = open('/code/vieclamtot_scraper/data/company.json', 'w')
        # print('---------- Opened Main Pipeline ----------')

    def close_spider(self, spider):
        # print('---------- Closing Main Pipeline ----------')
        json.dump(self.data_job, self.file_job, indent=4)
        self.file_job.close()

        json.dump(self.data_company, self.file_company, indent=4)
        self.file_company.close()
        # print('---------- Closed Main Pipeline ----------')

    def process_item(self, item, spider):
        
        if isinstance(item, VieclamtotJobScraperItem):
            # print('---------- Processing Job ----------')
            return self.process_job(item)
            
            # return self.process_job_item(item)
            
        else:
            # print('---------- Processing Company ----------')
            item = ItemAdapter(item)
            self.data_company.append(item.asdict())
            # return self.process_company_item(item)
        return item

    def process_job(self, item):

        item = ItemAdapter(item)

        # if re.match('\d+, .+', item['age_range']) is None:
        #     item['age_range'] = re.findall('\d+', item['age_range'])[0] + '+'
        
        # if re.match('.+, \d+', item['age_range']) is None:
        #     item['age_range'] = re.findall('\d+', item['age_range'])[0] + '-'

        if item['preferred_education'] == 'None':
            item['preferred_education'] = 'Không yêu cầu'

        if item['preferred_gender'] == 'None':
            item['preferred_gender'] = 'Không yêu cầu'

        if item['preferred_working_experience'] == 'None':
            item['preferred_working_experience'] = 'Không yêu cầu'

        if item['skills'] == 'None':
            item['skills'] = 'Không yêu cầu'

        self.data_job.append(item.asdict())

        # print(item.asdict())

        return item


class DuplicatesPipeline:

    def __init__(self):
        self.ids_seen = set()

    def open_spider(self, spider):
        # print('---------- Opening Duplicate Pipeline ----------')
        pass
    def close_spider(self, spider):
        # print('---------- Closing Dupilicate Pipeline ----------')
        pass

    def process_item(self, item, spider):
        # print('---------- Filtering Duplicate ----------')
        adapter = ItemAdapter(item)
        if adapter['id'] in self.ids_seen:
            raise DropItem()
        else:
            self.ids_seen.add(adapter['id'])
            return item
