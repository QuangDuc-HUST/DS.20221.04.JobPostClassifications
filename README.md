# DS.20221.04.JobPostClassifications
Data Science Project - DANDL

This branch contains code to crawl data from websites. 

In the folder `src/scripts`, there are scripts files to run the data pipeline when using __Google Colab__. 

In case you clone our project to local machine, please remmember to __correct__ the _directory names_ before run. 

As this is an __ETL__ pipeline, run the scripts as the order of the pipeline. For example

```
bash extract.sh
```

to start crawling data, then respective transform the data and load them to the data warehouse.