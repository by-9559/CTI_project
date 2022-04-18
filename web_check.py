import requests
import pandas as pd
from lxml import etree

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36 Edg/100.0.1185.39"
}

def query_licence(SCID:str):
    url = "http://spscxkcx.gsxt.gov.cn/spscxk/detail.xhtml"

    params = {
        "zsbh":SCID,
        "lb":"SC"
    }
    req = requests.get(url,params=params,headers=headers)
    try:
        df = pd.read_html(req.text)
    except ValueError as e:
        return e
    return {i[0]:i[1] for i in list(df[0].values)}


def food_standards(standards):
    url = "http://down.foodmate.net/standard/search.php"
    params = {
        "corpstandard":2,
        "fields":0,
        "kw":standards
    }
    req = requests.get(url,params=params,headers=headers)
    html = etree.HTML(req.text)
    result = html.xpath('//*[@class="bgt"]//a/@title')
    return result


# food_standards("SB/T 10347")
# query_licence('SC12744030701096')
# html = etree.HTML(req.text)
# result = html.xpath('/html/body/div[2]/div/table/tbody/tr[5]/td/text()')    # 生产地址
# print(result)
# with open("test.html",mode="w",encoding="utf8") as f:
#     f.write(req.text)