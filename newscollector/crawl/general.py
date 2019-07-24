#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
import logging
import re
import urllib.parse

logger = logging.getLogger('root')


# 每個網站分開的專案(資料夾)
def create_project_dir(directory):
    if not os.path.exists(directory):
        logger.info('Creating project '+ directory)
        os.makedirs(directory)


# 建立佇列和已爬取的檔案
def create_data_file(project_name, base_url):
    queue = project_name + '/queue.txt'
    crawled = project_name + '/crawled.txt'
    if not os.path.isfile(queue):
        write_file(queue, base_url)
    if not os.path.isfile(crawled):
        write_file(crawled, '')


# 建立新檔案
def write_file(path, data):
    f = codecs.open(path, 'w', 'utf-8')
    f.write(data)
    f.close()


# 加入資料至已存在的檔案
def append_to_file(path, data):
    with codecs.open(path, 'a', 'utf-8') as file:
        file.write(data + '\n')


# 刪除檔案中的內容
def delete_file_contents(path):
    with codecs.open(path, 'w', 'utf-8'):
        pass


# 讀取檔案，將每一行轉成清單集合
def file_to_set(file_name):
    results = set()
    with codecs.open(file_name, 'r', 'utf-8') as f:
        for line in f:
            results.add(line.replace('\n', ''))
    return results


# 循覽集合，每個新項目
def set_to_file(links, file):
    delete_file_contents(file)
    for link in sorted(links):
        append_to_file(file, link)

# 將 cjk 轉成 url encode
def replace_cjk_with_quote(s):
    new_s = []
    pattern = r'([\u2e80-\u2e99\u2e9b-\u2ef3\u2f00-\u2fd5\u3005\u3007\u3021-\u3029\u3038-\u303a\u303b\u3400-\u4db5\u4e00-\u9fc3\uf900-\ufa2d\ufa30-\ufa6a\ufa70-\ufad9\U00020000-\U0002a6d6\U0002a700-\U0002b734\U0002b740-\U0002b81d\U0002b820-\U0002cea1\U0002ceb0-\U0002ebe0\U0002f800-\U0002fa1d])'
    for w in s:
        if re.match(pattern, w):
            new_s.append(urllib.parse.quote(w))
        else:
            new_s.append(w)
    return "".join(new_s)
