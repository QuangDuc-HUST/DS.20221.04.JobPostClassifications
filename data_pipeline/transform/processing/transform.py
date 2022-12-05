import json
import copy
import re


def transform_company():
    # vl24h = open('/code/data_pipeline/extract/vieclam24h_scraper/data/company.json', 'r')
    vl24h = open('./data_pipeline/extract/vieclam24h_scraper/data/company.json', 'r')
    vl24h = json.load(vl24h)

    transform_company = []

    for i in range(len(vl24h)):
        temp_item = {}
        temp_item['id'] = vl24h[i]['id']
        temp_item['name'] = vl24h[i]['name']
        temp_item['coordinate'] = vl24h[i]['coordinate']if vl24h[i]['coordinate'] != '0, 0' else ''
        temp_item['address'] = vl24h[i]['address']
        temp_item['region'] = vl24h[i]['province']

        transform_company.append(temp_item)

    # transform_vl24h_file = open('./processing/staging/company.json', 'w')
    # json.dump(transform_company, transform_vl24h_file, indent=4)

    # vlt = open('/code/data_pipeline/extract/vieclamtot_scraper/data/company.json', 'r')
    vlt = open('./data_pipeline/extract/vieclamtot_scraper/data/company.json', 'r')
    vlt = json.load(vlt)

    for i in range(len(vlt)):
        temp_item = {}
        # print(vlt[i].keys())
        temp_item['id'] = vlt[i]['id']
        temp_item['name'] = vlt[i]['name']
        temp_item['coordinate'] = vlt[i]['location'].replace(',', ', ') if vlt[i]['location'] != '0,0' else ''

        adr = []
        for k in ['ward', 'district', 'city']:
            if vlt[i][k] != 'None':
                adr.append(k)
        temp_item['address'] = ', '.join([vlt[i][k] for k in adr])

        temp_item['region'] = vlt[i]['city'].replace("Tp H\u1ed3 Ch\u00ed Minh", 'TP.HCM').replace('Tp Hồ Chí Minh', 'TP.HCM')

        transform_company.append(temp_item)

    # transform_vlt_file = open('/code/data_pipeline/transform/staging/company/company.json', 'w')
    transform_vlt_file = open('./data_pipeline/transform/staging/company/company.json', 'w')
    json.dump(transform_company, transform_vlt_file, indent=4)


def transform_job():
    # t = 1
    # vl24h = open('/code/data_pipeline/extract/vieclam24h_scraper/data/job.json', 'r')
    vl24h = open('./data_pipeline/extract/vieclam24h_scraper/data/job.json', 'r')
    vl24h = json.load(vl24h)

    transform_job = []

    for i in range(len(vl24h)):
        try:
            temp_item = copy.deepcopy(vl24h[i])
            temp_item['skills'] = ''

            temp_item['job_type'] = temp_item.pop('industry')
            temp_item.pop('job_type_id')
            temp_item['title'] = temp_item.pop('post_title')
            # temp_item.pop('region')

            # temp_item['description'] = temp_item['description']

            if temp_item['salary_type'] == 'month':
                temp_item['salary_type'] == 'Theo tháng'

            for k in temp_item.keys():
                if temp_item[k] == 'None':
                    temp_item[k] = ''

            transform_job.append(temp_item)
            # if t == 1:
            #     k = sorted(temp_item.keys())
                  
        except Exception as e:
            # print(e)
            continue

    # transform_vl24h_file = open('./processing/staging/company.json', 'w')
    # json.dump(transform_company, transform_vl24h_file, indent=4)

    # vlt = open('/code/data_pipeline/extract/vieclamtot_scraper/data/job.json', 'r')
    vlt = open('./data_pipeline/extract/vieclamtot_scraper/data/job.json', 'r')
    vlt = json.load(vlt)

    for i in range(len(vlt)):
        try:
            temp_item = copy.deepcopy(vlt[i])
            temp_item.pop('job_id')
            # print(temp_item['url'])

            temp_item['description'] = temp_item.pop('full_description')
            temp_item['gender'] = temp_item.pop('preferred_gender')
            temp_item['education_requirements'] = temp_item.pop('preferred_education')
            temp_item['experience_requirements'] = temp_item.pop('preferred_working_experience')
            temp_item['job_location'] = temp_item.pop('address')

            # temp_item['description'] = temp_item['description']
            temp_item['region'] = temp_item['region'].replace("Tp H\u1ed3 Ch\u00ed Minh", 'TP.HCM').replace('Tp Hồ Chí Minh', 'TP.HCM')

            temp_item['age_range'] = temp_item.pop('min_age') + '-' + temp_item.pop('max_age')
            if re.match('\d+, .+', temp_item['age_range']) is None:
                temp_item['age_range'] = re.findall('\d+', temp_item['age_range'])[0] + '+'
            
            if re.match('.+, \d+', temp_item['age_range']) is None:
                temp_item['age_range'] = re.findall('\d+', temp_item['age_range'])[0] + '-'

            # if temp_item['benefits'] == 'None':
            #     temp_item['benefits'] = ''

            # temp_item['region'] = temp_item['region'].replace("Tp H\u1ed3 Ch\u00ed Minh", 'TP.HCM')

            for k in temp_item.keys():
                if temp_item[k] == 'None':
                    temp_item[k] = ''

            transform_job.append(temp_item)

        except Exception as e:
            print(e)
            continue

    # transform_vlt_file = open('/code/data_pipeline/transform/staging/job/job.json', 'w')
    transform_vlt_file = open('./data_pipeline/transform/staging/job/job.json', 'w')
    json.dump(transform_job, transform_vlt_file, indent=4)


transform_company()
transform_job()