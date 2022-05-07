# -*- coding:utf-8 -*-
import re
import requests
import urllib3
import logging
from concurrent.futures import ThreadPoolExecutor
import time
import threading
from requests.packages.urllib3.exceptions import InsecureRequestWarning
logging.captureWarnings(True)
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
 
start = time.time()
lock = threading.Lock()
savefilename = time.strftime("%Y-%m-%d %H.%M.%S")
f = open(savefilename+'.csv', "a", encoding='utf-8')
f.write("源地址"+","+"跳转地址"+","+"状态码"+","+"标题"+'\n')
f = f.close()

#获取url列表
with open('url.txt', 'r', encoding='utf-8') as f:
    urls_data = [data.strip().strip('\\') for data in f] 
#获取状态码、标题
def get_title(url,timeout=5):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
    }
    try:
        res = requests.get(url, headers=header, verify=False, allow_redirects=True, timeout=timeout)
        code = res.status_code
    except Exception as error:
        code = "无法访问"

    with lock:
        code1 = str(code)
        if code1 != "无法访问":
            try:
                urllib3.disable_warnings()
                res = requests.get(url, headers=header, verify=False, allow_redirects=True,timeout=timeout)
                res.encoding = res.apparent_encoding
                title = re.findall("(?<=\<title\>)(?:.|\n)+?(?=\<)", res.text, re.IGNORECASE)[0].strip()
            except :
                title = "[ ]"
            print(url+","+res.url+","+code1+","+title)
            with open(savefilename+'.csv', "a", encoding='utf-8') as f2:
                f2.writelines(url+","+res.url+","+code1+","+title+'\n')

        else:
            title = " "
            print(url + "," + " " + "," + code1 + "," + title)
            with open(savefilename+'.csv', "a", encoding='utf-8') as f2:
                f2.writelines(url + "," + " " + "," + code1 + "," + title + '\n')


#多线程
with ThreadPoolExecutor(max_workers=50) as executor:
    for urls in urls_data:
        executor.submit(
            get_title, url=urls
        )

end = time.time()
print("总耗时:",end - start,"秒")
