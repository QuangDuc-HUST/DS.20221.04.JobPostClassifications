import json
import os


__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
print(__location__)


class Config:
    def __init__(self, file_path=os.path.join(__location__, 'config.json')):
        with open(file_path, "r") as f:
            self.config = json.load(f)

    def get_config(self):
        return self.config

    def get_postgres_config(self):
        return self.config["postgres"]

    def get_postgres_user(self):
        return self.config["postgres"]["user"]

    def get_postgres_password(self):
        return self.config["postgres"]["password"]

    def get_postgres_host(self):
        return self.config["postgres"]["host"]

    def get_postgres_port(self):
        return self.config["postgres"]["port"]

    def get_postgres_database(self):
        return self.config["postgres"]["database"]

    def get_airtable_api(self):
        return self.config["airtable"]["api"]

    def get_airtable_base_id(self):
        return self.config["airtable"]["base_id"]

    def get_airtable_job_table(self):
        return self.config["airtable"]["job_table"]

    def get_airtable_company_table(self):
        return self.config["airtable"]["company_table"]
