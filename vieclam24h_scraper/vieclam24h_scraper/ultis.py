# import pytz
import scrapy
import math
# from scrapy_splash import SplashRequest
import json
import time
import datetime
import traceback
# import psycopg2
# from ..items import AllSpidersItem
# from geopy.geocoders import Nominatim
from io import StringIO
from html.parser import HTMLParser
from scrapy.crawler import CrawlerProcess
# from twisted.internet import reactor
# import pandas as pd
from urllib.parse import urljoin
# Selenium
# from selenium import webdriver

# from dotenv import find_dotenv, load_dotenv
import os
# load_dotenv(find_dotenv())
import sys
# import pytz
# from seleniumwire import webdriver 
# from selenium.webdriver.chrome.options import Options
import re

# setting path
sys.path.append("..")
from configuration.config import Config

# cfg = Config("../configuration/config.json")
# one_connection = psycopg2.connect(
#     user = cfg.get_postgres_user(),
#     password = cfg.get_postgres_password(),
#     host = cfg.get_postgres_host(),
#     port = cfg.get_postgres_port(),
#     database = cfg.get_postgres_database(),
# )

# one_connection = psycopg2.connect(
#     user = "postgres",
#     password = "30082002Dl!",
#     host = "localhost",
#     port = "5432",
#     database = "vieclamtot",
# )

ignore_links, ignore_contents = [], []
DOWNLOAD_TIMEOUT = 10

"""
  Class kiểm tra dung lượng cơ sở dữ liệu đang quét và backup qua cơ sở dữ liệu trung tâm
"""

# class BackupDB():
  
#     global one_connection

#     connection = one_connection

#     cursor = connection.cursor()

#     def _getOneSize(self,item):
#         num = float(item.split()[0])
#         if "kB" in item: return num/100
#         if "GB" in item: return num*1000
#         return num

#     def _getCurrentSize(self):
#       query = "SELECT pg_size_pretty( pg_total_relation_size('      ') ), pg_size_pretty( pg_total_relation_size('api_news') ), pg_size_pretty( pg_total_relation_size('api_real_estate_content' ) );"
#       self.cursor.execute(query)
#       lst = self.cursor.fetchone()
#       result = 0
#       for i in lst:
#           result += self._getOneSize(i)
#       return result

#     def _getLimitSize(self):
#         query = "SELECT value FROM api_crawling_settings WHERE types = 'crawling_capacity';"
#         self.cursor.execute(query)
#         result = self.cursor.fetchone()
#         if result:
#             result = float(result[0])
#         else:
#             result = 0
#         return result

#     def stop(self):
#         print("STOP !!!")
#         os.chdir(os.getenv("CURRENT_DIR"))
#         command = 'tmux new-session -s backup -d && tmux send-keys -t backup "python3 backup.py" Enter && tmux kill-session -t crawler'
#         os.system(command)

#     def backup(self):
#         currentSize = self._getCurrentSize()
#         limitSize = self._getLimitSize()
      
#         if currentSize >= limitSize:
#             self.stop()
        

""" 
  Class quy chuẩn để loại bỏ các ký tự không mong muốn để tiền xử lý dữ liệu được trả về khi quét trên website
"""

# class MLStripper(HTMLParser):
#     def __init__(self):
#         super().__init__()
#         self.reset()
#         self.strict = False
#         self.convert_charrefs= True
#         self.text = StringIO()
#     def handle_data(self, d):
#         self.text.write(d)
#     def get_data(self):
#         return self.text.getvalue()


# def newCursor():
#     return one_connection.cursor()

# def updateIgnoreList():
#     global one_connection, ignore_links, ignore_contents
#     connection = one_connection
#     cursor = connection.cursor()
    
#     query = "UPDATE          SET is_crawled=true WHERE url IN (SELECT url FROM api_real_estate_content)"
#     cursor.execute(query)
#     connection.commit()

#     query = "SELECT url FROM        "
#     cursor.execute(query)
#     ignore_links = cursor.fetchall()
#     ignore_links = [x[0] for x in ignore_links]

#     query = "SELECT url FROM         WHERE is_crawled=true"
#     cursor.execute(query)
#     ignore_contents = cursor.fetchall()
#     ignore_contents = [x[0] for x in ignore_contents]

def getLinkData(obj, meta, link):
    """
    Sinh dữ liệu của 1 hàng để chèn vào bảng        
    domain_first: có chèn domain vào trước link hay không (mặc định là có)
    """
    json_data = {}
    # json_data["search_keyword"] = meta["search_keyword"]
    # json_data["page"] = str(meta["page"])
    json_data["website"] = obj.website
    # json_data["url"] = obj.url + link if domain_first else link
    json_data["url"] = link
    # json_data["url_type"] = meta["url_type"]
    # json_data["post_type"] = meta["post_type"]
    # json_data["error"] = ' '
    json_data["updated_at"] = str(datetime.datetime.now().timestamp())
    return json_data

# def normalize(json_data):
#     lower = ["number_of_floors", "floor", "number_of_bedrooms", "number_of_bathrooms", "total_site_area", "building_area", "carpet_areas", "price", "price_unit", "longitude", "latitude", "legal_info", "project_size"]
#     for key in lower:
#         json_data[key] = json_data[key].lower().strip().replace(",",".").replace("m2","m²")
#         if key.startswith("number_of_") and ' ' in json_data[key]:
#             json_data[key] = json_data[key].split()[0]
#     return json_data

def insertOne(json_data, connection, table='app_vieclamtot_scraper'):
    global one_connection, ignore_links, ignore_contents
    connection = one_connection
    cursor = connection.cursor()
    try:
        # if table == 'api_real_estate_content':
        #     json_data = normalize(json_data)
        cursor = connection.cursor()

        columns, values = list(json_data.keys()), list(json_data.values())
        for i in range(len(values)): 
            values[i] = values[i].replace("'",'"')

        columns = ', '.join(columns)
        values = "', '".join(values)

        query = """INSERT INTO {} ({}) VALUES ('{}') ON CONFLICT (url) DO NOTHING""".format(table, columns, values)
        cursor.execute(query)
        connection.commit()

        
    except BaseException:
        # Lỗi sẽ được in ra và yêu cầu truy xuất để ghi dữ liệu sẽ được thu hồi để việc quét đa luồng được tiếp tục
        connection.rollback()
        # try:
        #     json_data['html'] = ' '
        #     json_data['strip_content'] = ' '
        #     json_data['raw_content'] = ' '
        # except:
        #     pass
        print("ERROR !!!",values,str(traceback.format_exc()),sep='\n')
    
    # backup = BackupDB()
    # backup.backup()

# def insertMultiLinks(obj, links, meta, domain_first=True):
#     global one_connection, ignore_links, ignore_contents
#     connection = one_connection
#     cursor = connection.cursor()
#     """
#     Chèn nhiều link vào bảng        
#     domain_first: có chèn domain vào trước link hay không (mặc định là có)
#     """
#     links = [obj.url + link if domain_first else link for link in links]
    
#     for link in links:
#         json_data = getLinkData(obj,meta,link)
#         insertOne(json_data, None)

# def queryLinks(connection):
#     global one_connection, ignore_links, ignore_contents
#     connection = one_connection
#     cursor = connection.cursor()
#     """Lấy ra tất cả url của website đã lưu trong bảng      """    
#     query = "SELECT url FROM {}      WHERE is_crawled = 'FALSE'".format("app_vieclamtot_scraper")
#     cursor = connection.cursor()
#     cursor.execute(query)
#     links = cursor.fetchall()
#     return links

def queryTimes(connection):
  cursor = connection.cursor()
  query = "select job_id, max(post_time) from app_vieclamtot_scraper where auto='True' group by job_id"
  cursor.execute(query)
  keyword_times = cursor.fetchall()
  job_id_times = {i:None for i in range(1,25)}
  for x, y in keyword_times:
    job_id_times[int(x)] = y
  return job_id_times

def save_statistic(time, num_post, connection):
  cursor = connection.cursor()
  job_names = ['crawled_at', 'builder', 'seller', 'driver', 'maid', 'restaurant_hotel', 'customer_care', 'guard', 'electrician', 'weaver', 'beauty_care', 'food_processor', 'assistant', 'mechanic', 'unskilled_labor', 'salesman', 'real_estate', 'worker', 'multi_industry', 'receptionist', 'chef_bartender', 'audit', 'metalist', 'carpenter', 'shipper']  
  num_of_post = ", ".join(list(map(str, num_post.values())))
  columns = ', '.join(job_names)
  query = f"INSERT INTO app_vieclamtot_statistic({columns}) VALUES('{time}', {num_of_post})"
  cursor.execute(query)
  connection.commit()


class Vieclam24hContent:
  """
  Class đặc tả dữ liệu của một hàng trong bảng viec_lam_tot_content
  """
  def __init__(self, website = "", response = None):
    """Lưu các giá trị mặc định nếu object không khai báo"""
    self.columns = ["website", "url", "post_title", "full_description", "street_number", "updated_at"]
    
    self.content = {}
    for c in self.columns:
      self.content[c] = " "
    
    self.content["website"] = website 
    # self.content["updated_at"] = str(datetime.datetime.now(pytz.timezone('Asia/Ho_Chi_Minh')))
    self.content["updated_at"] = str(datetime.datetime.now().timestamp())

    if response:
      self.content["url"] = response.url

  
  def json(self):
    return self.content

  def update(self, json_data):
    for key in json_data:
      if json_data[key] is not None:
        self.content[key] = str(json_data[key]) 