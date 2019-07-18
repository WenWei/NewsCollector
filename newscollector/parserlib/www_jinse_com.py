#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
from .iparser import IParser


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
            'https?:\/\/www\.jinse\.com\/blockchain\/(\d+)\.html'
        ]

        for pattern in patterns:
            if re.match(pattern, url):
                return True

        return False

    def parse(self, content):
        print('www_jinse_com/blockchain/x.html')
        pass


class News(IParser):

    def __init__(self):
        super().__init__()

    def is_match(self, url):
        patterns = [
            'https?:\/\/www\.jinse\.com\/news\/blockchain\/(\d+)\.html'
        ]

        for pattern in patterns:
            if re.match(pattern, url):
                return True

        return False

    def parse(self, content):
        print('www_jinse_com/blockchain/x.html')
        pass


if __name__ == "__main__":
    parser = Home()
    print(parser.is_match('https://www.jinse.com/blockchain/414531.html'))
    print(parser.is_match('https://www.jinse.com/blockchain/abcdef.html'))
    print(parser.is_match('http://www.jinse.com/blockchain/414531.html'))
    print(parser.is_match('http://www.jinse.com/blockchain/cdefas.html'))