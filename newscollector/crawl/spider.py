#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib.request import urlopen
from urllib.request import Request
from .link_finder import LinkFinder
from .general import file_to_set, set_to_file, create_project_dir, create_data_file
from .content_model import *
import re
import logging
import datetime
import time


logger = logging.getLogger()


class Spider:
    
    # 類別變數（共享）
    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    queue = set()
    crawled = set()

    def __init__(self, project_name, base_url, domain_name):
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queue_file = 'data/' + Spider.project_name + '/queue.txt'
        Spider.crawled_file = 'data/' +Spider.project_name + '/crawled.txt'
        self.boot()
        self.crawl_page('First spider', Spider.base_url)

    @staticmethod
    def boot():
        create_project_dir('data/' +Spider.project_name)
        create_data_file('data/' +Spider.project_name, Spider.base_url)
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)

    @staticmethod
    def crawl_page(thread_name, page_url, result_callback=None):
        if page_url not in Spider.crawled:
            print(thread_name + 'now crawling ' + page_url)
            print('Queue ' + str(len(Spider.queue)) + ' | Crawled '+ str(len(Spider.crawled)))
            contentmodel = Spider.gather_content(page_url)
            if contentmodel is not None:
                Spider.add_link_to_queue(contentmodel['links'])
                Spider.queue.remove(page_url)
                Spider.crawled.add(page_url)
                Spider.update_files()
                if result_callback!=None:
                    result_callback(contentmodel)

    @staticmethod
    def gather_content(page_url):
        html_string = ''
        contentmodel = {
            'page_url':page_url,
            'crawldatetime': datetime.datetime.now(),
            'contenttype': None,
            'content': None,
            'status': CONTENT_STATUS_UNKNOW,
            'links': []
        }
        try:
            req = Request(page_url)
            req.add_header('user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36')
            response = urlopen(req)
            content_type = response.getheader('Content-Type')
            if re.match('text\/html', content_type):
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
            finder = LinkFinder(Spider.base_url, page_url)
            finder.feed(html_string)
            contentmodel['contenttype'] = content_type
            contentmodel['content'] = html_string
            contentmodel['links'] = finder.page_links()
            contentmodel['status'] = CONTENT_STATUS_OK
        except:
            logger.error('Error: an not crawl page '+ page_url)
            contentmodel['status'] = CONTENT_STATUS_FAIL
            return None
        return contentmodel

    # @staticmethod
    # def gather_links(page_url):
    #     html_string = ''
    #     try:
    #         req = Request(page_url)
    #         req.add_header('user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36')
    #         response = urlopen(req)
    #         content_type = response.getheader('Content-Type')
    #         if re.match('text\/html', content_type):
    #             html_bytes = response.read()
    #             html_string = html_bytes.decode("utf-8")
    #         finder = LinkFinder(Spider.base_url, page_url)
    #         finder.feed(html_string)
    #     except:
    #         #print('Error: an not crawl page')
    #         logger.error('Error: an not crawl page '+ page_url)
    #         return set()
    #     return finder.page_links()

    @staticmethod
    def add_link_to_queue(links):
        for url in links:
            if url in Spider.queue:
                continue
            if url in Spider.crawled:
                continue
            if Spider.domain_name not in url:
                continue
            Spider.queue.add(url)


    @staticmethod
    def update_files():
        set_to_file(Spider.queue, Spider.queue_file)
        set_to_file(Spider.crawled, Spider.crawled_file)
