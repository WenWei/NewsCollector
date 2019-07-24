import re
import unittest
import sys
import datetime
from urllib.request import urlopen
from urllib.request import Request
import logging

sys.path.append('../../newscollector')


# import NewsCollector.parser#.www_jinse_com.home
# import sys
# sys.path.insert(0,'/path/to/cts_sap_polaris/lib')

from newscollector.parserlib.www_jinse_com import Home, News, Www_Jinse_Com
from newscollector.crawl.content_model import CONTENT_STATUS_NONE, CONTENT_STATUS_OK, CONTENT_STATUS_FAIL, CONTENT_STATUS_UNKNOW


class TestWwwJinseCom(unittest.TestCase):
    def test_get_parsers(self):
        wjc = Www_Jinse_Com()
        parsers = wjc.get_parsers()
        self.assertGreaterEqual(len(parsers), 1)


def gather_content(page_url):
        html_string = ''
        contentmodel = {
            'page_url': page_url,
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
            if re.match(r'text\/html', content_type):
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
            contentmodel['contenttype'] = content_type
            contentmodel['content'] = html_string
            contentmodel['links'] = []
            contentmodel['status'] = CONTENT_STATUS_OK
        except:
            logger.error('Error: an not crawl page '+ page_url)
            contentmodel['status'] = CONTENT_STATUS_FAIL
            return None
        return contentmodel

class TestHome(unittest.TestCase):
    def test_is_match(self):
        """
        測試網址檢查
        """
        parser = Home()
        self.assertTrue(parser.is_match('https://www.jinse.com/'))
        self.assertTrue(parser.is_match('https://www.jinse.com'))
        self.assertTrue(parser.is_match('https://m.jinse.com/'))
        self.assertTrue(parser.is_match('https://m.jinse.com'))

        self.assertFalse(parser.is_match('https://www.jinse.com/blockchain/abcdef.html'))


class TestNews(unittest.TestCase):
    def test_is_match(self):
        """
        測試網址檢查
        """
        parser = News()
        self.assertTrue(parser.is_match('https://www.jinse.com/news/blockchain/414347.html'))
        self.assertFalse(parser.is_match('https://www.jinse.com/news/blockchain/abcdef.html'))

    def test_parse(self):
        contentmodel = gather_content('https://www.jinse.com/news/blockchain/417295.html')
        parser = News()
        result = parser.parse(contentmodel)
        self.assertEqual(result['page_url'], 'https://www.jinse.com/news/blockchain/417295.html')
        self.assertIsNotNone(result['infos'])
        
if __name__ == '__main__':
    unittest.main()
