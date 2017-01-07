import unittest
from testfixtures import log_capture
from tktitler import (
    tk_prefix, tk_kprefix, tk_postfix, email,
    get_gfyear, set_gfyear,
    parse_relative, parse,
    PREFIXTYPE_NORMAL, PREFIXTYPE_UNICODE,
    POSTFIXTYPE_SINGLE, POSTFIXTYPE_DOUBLE, POSTFIXTYPE_SLASH,
    POSTFIXTYPE_LONGSLASH,
    EMAILTYPE_POSTFIX, EMAILTYPE_PREFIX,
)


class TestPrefixNormal(unittest.TestCase):

    def test_sameyear(self):
        self.assertEqual(tk_prefix(("CERM", 2016), 2016), "CERM")

    def test_year_minus_01(self):
        self.assertEqual(tk_prefix(("CERM", 2015), 2016), "GCERM")

    def test_year_minus_02(self):
        self.assertEqual(tk_prefix(("CERM", 2014), 2016), "BCERM")

    def test_year_minus_03(self):
        self.assertEqual(tk_prefix(("CERM", 2013), 2016), "OCERM")

    def test_year_minus_04(self):
        self.assertEqual(tk_prefix(("CERM", 2012), 2016), "TOCERM")

    def test_year_minus_05(self):
        self.assertEqual(tk_prefix(("CERM", 2011), 2016), "T2OCERM")

    def test_year_minus_15(self):
        self.assertEqual(tk_prefix(("CERM", 2001), 2016), "T12OCERM")

    def test_year_minus_36(self):
        self.assertEqual(tk_prefix(("CERM", 1980), 2016), "T33OCERM")

    def test_year_plus_1(self):
        self.assertEqual(tk_prefix(("CERM", 2017), 2016), "KCERM")

    def test_year_plus_2(self):
        self.assertEqual(tk_prefix(("CERM", 2018), 2016), "K2CERM")

    def test_year_plus_15(self):
        self.assertEqual(tk_prefix(("CERM", 2031), 2016), "K15CERM")

    def test_KASS(self):
        self.assertEqual(tk_prefix(("KASS", 2016), 2016), "KA$$")

    def test_FUSS(self):
        self.assertEqual(tk_prefix(("FUSS", 2016), 2016), "FUSS")

    def test_FUAEAE(self):
        self.assertEqual(tk_prefix(("FUÆÆ", 2016), 2016), "FUÆÆ")

    def test_FUOEOE(self):
        self.assertEqual(tk_prefix(("FUØØ", 2016), 2016), "FUØØ")

    def test_FUAAAA(self):
        self.assertEqual(tk_prefix(("FUÅÅ", 2016), 2016), "FUÅÅ")

    def test_empty(self):
        self.assertEqual(tk_prefix(("", 2016), 2016), "")

    def test_empty_minus_04(self):
        self.assertEqual(tk_prefix(("", 2012), 2016), "TO")

    def test_empty_minus_15(self):
        self.assertEqual(tk_prefix(("", 2001), 2016), "T12O")

    def test_longstring(self):
        self.assertEqual(tk_prefix(("This is a long string", 2012), 2016),
                         "TOThis is a long string")

    def test_explicit_type_plus_2(self):
        self.assertEqual(
            tk_prefix(("CERM", 2018), 2016, type=PREFIXTYPE_NORMAL), "K2CERM")

    def test_explicit_type_minus_15(self):
        self.assertEqual(
            tk_prefix(("CERM", 2001), 2016, type=PREFIXTYPE_NORMAL),
            "T12OCERM")

    def test_validation_root_int(self):
        with self.assertRaisesRegex(TypeError,
                                    "int is not a valid type for root."):
            tk_prefix((0, 2012), 2016)

    def test_validation_period_float(self):
        with self.assertRaisesRegex(TypeError,
                                    "float is not a valid type for period."):
            tk_prefix(("CERM", 2012.), 2016)

    def test_validation_period_string(self):
        with self.assertRaisesRegex(TypeError,
                                    "str is not a valid type for period."):
            tk_prefix(("CERM", '2012'), 2016)

    def test_validation_gfyear_string(self):
        with self.assertRaisesRegex(TypeError,
                                    "str is not a valid type for gfyear."):
            tk_prefix(("CERM", 2012), "2016")


class TestPrefixUnicode(unittest.TestCase):

    def test_sameyear(self):
        self.assertEqual(
            tk_prefix(("CERM", 2016), 2016, type=PREFIXTYPE_UNICODE), "CERM")

    def test_year_minus_01(self):
        self.assertEqual(
            tk_prefix(("CERM", 2015), 2016, type=PREFIXTYPE_UNICODE), "GCERM")

    def test_year_minus_05(self):
        self.assertEqual(
            tk_prefix(("CERM", 2011), 2016, type=PREFIXTYPE_UNICODE),
            "T²OCERM")

    def test_year_minus_13(self):
        self.assertEqual(
            tk_prefix(("CERM", 2003), 2016, type=PREFIXTYPE_UNICODE),
            "T¹⁰OCERM")

    def test_year_minus_36(self):
        self.assertEqual(
            tk_prefix(("CERM", 1980), 2016, type=PREFIXTYPE_UNICODE),
            "T³³OCERM")

    def test_year_plus_1(self):
        self.assertEqual(
            tk_prefix(("CERM", 2017), 2016, type=PREFIXTYPE_UNICODE), "KCERM")

    def test_year_plus_2(self):
        self.assertEqual(
            tk_prefix(("CERM", 2018), 2016, type=PREFIXTYPE_UNICODE), "K²CERM")

    def test_year_plus_15(self):
        self.assertEqual(
            tk_prefix(("CERM", 2031), 2016, type=PREFIXTYPE_UNICODE),
            "K¹⁵CERM")


class TestKprefix(unittest.TestCase):

    def test_sameyear(self):
        self.assertEqual(tk_kprefix(("CERM", 2016), 2016), "KGCERM")

    def test_year_minus_01(self):
        self.assertEqual(tk_kprefix(("CERM", 2015), 2016), "KBCERM")

    def test_year_minus_04(self):
        self.assertEqual(tk_kprefix(("CERM", 2012), 2016), "KT2OCERM")

    def test_year_minus_05(self):
        self.assertEqual(tk_kprefix(("CERM", 2011), 2016), "KT3OCERM")

    def test_year_plus_1(self):
        self.assertEqual(tk_kprefix(("CERM", 2017), 2016), "KCERM")

    def test_year_plus_2(self):
        self.assertEqual(tk_kprefix(("CERM", 2018), 2016), "K2CERM")

    def test_unicode_year_minus_05(self):
        self.assertEqual(
            tk_kprefix(("CERM", 2011), 2016, type=PREFIXTYPE_UNICODE),
            "KT³OCERM")


class TestPostfix(unittest.TestCase):

    def test_notype(self):
        self.assertEqual(tk_postfix(("CERM", 2016)), "CERM16")

    def test_explicit_type(self):
        self.assertEqual(tk_postfix(("CERM", 2016), type=POSTFIXTYPE_SINGLE),
                         "CERM16")

    def test_double(self):
        self.assertEqual(tk_postfix(("CERM", 2016), type=POSTFIXTYPE_DOUBLE),
                         "CERM1617")

    def test_slash(self):
        self.assertEqual(tk_postfix(("CERM", 2016), type=POSTFIXTYPE_SLASH),
                         "CERM 16/17")

    def test_longslash(self):
        self.assertEqual(
            tk_postfix(("CERM", 2016), type=POSTFIXTYPE_LONGSLASH),
            "CERM 2016/17")


class TestEmail(unittest.TestCase):

    def test_notype(self):
        self.assertEqual(email(("CERM", 2011), 2016), "CERM11")

    def test_AE(self):
        self.assertEqual(email(("FUHÆ", 2011), 2016), "FUHAE11")

    def test_OE(self):
        self.assertEqual(email(("FUHØ", 2011), 2016), "FUHOE11")

    def test_AAAA(self):
        self.assertEqual(email(("FUÅÅ", 2011), 2016), "FUAAAA11")

    def test_aa(self):
        self.assertEqual(email(("fuhå", 2011), 2016), "fuhaa11")

    def test_postfix(self):
        self.assertEqual(email(("FUHØ", 2011), 2016,  type=EMAILTYPE_POSTFIX),
                         "FUHOE11")

    def test_prefix(self):
        self.assertEqual(email(("FUHØ", 2011), 2016,  type=EMAILTYPE_PREFIX),
                         "T2OFUHOE")


class TestOverride(unittest.TestCase):

    def test_decorator(self):
        self.assertEqual(set_gfyear(2013)(get_gfyear)(), 2013)

    def test_context_manager(self):
        with set_gfyear(2012):
            self.assertEqual(get_gfyear(), 2012)

    def test_reentrant(self):
        with set_gfyear(2011):
            self.assertEqual(get_gfyear(), 2011)
            with set_gfyear(2012):
                self.assertEqual(get_gfyear(), 2012)
            self.assertEqual(get_gfyear(), 2011)

    def test_prefix(self):
        with set_gfyear(2015):
            self.assertEqual(tk_prefix(('CERM', 2014)), 'GCERM')

    def test_kprefix(self):
        with set_gfyear(2015):
            self.assertEqual(tk_kprefix(('CERM', 2014)), 'KBCERM')

    def test_postfix(self):
        with set_gfyear(2015):
            self.assertEqual(tk_postfix(('CERM', 2014)), 'CERM14')


class TestParseRelative(unittest.TestCase):

    def test_relative_current(self):
        self.assertEqual(parse_relative('FORM'), (0, 'FORM', None))

    def test_simple_prefix(self):
        self.assertEqual(parse_relative('GFORM'), (1, 'FORM', None))

    def test_multi_prefix(self):
        self.assertEqual(parse_relative('BTKFORM'), (2, 'FORM', None))

    def test_exponent(self):
        self.assertEqual(parse_relative('OT2OFORM'), (8, 'FORM', None))

    def test_short_postfix(self):
        self.assertEqual(parse_relative('OT2OFORM16'), (8, 'FORM', 2016))

    def test_long_postfix(self):
        self.assertEqual(parse_relative('FORM1516'), (0, 'FORM', 2015))

    def test_full_postfix(self):
        self.assertEqual(parse_relative('FORM2015'), (0, 'FORM', 2015))

    def test_fu(self):
        self.assertEqual(parse_relative('GFU14'), (1, 'FU', 2014))

    def test_fu_int(self):
        self.assertEqual(parse_relative('GFUOEAE14'), (1, 'FUOEAE', 2014))

    def test_lower(self):
        self.assertEqual(parse_relative('gfuoeae14'), (1, 'FUOEAE', 2014))

    def test_unicode_superscript(self):
        self.assertEqual(parse_relative('T²OFORM'), (5, 'FORM', None))

    def test_kass_dollar(self):
        self.assertEqual(parse_relative('GKA$$'), (1, 'KASS', None))

    def test_kass_funny(self):
        self.assertEqual(parse_relative('GKA$\N{POUND SIGN}'),
                         (1, 'KASS', None))

    def test_cerm_funny(self):
        self.assertEqual(parse_relative('\N{DOUBLE-STRUCK CAPITAL C}ERM'),
                         (0, 'CERM', None))

    def test_unknown(self):
        self.assertEqual(parse_relative('OABEN'),
                         (3, 'ABEN', None))

    def test_prefix(self):
        self.assertEqual(parse_relative('G12'), (12, '', None))

    def test_postfix(self):
        self.assertEqual(parse_relative('12'), (0, '', 2012))

    def test_bestfu(self):
        self.assertEqual(parse_relative('BESTFU'), (0, 'BESTFU', None))

    @log_capture()
    def test_2021(self, l):
        self.assertEqual(parse_relative('FORM2021'), (0, 'FORM', 2020))

        l.check(
            ('tktitler', 'WARNING', 'While parsing an alias, the technically '
             'ambiguous postfix 2021 was met. It it assumed it means '
             '2020/2021.')
        )


class TestParse(unittest.TestCase):

    def test_arg(self):
        self.assertEqual(parse('FORM', 2016), ('FORM', 2016))

    def test_context(self):
        with set_gfyear(2013):
            self.assertEqual(parse('FORM'), ('FORM', 2013))

    def test_prefix_minus_1(self):
        with set_gfyear(2013):
            self.assertEqual(parse('GFORM'), ('FORM', 2012))

    def test_prefix_minus_2(self):
        with set_gfyear(2013):
            self.assertEqual(parse('BFORM'), ('FORM', 2011))

    def test_prefix_minus_3(self):
        with set_gfyear(2013):
            self.assertEqual(parse('OFORM'), ('FORM', 2010))

    def test_prefix_minus_4(self):
        with set_gfyear(2013):
            self.assertEqual(parse('TOFORM'), ('FORM', 2009))

    def test_prefix_minus_5(self):
        with set_gfyear(2013):
            self.assertEqual(parse('T2OFORM'), ('FORM', 2008))

    def test_prefix_minus_35(self):
        with set_gfyear(2013):
            self.assertEqual(parse('T32OFORM'), ('FORM', 1978))

    def test_prefix_unicode_minus_5(self):
        with set_gfyear(2013):
            self.assertEqual(parse('T²OFORM'), ('FORM', 2008))

    def test_prefix_unicode_minus_35(self):
        with set_gfyear(2013):
            self.assertEqual(parse('T³²OFORM'), ('FORM', 1978))

    def test_prefix_plus_1(self):
        with set_gfyear(2013):
            self.assertEqual(parse('KFORM'), ('FORM', 2014))

    def test_prefix_plus_3(self):
        with set_gfyear(2013):
            self.assertEqual(parse('K3FORM'), ('FORM', 2016))

    def test_prefix_unicode_plus_3(self):
        with set_gfyear(2013):
            self.assertEqual(parse('K³FORM'), ('FORM', 2016))

    def test_prefix_unicode_combined_1(self):
        with set_gfyear(2013):
            self.assertEqual(parse('OK³FORM'), ('FORM', 2013))

    def test_prefix_unicode_combined_2(self):
        with set_gfyear(2013):
            self.assertEqual(parse('T2OK³FORM'), ('FORM', 2011))

    def test_postfix_short(self):
        with set_gfyear(2013):
            self.assertEqual(parse('FORM16'), ('FORM', 2016))

    def test_postfix_double(self):
        with set_gfyear(2013):
            self.assertEqual(parse('FORM1617'), ('FORM', 2016))

    def test_postfix_long(self):
        with set_gfyear(2013):
            self.assertEqual(parse('FORM2016'), ('FORM', 2016))

    def test_postfix_slash(self):
        with set_gfyear(2013):
            self.assertEqual(parse('FORM16/17'), ('FORM', 2016))

    def test_postfix_longslash(self):
        with set_gfyear(2013):
            self.assertEqual(parse('FORM2016/17'), ('FORM', 2016))

    def test_postfix_reallylongslash(self):
        with set_gfyear(2013):
            self.assertEqual(parse('FORM2016/2017'), ('FORM', 2016))

    def test_postfix_2021_long(self):
        with set_gfyear(2013):
            self.assertEqual(parse('FORM2021'), ('FORM', 2020))

    def test_postfix_2021_slash(self):
        with set_gfyear(2013):
            self.assertEqual(parse('FORM20/21'), ('FORM', 2020))


if __name__ == '__main__':
    unittest.main()
