import unittest
from utilities import sina_fin

# import utilities.sina_fin

class TestSinaFinanceApiClient(unittest.TestCase):
    def test_get_name(self):
        self.assertEqual("CHOW TAI FOOK", sina_fin.get_name("01929"))
        self.assertEqual("浦发银行", sina_fin.get_name("600000"))
        self.assertEqual("中青旅", sina_fin.get_name("600138"))
        self.assertEqual("洋河股份", sina_fin.get_name("002304"))
        self.assertEqual("长荣股份", sina_fin.get_name("300195"))
        self.assertEqual("恒中企A", sina_fin.get_name("150175"))
        self.assertEqual("华夏沪港通恒生ETF联接A", sina_fin.get_name("of000948"))

    def _get_price(self, testing_quote="600000", low=2, high=200):
        price = sina_fin.get_price(testing_quote)
        self.assertLess(float(price), high)
        self.assertGreater(float(price), low)

    def test_get_price(self):
        self._get_price("600000")
        self._get_price("002304")
        self._get_price("300195")
        self._get_price("01929")
        self._get_price("150175", 0.5, 2)
        self._get_price("of000948", 0.5, 3)