import airtable as at
from pyairtable import Api, Base, Table
import requests
import time
import json
import pandas as pd


token = 'keyC0G5NLjL4qXKLJ'
# auth = at.auth.AirtableAuth(token)
base_id = 'appoGSNO1FZ8XvKT8'
table_name = 'job'
table = Base(token, base_id)
# print(table.get_all())

start = time.time()
job_data = json.load(open('./processing/staging/job/job.json', 'r'))
# table.batch_create(table_name, job_data)
for j in job_data[::-1]:
    try:
        table.create(table_name, j)
    except Exception as e:
        print(e)
# t = table.all(table_name='job')
# print(t)
end = time.time()
print(end - start)

# x = pd.DataFrame(job_data)
# sample = x.iloc[:5]
# cols = list(sample.columns.values)
# new_cols = ['url']
# for c in cols:
#     if c != new_cols[0]:
#         new_cols.append(c)
# sample = sample[new_cols]
# sample.to_csv('./sample.csv', index=False)

print(len(job_data))