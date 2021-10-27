import tktitler as tk

import re
import abc
import functools
import unicodedata

import logging

logger = logging.getLogger(__name__)

_gfyear = _GFYEAR_UNSET = object()

DIGRAPHS = {'Æ': 'AE', 'Ø': 'OE', 'Å': 'AA', 'Ü': 'UE'}
'Dictionary der mapper hvert stort dansk bogstav til en ASCII-forlængelse.'

_SPECIAL_CASES = (
)


class _TitleABC(metaclass=abc.ABCMeta):
    pass


title_class = _TitleABC.register


def get_gfyear(gfyear=None):
    '''Returner et ikke-None argument eller det nuværende gfyear.

    :param int gfyear: kan gives en ikke-None værdi for at overskrive
                       det nuværende gfyear.

    :rtype: int

    :example:

    >>> def current_age(gfyear=None):
    ...     return tk.get_gfyear(gfyear) - 1956
    >>> current_age(2016)
    60
    >>> with tk.set_gfyear(2031):
    ...     current_age()
    75
    '''

    if gfyear is None:
        r = _gfyear
    else:
        r = gfyear
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
        if callable(context_gfyear):
            self.context_gfyear_callable = context_gfyear
        else:
            self.context_gfyear = context_gfyear

    def __enter__(self):
        global _gfyear
        self.prev_gfyear = _gfyear
        try:
            _gfyear = self.context_gfyear
        except AttributeError:
            _gfyear = self.context_gfyear_callable()

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
    '''Sæt årstallet hvor den nuværende BEST er valgt.

    Kan bruges som :std:term:`decorator` eller :std:term:`context manager`.

    :param int gfyear: året som relative titler i kodeblokken bliver regnet ud
                       efter. Typisk året hvor nuværnde BEST er valgt.

    :example:

    >>> with tk.set_gfyear(2013):
    ...     tk.prefix(('FORM', 2012))
    'GFORM'

    >>> @tk.set_gfyear(2016)
    ... def get_j60_name(title):
    ...     return tk.prepostfix(title)
    >>> get_j60_name(('FORM', 2013))
    'OFORM 2013/14'

    Man kan give en lambda som argument for at beregne året på ny hver gang
    funktionen bliver kaldt. Den givne lambda bliver kaldt én gang i starten
    af funktionen. For eksempel:

    >>> y = 2013
    >>> @tk.set_gfyear(lambda: y)
    ... def foo():
    ...     return tk.prefix(('FORM', 2012))
    >>> foo()
    'GFORM'
    >>> y = 2015
    >>> foo()
    'OFORM'

    Hvis man bruger constance, kan man eksempelvis hente året fra databasen:

    >>> from constance import config  # doctest: +SKIP
    >>> @tk.set_gfyear(lambda: config.GFYEAR)
    ... def get_title_list(titles):
    ...     result = []
    ...     for x in titles:
    ...         result.append(tk.prefix(x))
    ...     return ', '.join(result)
    '''
    return _Override(gfyear)


_PREFIXTYPE_NORMAL = "normal"
_PREFIXTYPE_UNICODE = "unicode"
_PREFIXTYPE_TEX = "tex"


def _escape_tex(s):
    return str(s).replace('$', r'\$')


def prefix(title, gfyear=None, *, type=_PREFIXTYPE_NORMAL):
    """
    Givet en titel af (root, period), returner titlen skrevet med prefix.

    :param tuple title: tupel af en str og int, hvor strengen er roden af
                        titlen og int er perioden.
    :param int gfyear: året hvor nuværende BEST er blevet valgt. Det kan også
                       sættes som en context. Se :doc:`gfyear`.
    :param str type: Format af output. En af de følgende strenge:

                 ``normal``
                     Giver potenser med normale ASCII tal.

                 ``unicode``
                     Giver potenser med unicode-superscript tal.

                 ``tex``
                     Giver potenser med TeX-superscript tal samt escapede tegn.

    :rtype: str

    :example:

    >>> tk.prefix(('KASS', 2011), gfyear=2016)
    'T2OKA$$'

    >>> tk.prefix(('FORM', 2010), 2016, type='unicode')
    'T³OFORM'

    >>> with tk.set_gfyear(2015):
    ...     tk.prefix(('CERM', 2017), type='tex')
    'K$^{2}$CERM'

    """
    (root, period), gfyear = _validate(title, gfyear)

    root = _funny_substitute(root)
    age = gfyear - period

    if type == _PREFIXTYPE_TEX:
        root = _escape_tex(root)

    def identity(n):
        return n

    def unicode_superscript(n):
        digits = '⁰¹²³⁴⁵⁶⁷⁸⁹'
        return ''.join(digits[int(i)] for i in str(n))

    def tex_superscript(n):
        return '$^{%s}$' % (n,)

    sup_fn = None
    if type == _PREFIXTYPE_NORMAL:
        sup_fn = identity
    elif type == _PREFIXTYPE_UNICODE:
        sup_fn = unicode_superscript
    elif type == _PREFIXTYPE_TEX:
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


def kprefix(title, gfyear=None, *, type=_PREFIXTYPE_NORMAL):
    """
    Givet en titel af (root, period), returner titlen skrevet med et prefix
    der starter med K.

    :param tuple title: tupel af en str og int, hvor strengen er roden af
                        titlen og int er perioden.
    :param int gfyear: året hvor nuværende BEST er blevet valgt. Det kan også
                       sættes som en context. Se :doc:`gfyear`.
    :param str type: Format af output. En af de følgende strenge:

                 ``normal``
                     Giver potenser med normale ASCII tal.

                 ``unicode``
                     Giver potenser med unicode-superscript tal.

                 ``tex``
                     Giver potenser med TeX-superscript tal samt escapede tegn.


    :rtype: str

    :example:

    >>> tk.prefix(('KASS', 2011), gfyear=2016)
    'T2OKA$$'

    >>> tk.kprefix(('KASS', 2011), gfyear=2016)
    'KT3OKA$$'

    >>> tk.kprefix(('CERM', 2018), gfyear=2016)
    'K2CERM'

    >>> tk.kprefix(('UNDESERVICE', 2007), 2012)
    'KT3OUNDESERVICE'

    """
    (root, period), gfyear = _validate(title, gfyear)

    if gfyear < period:
        return prefix((root, period), gfyear, type=type)
    return "K" + prefix((root, period - 1), gfyear, type=type)


_POSTFIXTYPE_SINGLE = "single"  # FUHØ11
_POSTFIXTYPE_DOUBLE = "double"  # FUHØ1112
_POSTFIXTYPE_SLASH = "slash"  # FUHØ 11/12
_POSTFIXTYPE_LONGSLASH = "longslash"  # FUHØ 2011/12


def postfix(title, *, type=_POSTFIXTYPE_SINGLE):
    """
    Givet en titel af (root, period), returner titlen skrevet med postfix.

    :param tuple title: tupel af en str og int, hvor strengen er roden af
                        titlen og int er perioden.
    :param str type: Format af output. En af de følgende strenge:

                 ``single``
                     Giver et tocifret postfix, f.eks. FUHI11.

                 ``double``
                     Giver et firecifret postfix, f.eks. FUHI1112

                 ``slash``
                     Giver et postfix med skråstreg og mellemrum,
                     f.eks. FUHI 11/12

                 ``longslash``
                     Giver langt postfix med skråstreg og mellemrum,
                     f.eks. FUHI 2011/12

    :rtype: str

    :example:

    >>> tk.postfix(('KASS', 2011))
    'KA$$11'

    >>> tk.postfix(('FORM', 2010), type='double')
    'FORM1011'

    >>> tk.postfix(('CERM', 2017), type='slash')
    'CERM 17/18'

    >>> tk.postfix(('FUHØ', 2011), type='longslash')
    'FUHØ 2011/12'

    """
    root, period = validate_title(title)

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

    if type == _POSTFIXTYPE_SINGLE:
        postfix = str(period)[2:4]
    elif type == _POSTFIXTYPE_DOUBLE:
        postfix = str(period)[2:4] + str(period+1)[2:4]
    elif type == _POSTFIXTYPE_SLASH:
        postfix = space + str(period)[2:4] + "/" + str(period+1)[2:4]
    elif type == _POSTFIXTYPE_LONGSLASH:
        postfix = space + str(period) + "/" + str(period+1)[2:4]
    else:
        raise ValueError("\'%s\' is not a valid type-parameter" % type)

    assert isinstance(root + postfix, str)
    return root + postfix


def prepostfix(title, gfyear=None, *, prefixtype=_PREFIXTYPE_NORMAL,
               postfixtype=_POSTFIXTYPE_LONGSLASH):
    """
    Givet en titel af (root, period), returner titlen skrevet med
    både prefix og postfix.

    Titler med både pre- og postfix kan bruges i lister over årgange
    så det er nemt for brugeren at slå op efter enten prefix eller postfix.
    Bemærk at outputtet fra denne funktion ikke kan genfortolkes med
    :func:`parse`, da prefixet parses relativt til postfixet.

    :param tuple title: tupel af en str og int, hvor strengen er roden af
                        titlen og int er perioden.
    :param int gfyear: året hvor nuværende BEST er blevet valgt. Det kan også
                       sættes som en context. Se :doc:`gfyear`.
    :param str prefixtype: Format af prefix. En af de følgende strenge:

                 ``normal``
                     Giver potenser med normale ASCII tal.

                 ``unicode``
                     Giver potenser med unicode-superscript tal.

                 ``tex``
                     Giver potenser med TeX-superscript tal samt escapede tegn.
    :param str postfixtype: Format af postfix. En af de følgende strenge:

                 ``single``
                     Giver et tocifret postfix, f.eks. FUHI11.

                 ``double``
                     Giver et firecifret postfix, f.eks. FUHI1112

                 ``slash``
                     Giver et postfix med skråstreg og mellemrum,
                     f.eks. FUHI 11/12

                 ``longslash``
                     Giver langt postfix med skråstreg og mellemrum,
                     f.eks. FUHI 2011/12

    :rtype: str

    :example:

    >>> tk.prepostfix(('KASS', 2011), gfyear=2016)
    'T2OKA$$ 2011/12'

    """
    root, period = validate_title(title)
    preAndName = prefix(title, gfyear, type=prefixtype)
    if root == "EFUIT" or period < 1959:
        return preAndName
    post = postfix(("", period), type=postfixtype)
    return '%s %s' % (preAndName, post)


_EMAILTYPE_POSTFIX = "postfix"  # FUHOE11
_EMAILTYPE_PREFIX = "prefix"  # T2OFUHOE


def email(title, gfyear=None, *, type=_EMAILTYPE_POSTFIX):
    """
    Givet en titel af (root, period), returner titlens emailnavn.

    :param tuple title: tupel af en str og int, hvor strengen er roden af
                        titlen og int er perioden.
    :param int gfyear: året hvor nuværende BEST er blevet valgt. Det kan også
                       sættes som en context. Se :doc:`gfyear`.
    :param str type: Format af output. En af de følgende strenge:

                     ``postfix``
                         Giver et emailnavn som postfix. f.eks. FORM12.

                     ``prefix``
                         Giver et emailnavn som prefix. f.eks. OEFUIT.
                         Den er nyttig til EFUIT-titler hvor årstallet ikke
                         nødvendigvis hænger sammen med hvornår en EFUIT var
                         EFUIT.

    :rtype: str

    :example:

    >>> tk.email(('KASS', 2011), 2017)
    'KASS11'

    >>> tk.email(('FUHØ', 2010), 2016, type='prefix')
    'T3OFUHOE'

    >>> tk.email(('FUÅÆ', 2012), 2015)
    'FUAAAE12'

    """
    (root, period), gfyear = _validate(title, gfyear)

    root = _normalize(root)
    try:
        root = next(email for r, p, email in _SPECIAL_CASES if (r, p) == (root, period))
    except StopIteration:
        root = _multireplace(root, DIGRAPHS)
        digraphs_lower = {ch.lower(): di.lower() for ch, di in DIGRAPHS.items()}
        root = _multireplace(root, digraphs_lower)

    if root == 'EFUIT' and type == _EMAILTYPE_POSTFIX:
        logger.warning('Returning an EFUIT email with postfix. The postfix '
                       'does not necessarily represent the actual year the '
                       'given EFUIT was EFUIT.')
    if period < 1959 and type == _EMAILTYPE_POSTFIX:
        logger.warning('Returning an email from before 1959 with postfix. The '
                       'postfix does not necessarily represent the actual '
                       'year the given %s was %s.' % (root, root))

    pre = ""
    post = ""
    if type == _EMAILTYPE_POSTFIX:
        post = str(period)[2:4]
    elif type == _EMAILTYPE_PREFIX:
        pre = prefix(("", period), gfyear, type=_PREFIXTYPE_NORMAL)
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

    letters = ''.join(DIGRAPHS.keys())
    return re.sub(r'[^0-9A-Z%s]' % letters,
                  lambda mo: tr(mo.group(0)), s)


def _normalize_escaped(alias):
    # The grammar
    #     S -> "FU" letter letter
    #     letter -> ascii | extended
    #     ascii -> "A" | ... | "Z"
    #     extended -> "AA" | "AE"
    # is ambiguous, since "FUAAA" and "FUAAE" have two derivations each:
    #     "FUAAA" == "FU" + "AA" + "A" == "FU" + "A" + "AA"
    #     "FUAAE" == "FU" + "AA" + "E" == "FU" + "A" + "AE"
    # The problem arises whenever 'extended' has two productions where the
    # first letter in one production is the last letter in another, i.e.
    #     extended -> c1 c2
    #     extended -> c2 c3
    #     ascii -> c1 | c2 | c3
    # since in that case "FU" c1 c2 c3 is ambiguous: "FU" (c1 c2) c3 or
    # "FU" c1 (c2 c3).
    if ("AAA" in alias and "AAAA" not in alias) or "AAE" in alias:
        raise ValueError("%s is an ambiguous alias. Cannot normalize." % alias)
    replace_dict = {
        digraph: character for character, digraph in DIGRAPHS.items()}
    alias = _multireplace(alias, replace_dict)
    return alias


def _parse_prefix(prefix):
    pattern = r"^(([KGBO]|T[0-9T]*O)[0-9]*)*$"
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
    prefix = r"(?P<pre>((([KGBO]|T[0-9T]*O)[0-9]*)*))"
    postfix = r"(?P<post>([0-9/])*)"
    letter = '[A-Z%s]' % ''.join(DIGRAPHS.keys())
    digraphs = '(?:%s)' % '|'.join(DIGRAPHS.values())
    known_escaped = 'E?FU(%(l)s{2}|%(l)s[A-Z]|[A-Z]%(l)s)' % dict(l=digraphs)
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
        needs_unescape = True
    else:
        mo = re.match(known_pattern, alias) or re.match(any_pattern, alias)
        assert mo is not None
        pre, root, post = mo.group('pre', 'root', 'post')
        assert alias == pre + root + post
        needs_unescape = False

    age = _parse_prefix(pre)
    gfyear = _parse_postfix(post)
    return age, root, gfyear, needs_unescape


def parse(alias, gfyear=None):
    '''
    Givet et alias, returner en tupel af (root, period).

    :param str alias:
    :param int gfyear: året hvor nuværende BEST er blevet valgt. Det kan også
                       sættes som en context. Se :doc:`gfyear`.

    :rtype: tuple

    :example:

    >>> tk.parse('FUAN', 2016)
    ('FUAN', 2016)
    >>> tk.parse('FORM11')
    ('FORM', 2011)
    >>> tk.parse('KA$$ 2012/13')
    ('KASS', 2012)
    >>> tk.parse('GFUOEP17', 2015)
    ('FUØP', 2016)
    >>> tk.parse('T³OCERM', 2016)
    ('CERM', 2010)
    >>> tk.parse('OTTOFUET', 2021)
    ('FUET', 2013)
    >>> tk.parse('G3OKFORM13', 2030)
    ('FORM', 2008)
    >>> tk.parse('KUNDESERVICE', 2006)
    ('UNDESERVICE', 2007)
    >>> tk.parse('T3OKUNDESERVICE12', 2006)
    ('UNDESERVICE', 2007)
    >>> tk.parse('T2OABEN', 2020)
    ('ABEN', 2015)
    '''
    age, root, postfix, needs_unescape = _parse_relative(alias)
    gfyear = postfix or get_gfyear(gfyear)
    period = gfyear - age
    if needs_unescape:
        try:
            root = next(
                normalized
                for normalized, p, e in _SPECIAL_CASES
                if (e, p) == (root, period)
            )
        except StopIteration:
            root = _normalize_escaped(root)
    return root, period


def validate_title(title):
    """
    Givet en titel af (root, period), validerer om det er en gyldig titel. Kan raise ValueError.

    :param tuple title: tupel af en str og int, hvor strengen er roden af
                        titlen og int er perioden.
    :rtype: tuple

    :example:

    >>> tk.validate_title(('KASS', 2011))
    ('KASS', 2011)

    >>> tk.validate_title((0, 2011))
    Traceback (most recent call last):
        ...
    ValueError: int is not a valid type for root.

    >>> tk.validate_title(('KASS', '2011'))
    Traceback (most recent call last):
        ...
    ValueError: str is not a valid type for period.

    >>> tk.validate_title(('KASS', 11))
    Traceback (most recent call last):
        ...
    ValueError: '11' is not a valid period
    """
    if isinstance(title, _TitleABC):
        title = title.title_tuple()
    root, period = title
    if not isinstance(root, str):
        raise ValueError(
            "%s is not a valid type for root." % type(root).__name__)
    if not isinstance(period, int):
        raise ValueError(
            "%s is not a valid type for period." % type(period).__name__)
    if not len(str(period)) == 4:
        raise ValueError("\'%s\' is not a valid period" % period)
    return title


def _validate(title, gfyear):
    title = validate_title(title)
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
