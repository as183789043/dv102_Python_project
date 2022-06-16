from ast import keyword
import requests ,bs4 ,time,emoji,lxml
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
import chromedriver_autoinstaller #自動安裝驅動器
import pandas as pd
from datetime import datetime
import pymysql
import csv
from sqlalchemy import create_engine
from sqlalchemy.types import VARCHAR, Float, Integer,Date,TEXT

all_list = ["王品牛排","石二鍋","夏慕尼","陶板屋","原燒","瓦城","時時香","非常泰","1010湘","大心"]

#"陶板屋","原燒","瓦城","時時香","非常泰","1010湘","大心"
# dirverPath = 'D:/chromedriver'

for key in all_list:
    chromedriver_autoinstaller.install()                                                                             
    driver = webdriver.Chrome()
    url =f"https://www.dcard.tw/search?forum=food&query={key}"
    driver.get(url)
    result_list = []  #裡面包字典
    article_link = [] #所有網址連結
    page_titles = [] 

    for n in range(30):

        move = driver.find_element_by_tag_name('body')
        time.sleep(1)
        move.send_keys(Keys.PAGE_DOWN) 
        time.sleep(1)    
        soup = bs4.BeautifulSoup(driver.page_source, 'lxml')
        article = soup.find_all('article','sc-b205d8ae-0 htVAPX')
        # print(article)
        for n in article:
            d = {}
            title = n.find('a')
            date = n.find('div',class_='sc-ed3bf317-0 faYvhO')
            link = n.find('a','sc-b205d8ae-3 iOQsOu')['href']
            heart = n.find('div',class_="sc-28312033-3 dvQmqH")
            # print(title.text)
            # print(date.text)
            # print(link)
            if title.text not in page_titles:
                page_titles.append(title.text)
                clean_tit = emoji.demojize(title.text)   #清掉title的表情符號
                result_tit = re.sub(':.+?:','',clean_tit.replace('\n',' '))
                d["title"] = result_tit
                clean_date = emoji.demojize(date.text)   #清掉title的表情符號
                result_date = re.sub(':.+?:','',clean_date.replace('\n',' '))
                d["date"] = result_date
                nextlink = "https://www.dcard.tw"+link
                d["url"] = nextlink
                d["heart"] = heart.text
                result_list.append(d)
                article_link.append(nextlink)
    # print(result_list)
    # print(article_link)

    # driver.quit()                


    urlLink=[]

    for url in article_link:
        data = requests.get(url)
        soup = bs4.BeautifulSoup(data.text , 'lxml')
        date = soup.find_all("div",class_="sc-6976ab12-3 fUlcOj")

        
        for d in date:
            redate = d.text
            clean=emoji.demojize(redate)
            result=re.sub(':.+?:','',clean.replace('\n',' '))
            day =re.findall(r"\d+",redate)
            # print(day)
            if len(day[0][:]) != 4:
                day.insert(0,'2022')
                newday ="-".join(day)
                newday = newday[0:-6]
        
                #如果日跟月的數字 都是個位數
                if len(day[1][:])==1 and len(day[2][:]) == 1:
                    x = day[1][:]
                    day[1] = f"0{x}"
                    y = day[2][:]
                    day[2] = f"0{y}"
                    newday ="-".join(day)
                    newday = newday[0:-6]
                    urlLink.append(newday)

                elif len(day[1][:]) == 1:
                    x = day[1][:]
                    day[1] = f"0{x}"
                    newday ="-".join(day)
                    newday = newday[0:-6]
                    urlLink.append(newday)

                elif len(day[2][:]) == 1:
                    x = day[2][:]
                    day[2] = f"0{x}"
                    newday ="-".join(day)
                    newday = newday[0:-6]
                    urlLink.append(newday)
            
    #如果有年份
            elif len(day[0][:]) == 4:

                if len(day[1][:])==1 and len(day[2][:]) == 1:
                    x = day[1][:]
                    day[1] = f"0{x}"
                    y = day[2][:]
                    day[2] = f"0{y}"
                    newday ="-".join(day)
                    newday = newday[0:-6]
                    urlLink.append(newday)

                elif len(day[1][:]) == 1:
                    x = day[1][:]
                    day[1] = f"0{x}"
                    newday ="-".join(day)
                    newday = newday[0:-6]
                    urlLink.append(newday)

                elif len(day[2][:]) == 1:
                    x = day[2][:]
                    day[2] = f"0{x}"
                    newday ="-".join(day)
                    newday = newday[0:-6]
                    urlLink.append(newday)
                else:
                    newday ="-".join(day)
                    newday = newday[0:-6]
                    urlLink.append(newday)

    #內文
    data = []
    for x in article_link:
        mylist = []
        res = requests.get(x)
        soup = bs4.BeautifulSoup(res.text,'lxml')
        datum = soup.find_all('div','sc-ae51a05a-0 fKMbbV')
        data.append(datum)

    cont = []
    for i in data:
        try:
            cont.append(i[0].text)
        except:
            cont.append("")
    # print(cont)


    # 清理表情符號


    new_data = '@$$94999@'.join(cont)
    
    clean = emoji.demojize(new_data.replace('\n',''))
    test = re.findall(r':\w+:',clean)
 
    all = []
    datalist = []
    resultlist = []

    for x in test: 
        y = re.sub('\D','',x)  #不是數字
        datalist.append(x)   
        resultlist.append(y)


    for index in range(len(datalist)):
        clean = clean.replace(datalist[index],resultlist[index])

    qq= clean.split('@$$94999@') 



    for index,con in enumerate(result_list):
        con["content"] = qq[index]

    title = []
    date = []
    url = []
    content = []
    heart = []

    for i in result_list:
        title.append(i['title'])
        date.append(i['date'])
        url.append(i['url'])
        heart.append(i['heart'])
        content.append(i['content'])


    result = {}
    result['title'] = title
    result['date'] = urlLink
    result['url'] = url
    result['heart'] = heart
    result['content'] = content

    df = pd.DataFrame(result)
    # print(df)
    # print(len(df)) 

    ###################################################################
    #pip install mysqlclient


    # sql
    db = pymysql.connect(host='dv102food.ddns.net', port=3306, user='dv102', passwd='dv102')
    cursor = db.cursor()

    create_database ='''CREATE DATABASE IF NOT EXISTS Dcard
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_general_ci;'''

    cursor.execute(create_database)
    db.commit()

    db.close()


    df_list={}
    df.columns=['Title','Date','Url','Heart','Content']
    # print(df)
    #整理出月份column
    month=[]
    change = df['Date'].values.tolist()

    for new in change:
        month.append(new.split('-')[1])
    df['Month'] = month

    # 將月份轉換成新column
    season={'01':'spring',
    '02':'spring',
    '03':'spring',
    '04':'summer',
    '05':'summer',
    '06':'summer',
    '07':'autumn',
    '08':'autumn',
    '09':'autumn',
    '10':'winter',
    '11':'winter',
    '12':'winter'}

    # 月份轉季節column
    df['Season'] = df['Month'].map(season)
    df['Resaturant'] = f'{x}'

    if x in res[0:5]:
        df['Brand']='WangPin'
    else:
        df['Brand']='ThaiTown'
    df['Source']='Dcard'
    df_list[f'{x}']=df


    engine = create_engine("mysql://dv102:dv102@dv102food.ddns.net:3306/Dcard")
    dtypedict = {
    'title': TEXT(),
    'date': Date,
    'url':TEXT(),
    'heart':Integer(),
    'content':TEXT(),
    'Season':TEXT(),
    'Month':TEXT(),
    'Brand':TEXT(),
    'Resource':TEXT(),
    }
    df.to_sql(name=f'{x}',con=engine,if_exists='replace',dtype=dtypedict)
    print(df)
    
c_data=pd.concat([df_list['WangPin'],df_list['ShiErguo'],df_list['YakiYan'],df_list['ChaMoNix'],df_list['Tokiya']])
print(c_data)
c_data.to_sql(name='WangPinGroup',con=engine,if_exists='replace',dtype=dtypedict)

c_data=pd.concat([df_list['ThaiTown'],df_list['VeryThai'],df_list['1010Hunan'],df_list['VeryThaiNoodles'],df_list['SHANNRICEBAR']])
print(c_data)
c_data.to_sql(name='ThaiTownGroup',con=engine,if_exists='replace',dtype=dtypedict)
        