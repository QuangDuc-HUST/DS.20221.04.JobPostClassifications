#!/bin/bash

. /opt/env/bin/activate 
cd /code/data_pipeline/load
# python3 load_pg.py

python3 load_airtable.py