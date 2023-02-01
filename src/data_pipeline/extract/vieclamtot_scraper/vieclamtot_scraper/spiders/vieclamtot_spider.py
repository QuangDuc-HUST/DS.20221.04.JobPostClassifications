# from ..ultis import *
from vieclamtot_scraper.items import *
from utils.utils import *


class VieclamtotlinksSpider(scrapy.Spider):

    name = 'vieclamtot'
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"

    configure_logging(install_root_handler=False, )
    logging.basicConfig(
        handlers=[logging.FileHandler(filename='./logging/log_records_{}.txt'.format(str(int(time.mktime(date.today().timetuple())))), encoding='utf-8', mode='a+')],
        format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
        datefmt="%F %A %T",
        level=logging.INFO
    )
    
    def __init__(self, end_page='250', **kwargs):

        self.found = True
        self.url = "https://www.vieclamtot.com/viec-lam" 
        self.end_page = int(end_page)

        super().__init__(**kwargs)

    def get_id_list(self):

        f = open('./constants/job_id.txt', 'r')
        return [str(i.strip()) for i in f.readlines()]

    def start_requests(self):

        for t in self.get_id_list(): 
            for p in range(self.end_page):
                yield scrapy.Request(self.url + "-" + t + "?&page=" + str(p) + "&sp=0", callback=self.parse_links, meta={
                    "download_timeout": 10,
                    "max_retry_time": 1,
                    'id': int(t[t.find('sdjt') + 4 : ])
                })

            
            self.found = True

        # with open('../vieclamtot_scraper/self.data/sample_{}_page.json'.format(self.end_page), 'w') as file:
        #     json.dump(self.self.data, file, indent = 4)

    def preprocess(self, link):
        return urljoin(self.url, link)

    def parse_links(self, response):

        # print(response)
        # print(response.url.split('?')[0])
        # f = open('./constants/job_id.txt', 'a')

        # f.write(str(response.meta['id']) + '\n')
        # f.close()

        links = response.xpath('//a[contains(@class, "AdItem_adItem")]/@href').getall()

        # print(links)
        
        for link in links:
            # filter for priorities which might be posted long time ago
            if '[PL-top]' not in link:
                link = self.preprocess(link)
                yield scrapy.Request(link, callback=self._get_javascript_data, meta=response.meta)

    def _get_javascript_data(self, response):
        # print(response)

        all_data = {}
        for script in response.xpath("//script").getall():
            if '<script id="__NEXT_DATA__" type="application/json">' in str(script):
                all_data = json.loads(script.split('<script id="__NEXT_DATA__" type="application/json">')[1].split('</script>')[0])
                break
        self.data = all_data["props"]["initialState"]["adView"]["adInfo"]["ad"]
        self.parameters = all_data["props"]["initialState"]["adView"]["adInfo"]["ad_params"]
        
        yield self.parse_job(response)

    def parse_job(self, response):
        try:
            # print(response)
            itemvlt = ItemLoader(item=VieclamtotJobScraperItem())
            
            itemvlt.add_value('id', self.data['list_id'])
            itemvlt.add_value("job_id", self.data["job_type"])
            itemvlt.add_value("post_time", self.data["list_time"])

            itemvlt.add_value("title", self.data['subject'])
            itemvlt.add_value("full_description", self.data['body'])
            itemvlt.add_value("vacancies", self.data["vacancies"])
            itemvlt.add_value("min_salary", str(self.data.get("min_salary")))
            itemvlt.add_value("max_salary", str(self.data.get("max_salary")))
            itemvlt.add_value("min_age", str(self.data.get("min_age")))
            itemvlt.add_value("max_age", str(self.data.get("max_age")))
            itemvlt.add_value("benefits", str(self.data.get("benefits")))
            itemvlt.add_value("skills", str(self.data.get("skills")))
            itemvlt.add_value("region", str(self.data.get("region_name")))

            itemvlt.add_value("address", str(self.parameters.get("address", {}).get("value")))
            itemvlt.add_value("salary_type", str(self.parameters["salary_type"]["value"]))
            itemvlt.add_value("contract_type", str(self.parameters["contract_type"]["value"]))
            itemvlt.add_value("job_type", str(self.parameters["job_type"]["value"]))
            itemvlt.add_value("preferred_education", str(self.parameters.get("preferred_education", {}).get("value")))
            itemvlt.add_value("preferred_gender", str(self.parameters.get("preferred_gender", {}).get("value")))
            itemvlt.add_value("preferred_working_experience", str(self.parameters.get("preferred_working_experience", {}).get("value")))

            itemvlt.add_value("url", response.url)
            now = time.strftime(r"%d/%m/%Y %H:%M:%S", time.localtime())
            itemvlt.add_value('created_time', now)
            itemvlt.add_value('updated_time', now)

        
        except Exception as e:
            with open('./error/error_job_url_{}.txt'.format(str(int(time.mktime(date.today().timetuple())))), 'a') as f:
                f.write(str(response.url) + ', ' + str(e) + '\n')
                f.close()
        
        try:

            itemvlt.add_value("company_id", self.data['account_id'])
            itemvlt.add_value("company_name", str(self.parameters.get("company_name", {}).get("value")))
            itemvlt.add_value("company_location", str(self.data.get('location')))
            itemvlt.add_value("company_city", str(self.data.get("region_name")))
            itemvlt.add_value("company_district", str(self.data.get("area_name")))
            itemvlt.add_value("company_ward", str(self.data.get("ward_name")))

        except Exception as e:
            with open('./error/error_company_url_{}.txt'.format(str(int(time.mktime(date.today().timetuple())))), 'a') as f:
                f.write(str(response.url) + ', ' + str(e) + '\n')
                f.close()

        return itemvlt.load_item()

