import os
# import thread


# os.system('bash -c "cd vieclam24h_scraper && scrapy crawl vieclam24h"')

from subprocess import Popen, PIPE, STDOUT

scraper_names = ['vieclam24h', 'vieclamtot']
# run commands in parallel
for scraper_name in scraper_names:
    # print('------------ STARTING SCRAPER ', scraper_name.upper(), ' ------------')

    process = Popen("cd /code/{}_scraper && scrapy crawl {}".format(scraper_name, scraper_name), shell=True)
    process.wait()

    # print('------------ STARTED SCRAPER ', scraper_name.upper(), ' ------------')
            
# collect statuses
# exitcodes = [p.wait() for p in processes]