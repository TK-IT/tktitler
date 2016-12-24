# encoding: utf8
from __future__ import unicode_literals

import re
import functools
import unicodedata


_gfyear = _GFYEAR_UNSET = object()


PREFIXTYPE_NORMAL = "normal"
PREFIXTYPE_UNICODE = "unicode"


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
POSTFIXTYPE_SLASH = "slash"  # FUHØ11/12
POSTFIXTYPE_LONGSINGLE = "longsingle"  # FUHØ2011
POSTFIXTYPE_LONGSLASH = "longslash"  # FUHØ2011/2012


def tk_postfix(title, type=POSTFIXTYPE_SINGLE):
    _validate_title(title)

    root, period = title
    root = _funny_substitute(root)

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

    assert isinstance(root + postfix, str)
    return root + postfix


EMAILTYPE_POSTFIX = "postfix"  # FUHOE11
EMAILTYPE_PREFIX = "prefix"  # T2OFUHOE


def email(title, gfyear=None, type=EMAILTYPE_POSTFIX):
    gfyear = _validate(title, gfyear)

    root, period = title

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

    s = input_alias.upper()
    return re.sub(r'[^0-9A-ZÆØÅ]', lambda mo: tr(mo.group(0)), s)


class _Prefix:
    VALUE = dict(K=-1, G=1, B=2, O=3, T=1)

    def __init__(self, data):
        self.data = [(self.VALUE[b] and b, e) for b, e in data]

    def _ages(self):
        for base, exponent in self.data:
            e = 1 if exponent is None else exponent
            yield e * self.VALUE[base]

    def age(self):
        return sum(self._ages())

    @classmethod
    def parse(cls, s):
        if not re.match(r'^([KGBOT][KGBOT0-9]*)?$', s):
            raise ValueError(s)
        factors = re.findall(r'([KGBOT])([0-9]*)', s)
        return cls([(b, int(e) if e else None)
                    for b, e in factors])

    def __str__(self):
        return ''.join('%s%s' % (b, e or '') for b, e in self.data)

    def __repr__(self):
        return "_Prefix.parse('%s')" % self


class _Postfix:
    def __init__(self, period, kind):
        self.period = period
        self.kind = kind

    @classmethod
    def parse(cls, postfix):
        if not isinstance(postfix, str):
            raise TypeError(type(postfix))
        if not postfix:
            raise ValueError(postfix)
        if len(postfix) == 2:
            v = int(postfix)
            period = 2000 + v if v < 56 else 1900 + v
            return cls(period, POSTFIXTYPE_SINGLE)
        elif len(postfix) == 4:
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
                period = 2000 + first if first < 56 else 1900 + first
                return cls(period, POSTFIXTYPE_DOUBLE)
            elif first in (19, 20):
                # 19xx or 20xx
                return cls(int(postfix), POSTFIXTYPE_LONGSINGLE)
            else:
                raise ValueError(postfix)
        elif '/' in postfix:
            first, second = map(int, postfix.split('/'))
            if len(postfix) == 5:
                if (first + 1) % 100 != second:
                    raise ValueError(postfix)
                period = 2000 + first if first < 56 else 1900 + first
                return cls(period, POSTFIXTYPE_SLASH)
            elif len(postfix) == 9:
                if not 1900 <= first < first + 1 == second < 2100:
                    raise ValueError(postfix)
                return cls(first, POSTFIXTYPE_LONGSLASH)
            else:
                raise ValueError(postfix)
        else:
            raise ValueError(postfix)

    def __str__(self):
        if self.kind == POSTFIXTYPE_SINGLE:
            return str(self.period)[2:4]
        elif self.kind == POSTFIXTYPE_DOUBLE:
            return str(self.period)[2:4] + str(self.period+1)[2:4]
        elif self.kind == POSTFIXTYPE_SLASH:
            return str(self.period)[2:4] + "/" + str(self.period+1)[2:4]
        elif self.kind == POSTFIXTYPE_LONGSINGLE:
            return str(self.period)
        elif self.kind == POSTFIXTYPE_LONGSLASH:
            return str(self.period) + "/" + str(self.period+1)
        else:
            raise ValueError("'%s' is not a valid type-parameter" % self.kind)


class _Title:
    def __init__(self, pre, root, post):
        self.pre = pre
        self.root = root
        self.post = post

    def __str__(self):
        return '%s%s%s' % (self.pre, self.root, self.post or '')

    def __repr__(self):
        return "_Title.parse('%s')" % self

    @classmethod
    def parse(cls, input_alias):
        alias = _normalize(input_alias)
        prefix = r"(?P<pre>(?:[KGBOT][KGBOT0-9]*)?)"
        postfix = r"(?P<post>[0-9]*)"
        letter = '[A-Z]|Æ|Ø|Å|AE|OE|AA'
        known = ('CERM|FORM|INKA|KASS|NF|PR|SEKR|VC|' +
                 'E?FU(?:%s){2}|' % letter +
                 'BEST|FU')
        known_pattern = '^%s(?P<root>%s)%s$' % (prefix, known, postfix)
        any_pattern = '^%s(?P<root>.*?)%s$' % (prefix, postfix)
        mo = re.match(known_pattern, alias) or re.match(any_pattern, alias)
        if mo is None:
            raise ValueError(alias)
        pre, root, post = mo.group('pre', 'root', 'post')
        postfix = _Postfix.parse(post) if post else None
        return cls(_Prefix.parse(pre), root, postfix)

    def __iter__(self):
        return iter((self.pre, self.root, self.post))


def parse_relative(input_alias):
    pre, root, post = _Title.parse(input_alias)
    return pre.age(), root, post.period if post else None


def parse(alias, gfyear=None):
    age, root, postfix = parse_relative(alias)
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


def get_period(prefix, postfix, gfyear=None):
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
    >>> get_period("T3O", "", 2016)
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

    root, period = parse('%sFORM%s' % (prefix, postfix), gfyear)
    return period


def parse_bestfu_alias(alias, gfyear=None):
    """
    Resolve a BEST/FU alias into a (kind, root, period)-tuple
    where kind is 'BEST', 'FU' or 'EFU',
    root is the actual title, and period is which period the title
    refers to.
    >>> parse_bestfu_alias('OFORM', 2016)
    ('BEST', 'FORM', 2013)
    """

    root, period = parse(alias, gfyear)
    letter = '(?:[A-Z]|Æ|Ø|Å|AE|OE|AA)'
    title_patterns = [
        ('BEST', '^(?:CERM|FORM|INKA|KASS|NF|PR|SEKR|VC)$'),
        ('FU', '^FU%s%s$' % (letter, letter)),
        ('EFU', '^EFU%s%s$' % (letter, letter)),
    ]
    for kind, p in title_patterns:
        if re.match(p, root):
            return kind, root, period
    raise ValueError(alias)
