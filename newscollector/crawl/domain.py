#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib.parse import urlparse

# 取得域名 例如：example.com
def get_domain_name(url):
    try:
        results = get_sub_domain_name(url).split('.')
        return results[-2] + '.' + results[-1]
    except:
        return 

# 取得子域名(sub domain name) 例如：name.example.com
def get_sub_domain_name(url):
    try:
        return urlparse(url).netloc
    except:
        return ''
