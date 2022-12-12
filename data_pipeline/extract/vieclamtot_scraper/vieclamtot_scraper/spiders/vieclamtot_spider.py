# from ..ultis import *
from vieclamtot_scraper.items import *
from utils.utils import *


class VieclamtotlinksSpider(scrapy.Spider):

    name = 'vieclamtot'

    configure_logging(install_root_handler=False, )
    logging.basicConfig(
        handlers=[logging.FileHandler(filename='./logging/log_records_{}.txt'.format(str(int(time.mktime(date.today().timetuple())))), encoding='utf-8', mode='a+')],
        format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
        datefmt="%F %A %T",
        level=logging.INFO
    )
    # Lấy kết nối tổng để đảm bảo chỉ có 1 connection đến PostgreSQL, tránh được việc quá tải nhiều yêu cầu truy xuất khi quét đa luồng
    # global one_connection
    # connection = one_connection
    # cursor = connection.cursor()
    
    def __init__(self, end_page='1', **kwargs):

        self.found = True
        self.url = "https://www.vieclamtot.com/viec-lam" 
        self.end_page = int(end_page)

        super().__init__(**kwargs)

    def get_id_list(self):

        f = open('./constants/job_id.txt', 'r')
        return [int(i.strip()) for i in f.readlines()]

    def start_requests(self):

        for t in self.get_id_list(): 
            for p in range(self.end_page):
                if self.found:
                    yield scrapy.Request(self.url + "-sdjt" + str(t) + "?&page=" + str(p) + "&sp=0", callback=self.parse_links, meta={
                        "download_timeout": 10,
                        "max_retry_time": 1,
                        'id': t
                    })
                    
                else:
                    break
            
            self.found = True

        # with open('../vieclamtot_scraper/self.data/sample_{}_page.json'.format(self.end_page), 'w') as file:
        #     json.dump(self.self.data, file, indent = 4)

    def preprocess(self, link):
        return urljoin(self.url, link)

    def parse_links(self, response):

        # print(response.url)
        # print(response.url.split('?')[0])
        # f = open('./constants/job_id.txt', 'a')

        if response.url.split('?')[0] == self.url:
            self.found = False
            return

        # f.write(str(response.meta['id']) + '\n')
        # f.close()
        self.found = True

        links = response.xpath('//a[contains(@class, "AdItem_adItem")]/@href').getall()

        # print(links)
        
        for link in links:
            # filter for priorities which might be posted long time ago
            if '[PL-top]' not in link:
                link = self.preprocess(link)
                yield scrapy.Request(link, callback=self._get_javascript_data, meta=response.meta)

    def _get_javascript_data(self, response):

        all_data = {}
        for script in response.xpath("//script").getall():
            if '<script id="__NEXT_DATA__" type="application/json">' in str(script):
                all_data = json.loads(script.split('<script id="__NEXT_DATA__" type="application/json">')[1].split('</script>')[0])
                break
        self.data = all_data["props"]["initialState"]["adView"]["adInfo"]["ad"]
        self.parameters = all_data["props"]["initialState"]["adView"]["adInfo"]["ad_params"]
        
        yield self.parse_job(response)
        yield self.parse_company(response)

    def parse_job(self, response):
        try:

            jobItem = ItemLoader(item=VieclamtotJobScraperItem())
            
            jobItem.add_value('id', self.data['list_id'])
            jobItem.add_value("company_id", self.data['account_id'])
            jobItem.add_value("job_id", self.data["job_type"])
            jobItem.add_value("post_time", self.data["list_time"])

            jobItem.add_value("title", self.data['subject'])
            jobItem.add_value("full_description", self.data['body'])
            jobItem.add_value("vacancies", self.data["vacancies"])
            jobItem.add_value("min_salary", str(self.data.get("min_salary")))
            jobItem.add_value("max_salary", str(self.data.get("max_salary")))
            jobItem.add_value("min_age", str(self.data.get("min_age")))
            jobItem.add_value("max_age", str(self.data.get("max_age")))
            jobItem.add_value("benefits", str(self.data.get("benefits")))
            jobItem.add_value("skills", str(self.data.get("skills")))
            jobItem.add_value("region", str(self.data.get("region_name")))

            jobItem.add_value("address", str(self.parameters.get("address", {}).get("value")))
            jobItem.add_value("salary_type", str(self.parameters["salary_type"]["value"]))
            jobItem.add_value("contract_type", str(self.parameters["contract_type"]["value"]))
            jobItem.add_value("job_type", str(self.parameters["job_type"]["value"]))
            jobItem.add_value("preferred_education", str(self.parameters.get("preferred_education", {}).get("value")))
            jobItem.add_value("preferred_gender", str(self.parameters.get("preferred_gender", {}).get("value")))
            jobItem.add_value("preferred_working_experience", str(self.parameters.get("preferred_working_experience", {}).get("value")))

            jobItem.add_value("url", response.url)
            now = time.strftime(r"%d/%m/%Y %H:%M:%S", time.localtime())
            jobItem.add_value('created_time', now)
            jobItem.add_value('updated_time', now)

            return jobItem.load_item()
        
        except Exception as e:
            with open('./error/error_job_url_{}.txt'.format(str(int(time.mktime(date.today().timetuple())))), 'a') as f:
                f.write(str(response.url) + ', ' + str(e) + '\n')
                f.close()
        
        # try:
        #     opt = Options()
        #     opt.add_argument('--no-sandbox')
        #     opt.add_argument('--headless')
        #     opt.add_argument('--disable-dev-shm-usage')
            
        #     driver = webdriver.Chrome('chromedriver', chrome_options=opt)
        #     driver.get(response.url)
        #     rq = driver.wait_for_request('/v1/public/ad-listing/phone')
        #     rl = json.loads(rq.response.body)
            
        #     driver.close()
        #     driver.quit()
        #     jobItem.add_value("phone", rl["phone"]
        # except Exception as e:
        #     jobItem.add_value("phone", ''
        #     print(e)

    def parse_company(self, response):
        try:

            companyItem = ItemLoader(item=VieclamtotCompanyScraperItem())

            companyItem.add_value("id", self.data['account_id'])
            companyItem.add_value("name", str(self.parameters.get("company_name", {}).get("value")))
            companyItem.add_value("location", str(self.data.get('location')))
            companyItem.add_value("city", str(self.data.get("region_name")))
            companyItem.add_value("district", str(self.data.get("area_name")))
            companyItem.add_value("ward", str(self.data.get("ward_name")))

            return companyItem.load_item()
        except Exception as e:
            with open('./error/error_company_url_{}.txt'.format(str(int(time.mktime(date.today().timetuple())))), 'a') as f:
                f.write(str(response.url) + ', ' + str(e) + '\n')
                f.close()
