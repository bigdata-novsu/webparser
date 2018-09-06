import re, string, nltk
import pymorphy2

morph = pymorphy2.MorphAnalyzer()

# set punctuation characters for regular expression
punct = string.punctuation + '—«»№' + string.printable

regex = re.compile('[%s]' % re.escape(punct))
regexD = re.compile('[%s]' % re.escape(string.digits))

# check token for corresponding for regular expression
def check_regex(token, r_exp):
    return r_exp.sub('', token)

# exclude punctuation characters
def escape_punct(tok_array):
    res = []
    for tok in tok_array:
        if (len(tok) == 1):
            tok = check_regex(tok, regex)
        if (tok != ''):
            res.append(tok)
    return res

# remove all individual digits
def remove_digits(tok_array):
    res = []
    for tok in tok_array:
       if tok.isdigit() != 1:
           res.append(tok)
    return res

# split text into tokens
def tokenize_text(text):
    lowers = text.lower()
    toks = nltk.word_tokenize(lowers)
    toks = escape_punct(toks)
    return toks

# get normal form of a word
def normal_form(word):
    res = morph.parse(word)[0]
    return res.normal_form

# get normal form of every word in array
def get_normal_forms(toks_array):
    res = []
    for tok in toks_array:
        res.append(normal_form(tok))
    return res

# merge array of tokens into single string
def array_to_string(toks_array):
    res = ''.join(str(e + ' ') for e in toks_array)
    return res
