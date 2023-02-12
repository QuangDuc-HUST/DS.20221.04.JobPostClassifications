# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import Join, MapCompose, TakeFirst
from w3lib.html import remove_tags
from datetime import datetime


def lowercase(text: str):
    return text.lower()


def unix_to_human_time(text: str):
    return datetime.utcfromtimestamp(int(text)).strftime('%Y-%m-%d %H:%M:%S')


def remove_nbps(text: str):
    return text.replace(u'\xa0', u' ').replace(r'&nbsp;', ' ')


def process_none_value(text):
    return '' if text is None else text


def process_num(num):
    if num is None:
        return 0
    return num


class TakeFirst1:
    def __call__(self, values):
        for value in values:
            if value is not None and value != '':
                return value
        return ''


class Vieclam24HScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst1()
    )
    job_type_id = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst1())
    post_time = scrapy.Field(
        input_processor=MapCompose(unix_to_human_time),
        output_processor=TakeFirst1()
    )
    post_title = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst1()
    )
    description = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst1()
    )
    vacancies = scrapy.Field(
        input_processor=MapCompose(),
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
    age_range = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst1()
    )
    gender = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst1()
    )
    benefits = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst1()
    )
    job_location = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst1()
    )
    region = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst1()
    )
    salary_type = scrapy.Field(
        input_processor=MapCompose(lowercase),
        output_processor=TakeFirst1()
    )
    contract_type = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst1()
    )
    industry = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst1()
    )
    education_requirements = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst1()
    )
    experience_requirements = scrapy.Field(
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

    company_province = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst1()
    )

    company_coordinate = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=Join(', ')
    )

    company_address = scrapy.Field(
        input_processor=MapCompose(process_none_value),
        output_processor=TakeFirst1()
    )

    def __str__(self):
        return ""
