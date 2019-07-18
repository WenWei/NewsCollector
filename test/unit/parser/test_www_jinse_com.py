import unittest
import sys

#sys.path.append('../NewsCollector')

print(__name__)

# import NewsCollector.parser#.www_jinse_com.home
# import sys
# sys.path.insert(0,'/path/to/cts_sap_polaris/lib')

from newscollector.parser.www_jinse_com import Home, News, Www_Jinse_Com


class TestWwwJinseCom(unittest.TestCase):
    def test_get_parsers(self):
        wjc = Www_Jinse_Com()
        parsers = wjc.get_parsers()
        self.assertGreaterEqual(len(parsers), 1)


class TestHome(unittest.TestCase):
    def test_is_match(self):
        """
        測試網址檢查
        """
        parser = Home()
        self.assertTrue(parser.is_match('https://www.jinse.com/blockchain/414531.html'))
        self.assertFalse(parser.is_match('https://www.jinse.com/blockchain/abcdef.html'))


class TestNews(unittest.TestCase):
    def test_is_match(self):
        """
        測試網址檢查
        """
        parser = News()
        self.assertTrue(parser.is_match('https://www.jinse.com/news/blockchain/414347.html'))
        self.assertFalse(parser.is_match('https://www.jinse.com/news/blockchain/abcdef.html'))

if __name__ == '__main__':
    unittest.main()
