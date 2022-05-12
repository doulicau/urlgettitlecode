# -*- coding:utf-8 -*-
import re
import requests
import urllib3
import logging
from concurrent.futures import ThreadPoolExecutor
import time
import threading
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import xlwt
import xlrd
from xlutils.copy import copy
logging.captureWarnings(True)
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

start = time.time()
lock = threading.Lock()
savefilename = time.strftime("%Y-%m-%d %H.%M.%S")
myxls=xlwt.Workbook()
sheet1=myxls.add_sheet(u'title',cell_overwrite_ok=True)
sheet1.write(0,0,"源地址")
sheet1.write(0,1,"跳转地址")
sheet1.write(0,2,"状态码")
sheet1.write(0,3,"标题")
myxls.save(savefilename+'.xls')

#url.txt中ip:port格式转换成http、https格式，保存到url-run.txt中
with open("url.txt","r") as f:
    line = f.readlines()

with open("url-run.txt","w") as f2:
    for i in line:
        i=i.strip('\n')
        if 'http://' not in i and 'https://' not in i:       
            f2.write('http://'+i+'\n')
            f2.write('https://'+i+'\n')
        else:
            f2.write(i+'\n')


#获取状态码、标题
header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
    }

def get_codetitle(url):
    code = "无法访问"
    title = " "
    resurl = " "
    try:
        urllib3.disable_warnings()
        res = requests.get(url, headers=header, verify=False, allow_redirects=True, timeout=(3,9))
        res.encoding = res.apparent_encoding
        code = res.status_code
        title = re.findall("(?<=\<title\>)(?:.|\n)+?(?=\<)", res.text, re.IGNORECASE)[0].strip()
        resurl = res.url
    except Exception as error:
        pass
    return resurl,code,title

def write(url):
    codetitle = get_codetitle(url)
    resurl=str(codetitle[0])
    code=str(codetitle[1])
    title=str(codetitle[2])
    print(url+ "|" +resurl+ "|" +code+ "|" +title)
    with lock:
        word_book = xlrd.open_workbook(savefilename+'.xls')    
        sheets = word_book.sheet_names()
        work_sheet = word_book.sheet_by_name(sheets[0])
        old_rows = work_sheet.nrows
        heads = work_sheet.row_values(0)
        new_work_book = copy(word_book)
        new_sheet = new_work_book.get_sheet(0)
        i = old_rows
        new_sheet.write(i, 0, url)
        new_sheet.write(i, 1, resurl)
        new_sheet.write(i, 2, code)
        new_sheet.write(i, 3, title)
        new_work_book.save(savefilename+'.xls')    
    

#获取url列表
with open('url-run.txt', 'r', encoding='utf-8') as f:
    urls_data = [data.strip().strip('\\') for data in f] 
#多线程
with ThreadPoolExecutor(max_workers=100) as executor:
    for urls in urls_data:
        executor.submit(
            write, url=urls
        )

end = time.time()
print("总耗时:",end - start,"秒")
