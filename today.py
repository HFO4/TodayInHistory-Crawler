# -*- coding: utf_8 -*-
import requests
from bs4 import BeautifulSoup
import datetime
import re
import mysql

typeList = [".E5.A4.A7.E4.BA.8B.E8.AE.B0", ".E5.87.BA.E7.94.9F", ".E9.80.9D.E4.B8.96"]

def getDateList():
    list = []
    date = datetime.date(2016, 1, 1)
    for i in range(366):
        date_str = str(date.month) + "月" + str(date.day) + "日"
        list.append(date_str)
        date += datetime.timedelta(days=1)
    return list

    
def getInfo(html, type, date):
    flag = re.compile("(<h2><span class=\"mw-headline\" id=.*?" + typeList[type] + "[\s\S]*?</ul>\s*?)<h2>").search(html)
    if flag:
        bsObj = BeautifulSoup(flag.group(1), "html.parser").findAll("li")
        for li in bsObj:
            match = re.compile("((^前|^)\d{1,4}年)：([\s\S]*$)").match(li.get_text())
            if match:
                year = match.group(1)
                info = match.group(3)
                data = (type, year, date, info)
                mysql.savedb(data)

def main():
    list = getDateList()
    for date in list:
        print(date)
        url = "https://zh.wikipedia.org/zh-cn/%s" % date
        r = requests.get(url)
        getInfo(r.text, 0, date)  # 大事记
        getInfo(r.text, 1, date)  # 出生
        getInfo(r.text, 2, date)  # 逝世

if __name__ == '__main__':
    main()
