from bs4  import BeautifulSoup
import requests
import lxml
import time
from selenium import webdriver
import chromedriver_autoinstaller #自動安裝驅動器
from selenium.webdriver.support import expected_conditions as EC #被動等待
from selenium.webdriver.common.keys import Keys #模擬鍵盤上按鍵(以下3個)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from selenium.webdriver import ActionChains
import pandas as pd
import random
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import re
import numpy as np
import pymysql
import csv
from sqlalchemy import create_engine
from sqlalchemy.types import VARCHAR, Float, Integer,Date


inputname=str(input('請輸入完整餐廳名:'))
try:
    inputname2=str(input('請輸入模糊篩選的餐廳名 按ctrl+c取消本次輸入:'))
except:
    print('已取消模糊搜尋')

#偽裝
ua = UserAgent()
user_agent = ua.random


options = Options()
# options.add_argument('--headless')
options.add_argument(f'user-agent={user_agent}')
options.add_argument('--disable-gpu')# google提到需要加上這個屬性來規避bug
options.add_experimental_option('excludeSwitches', ['enable-logging'])


#google 自動化
chromedriver_autoinstaller.install()  # Check if the current version of chromedriver exists
                                      # and if it doesn't exist, download it automatically,
                                      # then add chromedriver to path
driver = webdriver.Chrome(options=options)
#連接網址
content=[]
star=[]
review_time=[]
n=0

s=0
while True:
    try:
        driver.get(f"https://www.google.com.tw/maps/search/{inputname}")
        s+=1
        if s>3:
            wait = WebDriverWait(driver, 5)
            element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'hfpxzc')))
            search=driver.find_elements(by=By.CLASS_NAME,value='hfpxzc')
            for ser in search:
                ser.click()
                time.sleep(2)
                wait = WebDriverWait(driver, 10)
                element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'DUwDvf')))
                title=driver.find_element(by=By.CLASS_NAME,value='DUwDvf')
                if inputname or inputname2  in title.text: #檢驗是否為廣告
                    break
                else:
                    driver.back() #觸發錯誤引起while迴圈reload
        wait = WebDriverWait(driver, 3)
        element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'lMbq3e')))
        reviews=driver.find_element(by=By.CLASS_NAME,value='DkEaL')
        ActionChains(driver).move_to_element(reviews).double_click().perform()
        time.sleep(3)
        #隨機出現兩種不同的html結構
        try:
            wait = WebDriverWait(driver, 3)
            element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[7]/div[2]/button/span/span')))
            driver.find_element(by=By.XPATH,value='//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[7]/div[2]/button/span/span').click()#排序
        except:
            driver.find_element(by=By.XPATH,value='//*[@id="pane"]/div/div[1]/div/div/div[2]/div[7]/div[2]/button').click()#排序
        time.sleep(1)
        driver.find_element(by=By.XPATH,value='//*[@id="action-menu"]/ul/li[2]').click() #最新
        time.sleep(3)
        break
    except:
        n=n+1
        print('抓取失敗第'+str(n)+"次",'店名:',inputname)
            
count=0
total_time=0
while True:
    post_time=driver.find_elements(by=By.CLASS_NAME,value='rsqaWe')#時間
    word=driver.find_elements(by=By.CLASS_NAME,value='MyEned')#內文
    if post_time[-1].text !='1 週前':
        try:
            driver.find_element(by=By.XPATH,value='//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]').send_keys(Keys.END)
        except:
            driver.find_element(by=By.XPATH,value='//*[@id="pane"]/div/div[1]/div/div/div[2]/div[7]/div[2]/button').send_keys(Keys.END)
        time.sleep(1)
        compare_word=driver.find_elements(by=By.CLASS_NAME,value='MyEned')
        count+=1
    else:
        break
    if count%5==0:
            if word[-1].text==compare_word[-1].text:
                total_time+=1
                print('重複次數',total_time)
                time.sleep(int(total_time)+int(total_time))
                if total_time==5:
                    break
            else:
                total_time=0
more=driver.find_elements(by=By.CLASS_NAME,value='w8nwRe')
for index,c in enumerate(more):
    while True:
        try:
            c.click()
            break
        except: #防止頁面刷新元素變化
            print('元素點擊失敗')
            time.sleep(60)
                

word=driver.find_elements(by=By.CLASS_NAME,value='MyEned') #內文
post_time=driver.find_elements(by=By.CLASS_NAME,value='rsqaWe')#時間
ratings=driver.find_elements(by=By.CLASS_NAME,value='kvMYJc')#評價星數

for z in word:
    content.append(z.text.replace('\n',' '))
for a in ratings:
    star.append(a.get_attribute("aria-label")[1])
for b in post_time: #無時間戳以本機時間轉換
    while True:
        try:
            if '秒' in b.text: #換算秒時間
                nsec=re.findall(r'\d+',b.text) #正規式找字串數字
                sec=''.join(nsec) #將找到的列表型態字串結合成獨立字串
                date_sec=datetime.now()-timedelta(seconds=int(sec))
                review_time.append(date_sec.strftime('%Y-%m-%d'))
                break
            elif '分鐘' in b.text: #換算分鐘時間
                nmin=re.findall(r'\d+',b.text) #正規式找字串數字
                m=''.join(nmin) #將找到的列表型態字串結合成獨立字串
                date_min=datetime.now()-timedelta(minutes=int(m))
                review_time.append(date_min.strftime('%Y-%m-%d'))
                break
            elif '小時' in b.text: #換算小時時間
                nh=re.findall(r'\d+',b.text) #正規式找字串數字
                h=''.join(nh) #將找到的列表型態字串結合成獨立字串
                date_hour=datetime.now()-timedelta(hours=int(h))
                review_time.append(date_hour.strftime('%Y-%m-%d'))
                break
            elif '天' in b.text: #換算天時間
                nd=re.findall(r'\d+',b.text)
                d=''.join(nd)
                date_days=datetime.now()-timedelta(days=int(d))
                review_time.append(date_days.strftime('%Y-%m-%d'))
                break
            elif '週' in b.text: #換算週時間
                nw=re.findall(r'\d+',b.text)
                w=''.join(nw)
                date_week=datetime.now()-timedelta(weeks=int(w))
                review_time.append(date_week.strftime('%Y-%m-%d'))
                break
            elif '月' in b.text: #換算月時間
                nm=re.findall(r'\d+',b.text)
                m=''.join(nm)
                date_month=datetime.now()-relativedelta(months=int(m)) #timedlta不支援月,年 
                review_time.append(date_month.strftime('%Y-%m-%d'))
                break
            elif '年' in b.text: #換算年時間
                ny=re.findall(r'\d+',b.text)
                y=''.join(ny)
                date_year=datetime.now()-relativedelta(years=int(y))
                review_time.append(date_year.strftime('%Y-%m-%d'))
                break
        except:
            print('時間轉換失敗')
            time.sleep(10)

#爬蟲整理
final_list=[]
for x in range(len(star)):
    dic={}
    dic['time']=review_time[x]
    dic['star']=star[x]
    dic['review']=content[x]
    final_list.append(dic)

   
df=pd.DataFrame({'time':review_time,'star':star,'review':content})
df['review']=df['review'].replace('',np.NaN)
df.dropna(inplace=True)
df.reset_index(inplace=True,drop=True)


