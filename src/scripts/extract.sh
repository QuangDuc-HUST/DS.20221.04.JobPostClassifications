#!/bin/bash

for i in vieclamtot vieclam24h
do
    echo /content/DS.20221.04.JobPostClassifications/src/data_pipeline/extract/"$i"_scraper/
    cd /content/DS.20221.04.JobPostClassifications/src/data_pipeline/extract/"$i"_scraper/
    scrapy crawl $i
    echo "Finished crawling $i"
done