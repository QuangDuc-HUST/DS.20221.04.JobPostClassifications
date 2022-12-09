#!/bin/bash

for i in vieclamtot vieclam24h
do
    cd $home_dir/$i_scraper/
    scrapy crawl $i
    echo "Finished crawling $i"
done