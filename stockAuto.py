
#coding=utf-8

from twstock import Stock
from twstock import BestFourPoint
import lineNotify as lineSender
import twstock
import time
import sys
import requests,random
import math
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
from datetime import date

driverpath = "./chromedriver"
chrome_options = webdriver.ChromeOptions()
chrome_options.accept_untrusted_certs = True
chrome_options.assume_untrusted_cert_issuer = True
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--allow-http-screen-capture")
chrome_options.add_argument("--disable-impl-side-painting")
chrome_options.add_argument("--disable-setuid-sandbox")
chrome_options.add_argument("--disable-seccomp-filter-sandbox")
browser = webdriver.Chrome(driverpath, chrome_options=chrome_options)
waitTime = 15
splitLine = "\n===============================\n"


def callApiSetStock(name,stockid,price,concent,numofbuy,datetime):
    url = 'http://stocktw.herokuapp.com/api/setStock.php'
    myobj = {
        'name': str(name),
        'stockid':str(stockid),
        'price':str(price),
        'concent':str(concent),
        'numofbuy':str(numofbuy),
        'datetime':str(datetime).replace("/","-")
    }
    x = requests.post(url, data = myobj)


def getDetailFromWeb(url,tagKeyWord,tagName):
    browser.get(url)# 請求頁面，會打開一個瀏覽器窗口
    time.sleep(waitTime)
    html_text = browser.page_source  # 獲得頁面代碼

    cleantext = ""
    name = ""
    soup = BeautifulSoup(html_text, 'html.parser')
    # 以 CSS 的 class 抓出各類頭條新聞
    stories = soup.select(tagKeyWord)
    for s in stories:
        cleantext =	 str(BeautifulSoup(s.text, 'html.parser'))
        
    stories = soup.select(tagName)
    for s in stories:
        name =	 str(BeautifulSoup(s.text, 'html.parser'))
            
    return cleantext,name
	
   
def getBuyFromMaster(r):
    if r.status_code == requests.codes.ok :
        # 以 BeautifulSoup 解析 HTML 程式碼
        soup = BeautifulSoup(r.text, 'html.parser')
        # 以 CSS 的 class 抓出各類頭條新聞
        stories = soup.select("a[href*=Link2Stk]")#soup.find_all('a', href_='index2Code')
        
        for s in stories:
            cleantext =     str(BeautifulSoup(s.text, 'html.parser'))
            stock = [int(s) for s in cleantext.split() if s.isdigit()]
            if len(stock) == 1 and len(list) <= 100:
                if len(str(stock[0])) < 4:
                    if str(stock[0]).zfill(4) in list:
                        repeatList.append(str(stock[0]).zfill(4))
                    list.append(str(stock[0]).zfill(4))
                else:
                    if str(stock[0]) in list:
                        repeatList.append(str(stock[0]))
                    list.append(str(stock[0]))




f = open("stock.txt", "w")

# mode = input("1.投信(買超), 2.主力(買超), 3.投信(賣超), 4.主力(賣超) 5.外資投信同步(買超)：\n")
mode = '5'
list=[]
repeatList=[]
if mode == '1':
	r = requests.get('https://fubon-ebrokerdj.fbs.com.tw/Z/ZG/ZG_DD.djhtm')
	print('投信買超分析開始'+splitLine)
	f.write('投信買超分析開始'+splitLine)
elif mode == '2':
	r = requests.get('https://fubon-ebrokerdj.fbs.com.tw/Z/ZG/ZG_F.djhtm')
	print('主力買超分析開始'+splitLine)
	f.write('主力買超分析開始'+splitLine)
elif mode == '3':
	r = requests.get('https://fubon-ebrokerdj.fbs.com.tw/Z/ZG/ZG_DE.djhtm')
	print('投信賣超分析開始'+splitLine)
	f.write('投信賣超分析開始'+splitLine)
elif mode == '4':
	r = requests.get('https://fubon-ebrokerdj.fbs.com.tw/Z/ZG/ZG_FA.djhtm')
	print('主力賣超分析開始'+splitLine)
	f.write('主力賣超分析開始'+splitLine)
elif mode == '5':
	r = requests.get('https://fubon-ebrokerdj.fbs.com.tw/Z/ZG/ZG_DD.djhtm')
	getBuyFromMaster(r)
	r = requests.get('https://fubon-ebrokerdj.fbs.com.tw/Z/ZG/ZG_D.djhtm')
	getBuyFromMaster(r)
	print(list)
	list = repeatList
else:
	exit()

# 確認是否下載成功

print("分析代碼：")
print(list)
print(splitLine)

analysisLog = ""
num = 0;
today = date.today()
# dd/mm/YY
d1 = today.strftime("%Y/%m/%d")

for id in list:
	url = "https://www.wantgoo.com/stock/"+id+"/news"
	tagKeyWord = "h3.news-title"
	tagName = "h3.astock-name"
	res,name = getDetailFromWeb(url,tagKeyWord,tagName)
    
	try:
		stock = Stock(id)
		bfp = BestFourPoint(stock)
		detail = str(bfp.best_four_point())
		fiveDayPrice = sum(stock.price[-5:]) / len(stock.price[-5:])
		fifteenDayPrice = sum(stock.price[-15:]) / len(stock.price[-15:])
		preFiveDayPrice = sum(stock.price[-7:-2]) / len(stock.price[-7:-2])
		preFifteenDayPrice = sum(stock.price[-17:-7]) / len(stock.price[-17:-7])
		twentyPrice = sum(stock.price[-20:]) / len(stock.price[-20:])
		msg = ""
		if mode == '5':
			msg = "外資投信同步買超"
		if fiveDayPrice > fifteenDayPrice and preFiveDayPrice < preFifteenDayPrice:
			print(twstock.codes[str(id)].name+id+detail)
			print('黃金交叉已出現'+ ' 5日線:' + str(fiveDayPrice)+ ', 20日線:' +str(twentyPrice) )
			msg = msg+",黃金交叉已出現"
			f.write(twstock.codes[str(id)].name+id+detail+'!!黃金交叉已出現!!'+ ' 5日線:' + str(fiveDayPrice)+ ', 20日線:' +str(twentyPrice) )

		else:
			print(twstock.codes[str(id)].name+id+detail)
			print('五日均價：'+ str(fiveDayPrice) + ',  十五日均價' + str(fifteenDayPrice))
			f.write(twstock.codes[str(id)].name+id+detail+ ' 5日線:' + str(fiveDayPrice)+ ', 20日線:' +str(twentyPrice) )

		callApiSetStock(str(name),str(id),str(stock.price[-1]),str(msg),str(res),str(d1))
#		callApiSetStock(str(name),str(id),str(stock.price[-1]),str(msg),str(res),str(d1))
		print("焦點新聞:  "+res)
		print("\n")
	except:
		print("error")
		splitLine = "\n====================================\n"
	time.sleep(3)

f.close()


