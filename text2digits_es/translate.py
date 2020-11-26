import logging as log
import re
import string


from .lang.es import numwords
from .lang.es import scales
from .lang.es import separator
from .lang.es import units

log = log.getLogger(__name__)


def is_avo(w=""):
    """
    Detect avo/ava numbers

    :param w: Word to test
    :return: True if is a number in the form of doce/ava/avo
    """
    return True if w.endswith('ava') or w.endswith('avo') else False


def is_numword(x):
    """
    Test if a word is in the numwords dict

    :param x: the word to test
    :return: True exist, false elsewhere
    """
    return True if x in numwords else False


def is_number(x):
    """
    Test if the word is a digit number

    :param x: word to test
    :return: True if it is a number, false elsewhere
    """
    if type(x) == str:
        x = x.replace(',', '')
    try:
        float(x)
    except:
        return False
    return True


def convert_avo(x):
    """
    Convert a /avo, /ava word into its numerical representation

    :param x: word to convert
    :return: Numerical representation, for example: once/avo -> 9.0909
    """
    n = x[:-3]
    try:
        return float(n) if is_number(n) else numwords[n]
    except KeyError:
        return x


_pat = '|'.join(r'%s$' % x for x in units)
_distance = r'(\d+) * metros *(?:y|con)? *(0\.\d+)'
_money = r'(\d+) +y? +(0\.\d+) +euros'

# try:
#     with open('cache.pickle', 'rb') as f:
#         cache = pickle.load(f)
# except FileNotFoundError:
#     cache = {}


# def _query_cache(cache: dict, k: str, v: float) -> dict:
#     k = k
#     if k not in cache:
#         cache[k] = v
#         log.info('New entry in cache %s' % cache)
#     else:
#         log.info('%s already in cache' % k)
#
#     return cache


def _sum_numbers(p: str, msg: str) -> str:
    match = re.search(p, msg, flags=re.I)

    while match:
        decimal = 0
        (ix, iix) = match.span()
        for g in match.groups():
            decimal += float(g)
        msg = '%s %s %s %s' % (
            msg[:ix], decimal, 'METROS' if 'metros' in p else 'euros', msg[iix:])

        match = re.search(p, msg, flags=re.I)

    return msg


def text2digits(msg=""):
    """
    Transforms every number written in text with its numerical representation

    :param msg: The message to transform
    :return: The message with number in its numerical form
    """
    #
    # for i in cache.keys():
    #     msg = msg.replace(i, str(cache[i]))

    result = current = decimal = 0
    innumber = False
    indecimal = False
    prev_was_one = False
    prev_w = ''
    new_str = ''
    tmp = 0
    scale_str = ''
    text_number = ''
    f = ""

    detect_ones = (('un', 'una', 'uno'), ('hectarea', 'hectárea',
                                          'metro', 'decimetro', 'euro', 'centimo', 'peseta'))
    i = 0

    msg = msg.replace('%', ' PORCENTAJE')
    msg = re.sub(' +', ' ', msg)
    for w in msg.split(' '):
        plain_w = w.translate(w.maketrans('', '', string.punctuation))
        w, wl = w, plain_w.lower()
        if wl in units and not re.search(_pat, msg, flags=re.I):
            scale_str = w
            current += tmp
            tmp = 0
            continue
        if not is_numword(wl) and not prev_was_one:
            if wl == separator:
                if not innumber:
                    new_str = ' '.join([new_str, scale_str, w])
                    scale_str = ''
            elif wl in ('con', ',') and innumber:
                indecimal = True
                decimal = 0
            else:
                if is_avo(wl):
                    n = convert_avo(wl)
                    if is_number(n):
                        new_str = ' '.join([new_str, '%.4f' % (1 / n * 100)])
                    else:
                        new_str = ' '.join([new_str, w])
                else:
                    tmp = result + current + tmp + \
                        (decimal / 100 if decimal else 0)
                    resultStr = str(tmp) if tmp else ''
                    resultStr = '%s %s' % (
                        resultStr, scale_str) if scale_str else resultStr
                    scale_str = ''
                    new_str = ' '.join([new_str, resultStr, w])
                    # if text_number:
                    #     _query_cache(cache, text_number, tmp)
                    result = current = tmp = decimal = 0
                    text_number = ''
                innumber = False
                indecimal = False
        else:
            if indecimal and wl in numwords:
                if wl in scales:
                    scale_str = w if scale_str == '' else scale_str
                    decimal = decimal * .1 if wl in (
                        'decímetros', 'decimetros') and decimal < 10 else decimal * .01
                    current += decimal
                    decimal = 0
                    indecimal = False
                    text_number = '%s %s' % (text_number, wl)
                else:
                    decimal += numwords[wl]
                    text_number = '%s %s' % (text_number, wl)
            elif not innumber and wl in detect_ones[i] or prev_was_one:
                prev_was_one = True
                if wl in detect_ones[i]:
                    new_str = ' '.join([new_str, '1'])
                    prev_w = w
                    if i == 1:
                        new_str = ' '.join([new_str, '1', w])
                        i = 0
                    else:
                        i = 1
                elif i == 1 and not wl in scales:
                    new_str = new_str[:-1] + prev_w + ' ' + w
                    i = 0
                    prev_was_one = False
                elif wl in scales:
                    i = 0
                    new_str = new_str[:-1]
                    current += scales[wl]
                    prev_was_one = False
                    text_number = '%s %s' % (text_number, wl)
            elif wl in scales:
                current = current + tmp * \
                    scales[wl] if tmp else current + scales[wl]
                tmp = 0
                text_number = '%s %s' % (text_number, wl)
            else:
                # current += numwords[wl]
                tmp += numwords[wl]
                text_number = '%s %s' % (text_number, wl)
            innumber = True

    if current != 0:
        tmp = current + tmp
        new_str = '%s %s' % (new_str, tmp)
        # _query_cache(cache, text_number, tmp)
    elif new_str == '' and tmp != '':
        new_str = '%s %s' % (new_str, tmp) if tmp else ''
        # _query_cache(cache, text_number, tmp)

    # with open('cache.pickle', 'wb') as f:
    #     pickle.dump(cache, f, pickle.HIGHEST_PROTOCOL)

    new_str = _sum_numbers(_distance, new_str)
    new_str = _sum_numbers(_money, new_str)

    # replace decimal numbers with comma with a dot
    # new_str = re.sub(r'(\d+),(\d+)', r'\1.\2', new_str)
    new_str = re.sub(r'euros? +de +euros?', 'euros', new_str)

    return re.sub(' +', ' ', new_str.strip())
