#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
import logging
from lxml import etree
from lxml import html
from .iparser import IParser
from io import StringIO, BytesIO
logger = logging.getLogger('root')

class Www_Jinse_Com():

    parsers = []

    def __init__(self):
        self.parsers.append(Home())
        self.parsers.append(News())

    def get_parsers(self):
        return self.parsers


class Home(IParser):

    def __init__(self):
        super().__init__()

    def is_match(self, url):
        patterns = [
            r'https?:\/\/(www|m)\.jinse\.com\/?$'
        ]

        for pattern in patterns:
            if re.match(pattern, url):
                return True

        return False

    def parse(self, contentmodel):
        contentmodel['kind']="home"


class News(IParser):
    """
    https://www.jinse.com/news/blockchain/417295.html
    熱文、新聞、政策、相對論、人物、行情、投研、技術、百科
    """
    def __init__(self):
        super().__init__()

    def is_match(self, url):
        pattern = r'https?:\/\/(www|m)\.jinse\.com\/news\/blockchain\/(\d+)\.html$'

        if re.match(pattern, url):
            return True

        return False


    def parse(self, contentmodel):
        logger.info('start parse:' + contentmodel['page_url'])
        dom = etree.HTML(contentmodel['content'])
        article_title = dom.xpath("//h2/text()")[0]
        article_author = dom.xpath("//div[contains(@class,'article-info')]/a/text()")[0]
        article_body = dom.xpath("string(//div[contains(@class, 'js-article-detail')])")
        tags = dom.xpath("//div[contains(@class,'tags')]/a/text()")
        contentmodel['kind']="news"
        contentmodel['infos'] = {
            "article_title": article_title,
            "article_author": article_author,
            "article_body": article_body,
            "published_at": None,
            "tags": tags
        }
        return contentmodel

class Blockchain(IParser):
    """
    https://www.jinse.com/blockchain/417295.html
    熱文
    """
    def __init__(self):
        super().__init__()

    def is_match(self, url):
        pattern = r'https?:\/\/(www|m)\.jinse\.com\/blockchain\/(\d+)\.html$'

        if re.match(pattern, url):
            return True

        return False


    def parse(self, contentmodel):
        logger.info('start parse:' + contentmodel['page_url'])
        dom = etree.HTML(contentmodel['content'])
        article_title = dom.xpath("//h2/text()")[0]
        article_author = dom.xpath("//div[contains(@class,'article-info')]/a/text()")[0]
        article_body = dom.xpath("string(//div[contains(@class, 'js-article-detail')])")
        tags = dom.xpath("//div[contains(@class,'tags')]/a/text()")
        contentmodel['kind']="blockchain"
        contentmodel['infos'] = {
            "article_title": article_title,
            "article_author": article_author,
            "article_body": article_body,
            "published_at": None,
            "tags": tags
        }
        return contentmodel

class Dissertation(IParser):
    """
    https://www.jinse.com/dissertation
    專題
    """
    def __init__(self):
        super().__init__()

    def is_match(self, url):
        pattern = r'https?:\/\/(www|m)\.jinse\.com\/dissertation\/(\d+)\.html$'

        if re.match(pattern, url):
            return True

        return False


    def parse(self, contentmodel):
        logger.info('start parse:' + contentmodel['page_url'])
        dom = etree.HTML(contentmodel['content'])
        article_title = dom.xpath("//h2/text()")[0]
        article_author = dom.xpath("//div[contains(@class,'article-info')]/a/text()")[0]
        article_body = dom.xpath("string(//div[contains(@class, 'js-article-detail')])")
        ele = dom.xpath("//div[contains(@class, 'js-article-detail')]")
        article_body_raw = "".join([ele if  isinstance(ele, str) else html.tostring(ele) for ele in eles])
        tags = dom.xpath("//div[contains(@class,'tags')]/a/text()")
        contentmodel['kind']="dissertation"
        contentmodel['infos'] = {
            "article_title": article_title,
            "article_author": article_author,
            "article_body": article_body,
            "article_body_raw": article_body_raw,
            "published_at": None,
            "tags": tags,
            
        }
        return contentmodel


if __name__ == "__main__":
    parser = Home()
    print(parser.is_match('https://www.jinse.com/blockchain/414531.html'))
    print(parser.is_match('https://www.jinse.com/blockchain/abcdef.html'))
    print(parser.is_match('http://www.jinse.com/blockchain/414531.html'))
    print(parser.is_match('http://www.jinse.com/blockchain/cdefas.html'))