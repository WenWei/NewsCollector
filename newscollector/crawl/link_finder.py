#!/usr/bin/env python
# -*- coding: utf-8 -*-

from html.parser import HTMLParser
from urllib import parse
import re
import logging

logger = logging.getLogger('root')


class LinkFinder(HTMLParser):

    def __init__(self, base_url, page_url):
        super().__init__()
        self.base_url = base_url
        self.page_url = page_url
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for(attribute, value) in attrs:
                if attribute == 'href':
                    url = parse.urljoin(self.base_url, value.strip(' \t\n\r'))
                    logger.info('handle_tag: '+url)
                    if re.match('https?://', url):
                        self.links.append(url)

    def page_links(self):
        return self.links

    def error(self, message):
        pass

# finder = LinkFinder()
# finder.feed('<html><head><title>test</title>')