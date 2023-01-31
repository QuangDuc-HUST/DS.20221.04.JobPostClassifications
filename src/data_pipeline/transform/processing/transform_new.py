import re
import traceback


def transform_vlt_company(item):

    item = dict(item)
    # print(item.keys())
    item['coordinate'] = item.pop('location').replace(',', ', ') if item['location'] != '0,0' else ''
    item['region'] = item['city'].replace("Tp H\u1ed3 Ch\u00ed Minh", 'TP.HCM').replace('Tp Hồ Chí Minh', 'TP.HCM')

    adr = []
    for k in ['ward', 'district', 'city']:
        if item[k] != 'None':
            adr.append(k)

    item['address'] = ', '.join([item.pop(k) for k in adr])

    return item


def transform_vlt_job(item):
    item = dict(item)
    try:
        item.pop('job_id')
        # print(item['url'])

        item['description'] = item.pop('full_description').replace(r"&nbsp;", r' ')
        item['gender'] = item.pop('preferred_gender')
        item['education_requirements'] = item.pop('preferred_education')
        item['experience_requirements'] = item.pop('preferred_working_experience')
        item['job_location'] = item.pop('address')

        item['region'] = item['region'].replace("Tp H\u1ed3 Ch\u00ed Minh", 'TP.HCM').replace('Tp Hồ Chí Minh', 'TP.HCM')

        item['age_range'] = item.pop('min_age') + '-' + item.pop('max_age')
        if re.match('\d+, .+', item['age_range']) is None:
            item['age_range'] = re.findall('\d+', item['age_range'])[0] + '+'
        
        if re.match('.+, \d+', item['age_range']) is None:
            item['age_range'] = re.findall('\d+', item['age_range'])[0] + '-'

        

        item['coordinate'] = item.pop('location').replace(',', ', ') if item['location'] != '0,0' else ''
        item['region'] = item['city'].replace("Tp H\u1ed3 Ch\u00ed Minh", 'TP.HCM').replace('Tp Hồ Chí Minh', 'TP.HCM')

        adr = []
        for k in ['ward', 'district', 'city']:
            if item[k] != 'None':
                adr.append(k)

        item['address'] = ', '.join([item.pop(k) for k in adr])

        for k in item.keys():
            if item[k] == 'None':
                item[k] = ''
        return item

    except Exception as e:
        print(traceback.format_exc())

def transform_vl24h(item):

    item = dict(item)
    try:
        item['job_type'] = item.pop('industry')
        item.pop('job_type_id')
        item['title'] = item.pop('post_title')

        if item['salary_type'] == 'month':
            item['salary_type'] == 'Theo tháng'

        for k in item.keys():
            if item[k] == 'None':
                item[k] = ''

        item['company_region'] = item.pop('company_province')
        item['company_coordinate'] = item['company_coordinate'] if item['company_coordinate'] != '0, 0' else ''
        return item

    except Exception as e:
        print(traceback.format_exc())
