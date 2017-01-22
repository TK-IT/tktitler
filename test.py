import unittest
from testfixtures import log_capture
import tktitler as tk


class TestPrefixNormal(unittest.TestCase):

    def test_sameyear(self):
        self.assertEqual(tk.prefix(("CERM", 2016), 2016), "CERM")

    def test_year_minus_01(self):
        self.assertEqual(tk.prefix(("CERM", 2015), 2016), "GCERM")

    def test_year_minus_02(self):
        self.assertEqual(tk.prefix(("CERM", 2014), 2016), "BCERM")

    def test_year_minus_03(self):
        self.assertEqual(tk.prefix(("CERM", 2013), 2016), "OCERM")

    def test_year_minus_04(self):
        self.assertEqual(tk.prefix(("CERM", 2012), 2016), "TOCERM")

    def test_year_minus_05(self):
        self.assertEqual(tk.prefix(("CERM", 2011), 2016), "T2OCERM")

    def test_year_minus_15(self):
        self.assertEqual(tk.prefix(("CERM", 2001), 2016), "T12OCERM")

    def test_year_minus_36(self):
        self.assertEqual(tk.prefix(("CERM", 1980), 2016), "T33OCERM")

    def test_year_plus_1(self):
        self.assertEqual(tk.prefix(("CERM", 2017), 2016), "KCERM")

    def test_year_plus_2(self):
        self.assertEqual(tk.prefix(("CERM", 2018), 2016), "K2CERM")

    def test_year_plus_15(self):
        self.assertEqual(tk.prefix(("CERM", 2031), 2016), "K15CERM")

    def test_KASS(self):
        self.assertEqual(tk.prefix(("KASS", 2016), 2016), "KA$$")

    def test_FUSS(self):
        self.assertEqual(tk.prefix(("FUSS", 2016), 2016), "FUSS")

    def test_FUAEAE(self):
        self.assertEqual(tk.prefix(("FUÆÆ", 2016), 2016), "FUÆÆ")

    def test_FUOEOE(self):
        self.assertEqual(tk.prefix(("FUØØ", 2016), 2016), "FUØØ")

    def test_FUAAAA(self):
        self.assertEqual(tk.prefix(("FUÅÅ", 2016), 2016), "FUÅÅ")

    def test_empty(self):
        self.assertEqual(tk.prefix(("", 2016), 2016), "")

    def test_empty_minus_04(self):
        self.assertEqual(tk.prefix(("", 2012), 2016), "TO")

    def test_empty_minus_15(self):
        self.assertEqual(tk.prefix(("", 2001), 2016), "T12O")

    def test_longstring(self):
        self.assertEqual(tk.prefix(("This is a long string", 2012), 2016),
                         "TOThis is a long string")

    def test_explicit_type_plus_2(self):
        self.assertEqual(
            tk.prefix(("CERM", 2018), 2016, type='normal'),
            "K2CERM")

    def test_explicit_type_minus_15(self):
        self.assertEqual(
            tk.prefix(("CERM", 2001), 2016, type='normal'),
            "T12OCERM")

    def test_validation_root_int(self):
        with self.assertRaisesRegex(TypeError,
                                    "int is not a valid type for root."):
            tk.prefix((0, 2012), 2016)

    def test_validation_period_float(self):
        with self.assertRaisesRegex(TypeError,
                                    "float is not a valid type for period."):
            tk.prefix(("CERM", 2012.), 2016)

    def test_validation_period_string(self):
        with self.assertRaisesRegex(TypeError,
                                    "str is not a valid type for period."):
            tk.prefix(("CERM", '2012'), 2016)

    def test_validation_gfyear_string(self):
        with self.assertRaisesRegex(TypeError,
                                    "str is not a valid type for gfyear."):
            tk.prefix(("CERM", 2012), "2016")

    def test_invalid_type(self):
        with self.assertRaisesRegex(
                ValueError,
                "'somestring' is not a valid type-parameter"):
            tk.prefix(("CERM", 2001), 2016, type="somestring")

    def test_invalid_title_root(self):
        with self.assertRaisesRegex(
                TypeError,
                "int is not a valid type for root."):
            tk.prefix((1, 2001), 2016)

    def test_invalid_title_period(self):
        with self.assertRaisesRegex(
                TypeError,
                "str is not a valid type for period."):
            tk.prefix(("CERM", "2001"), 2016)

    def test_invalid_title_period_len(self):
        with self.assertRaisesRegex(
                ValueError,
                "'20010' is not a valid period"):
            tk.prefix(("CERM", 20010), 2016)


class TestPrefixUnicode(unittest.TestCase):

    def test_sameyear(self):
        self.assertEqual(
            tk.prefix(("CERM", 2016), 2016, type='unicode'),
            "CERM")

    def test_year_minus_01(self):
        self.assertEqual(
            tk.prefix(("CERM", 2015), 2016, type='unicode'),
            "GCERM")

    def test_year_minus_05(self):
        self.assertEqual(
            tk.prefix(("CERM", 2011), 2016, type='unicode'),
            "T²OCERM")

    def test_year_minus_13(self):
        self.assertEqual(
            tk.prefix(("CERM", 2003), 2016, type='unicode'),
            "T¹⁰OCERM")

    def test_year_minus_36(self):
        self.assertEqual(
            tk.prefix(("CERM", 1980), 2016, type='unicode'),
            "T³³OCERM")

    def test_year_plus_1(self):
        self.assertEqual(
            tk.prefix(("CERM", 2017), 2016, type='unicode'),
            "KCERM")

    def test_year_plus_2(self):
        self.assertEqual(
            tk.prefix(("CERM", 2018), 2016, type='unicode'),
            "K²CERM")

    def test_year_plus_15(self):
        self.assertEqual(
            tk.prefix(("CERM", 2031), 2016, type='unicode'),
            "K¹⁵CERM")


class TestKprefix(unittest.TestCase):

    def test_sameyear(self):
        self.assertEqual(tk.kprefix(("CERM", 2016), 2016), "KGCERM")

    def test_year_minus_01(self):
        self.assertEqual(tk.kprefix(("CERM", 2015), 2016), "KBCERM")

    def test_year_minus_04(self):
        self.assertEqual(tk.kprefix(("CERM", 2012), 2016), "KT2OCERM")

    def test_year_minus_05(self):
        self.assertEqual(tk.kprefix(("CERM", 2011), 2016), "KT3OCERM")

    def test_year_plus_1(self):
        self.assertEqual(tk.kprefix(("CERM", 2017), 2016), "KCERM")

    def test_year_plus_2(self):
        self.assertEqual(tk.kprefix(("CERM", 2018), 2016), "K2CERM")

    def test_unicode_year_minus_05(self):
        self.assertEqual(
            tk.kprefix(("CERM", 2011), 2016, type='unicode'),
            "KT³OCERM")


class TestPostfix(unittest.TestCase):

    def test_notype(self):
        self.assertEqual(tk.postfix(("CERM", 2016)), "CERM16")

    def test_explicit_type(self):
        self.assertEqual(
            tk.postfix(("CERM", 2016), type='single'),
            "CERM16")

    def test_double(self):
        self.assertEqual(
            tk.postfix(("CERM", 2016), type='double'),
            "CERM1617")

    def test_slash(self):
        self.assertEqual(tk.postfix(("CERM", 2016), type='slash'),
                         "CERM 16/17")

    def test_longslash(self):
        self.assertEqual(
            tk.postfix(("CERM", 2016), type='longslash'),
            "CERM 2016/17")

    def test_empty_slash(self):
        self.assertEqual(tk.postfix(("", 2016), type='slash'),
                         "16/17")

    def test_empty_longslash(self):
        self.assertEqual(
            tk.postfix(("", 2016), type='longslash'),
            "2016/17")

    @log_capture()
    def test_EFUIT(self, l):
        self.assertEqual(tk.postfix(("EFUIT", 2016)), "EFUIT16")
        l.check(
            ('tktitler', 'WARNING', 'Returning an EFUIT postfix. The postfix '
             'does not necessarily represent the actual year the given EFUIT '
             'was EFUIT.')
        )

    @log_capture()
    def test_old_title(self, l):
        self.assertEqual(tk.postfix(("BEST", 1957)), "BEST57")
        l.check(
            ('tktitler', 'WARNING', 'Returning a postfix from before 1959. '
             'The postfix does not necessarily represent the actual year the '
             'given BEST was BEST.')
        )

    def test_invalid_type(self):
        with self.assertRaisesRegex(
                ValueError,
                "'somestring' is not a valid type-parameter"):
            tk.postfix(("CERM", 2001), type="somestring")


class TestPrepostfix(unittest.TestCase):

    def test_sameyear(self):
        self.assertEqual(tk.prepostfix(("CERM", 2016), 2016),
                         "CERM 2016/17")

    def test_year_minus_05(self):
        self.assertEqual(tk.prepostfix(("CERM", 2011), 2016),
                         "T2OCERM 2011/12")

    def test_year_plus_03(self):
        self.assertEqual(tk.prepostfix(("CERM", 2019), 2016),
                         "K3CERM 2019/20")

    def test_EFUIT(self):
        self.assertEqual(tk.prepostfix(("EFUIT", 2011), 2016),
                         "T2OEFUIT")

    def test_old_title(self):
        self.assertEqual(tk.prepostfix(("BEST", 1957), 2016),
                         "T56OBEST")


class TestEmail(unittest.TestCase):

    def test_notype(self):
        self.assertEqual(tk.email(("CERM", 2011), 2016), "CERM11")

    def test_AE(self):
        self.assertEqual(tk.email(("FUHÆ", 2011), 2016), "FUHAE11")

    def test_OE(self):
        self.assertEqual(tk.email(("FUHØ", 2011), 2016), "FUHOE11")

    def test_AAAA(self):
        self.assertEqual(tk.email(("FUÅÅ", 2011), 2016), "FUAAAA11")

    def test_aa(self):
        self.assertEqual(tk.email(("fuhå", 2011), 2016), "FUHAA11")

    def test_KASS(self):
        self.assertEqual(tk.email(("KA$$", 2011), 2016), "KASS11")

    def test_postfix(self):
        self.assertEqual(
            tk.email(("FUHØ", 2011), 2016, type='postfix'),
            "FUHOE11")

    def test_prefix(self):
        self.assertEqual(
            tk.email(("FUHØ", 2011), 2016, type='prefix'),
            "T2OFUHOE")

    @log_capture()
    def test_EFUIT(self, l):
        self.assertEqual(tk.email(("EFUIT", 2016), 2016), "EFUIT16")
        l.check(
            ('tktitler', 'WARNING', 'Returning an EFUIT email with postfix. '
             'The postfix does not necessarily represent the actual year the '
             'given EFUIT was EFUIT.')
        )

    @log_capture()
    def test_old_title(self, l):
        self.assertEqual(tk.email(("BEST", 1957), 2016), "BEST57")
        l.check(
            ('tktitler', 'WARNING', 'Returning an email from before 1959 '
             'with postfix. The postfix does not necessarily represent the '
             'actual year the given BEST was BEST.')
        )

    @log_capture()
    def test_EFUIT_pre(self, l):
        self.assertEqual(
            tk.email(("EFUIT", 2016), 2016, type='prefix'),
            "EFUIT")
        l.check()

    @log_capture()
    def test_old_title_pre(self, l):
        self.assertEqual(
            tk.email(("BEST", 1957), 2016, type='prefix'),
            "T56OBEST")
        l.check()

    def test_invalid_type(self):
        with self.assertRaisesRegex(
                ValueError,
                "'somestring' is not a valid type-parameter"):
            tk.email(("CERM", 2001), 2016, type="somestring")


class TestOverride(unittest.TestCase):

    def test_decorator(self):
        self.assertEqual(tk.set_gfyear(2013)(tk.get_gfyear)(), 2013)

    def test_context_manager(self):
        with tk.set_gfyear(2012):
            self.assertEqual(tk.get_gfyear(), 2012)

    def test_reentrant(self):
        with tk.set_gfyear(2011):
            self.assertEqual(tk.get_gfyear(), 2011)
            with tk.set_gfyear(2012):
                self.assertEqual(tk.get_gfyear(), 2012)
            self.assertEqual(tk.get_gfyear(), 2011)

    def test_prefix(self):
        with tk.set_gfyear(2015):
            self.assertEqual(tk.prefix(('CERM', 2014)), 'GCERM')

    def test_kprefix(self):
        with tk.set_gfyear(2015):
            self.assertEqual(tk.kprefix(('CERM', 2014)), 'KBCERM')

    def test_postfix(self):
        with tk.set_gfyear(2015):
            self.assertEqual(tk.postfix(('CERM', 2014)), 'CERM14')

    def test_notset(self):
        with self.assertRaisesRegex(
                ValueError,
                "No context gfyear set. Use the gfyear argument or "
                "set_gfyear."):
            tk.get_gfyear()

    def test_invalid_gfyear(self):
        with self.assertRaisesRegex(
                ValueError,
                "'12345' is not a valid gfyear"):
            tk.get_gfyear(12345)


class TestParseRelative(unittest.TestCase):

    def test_relative_current(self):
        self.assertEqual(tk._parse_relative('FORM'), (0, 'FORM', None))

    def test_simple_prefix(self):
        self.assertEqual(tk._parse_relative('GFORM'), (1, 'FORM', None))

    def test_multi_prefix(self):
        self.assertEqual(tk._parse_relative('BTOKFORM'), (5, 'FORM', None))

    def test_bent(self):
        self.assertEqual(tk._parse_relative('TVC02'), (0, 'TVC', 2002))

    def test_temp_title(self):
        self.assertEqual(tk._parse_relative('BTFORM'), (2, 'TFORM', None))

    def test_t_before_k(self):
        self.assertEqual(tk._parse_relative('TKFORM'), (0, 'TKFORM', None))

    def test_t_before_g(self):
        self.assertEqual(tk._parse_relative('TGFORM'), (0, 'TGFORM', None))

    def test_t_before_b(self):
        self.assertEqual(tk._parse_relative('TBFORM'), (0, 'TBFORM', None))

    def test_t3_before_b(self):
        self.assertEqual(tk._parse_relative('T3BFORM'), (0, 'T3BFORM', None))

    def test_exponent(self):
        self.assertEqual(tk._parse_relative('OT2OFORM'), (8, 'FORM', None))

    def test_short_postfix(self):
        self.assertEqual(tk._parse_relative('OT2OFORM16'), (8, 'FORM', 2016))

    def test_long_postfix(self):
        self.assertEqual(tk._parse_relative('FORM1516'), (0, 'FORM', 2015))

    def test_full_postfix(self):
        self.assertEqual(tk._parse_relative('FORM2015'), (0, 'FORM', 2015))

    def test_fu(self):
        self.assertEqual(tk._parse_relative('GFU14'), (1, 'FU', 2014))

    def test_fu_int(self):
        self.assertEqual(tk._parse_relative('GFUOEAE14'), (1, 'FUØÆ', 2014))

    def test_lower(self):
        self.assertEqual(tk._parse_relative('gfuoeae14'), (1, 'FUØÆ', 2014))

    def test_unicode_superscript(self):
        self.assertEqual(tk._parse_relative('T²OFORM'), (5, 'FORM', None))

    def test_kass_dollar(self):
        self.assertEqual(tk._parse_relative('GKA$$'), (1, 'KASS', None))

    def test_kass_funny(self):
        self.assertEqual(tk._parse_relative('GKA$\N{POUND SIGN}'),
                         (1, 'KASS', None))

    def test_cerm_funny(self):
        self.assertEqual(tk._parse_relative('\N{DOUBLE-STRUCK CAPITAL C}ERM'),
                         (0, 'CERM', None))

    def test_unknown(self):
        self.assertEqual(tk._parse_relative('OABEN'),
                         (3, 'ABEN', None))

    def test_prefix(self):
        self.assertEqual(tk._parse_relative('G12'), (12, '', None))

    def test_postfix(self):
        self.assertEqual(tk._parse_relative('12'), (0, '', 2012))

    def test_bestfu(self):
        self.assertEqual(tk._parse_relative('BESTFU'), (0, 'BESTFU', None))

    @log_capture()
    def test_2021(self, l):
        self.assertEqual(tk._parse_relative('FORM2021'), (0, 'FORM', 2020))

        l.check(
            ('tktitler', 'WARNING', 'While parsing an alias, the technically '
             'ambiguous postfix 2021 was met. It it assumed it means '
             '2020/2021.')
        )

    @log_capture()
    def test_2021_slash(self, l):
        self.assertEqual(tk._parse_relative('FORM20/21'), (0, 'FORM', 2020))
        l.check()

    def test_invalid_slash(self):
        with self.assertRaises(ValueError):
            tk._parse_relative('FORM1/314')


class TestParse(unittest.TestCase):

    def test_arg(self):
        self.assertEqual(tk.parse('FORM', 2016), ('FORM', 2016))

    def test_context(self):
        with tk.set_gfyear(2013):
            self.assertEqual(tk.parse('FORM'), ('FORM', 2013))

    def test_prefix_minus_1(self):
        with tk.set_gfyear(2013):
            self.assertEqual(tk.parse('GFORM'), ('FORM', 2012))

    def test_prefix_minus_2(self):
        with tk.set_gfyear(2013):
            self.assertEqual(tk.parse('BFORM'), ('FORM', 2011))

    def test_prefix_minus_3(self):
        with tk.set_gfyear(2013):
            self.assertEqual(tk.parse('OFORM'), ('FORM', 2010))

    def test_prefix_minus_4(self):
        with tk.set_gfyear(2013):
            self.assertEqual(tk.parse('TOFORM'), ('FORM', 2009))

    def test_prefix_minus_5(self):
        with tk.set_gfyear(2013):
            self.assertEqual(tk.parse('T2OFORM'), ('FORM', 2008))

    def test_prefix_minus_35(self):
        with tk.set_gfyear(2013):
            self.assertEqual(tk.parse('T32OFORM'), ('FORM', 1978))

    def test_prefix_unicode_minus_5(self):
        with tk.set_gfyear(2013):
            self.assertEqual(tk.parse('T²OFORM'), ('FORM', 2008))

    def test_prefix_unicode_minus_35(self):
        with tk.set_gfyear(2013):
            self.assertEqual(tk.parse('T³²OFORM'), ('FORM', 1978))

    def test_prefix_plus_1(self):
        with tk.set_gfyear(2013):
            self.assertEqual(tk.parse('KFORM'), ('FORM', 2014))

    def test_prefix_plus_3(self):
        with tk.set_gfyear(2013):
            self.assertEqual(tk.parse('K3FORM'), ('FORM', 2016))

    def test_prefix_unicode_plus_3(self):
        with tk.set_gfyear(2013):
            self.assertEqual(tk.parse('K³FORM'), ('FORM', 2016))

    def test_prefix_unicode_combined_1(self):
        with tk.set_gfyear(2013):
            self.assertEqual(tk.parse('OK³FORM'), ('FORM', 2013))

    def test_prefix_unicode_combined_2(self):
        with tk.set_gfyear(2013):
            self.assertEqual(tk.parse('T2OK³FORM'), ('FORM', 2011))

    def test_postfix_short(self):
        with tk.set_gfyear(2013):
            self.assertEqual(tk.parse('FORM16'), ('FORM', 2016))

    def test_postfix_double(self):
        with tk.set_gfyear(2013):
            self.assertEqual(tk.parse('FORM1617'), ('FORM', 2016))

    def test_postfix_long(self):
        with tk.set_gfyear(2013):
            self.assertEqual(tk.parse('FORM2016'), ('FORM', 2016))

    def test_postfix_slash(self):
        with tk.set_gfyear(2013):
            self.assertEqual(tk.parse('FORM16/17'), ('FORM', 2016))

    def test_postfix_longslash(self):
        with tk.set_gfyear(2013):
            self.assertEqual(tk.parse('FORM2016/17'), ('FORM', 2016))

    def test_postfix_reallylongslash(self):
        with tk.set_gfyear(2013):
            self.assertEqual(tk.parse('FORM2016/2017'), ('FORM', 2016))

    def test_postfix_2021_long(self):
        with tk.set_gfyear(2013):
            self.assertEqual(tk.parse('FORM2021'), ('FORM', 2020))

    def test_postfix_2021_slash(self):
        with tk.set_gfyear(2013):
            self.assertEqual(tk.parse('FORM20/21'), ('FORM', 2020))

    def test_postfix_space(self):
        with tk.set_gfyear(2013):
            self.assertEqual(tk.parse('FORM 1617'), ('FORM', 2016))

    def test_postfix_slash_space(self):
        with tk.set_gfyear(2013):
            self.assertEqual(tk.parse('FORM 16/17'), ('FORM', 2016))

    def test_postfix_longslash_space(self):
        with tk.set_gfyear(2013):
            self.assertEqual(tk.parse('FORM 2016/17'), ('FORM', 2016))

    def test_prefix_trailingspace(self):
        with tk.set_gfyear(2013):
            self.assertEqual(tk.parse('T2OFORM '), ('FORM', 2008))

    def test_postfix_trailingspace(self):
        with tk.set_gfyear(2013):
            self.assertEqual(tk.parse('FORM1617 '), ('FORM', 2016))

    def test_postfix_trailingspace_space(self):
        with tk.set_gfyear(2013):
            self.assertEqual(tk.parse('FORM 1617 '), ('FORM', 2016))

    def test_prefix_leadingspace(self):
        with tk.set_gfyear(2013):
            self.assertEqual(tk.parse(' T2OFORM'), ('FORM', 2008))

    def test_postfix_leadingspace(self):
        with tk.set_gfyear(2013):
            self.assertEqual(tk.parse(' FORM1617'), ('FORM', 2016))

    def test_postfix_leadingspace_space(self):
        with tk.set_gfyear(2013):
            self.assertEqual(tk.parse(' FORM 1617'), ('FORM', 2016))

    def test_postfix_bestfu(self):
        with tk.set_gfyear(2013):
            self.assertEqual(tk.parse('BESTFU16'), ('BESTFU', 2016))

    def test_postfix_bestfuslash(self):
        with tk.set_gfyear(2013):
            self.assertEqual(tk.parse('BEST/FU16'), ('BESTFU', 2016))

    def test_prefix_bestfu(self):
        with tk.set_gfyear(2013):
            self.assertEqual(tk.parse('BBESTFU'), ('BESTFU', 2011))

    def test_prefix_bestfuslash(self):
        with tk.set_gfyear(2013):
            self.assertEqual(tk.parse('BBEST/FU'), ('BESTFU', 2011))

    def test_AE_1(self):
        with tk.set_gfyear(2013):
            self.assertEqual(tk.parse('FUAE11'), ('FUAE', 2011))

    def test_AE_2(self):
        with tk.set_gfyear(2013):
            self.assertEqual(tk.parse('FUHAE11'), ('FUHÆ', 2011))

    def test_AE_3(self):
        with tk.set_gfyear(2013):
            self.assertEqual(tk.parse('FUAEH11'), ('FUÆH', 2011))

    def test_OE_1(self):
        with tk.set_gfyear(2013):
            self.assertEqual(tk.parse('FUOE11'), ('FUOE', 2011))

    def test_OE_2(self):
        with tk.set_gfyear(2013):
            self.assertEqual(tk.parse('FUHOE11'), ('FUHØ', 2011))

    def test_OE_3(self):
        with tk.set_gfyear(2013):
            self.assertEqual(tk.parse('FUOEH11'), ('FUØH', 2011))

    def test_AA_1(self):
        with tk.set_gfyear(2013):
            self.assertEqual(tk.parse('FUAA11'), ('FUAA', 2011))

    def test_AA_2(self):
        with tk.set_gfyear(2013):
            self.assertEqual(tk.parse('FUHAA11'), ('FUHÅ', 2011))

    def test_AA_3(self):
        with tk.set_gfyear(2013):
            self.assertEqual(tk.parse('FUAAH11'), ('FUÅH', 2011))

    def test_OEAA(self):
        with tk.set_gfyear(2013):
            self.assertEqual(tk.parse('FUOEAA11'), ('FUØÅ', 2011))

    def test_AAAA(self):
        with tk.set_gfyear(2013):
            self.assertEqual(tk.parse('FUAAAA11'), ('FUÅÅ', 2011))

    def test_AAA(self):
        with tk.set_gfyear(2013):
            with self.assertRaisesRegex(ValueError,
                                        "FUAAA is an ambiguous alias. Cannot "
                                        "normalize."):
                tk.parse('FUAAA11')

    def test_AAE(self):
        with tk.set_gfyear(2013):
            with self.assertRaisesRegex(ValueError,
                                        "FUAAE is an ambiguous alias. Cannot "
                                        "normalize."):
                tk.parse('FUAAE11')


class TestTitleRegister(unittest.TestCase):

    def setUp(self):
        @tk.title_class
        class FormTitle:
            def __init__(self, period):
                self.period = period

            def title_tuple(self):
                return ('FORM', self.period)

        self.form = FormTitle

    def test_prefix(self):
        self.assertEqual(tk.prefix(self.form(2013), 2016), 'OFORM')

    def test_kprefix(self):
        self.assertEqual(tk.kprefix(self.form(2014), 2016), 'KOFORM')

    def test_postfix(self):
        self.assertEqual(tk.postfix(self.form(2015)), 'FORM15')

    def test_prepostfix(self):
        self.assertEqual(tk.prepostfix(self.form(2015), 2016), 'GFORM 2015/16')


class TestTex(unittest.TestCase):

    def test_current(self):
        self.assertEqual(
            tk.prefix(('FORM', 2016), 2016, type='tex'),
            'FORM')

    def test_simple_old(self):
        self.assertEqual(
            tk.prefix(('FORM', 2012), 2016, type='tex'),
            'TOFORM')

    def test_simple_future(self):
        self.assertEqual(
            tk.prefix(('FORM', 2017), 2016, type='tex'),
            'KFORM')

    def test_exponent_old(self):
        self.assertEqual(
            tk.prefix(('FORM', 2010), 2016, type='tex'),
            'T$^{3}$OFORM')

    def test_exponent_new(self):
        self.assertEqual(
            tk.prefix(('FORM', 2018), 2016, type='tex'),
            'K$^{2}$FORM')

    def test_funny(self):
        self.assertEqual(
            tk.prefix(('KASS', 2013), 2016, type='tex'),
            r'OKA\$\$')


if __name__ == '__main__':
    unittest.main()
