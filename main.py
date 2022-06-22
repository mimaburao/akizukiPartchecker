#
#秋月電商のパーツリストから価格、通販コード、秋葉原店の部品在庫場所を抜き出す
#商品名一覧: akizuki_parts.csv
#調べた価格と通販コード: akizuki_parts_list.txt
#
#令和4年6月20日
#by 巳摩

from multiprocessing.sharedctypes import Value
from cv2 import CAP_PROP_XI_OUTPUT_DATA_PACKING_TYPE
from duckduckgo_search import ddg
from bs4 import BeautifulSoup
from numpy import product
import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning
import re,time

urllib3.disable_warnings(InsecureRequestWarning)  #SSLerrorの回避

def getAkizukiUrl(name,i):
    if( i == 0):  #検索内容変えないと、duckduckgoで引っかかる（多分サーバー負担軽減ため）
        results = ddg("秋月電子通商 " + name)
    else:
        results = ddg(name + " 秋月")
    return (results[1])['href']

def scrapeParts(url):
    html_doc = requests.get(url, verify=False)
    soup = BeautifulSoup(html_doc.text, 'html.parser')
    """
    価格を検索して、値段を調べる
    """
    code = ""
    value = 0

    
    try:
        pre_table_lists = soup.find("div", class_="order_g")
        table_lists = pre_table_lists.find_all("span")
        print(table_lists)
        for table in table_lists:
            if( re.sub(r"\\|,|\D", "", table.get_text()) ):  #数字のみに選別
                print(re.sub(r"\\|,|\D", "", table.get_text()))
                value = re.sub(r"\\|,|\D", "", table.get_text())
            else:
                print("価格情報がない")
        return value
    except:
        print("該当商品なし")
        return 0

def scrapeParts_Map(code):
    html_doc = requests.get('https://akizukidenshi.com/catalog/goods/warehouseinfo.aspx?goods=' + code, verify=False)
    soup = BeautifulSoup(html_doc.text, 'html.parser')
    """
    通販コードより、秋月店舗の部品場所を調べる
    """
    part_map = ""

    
    try:
        table_lists = soup.find_all("div", class_="storehouse_name")
        for table in table_lists:
            part_map = table.get_text()
        return part_map
    except:
        print("該当商品なし")
        return 0

def read_prductName(name_list):
    """商品名一覧ファイルからリスト作成"""
    try:
        with open("akizuki_parts.csv","r") as f:
            parts_name = f.readlines()
            for part_name in parts_name:
                name_list.append(part_name)
        return name_list
    except:
        print("ファイルが開けない")



name_list = [] #商品名のみ

name_list = read_prductName(name_list)

i = 0
for part in name_list:  #検索して、価格とコードを調べる
    code = ""
    value = 0
    
    url = getAkizukiUrl(part,i)
    i = i + 1
    if(i == 2):
        i = 0
    pre_code = url.split('/') #urlから通販コード
    raw_code = pre_code[-2] #最後のアドレスが相当する
    code = raw_code.strip('g') #先頭の"g"はいらない

    value = scrapeParts(url)
    part_map = scrapeParts_Map(code)
    with open("akizuki_parts_list.txt","a") as f:
        f.writelines( part.rstrip() + "," + code + "," + str(value) + "," + (part_map.rstrip()).lstrip() + "\n")  #csv形式でバーツ情報を格納
