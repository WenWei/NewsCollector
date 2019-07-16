#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
from queue import Queue
from crawl.spider import Spider
from crawl.domain import get_domain_name
from crawl.general import file_to_set

PROJECT_NAME = 'thenewboston'
HOMEPAGE = 'https://www.jinse.com/'
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE ='data/' + PROJECT_NAME + '/queue.txt'
CRAWLED_FILE ='data/' + PROJECT_NAME + 'crawled.txt'
NUMBER_OF_THREADS = 1
queue = Queue()  # Thread queue
Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)

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
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()

# 每個 queue 設為新工作
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
        print('put link: '+ link)
    queue.join()
    crawl()

# 檢查項目在佇列，則取出爬取該頁
def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the queue')
        create_jobs()

create_workers()
crawl()
