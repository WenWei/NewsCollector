#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .www_jinse_com import Www_Jinse_Com
from crawl.content_model import ContentModel
import logging

logger = logging.getLogger()

class ParserContext:
    parsers = []

    def __init__(self):
        for p in Www_Jinse_Com().get_parsers():
            self.parsers.append(p)

    def get_parser(self, raw_path):
        for p in self.parsers:
            if p.is_match(raw_path):
                return p

        return None

    def parse(self, raw_path, content):
        p = self.get_parser(raw_path)
        if p is not None:
            return p.parse(content)
        return None

    def parseContentModel(self, contentmodel):
        # if not isinstance(contentmodel, ContentModel):
        #     logger.error('error contentmodel: ' + repr(contentmodel))
        #     return None
        p = self.get_parser(contentmodel['page_url'])
        if p is not None:
            #return p.parse(contentmodel)
            return contentmodel

        return contentmodel
        



if __name__ == "__main__":
    context = ParserContext()
    print(context.get_parser('https://www.jinse.com/blockchain/414531.html'))

# for name, entity in parsers.__dict__.items():
#     if not name.startswith('__'):
#         cls = entity
#         print(cls.get_view_type())



# import os
# from os.path import dirname, join, isdir, abspath, basename
# from glob import glob
# import sys
# # pwd = dirname('C:/Users/DS.Tom/CryptoPrice/Exchanges/')
# pwd = os.path.dirname(os.path.abspath(__file__))
# pwd = os.path.join(pwd, 'parsers')
# print(pwd)
# sys.path.append(pwd)
# files = dict()

# for x in glob(join(pwd, '*.py')):
#         if not basename(x)[:2]=='__':
#             toimport = (basename(x)[:-3])
#             __import__(basename(x)[:-3], globals(), locals())
#             exec("import " + basename(x)[:-3] + " as " + basename(x)[:-3],globals(),locals())
#             exec("newclass = " + basename(x)[:-3] + "." + basename(x)[:-3]+"()")
#             files[basename(x)[:-3]] = newclass

# import sys
# current_module = sys.modules[__name__]

# import sys, inspect
# def print_classes():
#     for name, obj in inspect.getmembers(sys.modules[__name__]):
#         if inspect.isclass(obj):
#             print(obj)

# clsmembers = inspect.getmembers(sys.modules[__name__], inspect.isclass)

