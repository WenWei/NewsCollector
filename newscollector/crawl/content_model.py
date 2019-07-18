#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import time

CONTENT_STATUS_NONE = 'none'
CONTENT_STATUS_OK = 'ok'
CONTENT_STATUS_FAIL = 'fail'
CONTENT_STATUS_UNKNOW = 'unknow'

class ContentModel:

    def __init__(self, page_url = None, crawldatetime = None, contentType = None, content = None, status = None):
        if crawldatetime is None:
            crawldatetime = datetime.datetime.now()

        self.page_url = page_url
        self.datetime = crawldatetime
        self.contenttype = contentType
        self.content = content
        self.status = status
        self.links = set()