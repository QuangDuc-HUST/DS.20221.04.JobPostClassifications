# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from utils.utils import *
import scrapy
import sys
sys.path.append("..")


def unix_to_human_time(text: str):
    return datetime.utcfromtimestamp(int(text) // 1000).strftime('%Y-%m-%d %H:%M:%S')


def process_num(num):
    try:
        return int(num)
    except Exception as e:
        return 0  


class TakeFirst1:
    def __call__(self, values):
        for value in values:
            if value is not None and value != '':
                return value
        return ''


class VieclamtotJobScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    id = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst1()
    )
    job_id = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst1()
    )
    post_time = scrapy.Field(
        input_processor=MapCompose(unix_to_human_time),
        output_processor=TakeFirst1()
    )

    title = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst1()
    )
    full_description = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst1()
    )
    vacancies = scrapy.Field(
        input_processor=MapCompose(int),
        output_processor=TakeFirst1()
    )
    min_salary = scrapy.Field(
        input_processor=MapCompose(process_num),
        output_processor=TakeFirst1()
    )
    max_salary = scrapy.Field(
        input_processor=MapCompose(process_num),
        output_processor=TakeFirst1()
    )
    min_age = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst1()
    )
    max_age = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst1()
    )
    benefits = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst1()
    )
    skills = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst1()
    )
    region = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst1()
    )
    address = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst1()
    )
    salary_type = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst1()
    )
    contract_type = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst1()
    )
    job_type = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst1()
    )
    preferred_education = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst1()
    )
    preferred_gender = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst1()
    )
    preferred_working_experience = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst1()
    )

    url = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst1()
    )
    created_time = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst1()
    )
    updated_time = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst1()
    )
    company_id = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst1()
    )

    company_name = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst1()
    )

    company_location = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst1()
    )
    company_city = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst1()
    )
    company_district = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst1()
    )
    company_ward = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst1()
    )

    def __str__(self):
        return ""



