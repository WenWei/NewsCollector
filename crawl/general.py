#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs

# 每個網站分開的專案(資料夾)
def create_project_dir(directory):
    if not os.path.exists(directory):
        print('Creating project '+ directory)
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
