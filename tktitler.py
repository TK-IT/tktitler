# encoding: utf8
from __future__ import unicode_literals

import re


gfyear = 2016


PREFIXTYPE_NORMAL = "normal"
PREFIXTYPE_UNICODE = "unicode"


def prefix(titletupel, gfyear=gfyear, type=PREFIXTYPE_NORMAL):
    root, period = titletupel

    if not isinstance(root, str):
        raise TypeError(type(root).__name__)
    if not isinstance(period, int):
        raise TypeError(type(period).__name__)

    root = __funny_substitute(root)

    age = gfyear - period

    def identity(n):
        return n

    def unicode_superscript(n):
        digits = '⁰¹²³⁴⁵⁶⁷⁸⁹'
        return ''.join(digits[int(i)] for i in str(n))

    sup_fn = None
    if type == PREFIXTYPE_NORMAL:
        sup_fn = identity
    elif type == PREFIXTYPE_UNICODE:
        sup_fn = unicode_superscript
    else:
        raise ValueError("\'%s\' is not a valid type-parameter" % type)

    prefix = ['K', '', 'G', 'B', 'O', 'TO']
    if age < -1:
        return 'K%s' % sup_fn(-age) + root
    elif age + 1 < len(prefix):
        return prefix[age + 1] + root
    else:
        return 'T%sO%s' % (sup_fn(age - 3), root)


def kprefix(titletupel, gfyear=gfyear, type=PREFIXTYPE_NORMAL):
    root, period = titletupel
    age = gfyear - period
    if age <= -1:
        return prefix((root, period), gfyear, type)

    period -= 1
    return "K" + prefix((root, period), gfyear, type)


POSTFIXTYPE_SINGLE = "single"  # FUHØ11
POSTFIXTYPE_DOUBLE = "double"  # FUHØ1112
POSTFIXTYPE_SLASH = "slash"  # FUHØ11/12
POSTFIXTYPE_LONGSINGLE = "longsingle"  # FUHØ2011
POSTFIXTYPE_LONGSLASH = "longslash"  # FUHØ2011/2012


def postfix(titletupel, gfyear=gfyear, type=POSTFIXTYPE_SINGLE):
    root, period = titletupel

    if not isinstance(root, str):
        raise TypeError(type(root).__name__)
    if not isinstance(period, int):
        raise TypeError(type(period).__name__)
    if not len(str(period)) == 4:
        raise ValueError("\'%s\' is not a valid period" % period)

    root = __funny_substitute(root)

    postfix = ""

    if type == POSTFIXTYPE_SINGLE:
        postfix = str(period)[2:4]
    elif type == POSTFIXTYPE_DOUBLE:
        postfix = str(period)[2:4] + str(period+1)[2:4]
    elif type == POSTFIXTYPE_SLASH:
        postfix = str(period)[2:4] + "/" + str(period+1)[2:4]
    elif type == POSTFIXTYPE_LONGSINGLE:
        postfix = str(period)
    elif type == POSTFIXTYPE_LONGSLASH:
        postfix = str(period) + "/" + str(period+1)
    else:
        raise ValueError("\'%s\' is not a valid type-parameter" % type)

    return "" + root + postfix


EMAILTYPE_POSTFIX = "postfix"  # FUHOE11
EMAILTYPE_PREFIX = "prefix"  # T2OFUHOE


def email(titletupel, gfyear=gfyear, type=EMAILTYPE_POSTFIX):
    root, period = titletupel

    if not isinstance(root, str):
        raise TypeError(type(root).__name__)
    if not isinstance(period, int):
        raise TypeError(type(period).__name__)
    if not len(str(period)) == 4:
        raise ValueError("\'%s\' is not a valid period" % period)

    replace_dict = {'æ': 'ae', 'ø': 'oe', 'å': 'aa',
                    'Æ': 'AE', 'Ø': 'OE', 'Å': 'AA'}
    root = __multireplace(root, replace_dict)

    prefix_ = ""
    postfix_ = ""
    if type == EMAILTYPE_POSTFIX:
        postfix_ = str(period)[2:4]
    elif type == EMAILTYPE_PREFIX:
        prefix_ = prefix(("", period), gfyear, type=PREFIXTYPE_NORMAL)
    else:
        raise ValueError("\'%s\' is not a valid type-parameter" % type)
    return "" + prefix_ + root + postfix_


def parse(alias, gfyear=gfyear):
    pass  # return (root, period)


def __funny_substitute(root):
    replace_dict = {'KASS': 'KA$$'}
    root = __multireplace(root, replace_dict)
    return root


def __multireplace(string, replacements):
    """
    Given a string and a replacement map, it returns the replaced string.
    :param str string: string to execute replacements on
    :param dict replacements: replacement dictionary {value to find: value to
    replace}
    :rtype: str
    """
    # Taken from
    # https://gist.github.com/bgusach/a967e0587d6e01e889fd1d776c5f3729

    # Place longer ones first to keep shorter substrings from matching where
    # the longer ones should take place For instance given the replacements
    # {'ab': 'AB', 'abc': 'ABC'} against the string 'hey abc', it should
    # produce 'hey ABC' and not 'hey ABc'
    substrs = sorted(replacements, key=len, reverse=True)

    # Create a big OR regex that matches any of the substrings to replace
    regexp = re.compile('|'.join(map(re.escape, substrs)))

    # For each match, look up the new string in the replacements
    return regexp.sub(lambda match: replacements[match.group(0)], string)

def get_period(prefix, postfix, gfyear):
    """
    Parse a given prefix and postfix into a period.
    prefix and postfix are possibly empty strings,
    and gfyear is an int.
    If both strings are empty, the gfyear is returned:
    >>> get_period("", "", 2016)
    2016
    If only a prefix is given, it is subtracted from the gfyear:
    >>> get_period("B", "", 2016)
    2014
    >>> get_period("T30", "", 2016)
    2010
    >>> get_period("G2B2", "", 2016)
    2010
    These are the three different ways of writing 2010 as postfix.
    Note that the gfyear is ignored when postfix is given.
    >>> get_period("", "2010", 2016)
    2010
    >>> get_period("", "10", 2017)
    2010
    >>> get_period("", "1011", 2018)
    2010
    If both prefix and postfix are given, the prefix is subtracted from
    the postfix, and the gfyear is ignored:
    >>> get_period("O", "2016", 2030)
    2013
    """

    prefix = prefix.upper()
    if not re.match(r'^([KGBOT][0-9]*)*$', prefix):
        raise ValueError("Invalid prefix: %r" % prefix)
    if not re.match(r'^([0-9]{2}){0,2}$', postfix):
        raise ValueError("Invalid postfix: %r" % postfix)

    if not postfix:
        period = gfyear
    else:
        if len(postfix) == 4:
            first, second = int(postfix[0:2]), int(postfix[2:4])
            # Note that postfix 1920, 2021 and 2122 are technically ambiguous,
            # but luckily there was no BEST in 1920 and this script hopefully
            # won't live until the year 2122, so they are not actually
            # ambiguous.
            if postfix == '2021':
                # TODO: Should '2021' be parsed as 2020/21 or 2021/22?
                raise NotImplementedError(postfix)
            if (first + 1) % 100 == second:
                # There should be exactly one year between the two numbers
                if first > 56:
                    period = 1900 + first
                else:
                    period = 2000 + first
            elif first in (19, 20):
                # 19xx or 20xx
                period = int(postfix)
            else:
                raise ValueError(postfix)
        elif len(postfix) == 2:
            year = int(postfix[0:2])
            if year > 56:  # 19??
                period = 1900 + year
            else:  # 20??
                period = 2000 + year
        else:
            raise ValueError(postfix)

    # Now evaluate the prefix:
    prefix_value = dict(K=-1, G=1, B=2, O=3, T=1)
    grad = 0
    for base, exponent in re.findall(r"([KGBOT])([0-9]*)", prefix):
        exponent = int(exponent or 1)
        grad += prefix_value[base] * exponent

    return period - grad


def parse_bestfu_alias(alias, gfyear):
    """
    Resolve a BEST/FU alias into a (kind, root, period)-tuple
    where kind is 'BEST', 'FU' or 'EFU',
    root is the actual title, and period is which period the title
    refers to.
    >>> parse_bestfu_alias('OFORM', 2016)
    ('BEST', 'FORM', 2013)
    """

    alias = alias.upper()
    prefix_pattern = r"(?P<pre>(?:[KGBOT][KGBOT0-9]*)?)"
    postfix_pattern = r"(?P<post>(?:[0-9]{2}|[0-9]{4})?)"
    letter = '[A-Z]|Æ|Ø|Å|AE|OE|AA'
    letter_map = dict(AE='Æ', OE='Ø', AA='Å')
    title_patterns = [
        ('BEST', 'CERM|FORM|INKA|KASS|NF|PR|SEKR|VC'),
        ('FU', '(?P<a>E?FU)(?P<b>%s)(?P<c>%s)' % (letter, letter)),
    ]
    for kind, p in title_patterns:
        pattern = '^%s(?P<root>%s)%s$' % (prefix_pattern, p, postfix_pattern)
        mo = re.match(pattern, alias)
        if mo is not None:
            period = get_period(mo.group("pre"), mo.group("post"), gfyear)
            root = mo.group('root')
            if kind == 'FU':
                fu_kind = mo.group('a')
                letter1 = mo.group('b')
                letter2 = mo.group('c')
                assert root == fu_kind + letter1 + letter2
                # Translate AE OE AA
                letter1_int = letter_map.get(letter1, letter1)
                letter2_int = letter_map.get(letter2, letter2)
                root_int = fu_kind + letter1_int + letter2_int
                return fu_kind, root_int, period
            else:
                return kind, root, period
    raise ValueError(alias)
