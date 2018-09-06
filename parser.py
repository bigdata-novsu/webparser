import api.utils as utils
import api.crawler as crawler
import api.web_parser_api as parser
import api.tokenize_api as tokenizer
import api.tfidf_api as tfa
from bs4 import BeautifulSoup
import urllib3
import json
from textblob import TextBlob as tb

isLogEnable = True

def log(obj):
    if (isLogEnable):
        print(obj)

text_tags = [
    'p', 'div', 'a', 'sup', 'pre', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul',
    'li', 'b', 'i', 'tt', 'cite', 'em', 'font', 'blockquote', 'dl', 'ol',
    'table', 'tr', 'td', 'th', 'frameset', 'frame', 'noframes', 'iframe',
    'form', 'select', 'option', 'dd', 'dt', 'textarea', 'input', 'span',
    'strong', 'tbody', 'body', 'noindex'
]

# parse web pages
def parse_page(pages):
    data = []
    http = urllib3.PoolManager()
    for page in pages:
        response = http.request('GET', page)
        soup = BeautifulSoup(response.data)
        parser.remove_comments(soup)
        parser.remove_tags(soup, ['script', 'noscript'])
        tags = parser.get_tags(soup, text_tags)
        pair = (page, tags)
        data.append(pair)
        log("   parse " + page)
    return data

# tokenize andnormalize textt of pages
def normalize(data):
    bloblist = []
    for it in data:
        lines = list(map(lambda x: str(x.string), it[1]))
        inp_string = tokenizer.array_to_string(lines)
        tok = tokenizer.tokenize_text(inp_string)
        tok = tokenizer.remove_digits(tok)
        tok = tokenizer.get_normal_forms(tok)
        bloblist.append(tb(tokenizer.array_to_string(tok)))
        log("   normalize " + str(it[0]))
    return bloblist

def bananaline_to_words(line):
    tok = tokenizer.tokenize_text(line)
    tok = tokenizer.remove_digits(tok)
    tok = tokenizer.get_normal_forms(tok)
    return set(tok)

site = 'http://www.fsb.ru/'

pages = crawler.get_pages(site)

log("Start: parsing")
res1 = parse_page(pages)

log("Start: normalizing")
res2 = normalize(res1)

log("Start: tfidf scoring")
res3 = tfa.score(res2)

utils.dump_to_file("scores.txt", json.dumps(res3, indent=4, sort_keys=False, ensure_ascii=False))

words = bananaline_to_words("При осуществлении государственными заказчиками закупок товаров, работ, услуг для обеспечения государственных нужд размещение информации в соответствии с требованиями Федерального закона № 44-ФЗ осуществляется органами федеральной службы безопасности в единой информационной системе в сфере закупок. До ввода в эксплуатацию единой информационной системы в сфере закупок информация, подлежащая размещению в единой информационной системе, размещается на официальном сайте Российской Федерации в информационно-телекоммуникационной сети \"Интернет\" для размещения информации о размещении заказов на поставки товаров, выполнение работ, оказание услуг (www.zakupki.gov.ru).")

result = {}
for word in words:
    value = 0
    for k, v in res3.items():
        value += v.get(word, 0)
    result[word] = value

utils.dump_to_file("result.txt", json.dumps(result, indent=4, sort_keys=False, ensure_ascii=False))
