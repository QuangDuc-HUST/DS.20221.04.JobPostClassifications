from configuration import config


config = config.Config()

def load_job(data, base):

    table_name = config.get_airtable_job_table()
    base.batch_create(table_name=table_name, records=data)
    # base.create(table_name, data)

def load_company(data, base):

    table_name = config.get_airtable_company_table()
    base.batch_create(table_name=table_name, records=data)
    # base.create(table_name, data)