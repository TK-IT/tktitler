# encoding: utf8
from __future__ import unicode_literals

import re
import functools
import unicodedata

import logging

logger = logging.getLogger(__name__)

_gfyear = _GFYEAR_UNSET = object()


def get_gfyear(argument_gfyear=None):
    if argument_gfyear is None:
        r = _gfyear
    else:
        r = argument_gfyear
    if r is _GFYEAR_UNSET:
        raise ValueError("No context gfyear set. Use the gfyear argument " +
                         "or set_gfyear.")
    if not isinstance(r, int):
        raise TypeError(
            "%s is not a valid type for gfyear." % type(r).__name__)
    if len(str(r)) != 4:
        raise ValueError("\'%s\' is not a valid gfyear" % r)
    return r


class _Override(object):
    def __init__(self, context_gfyear):
        self.context_gfyear = context_gfyear

    def __enter__(self):
        global _gfyear
        self.prev_gfyear = _gfyear
        _gfyear = self.context_gfyear

    def __exit__(self, exc_type, exc_value, exc_traceback):
        global _gfyear
        _gfyear = self.prev_gfyear

    def __call__(self, fun):
        @functools.wraps(fun)
        def wrapped(*args, **kwargs):
            with self:
                return fun(*args, **kwargs)

        return wrapped


def set_gfyear(gfyear):
    return _Override(gfyear)


PREFIXTYPE_NORMAL = "normal"
PREFIXTYPE_UNICODE = "unicode"


def tk_prefix(title, gfyear=None, type=PREFIXTYPE_NORMAL):
    gfyear = _validate(title, gfyear)

    root, period = title
    root = _funny_substitute(root)
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
        return 'T%sO' % sup_fn(age - 3) + root


def tk_kprefix(title, gfyear=None, type=PREFIXTYPE_NORMAL):
    gfyear = _validate(title, gfyear)

    root, period = title
    if gfyear < period:
        return tk_prefix((root, period), gfyear, type)
    return "K" + tk_prefix((root, period - 1), gfyear, type)


POSTFIXTYPE_SINGLE = "single"  # FUHØ11
POSTFIXTYPE_DOUBLE = "double"  # FUHØ1112
POSTFIXTYPE_SLASH = "slash"  # FUHØ 11/12
POSTFIXTYPE_LONGSLASH = "longslash"  # FUHØ 2011/12


def tk_postfix(title, type=POSTFIXTYPE_SINGLE):
    _validate_title(title)

    root, period = title
    root = _funny_substitute(root)

    space = " "
    if root == "":
        space = ""

    postfix = ""

    if type == POSTFIXTYPE_SINGLE:
        postfix = str(period)[2:4]
    elif type == POSTFIXTYPE_DOUBLE:
        postfix = str(period)[2:4] + str(period+1)[2:4]
    elif type == POSTFIXTYPE_SLASH:
        postfix = space + str(period)[2:4] + "/" + str(period+1)[2:4]
    elif type == POSTFIXTYPE_LONGSLASH:
        postfix = space + str(period) + "/" + str(period+1)[2:4]
    else:
        raise ValueError("\'%s\' is not a valid type-parameter" % type)

    assert isinstance(root + postfix, str)
    return root + postfix


EMAILTYPE_POSTFIX = "postfix"  # FUHOE11
EMAILTYPE_PREFIX = "prefix"  # T2OFUHOE


def email(title, gfyear=None, type=EMAILTYPE_POSTFIX):
    gfyear = _validate(title, gfyear)

    root, period = title

    root = _normalize(root)
    replace_dict = {'æ': 'ae', 'ø': 'oe', 'å': 'aa',
                    'Æ': 'AE', 'Ø': 'OE', 'Å': 'AA'}
    root = _multireplace(root, replace_dict)

    prefix = ""
    postfix = ""
    if type == EMAILTYPE_POSTFIX:
        postfix = str(period)[2:4]
    elif type == EMAILTYPE_PREFIX:
        prefix = tk_prefix(("", period), gfyear, type=PREFIXTYPE_NORMAL)
    else:
        raise ValueError("\'%s\' is not a valid type-parameter" % type)
    assert isinstance(prefix + root + postfix, str)
    return prefix + root + postfix


def _normalize(input_alias):
    s = input_alias.upper()
    s = s.replace(' ', '')

    replace_dict = {'BEST/FU': 'BESTFU'}
    s = _multireplace(s, replace_dict)

    table = {'$': 'S',
             '\N{POUND SIGN}': 'S',
             '\N{DOUBLE-STRUCK CAPITAL C}': 'C'}

    def tr(c):
        try:
            return table[c]
        except KeyError:
            try:
                return str(unicodedata.digit(c))
            except ValueError:
                return c

    return re.sub(r'[^0-9A-ZÆØÅ]', lambda mo: tr(mo.group(0)), s)


def _parse_prefix(prefix):
    pattern = r"^([KGBOT][KGBOT0-9]*)?$"
    if not re.match(pattern, prefix):
        raise ValueError(prefix)
    prefix_value = dict(K=-1, G=1, B=2, O=3, T=1)
    factors = []
    for base, exponent in re.findall(r"([KGBOT])([0-9]*)", prefix):
        factors.append(int(exponent or 1) * prefix_value[base])
    return sum(factors)


def _parse_postfix(postfix):
    if not isinstance(postfix, str):
        raise TypeError(type(postfix))
    if not postfix:
        return

    postfix = postfix.replace('/', '')

    if len(postfix) == 2:
        v = int(postfix)
        return 2000 + v if v < 56 else 1900 + v
    elif len(postfix) == 4:
        first, second = int(postfix[0:2]), int(postfix[2:4])
        # Note that postfix 1920, 2021 and 2122 are technically ambiguous,
        # but luckily there was no BEST in 1920 and this script hopefully
        # won't live until the year 2122, so they are not actually
        # ambiguous.
        if postfix == '2021':
            # POSTFIXTYPE_LONGSINGLE is never used in email recipients,
            # whereas POSTFIXTYPE_DOUBLE is used in 1/3 of the cases in
            # which as postfix is given (with the remainder using
            # POSTFIXTYPE_SINGLE).
            logger.warning('While parsing an alias, the technically ambiguous '
                           'postfix 2021 was met. It it assumed it means '
                           '2020/2021.')
            return 2020
        if (first + 1) % 100 == second:
            # There should be exactly one year between the two numbers
            return 2000 + first if first < 56 else 1900 + first
        elif first in (19, 20):
            # 19xx or 20xx
            return int(postfix)
    elif len(postfix) == 6:
        longFirst, shortFirst = int(postfix[0:4]), int(postfix[2:4])
        second = int(postfix[4:6])
        if (shortFirst + 1) % 100 == second:
            # 2012/13
            return longFirst
    elif len(postfix) == 8:
        first, second = int(postfix[0:4]), int(postfix[4:8])
        if (first + 1) == second:
            # 2012/2013
            return first
    raise ValueError(postfix)


def _parse_relative(input_alias):
    alias = _normalize(input_alias)
    prefix = r"(?P<pre>(?:[KGBOT][KGBOT0-9]*)?)"
    postfix = r"(?P<post>([0-9/])*)"
    letter = '[A-Z]|Æ|Ø|Å|AE|OE|AA'
    known = ('CERM|FORM|INKA|KASS|NF|PR|SEKR|VC|' +
             'E?FU(?:%s){2}|' % letter +
             'BEST|FU|BESTFU')
    known_pattern = '^%s(?P<root>%s)%s$' % (prefix, known, postfix)
    any_pattern = '^%s(?P<root>.*?)%s$' % (prefix, postfix)
    mo = re.match(known_pattern, alias) or re.match(any_pattern, alias)
    assert mo is not None
    pre, root, post = mo.group('pre', 'root', 'post')
    assert alias == pre + root + post
    age = _parse_prefix(pre)
    gfyear = _parse_postfix(post)
    return age, root, gfyear


def parse(alias, gfyear=None):
    age, root, postfix = _parse_relative(alias)
    gfyear = postfix or get_gfyear(gfyear)
    return root, gfyear - age


def _validate_title(title):
    root, period = title
    if not isinstance(root, str):
        raise TypeError(
            "%s is not a valid type for root." % type(root).__name__)
    if not isinstance(period, int):
        raise TypeError(
            "%s is not a valid type for period." % type(period).__name__)
    if not len(str(period)) == 4:
        raise ValueError("\'%s\' is not a valid period" % period)


def _validate(title, gfyear):
    _validate_title(title)
    return get_gfyear(gfyear)


def _funny_substitute(root):
    replace_dict = {'KASS': 'KA$$'}
    root = _multireplace(root, replace_dict)
    return root


def _multireplace(string, replacements):
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
