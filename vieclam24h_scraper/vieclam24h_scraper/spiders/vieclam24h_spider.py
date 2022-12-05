from ..ultis import *
from vieclam24h_scraper.items import *
from scrapy.loader import ItemLoader
import logging
from scrapy.utils.log import configure_logging
from datetime import date


class Vieclam24hSpider(scrapy.Spider):
    
    name = 'vieclam24h'
    configure_logging(install_root_handler=False, )
    logging.basicConfig(
        handlers=[logging.FileHandler(filename='./logging/log_records_{}.txt'.format(str(int(time.mktime(date.today().timetuple())))), 
                                                 encoding='utf-8', mode='a+')],
                    format="%(asctime)s %(name)s:%(levelname)s:%(message)s", 
                    datefmt="%F %A %T", 
                    level=logging.INFO
    )

    def __init__(self, end_page='20', **kwargs):

        self.url = "https://vieclam24h.vn/tim-kiem-viec-lam-nhanh"
        self.end_page = int(end_page)
        self.metadata = None
        self.first_item = True

        super().__init__(**kwargs)

    def start_requests(self):
        for t in range(113, 181): #181
            for p in range(self.end_page):
                yield scrapy.Request(self.url + "?field_ids[]=" + str(t) + "&page=" + str(p), callback=self.parse_links, meta={
                    "download_timeout": 10,
                    "max_retry_time": 1,
                    'job_type_id': t
                })

    def preprocess(self, link):
        return urljoin("https://vieclam24h.vn", link)

    def parse_links(self, response):

        links = response.xpath('//a[contains(@class, "flex rounded-sm border")]/@href').getall()

        for link in links:

            link = self.preprocess(link)
            yield scrapy.Request(link, callback=self._get_javascript_data, meta=response.meta)
            

    def _get_javascript_data(self, response):

        data = {}
        for script in response.xpath("//script").getall():
            if '<script type="application/ld+json">' in str(script):
                self.parameters = json.loads(response.xpath('//script').getall()[2].replace('<script type="application/ld+json">', '').replace('</script>', ''))

            if '<script id="__NEXT_DATA__" type="application/json">' in str(script):
                data = json.loads(script.split('<script id="__NEXT_DATA__" type="application/json">')[1].split('</script>')[0])
                break

        self.job_detail = data["props"]["initialState"]['api']['jobDetailHiddenContact']['data']
        self.employer_detail = data["props"]["initialState"]['api']['employerDetailHiddenContact']['data']

        # if self.first_item:
        self.metadata = data['props']['initialState']['api']['initCommon']['data']
            # self.first_item = False

        # return job_detail, employer_detail, parameters, data

        yield self.parse_job(response)
        yield self.parse_company(response)

    def parse_job(self, response):
        try:
            jobItem = ItemLoader(item=Vieclam24HScraperJobItem())

            jobItem.add_value('id', self.job_detail['id'])
            jobItem.add_value('company_id', self.employer_detail['id'])
            jobItem.add_value('post_time', self.job_detail['updated_at'])
            jobItem.add_value('post_title', self.job_detail['title'])
            jobItem.add_value('description', self.job_detail['description'])
            jobItem.add_value('vacancies', self.job_detail["vacancy_quantity"])
            jobItem.add_value('min_salary', self.job_detail['salary_min'])
            jobItem.add_value('max_salary', self.job_detail['salary_max'])
            jobItem.add_value('age_range', str(self.job_detail.get('age_range')))
            jobItem.add_value('gender', self.job_detail['gender'])
            jobItem.add_value('benefits', self.job_detail["benefit"])
            jobItem.add_value('education_requirements', self.job_detail['degree_requirement'])
            jobItem.add_value('experience_requirements', self.job_detail['experience_range'])
            jobItem.add_value('contract_type', self.job_detail['working_method'])

            # print(response.url)
            if self.parameters != []:
                jobItem.add_value('job_location', self.parameters['jobLocation']['address']['streetAddress'])
                jobItem.add_value('region', self.parameters['jobLocation']['address'].get("addressRegion", ""))
                jobItem.add_value('salary_type', self.parameters['baseSalary']['value']['unitText'])
                jobItem.add_value('industry', self.parameters['industry'])

            jobItem.add_value('job_type_id', response.meta['job_type_id'])
            jobItem.add_value('url', response.url)

            now = time.strftime(r"%d/%m/%Y %H:%M:%S", time.localtime())
            jobItem.add_value('created_time', now)
            jobItem.add_value('updated_time', now)

            return jobItem.load_item()
        except Exception as e:
            with open('./vieclam24h_scraper/error/error_url.txt', 'a') as f:
                f.write(str(response.url) + ', ' + str(e) + '\n')
                f.close()

    def parse_company(self, response):
        try:
            companyItem = ItemLoader(item=Vieclam24HScraperCompanyItem())

            companyItem.add_value('id', self.employer_detail['id'])
            companyItem.add_value('name', self.employer_detail['name'])
            companyItem.add_value('coordinate', [str(self.employer_detail.get('latitude')), str(self.employer_detail.get('longitude'))])
            companyItem.add_value('address', self.employer_detail['address'])
            companyItem.add_value('province', self.employer_detail['province_id'])

            return companyItem.load_item()
        except Exception as e:
            with open('./vieclam24h_scraper/error/error_url.txt', 'a') as f:
                f.write(str(response.url) + ', ' + str(e) + '\n')
                f.close()