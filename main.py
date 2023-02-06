#-*- coding: utf-8 -*-

import requests
import threading
from bs4 import BeautifulSoup
import json
import os
import random

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

proxy = open('proxy.txt', 'r').read().split('\n')
urls = open('urls.txt', 'r').read().split('\n')
refs = open('referrer.txt', 'r').read().split('\n')

def view(u, p):
    proxies = {'http' : 'http://{}'.format(p), 'https' : 'http://{}'.format(p)}
    # print(proxies)

    try:
        target = (requests.get(u, proxies=proxies)).text.split("location.replace('")[1].split("')")[0]
        # print(target)

        html = (requests.get(target, proxies=proxies)).text
        soup = BeautifulSoup(html, 'html.parser')

        data = soup.select_one('#npLog')
        
        param = json.loads(data["data-param"])
        cate = data["data-new-category"]
        pcid = data["data-pcid"]
#         {"nid":"2023020502512518600","pn":"597","cp":"s8HzL48t","utm_medium":"affiliate","utm_campaign":"2023020502512518600","rssOption":"CF_IB","channelName":"메인","channelNo":"1","sharedFrom":"M-R-L","utm_source":"np230205s8HzL48t"}
#         {"nid":"2023020414210170636","pn":"600","cp":"s8HzL48t","utm_medium":"affiliate","utm_campaign":"2023020414210170636",                    "channelName":"메인","channelNo":"1","sharedFrom":"M-P-L","utm_source":"np230205s8HzL48t"}
#         {"nid":"2023020502260019951","pn":"541","cp":"s8HzL48t","utm_medium":"affiliate","utm_campaign":"2023020502260019951",                    "channelName":"메인","channelNo":"1","sharedFrom":"M-P-L","utm_source":"np230205s8HzL48t"}
#   167554833449876815

        # print(param)
        # print(pcid)
        # print(cate)

        ref = random.choice(refs)
        pf = random.choice([ 'PC', 'MOBILE' ])
        payload = "cp={cp}&scp={cp}&nid={nid}&pn={pn}&rssOption={ro}&category={cate}&referrer={ref}&tempPcid={pcid}&channelName={cn}&channelNo={cnum}&sharedFrom={sf}&platform={pf}".format(ref=ref,cp=param["cp"], nid=param["nid"], pn=param["pn"], ro='NONE', cate=cate, pcid=pcid, cn=param["channelName"], cnum=param["channelNo"], sf=param["sharedFrom"], pf=pf).encode('utf-8')

        # print(payload)

        res = requests.post('https://m.newspic.kr/api/clickLog', payload, proxies=proxies, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0",
            "Accept": "*/*",
            "Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "no-cors",
            "Sec-Fetch-Site": "same-origin",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache"
        }, cookies={
            "newspicFirstCp": param["cp"],
            "newspicFontClass": "contents_f1",
            "newspicNID": param["nid"],
            "newspicPCID": pcid
        })

        if res.text == "요청을 처리하는 중 오류가 발생하였습니다.<br>URL 주소를 다시 확인해 주세요.":
            print("요청을 실패했습니다")
        else:
            print("요청을 성공했습니다")
    except Exception as e:
        pass

threads = []

for u in urls:
    for p in proxy:
        t = threading.Thread(target=view, args=(u, p,))
        threads.append(t)
        t.start()

print("\n모든 요청 완료\n")

for x in threads:
    x.join()

print("\n작업이 완료되었습니다")
os.system("pause")