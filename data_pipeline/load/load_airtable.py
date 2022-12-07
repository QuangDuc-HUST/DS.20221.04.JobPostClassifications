import airtable as at
from pyairtable import Api, Base, Table
import requests
import time
import json
import pandas as pd
import configuration.config as cfg


config = cfg.Config()

api_key = config.get_airtable_api()
base_id = config.get_airtable_base_id()
base = Base(api_key=api_key, base_id=base_id)


def load_job():

    start = time.time()
    # job_data = json.load(open('/code/data_pipeline/transform/staging/job/job.json', 'r'))
    job_data = json.load(open('./data_pipeline/transform/staging/job/job.json', 'r'))
    table_name = config.get_airtable_job_table()

    # Get sample file for initialization in airtable

    # x = pd.DataFrame(job_data)
    # sample = x.iloc[:5]
    # cols = list(sample.columns.values)
    # new_cols = ['url']
    # for c in cols:
    #     if c != new_cols[0]:
    #         new_cols.append(c)
    # sample = sample[new_cols]
    # sample.to_csv('./sample_job.csv', index=False)

    # Insert
    base.batch_create(table_name=table_name, records=job_data)

    # Retrieve    
    # jobs = base.all(table_name=table_name)
    # job_df = pd.DataFrame(jobs)
    # job_df.to_csv('./sample_select_job.csv')
    # print(len(jobs))

    end = time.time()

    print(end - start)


load_job()


def load_company():

    start = time.time()
    # company_data = json.load(open('/code/data_pipeline/transform/staging/company/company.json', 'r'))
    company_data = json.load(open('./data_pipeline/transform/staging/company/company.json', 'r'))
    table_name = config.get_airtable_company_table()

    # Get sample file for initialization in airtable
    # x = pd.DataFrame(company_data)
    # sample = x.iloc[:5]
    # sample.to_csv('./sample_company.csv', index=False)

    # Insert
    base.batch_create(table_name=table_name, records=company_data)

    # Retrieve
    # companies = table.all(table_name=table_name)
    # print(len(companies))
    
    end = time.time()
    
    print(end - start)
