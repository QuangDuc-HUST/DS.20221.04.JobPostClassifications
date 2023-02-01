from vieclam24h_scraper.items import *
from utils.utils import *


class Vieclam24hSpider(scrapy.Spider):
    
    name = 'vieclam24h'
    configure_logging(install_root_handler=False, )
    logging.basicConfig(
        handlers=[logging.FileHandler(filename='./logging/log_records_{}.txt'.format(str(int(time.mktime(date.today().timetuple())))), encoding='utf-8', mode='a+')],
        format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
        datefmt="%F %A %T",
        level=logging.INFO
    )

    def __init__(self, **kwargs):

        self.url = "https://vieclam24h.vn/tim-kiem-viec-lam-nhanh"
        self.metadata = None
        self.first_item = True

        super().__init__(**kwargs)

    def start_requests(self):
        for t in range(1, 36): 

            r = requests.get("https://vieclam24h.vn/tim-kiem-viec-lam-nhanh?occupation_ids[]=" + str(t))
            soup = BeautifulSoup(r.content, "html.parser")  
            dom = etree.HTML(str(soup)) 
            pages = dom.xpath('//*[@id="__next"]/div/main/div/div/div/div[1]/div[1]/div/div[1]/span')[0].text
            self.end_page = int(pages.replace(',', ''))//30 + 2

            print(self.end_page)

            for p in range(self.end_page):
                yield scrapy.Request(self.url + "?occupation_ids[]=" + str(t) + "&page=" + str(p), callback=self.parse_links, meta={
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
            
        if self.parameters == []:
            # f = json.load(open('./error/error.json', 'r'))
            # f.append({'url': response.url, 'job_type_id': response.meta['job_type_id']})
            # json.dump(f, open('./error/error.json', 'w'))
            return 

        self.job_detail = data["props"]["initialState"]['api']['jobDetailHiddenContact']['data']
        self.employer_detail = data["props"]["initialState"]['api']['employerDetailHiddenContact']['data']

        # if self.first_item:
        self.metadata = data['props']['initialState']['api']['initCommon']['data']
        # self.first_item = False

        # return job_detail, employer_detail, parameters, data
        # if self.job_detail['updated_at'] >= 1672506000:
        if self.job_detail['updated_at'] >= 1640970000 and self.job_detail['updated_at'] < 1672506000:
            print(self.job_detail['updated_at'])
            yield self.parse_job(response)

    def parse_job(self, response):
        try:
            item24h = ItemLoader(item=Vieclam24HScraperItem())

            item24h.add_value('id', self.job_detail['id'])
            item24h.add_value('post_time', self.job_detail['updated_at'])
            item24h.add_value('post_title', self.job_detail['title'])
            item24h.add_value('description', self.job_detail['description'])
            item24h.add_value('vacancies', self.job_detail["vacancy_quantity"])
            item24h.add_value('min_salary', self.job_detail['salary_min'])
            item24h.add_value('max_salary', self.job_detail['salary_max'])
            item24h.add_value('age_range', str(self.job_detail.get('age_range')))
            item24h.add_value('gender', self.job_detail['gender'])
            item24h.add_value('benefits', self.job_detail["benefit"])
            item24h.add_value('education_requirements', self.job_detail['degree_requirement'])
            item24h.add_value('experience_requirements', self.job_detail['experience_range'])
            item24h.add_value('contract_type', self.job_detail['working_method'])

            # print(response.url)
            if self.parameters != []:
                item24h.add_value('job_location', self.parameters['jobLocation']['address']['streetAddress'])
                item24h.add_value('region', self.parameters['jobLocation']['address'].get("addressRegion", ""))
                item24h.add_value('salary_type', self.parameters['baseSalary']['value']['unitText'])
                item24h.add_value('industry', self.parameters['industry'])

            item24h.add_value('job_type_id', response.meta['job_type_id'])
            item24h.add_value('url', response.url)

            now = time.strftime(r"%d/%m/%Y %H:%M:%S", time.localtime())
            item24h.add_value('created_time', now)
            item24h.add_value('updated_time', now)

        except Exception as e:
            print("Viec Lam 24h: Job Error")
            print(traceback.format_exc())

        try:

            item24h.add_value('company_id', self.employer_detail['id'])
            item24h.add_value('company_name', self.employer_detail['name'])
            item24h.add_value('company_coordinate', [str(self.employer_detail.get('latitude')), str(self.employer_detail.get('longitude'))])
            item24h.add_value('company_address', self.employer_detail['address'])
            item24h.add_value('company_province', self.employer_detail['province_id'])

        except Exception as e:
            print("Viec Lam 24h: Company Error")
            print(traceback.format_exc())

        return item24h.load_item()
        