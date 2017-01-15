# encoding: utf8
from __future__ import unicode_literals

import re
import abc
import functools
import unicodedata

import logging

logger = logging.getLogger(__name__)

_gfyear = _GFYEAR_UNSET = object()


class _TitleABC(metaclass=abc.ABCMeta):
    pass


title_class = _TitleABC.register


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
"""Type til :func:`prefix` der giver output med normale ASCII tal."""
PREFIXTYPE_UNICODE = "unicode"
"""Type til :func:`prefix` der giver output med unicode-superscript tal."""
PREFIXTYPE_TEX = "tex"
"""Type til :func:`prefix` der giver output med TeX-superscript numre og
escapede tegn.

"""


def _escape_tex(s):
    return str(s).replace('$', r'\$')


def prefix(title, gfyear=None, *, type=PREFIXTYPE_NORMAL):
    """
    Given en title af (root, period), retunerer titlen skrevet med prefix.

    :param tuple title: tupel af en str og int, hvor strengen er roden af
                        titlen og int er perioden.
    :param int gfyear: året hvor nuværende BEST er blevet valgt. Det kan også
                       sættes som en context. Se :doc:`gfyear`.
    :param type: en keyword-only option til at ændre typen af outputet. Den
                 kan være :data:`PREFIXTYPE_NORMAL`, :data:`PREFIXTYPE_UNICODE`
                 eller :data:`PREFIXTYPE_TEX`.

    :rtype: str

    :example:

    >>> prefix(('KASS', 2011), gfyear=2016)
    'T2OKA$$'

    >>> prefix(('FORM', 2010), 2016, type=PREFIXTYPE_UNICODE)
    'T³OFORM'

    >>> with set_gfyear(2015):
    ...     prefix(('CERM', 2017), type=PREFIXTYPE_TEX)
    'K$^{2}$CERM'

    """
    (root, period), gfyear = _validate(title, gfyear)

    root = _funny_substitute(root)
    age = gfyear - period

    if type == PREFIXTYPE_TEX:
        root = _escape_tex(root)

    def identity(n):
        return n

    def unicode_superscript(n):
        digits = '⁰¹²³⁴⁵⁶⁷⁸⁹'
        return ''.join(digits[int(i)] for i in str(n))

    def tex_superscript(n):
        return '$^{%s}$' % (n,)

    sup_fn = None
    if type == PREFIXTYPE_NORMAL:
        sup_fn = identity
    elif type == PREFIXTYPE_UNICODE:
        sup_fn = unicode_superscript
    elif type == PREFIXTYPE_TEX:
        sup_fn = tex_superscript
    else:
        raise ValueError("\'%s\' is not a valid type-parameter" % type)

    prefixes = ['K', '', 'G', 'B', 'O', 'TO']
    if age < -1:
        return 'K%s' % sup_fn(-age) + root
    elif age + 1 < len(prefixes):
        return prefixes[age + 1] + root
    else:
        return 'T%sO' % sup_fn(age - 3) + root


def kprefix(title, gfyear=None, *, type=PREFIXTYPE_NORMAL):
    """
    Givet en titel af (root, period), returner titlen skrevet med et prefix
    der starter med K.

    :param tuple title: tupel af en str og int, hvor strengen er roden af
                        titlen og int er perioden.
    :param int gfyear: året hvor nuværende BEST er blevet valgt. Det kan også
                       sættes som en context. Se :doc:`gfyear`.
    :param type: Format af output. Skal være enten
                 :data:`PREFIXTYPE_NORMAL`, :data:`PREFIXTYPE_UNICODE` eller
                 :data:`PREFIXTYPE_TEX`.

    :rtype: str

    :example:

    >>> prefix(('KASS', 2011), gfyear=2016)
    'T2OKA$$'

    >>> kprefix(('KASS', 2011), gfyear=2016)
    'KT3OKA$$'

    >>> kprefix(('CERM', 2018), gfyear=2016)
    'K2CERM'

    """
    (root, period), gfyear = _validate(title, gfyear)

    if gfyear < period:
        return prefix((root, period), gfyear, type=type)
    return "K" + prefix((root, period - 1), gfyear, type=type)


POSTFIXTYPE_SINGLE = "single"  # FUHØ11
"Type til :func:`postfix` der giver tocifret postfix, f.eks. FUHI11"
POSTFIXTYPE_DOUBLE = "double"  # FUHØ1112
"Type til :func:`postfix` der giver firecifret postfix, f.eks. FUHI1112"
POSTFIXTYPE_SLASH = "slash"  # FUHØ 11/12
"""Type til :func:`postfix` der giver postfix med skråstreg og mellemrum,
f.eks. FUHI 11/12"""
POSTFIXTYPE_LONGSLASH = "longslash"  # FUHØ 2011/12
"""Type til :func:`postfix` der giver langt postfix med skråstreg og mellemrum,
f.eks. FUHI 2011/12"""


def postfix(title, *, type=POSTFIXTYPE_SINGLE):
    """
    Givet en titel af (root, period), returner titlen skrevet med postfix.

    :param tuple title: tupel af en str og int, hvor strengen er roden af
                        titlen og int er perioden.
    :param type: Format af output. Skal være enten
                 :data:`POSTFIXTYPE_SINGLE`, :data:`POSTFIXTYPE_DOUBLE`,
                 :data:`POSTFIXTYPE_SLASH` eller :data:`POSTFIXTYPE_LONGSLASH`.

    :rtype: str

    :example:

    >>> postfix(('KASS', 2011))
    'KA$$11'

    >>> postfix(('FORM', 2010), type=POSTFIXTYPE_DOUBLE)
    'FORM1011'

    >>> postfix(('CERM', 2017), type=POSTFIXTYPE_SLASH)
    'CERM 17/18'

    >>> postfix(('FUHØ', 2011), type=POSTFIXTYPE_LONGSLASH)
    'FUHØ 2011/12'

    """
    root, period = _validate_title(title)

    if root == 'EFUIT':
        logger.warning('Returning an EFUIT postfix. The postfix does not '
                       'necessarily represent the actual year the given EFUIT '
                       'was EFUIT.')
    if period < 1959:
        logger.warning('Returning a postfix from before 1959. The postfix '
                       'does not necessarily represent the actual year the '
                       'given %s was %s.' % (root, root))

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


def prepostfix(title, gfyear=None, *, prefixtype=PREFIXTYPE_NORMAL,
               postfixtype=POSTFIXTYPE_LONGSLASH):
    root, period = _validate_title(title)
    preAndName = prefix(title, gfyear, type=prefixtype)
    if root == "EFUIT" or period < 1959:
        return preAndName
    post = postfix(("", period), type=postfixtype)
    return '%s %s' % (preAndName, post)


EMAILTYPE_POSTFIX = "postfix"  # FUHOE11
EMAILTYPE_PREFIX = "prefix"  # T2OFUHOE


def email(title, gfyear=None, *, type=EMAILTYPE_POSTFIX):
    (root, period), gfyear = _validate(title, gfyear)

    root = _normalize(root)
    replace_dict = {'æ': 'ae', 'ø': 'oe', 'å': 'aa',
                    'Æ': 'AE', 'Ø': 'OE', 'Å': 'AA'}
    root = _multireplace(root, replace_dict)

    if root == 'EFUIT' and type == EMAILTYPE_POSTFIX:
        logger.warning('Returning an EFUIT email with postfix. The postfix '
                       'does not necessarily represent the actual year the '
                       'given EFUIT was EFUIT.')
    if period < 1959 and type == EMAILTYPE_POSTFIX:
        logger.warning('Returning an email from before 1959 with postfix. The '
                       'postfix does not necessarily represent the actual '
                       'year the given %s was %s.' % (root, root))

    pre = ""
    post = ""
    if type == EMAILTYPE_POSTFIX:
        post = str(period)[2:4]
    elif type == EMAILTYPE_PREFIX:
        pre = prefix(("", period), gfyear, type=PREFIXTYPE_NORMAL)
    else:
        raise ValueError("\'%s\' is not a valid type-parameter" % type)
    assert isinstance(pre + root + post, str)
    return pre + root + post


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


def _normalize_escaped(alias):
    if ("AAA" in alias and "AAAA" not in alias) or "AAE" in alias:
        raise ValueError("%s is an ambiguous alias. Cannot normalize." % alias)
    replace_dict = {'OE': 'Ø',
                    'AE': 'Æ',
                    'AA': 'Å'}
    alias = _multireplace(alias, replace_dict)
    return alias


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

    if '/' in postfix:
        try:
            first, second = postfix.split('/')
        except ValueError:
            raise ValueError(postfix) from None
        lens = (len(first), len(second))
        first, second = int(first), int(second)
        if lens == (2, 2) and (first + 1) % 100 == second:
            # 12/13; note that 20/21 is not ambiguous.
            return 2000 + first if first < 56 else 1900 + first
        elif lens == (4, 4) and first + 1 == second:
            # 2012/2013
            return first
        elif lens == (4, 2) and (first + 1) % 100 == second:
            # 2012/13
            return first
    elif len(postfix) == 2:
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
    raise ValueError(postfix)


def _parse_relative(input_alias):
    alias = _normalize(input_alias)
    prefix = r"(?P<pre>(?:[KGBOT][KGBOT0-9]*)?)"
    postfix = r"(?P<post>([0-9/])*)"
    letter = '[A-Z]|Æ|Ø|Å'
    known_escaped = 'E?FU((AE|OE|AA){2}|(AE|OE|AA)[A-Z]|[A-Z](AE|OE|AA))'
    known = ('CERM|FORM|INKA|KASS|NF|PR|SEKR|VC|' +
             'E?FU(?:%s){2}|' % letter +
             'BEST|FU|BESTFU')
    known_escaped_pattern = '^%s(?P<root>%s)%s$' % (prefix, known_escaped,
                                                    postfix)
    known_pattern = '^%s(?P<root>%s)%s$' % (prefix, known, postfix)
    any_pattern = '^%s(?P<root>.*?)%s$' % (prefix, postfix)

    pre = root = post = ''

    mo = re.match(known_escaped_pattern, alias)
    if mo is not None:
        pre, root, post = mo.group('pre', 'root', 'post')
        root = _normalize_escaped(root)
    else:
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
    if isinstance(title, _TitleABC):
        title = title.title_tuple()
    root, period = title
    if not isinstance(root, str):
        raise TypeError(
            "%s is not a valid type for root." % type(root).__name__)
    if not isinstance(period, int):
        raise TypeError(
            "%s is not a valid type for period." % type(period).__name__)
    if not len(str(period)) == 4:
        raise ValueError("\'%s\' is not a valid period" % period)
    return title


def _validate(title, gfyear):
    title = _validate_title(title)
    return title, get_gfyear(gfyear)


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
