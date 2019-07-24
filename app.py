#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
from queue import Queue
from newscollector.crawl.spider import Spider
from newscollector.crawl.domain import get_domain_name
from newscollector.crawl.general import file_to_set
from newscollector.parserlib.parsercontext import ParserContext
import json
import datetime
from newscollector.dbutils import DbUtils
import os

import logging
import logging.config
from newscollector import logging_config
#logging.config.fileConfig('./logging.conf')
#logger = logging.getLogger('root')

PROJECT_NAME = 'thenewboston'
HOMEPAGE = 'https://www.jinse.com/'
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE ='data/' + PROJECT_NAME + '/queue.txt'
CRAWLED_FILE ='data/' + PROJECT_NAME + 'crawled.txt'
NUMBER_OF_THREADS = 1
queue = Queue()  # Thread queue
Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)
parserContext = ParserContext()
dbutil = DbUtils(os.getenv('NewsCollectorMongoDbConnectionString', 'mongodb://localhost:27017/'))


# 建立工作執行緒，當主線結束也會結束
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()

# 執行佇列中的下一個工作
def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url, result_callback)
        queue.task_done()

# 每個 queue 設為新工作
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
        logger.info('put link: '+ link)
    queue.join()
    crawl()

# 檢查項目在佇列，則取出爬取該頁
def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        logger.info(str(len(queued_links)) + ' links in the queue')
        create_jobs()

def result_callback(contentmodel):
    m = parserContext.parseContentModel(contentmodel)
    # jsonString = json.dumps(m, default = myconverter)
    # logger.info(jsonString)
    if m is not None:
        try:
            db = dbutil.getDatabase(PROJECT_NAME)
            collectionName = get_domain_name(contentmodel['page_url']).replace('.','_')
            collection = db[collectionName]
            collection.update_one({'page_url':m['page_url']}, {"$set":m}, upsert=True)
            #collection.find_and_modify(query={'page_url':m['page_url']}, update={"$set": m}, upsert=False, full_response= True)
            # insert_id = collection.insert_one(m).inserted_id
            # logger.info('inserted: '+ insert_id)
        except Exception as e:
            logger.exception(e)

def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

if __name__ == '__main__':
    # 執行 logging 設定
    logging_config.init()
    logger = logging.getLogger('__main__')
    logger.info('app.py runing')

    create_workers()
    crawl()
