#!/bin/bash

end_page=1

for i in vieclamtot vieclam24h
do
    echo /content/DS.20221.04.JobPostClassifications/data_pipeline/extract/"$i"_scraper/
    cd /content/DS.20221.04.JobPostClassifications/data_pipeline/extract/"$i"_scraper/
    scrapy crawl $i -a end_page="$end_page"
    echo "Finished crawling $i"
done