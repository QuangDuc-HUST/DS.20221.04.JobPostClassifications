import scrapy
from itemloaders.processors import Join, MapCompose, TakeFirst


class TransformedScraperJobItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    post_time = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    vacancies = scrapy.Field()
    salary_type = scrapy.Field()
    contract_type = scrapy.Field()
    job_type = scrapy.Field()
    min_salary = scrapy.Field()
    max_salary = scrapy.Field()
    age_range = scrapy.Field()
    gender = scrapy.Field()
    benefits = scrapy.Field()
    job_location = scrapy.Field()
    region = scrapy.Field()
    education_requirements = scrapy.Field()
    experience_requirements = scrapy.Field()
    skills = scrapy.Field()
    url = scrapy.Field()
    created_time = scrapy.Field()
    updated_time = scrapy.Field()

    company_id = scrapy.Field()
    company_name = scrapy.Field()
    company_region = scrapy.Field()
    company_coordinate = scrapy.Field()
    company_address = scrapy.Field()

    def __str__(self):
        return ""
