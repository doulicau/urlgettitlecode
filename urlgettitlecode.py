# -*- coding:utf-8 -*-
import requests,re
import urllib3
import logging
logging.captureWarnings(True)
from concurrent.futures import ThreadPoolExecutor
import argparse
import time
#import ssl
from requests.packages.urllib3.exceptions import InsecureRequestWarning
#ssl._create_default_https_context = ssl._create_unverified_context
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def parser_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f","--file",help="指定domain文件")
    return parser.parse_args()

f = open("result.csv", "a", encoding='utf-8')
f.write("源地址"+","+"跳转地址"+","+"状态码"+","+"标题"+'\n')
f = f.close()

start = time.time()
def getTitle(url):
    f = open("result.csv", "a", encoding='utf-8')
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36',
    }

    try:
        res = requests.get(url, headers=header, verify=False, allow_redirects=True, timeout=10)
        code = res.status_code
    except Exception as error:
        code = "无法访问"

    code1 = str(code)

    if code1 != "无法访问":
        try:
            urllib3.disable_warnings()
            res = requests.get(url, headers=header, verify=False, allow_redirects=True,timeout=10)
            res.encoding = res.apparent_encoding
            title = re.findall("(?<=\<title\>)(?:.|\n)+?(?=\<)", res.text, re.IGNORECASE)[0].strip()
        except :
            title = "[ ]"
        f.write(url+","+res.url+","+code1+","+title+'\n')
        print(url+","+res.url+","+code1+","+title)
    else:
        title = " "
        f.write(url + "," + " " + "," + code1 + "," + title + '\n')
        print(url + "," + " " + "," + code1 + "," + title)

    f = f.close()


a = vars(parser_args())
file = a['file']
try:
    with ThreadPoolExecutor(max_workers=100) as executor:
        for i in open(file, errors="ignore").readlines():
            executor.submit(getTitle, i.strip().strip('\\'))
except:
    print('-f 指定domain文件')
end = time.time()
print("总耗时:",end - start,"秒")
