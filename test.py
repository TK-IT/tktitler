import unittest
from tktitler import prefix, PREFIXTYPE_NORMAL, PREFIXTYPE_UNICODE


class TestPrefixNormal(unittest.TestCase):

    def test_sameyear(self):
        self.assertEqual(prefix(("CERM", 2016), 2016), "CERM")

    def test_year_minus_01(self):
        self.assertEqual(prefix(("CERM", 2015), 2016), "GCERM")

    def test_year_minus_02(self):
        self.assertEqual(prefix(("CERM", 2014), 2016), "BCERM")

    def test_year_minus_03(self):
        self.assertEqual(prefix(("CERM", 2013), 2016), "OCERM")

    def test_year_minus_04(self):
        self.assertEqual(prefix(("CERM", 2012), 2016), "TOCERM")

    def test_year_minus_05(self):
        self.assertEqual(prefix(("CERM", 2011), 2016), "T2OCERM")

    def test_year_minus_15(self):
        self.assertEqual(prefix(("CERM", 2001), 2016), "T12OCERM")

    def test_year_minus_36(self):
        self.assertEqual(prefix(("CERM", 1980), 2016), "T33OCERM")

    def test_year_plus_1(self):
        self.assertEqual(prefix(("CERM", 2017), 2016), "KCERM")

    def test_year_plus_2(self):
        self.assertEqual(prefix(("CERM", 2018), 2016), "K2CERM")

    def test_year_plus_15(self):
        self.assertEqual(prefix(("CERM", 2031), 2016), "K15CERM")

    def test_KASS(self):
        self.assertEqual(prefix(("KASS", 2016), 2016), "KA$$")

    def test_FUSS(self):
        self.assertEqual(prefix(("FUSS", 2016), 2016), "FUSS")

    def test_FUAEAE(self):
        self.assertEqual(prefix(("FUÆÆ", 2016), 2016), "FUÆÆ")

    def test_FUOEOE(self):
        self.assertEqual(prefix(("FUØØ", 2016), 2016), "FUØØ")

    def test_FUAAAA(self):
        self.assertEqual(prefix(("FUÅÅ", 2016), 2016), "FUÅÅ")

    def test_empty(self):
        self.assertEqual(prefix(("", 2016), 2016), "")

    def test_empty_minus_04(self):
        self.assertEqual(prefix(("", 2012), 2016), "TO")

    def test_empty_minus_15(self):
        self.assertEqual(prefix(("", 2001), 2016), "T12O")

    def test_longstring(self):
        self.assertEqual(prefix(("This is a quite long string", 2012), 2016),
                         "TOThis is a quite long string")


class TestPrefixUnicode(unittest.TestCase):

    def test_sameyear(self):
        self.assertEqual(prefix(("CERM", 2016), 2016, type=PREFIXTYPE_UNICODE),
                         "CERM")

    def test_year_minus_01(self):
        self.assertEqual(prefix(("CERM", 2015), 2016, type=PREFIXTYPE_UNICODE),
                         "GCERM")

    def test_year_minus_05(self):
        self.assertEqual(prefix(("CERM", 2011), 2016, type=PREFIXTYPE_UNICODE),
                         "T²OCERM")

    def test_year_minus_13(self):
        self.assertEqual(prefix(("CERM", 2003), 2016, type=PREFIXTYPE_UNICODE),
                         "T¹⁰OCERM")

    def test_year_minus_36(self):
        self.assertEqual(prefix(("CERM", 1980), 2016, type=PREFIXTYPE_UNICODE),
                         "T³³OCERM")

    def test_year_plus_1(self):
        self.assertEqual(prefix(("CERM", 2017), 2016, type=PREFIXTYPE_UNICODE),
                         "KCERM")

    def test_year_plus_2(self):
        self.assertEqual(prefix(("CERM", 2018), 2016, type=PREFIXTYPE_UNICODE),
                         "K²CERM")

    def test_year_plus_15(self):
        self.assertEqual(prefix(("CERM", 2031), 2016, type=PREFIXTYPE_UNICODE),
                         "K¹⁵CERM")
if __name__ == '__main__':
    unittest.main()
