# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
from scrapy.exceptions import DropItem
import re
from .items import *
import sys
sys.path.append('../../..')
from data_pipeline.transform.processing.transform_new import *
from data_pipeline.transform.processing.transformed_item import *



class DuplicatesPipeline:

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        # print('---------- Filtering Duplicate ----------')
        adapter = ItemAdapter(item)
        if adapter['id'] in self.ids_seen:
            raise DropItem()
        else:
            self.ids_seen.add(adapter['id'])
            return item


class Vieclam24HScraperLoadPipeline:

    def open_spider(self, spider):
        self.n_job = 0

        self.job = []

    def process_item(self, item, spider):
        # print(dict(item))
        self.job.append(dict(item))
    
    def close_spider(self, spider):
        json.dump(self.job, open('./../../transform/staging/staging_vieclam24h.json', 'w'))


class Vieclam24HScraperPreprocessPipeline:

    def __init__(self) -> None:
        self.first_item = True
        self.metadata = None
        self.data_job = []
        self.data_company = []

    def process_item(self, item, spider):
        # print('---------- Processing ----------')
        if self.first_item:
            # print('------------ Getting Metadata ----------------')
            self.metadata = spider.metadata
            self.get_age_range()
            self.get_gender()
            self.get_education()
            self.get_experience()
            self.get_working_method()
            self.get_province()

            # self.first_item = False
            # print('------------ Saved Metadata ----------------')

        return self.process_job_item(item)
        
    def process_job_item(self, item):

        item = ItemAdapter(item)
        if item['age_range'].strip() in ['None', '']:
            item['age_range'] = 'Không yêu cầu'
        else:
            item['age_range'] = self.age_range[int(item['age_range']) - 1]

        try:
            item['gender'] = self.gender[int(item['gender']) - 1]
        except Exception as e:
            print(e)
            item['gender'] = ''

        try:
            item['education_requirements'] = self.education[item['education_requirements'] - 1]
        except Exception as e:
            print(e)
            item['education_requirements'] = ''

        try:
            item['experience_requirements'] = self.experience[int(item['experience_requirements']) - 1]
        except Exception as e:
            print(e)
            item['experience_requirements'] = ''
        
        try:
            item['contract_type'] = self.working_method[int(item['contract_type']) - 1]
        except Exception as e:
            print(e)
            item['contract_type'] = ''

        item['company_province'] = self.provinces[item['company_province']]
        try:
            adr = item['company_address']
        except Exception as e:
            print(e)
            item['company_address'] = ''

        if item['company_coordinate'].replace('None', '').replace(', ', '').strip() == '':
            item['company_coordinate'] = ''

        # line = json.dumps(ItemAdapter(item).asdict()) + ",\n"
        # self.file.write(line)
        # self.data_job.append(item.asdict())
        # print(item.asdict())
        # print('---------- Processing Complete ----------')
        return Vieclam24HScraperItem(item)

    def get_age_range(self):
        age_range = sorted(self.metadata['job_requirement_age_range'], key=lambda x: x['value'])

        pattern = re.compile('[^\d^-]')

        for i in range(len(age_range)):
            age_range[i] = re.sub(pattern, '', age_range[i]['name'])

            if age_range[i].find('-') == -1:
                age_range[i] += '+'

        self.age_range = age_range

    def get_gender(self):
        gender = sorted(self.metadata['job_gender'], key=lambda x: x['value'])

        self.gender = [i['name'] for i in gender]

    def get_education(self):
        degree = sorted(self.metadata['job_degree_requirement'], key=lambda x: x['value'])

        self.education = [i['name'] for i in degree]

    def get_experience(self):
        experience = sorted(self.metadata['job_experience_range'], key=lambda x: x['value'])

        self.experience = [i['name'] for i in experience]

    def get_working_method(self):
        working_method = sorted(self.metadata['job_working_method'], key=lambda x: x['value'])

        self.working_method = [i['name'] for i in working_method]

    def get_province(self):
        provinces = sorted(self.metadata['provinces'], key=lambda x: x['id'])

        self.provinces = {i['id']: i['name'] for i in provinces}



        
