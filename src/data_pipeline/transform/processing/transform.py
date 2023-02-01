import json
import copy
import re
import traceback


def transform_vl24h(transform_company, transform_job):

    vl24h = open('./staging/staging_vieclam24h_2022.json', 'r')
    vl24h = json.load(vl24h)

    for i in range(len(vl24h)):
        try:
            temp_item = {}
            temp_item['id'] = vl24h[i]['company_id']
            temp_item['name'] = vl24h[i].pop('company_name')
            temp_item['coordinate'] = vl24h[i].pop('company_coordinate') if vl24h[i]['company_coordinate'] != '0, 0' else ''
            temp_item['address'] = vl24h[i].pop('company_address')
            temp_item['region'] = vl24h[i].pop('company_province')

            transform_company.append(temp_item)


        except Exception as e:
            print("Viec Lam 24h: Transfrom error!")
            print(traceback.format_exc())

        
        try:
            temp_item = copy.deepcopy(vl24h[i])
            temp_item['company_id'] = temp_item.pop('company_id')
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
            print(traceback.format_exc())
        
    # transform_file = open('./data/company.json', 'w')
    # json.dump(transform_company, transform_file, indent=4)

    # transform_file = open('./data/job.json', 'w')
    # json.dump(transform_job, transform_file, indent=4)

    return transform_company, transform_job


def transform_vlt(transform_company, transform_job):

    vlt = open('./staging/staging_vieclamtot_2021.json', 'r')
    vlt = json.load(vlt)

    for i in range(len(vlt)):
        try:
            temp_item = {}
            # print(vlt[i].keys())
            temp_item['id'] = vlt[i]['company_id']
            temp_item['name'] = vlt[i].pop('company_name')
            temp_item['coordinate'] = vlt[i].pop('company_location').replace(',', ', ') if vlt[i]['company_location'] != '0,0' else ''

            vlt[i]['company_city'] = vlt[i]['company_city'].replace("Tp H\u1ed3 Ch\u00ed Minh", 'TP.HCM').replace('Tp Hồ Chí Minh', 'TP.HCM')
            temp_item['region'] = vlt[i]['company_city']

            adr = []
            for k in ['company_ward', 'company_district', 'company_city']:
                if vlt[i][k] != 'None':
                    adr.append(k)
            temp_item['address'] = ', '.join([vlt[i].pop(k) for k in adr])

            transform_company.append(temp_item)
        except Exception as e:
            print(traceback.format_exc())

        try:
            temp_item = copy.deepcopy(vlt[i])
            temp_item.pop('job_id')
            # print(temp_item['url'])
            temp_item['company_id'] = temp_item.pop('company_id')
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
            print(traceback.format_exc())

    return transform_company, transform_job

def transform_data():

    transform_company = []
    transform_job = []

    # transform_company, transform_job = transform_vl24h(transform_company, transform_job)
    transform_company, transform_job = transform_vlt(transform_company, transform_job)

    transform_file = open('../load/data/company_vlt_2021.json', 'w')
    json.dump(transform_company, transform_file, indent=4)

    transform_file = open('../load/data/job_vlt_2021.json', 'w')
    json.dump(transform_job, transform_file, indent=4)

transform_data()