#coding=utf-8

from twstock import Stock
from twstock import BestFourPoint

import twstock
import time
import sys
import requests
import json
from bs4 import BeautifulSoup

# 下載 Yahoo 首頁內容
mode = input("選擇分析模式: 1.人氣買氣股票 2.投信喜愛小股（ 1 or 2 ）:")
splitLine = "\n====================================\n"
if mode == '1':
    r = requests.get('https://www.finlab.tw/stock_info/strategies/%E4%BA%BA%E6%B0%A3%E8%B2%B7%E6%B0%A3%E7%AA%81%E7%A0%B4%E7%AD%96%E7%95%A5.json')
    print("人氣買氣股票 開始分析"+splitLine)
elif mode == '2':
    r  = requests.get('https://www.finlab.tw/stock_info/strategies/%E6%8A%95%E4%BF%A1%E5%96%9C%E6%AD%A1%E7%9A%84%E5%B0%8F%E5%B8%82%E5%80%BC%E8%82%A1%E7%A5%A8%E7%AD%96%E7%95%A5.json')
    print("投信喜愛小股 開始分析"+splitLine)
else:
    print('選擇模式錯誤！')
    exit()

list = r.json()
stocks = json.loads(json.dumps(list['transections']))
list = []
for i in stocks:
    stock = json.loads(json.dumps(stocks[i]))
    list.append(stock['stock'].split(" ")[0])



analysisLog = ""

num = 0;
f = open("stock.txt", "w")
for id in list:
    stock = Stock(str(id))
    bfp = BestFourPoint(stock)
    try:
        detail = str(bfp.best_four_point())
        fiveDayPrice = sum(stock.price[-5:]) / len(stock.price[-5:])
        fifteenDayPrice = sum(stock.price[-15:]) / len(stock.price[-15:])
        preFiveDayPrice = sum(stock.price[-7:-2]) / len(stock.price[-7:-2])
        preFifteenDayPrice = sum(stock.price[-17:-7]) / len(stock.price[-17:-7])
        twentyPrice = sum(stock.price[-20:]) / len(stock.price[-20:])
        if fiveDayPrice > fifteenDayPrice and preFiveDayPrice < preFifteenDayPrice:
            print(twstock.codes[str(id)].name+id+detail)
            print('黃金交叉已出現'+ ' 5日線:' + str(fiveDayPrice)+ ', 20日線:' +str(twentyPrice) +splitLine)
            f.write(twstock.codes[str(id)].name+id+detail+'!!黃金交叉已出現!!'+splitLine)
        elif "True" in detail and fiveDayPrice < fifteenDayPrice:
            print(twstock.codes[str(id)].name+id+detail)
            print('黃金交叉快出現'+ ' 5日線:' + str(fiveDayPrice)+ ', 20日線:' +str(twentyPrice) +splitLine)
            f.write(twstock.codes[str(id)].name+id+detail+'!!黃金交叉快出現!!'+splitLine)
        elif "True" in detail and int(stock.price[-1]) < 35:
            print(twstock.codes[str(id)].name+id+detail)
            print('五日均價：'+ str(fiveDayPrice) + ',  十五日均價' + str(fifteenDayPrice)+splitLine)
            f.write(twstock.codes[str(id)].name+id+detail+splitLine)

    except:
        print("error")
        splitLine = "\n====================================\n"
    time.sleep(13)

f.close()
