import psycopg2 
import sys
sys.path.append('..')
from configuration.config import Config
import json


cfg = Config("../configuration/config.json")

print(cfg)

one_connection = psycopg2.connect(
    user = cfg.get_postgres_user(),
    password = cfg.get_postgres_password(),
    host = cfg.get_postgres_host(),
    port = cfg.get_postgres_port(),
    database = cfg.get_postgres_database(),
)

cursor = one_connection.cursor()

def load_company():

    c = open('/code/processing/staging/company/company.json', 'r')
    c = json.load(c)

    for i in c:

        cursor.execute("INSERT INTO {} ({}) VALUES ( ".format('company', ','.join(i.keys())) + ",".join(["'" + str(i).replace("'", '"') + "'" for i in i.values()]) + ");", 
                    i.keys())

        one_connection.commit()


def load_job():
    c = open('/code/processing/staging/job/job.json', 'r')
    c = json.load(c)

    for i in c:
        # print("INSERT INTO {} ({}) VALUES ( ".format('job', ','.join(i.keys())) + ",".join(["'" + str(i).replace("'", '"') + "'" for i in i.values()]) + ");")
        
        cursor.execute("INSERT INTO {} ({}) VALUES ( ".format('job', ','.join([v for v in i.keys() if str(i[v]) != ''])) + ",".join(["'" + str(i).replace("'", '"') + "'" for i in i.values() if str(i) != '']) + ");", 
                    )

        one_connection.commit()

load_job()
load_company()

one_connection.close()