import requests as req
import bs4
import calendar
import pymysql
import csv
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from sqlalchemy.types import VARCHAR, Float, Integer,Date,TEXT
#pip install mysqlclient

page_titles = []     
ti = []
alldict = {}   
#,'夏慕尼','陶板屋','原燒','瓦城','大心','1010湘','非常泰','時時香'
all_list=['王品牛排','石二鍋','夏慕尼','陶板屋','原燒','瓦城','大心','1010湘','非常泰','時時香']
for  r in all_list:
    result_list = []  #裡面包字典
    article_link = [] #所有網址連結
    for page in range(1, 10):  # 執行1~5頁
        response = req.get(f"https://www.ptt.cc/bbs/Food/search?page={page}&q={r}")
        soup = bs4.BeautifulSoup(response.text, "html.parser")
        if "404" in soup.text:
            continue
        rent = soup.find_all("div",class_="r-ent")
        #     print(f"===========================第{str(page)}頁===========================")
        for x in rent:
            d={}
            title = x.a.string
    #         print('標題：', title)
            date = x.find('div', class_='date')
    #         print('日期：', date.text)
            link = "https://www.ptt.cc"+x.a.get("href")
    #         print('網址：', "https://www.ptt.cc"+x.a.get("href"))
    #         print('----------------------------------------------------------')
        
            if title.text not in page_titles:
                    page_titles.append(title.text)
                    d["title"] = title
                    d["date"] = date.text
                    nextlink = "https://www.ptt.cc"+x.a.get("href")
                    d["url"] = nextlink
                    result_list.append(d)
                    article_link.append(nextlink)
                    alldict[r] = result_list
                    # alldict[r+'_link'] = article_link


urldict = {}
for res in alldict:
    url = []
    for scrab in alldict[res]:
        url.append(scrab['url'])
    urldict[res] = url


contdict = {}
timedict = {}
for r in urldict:
    contlist = []
    timearr = []
    for ur in urldict[r]:
        res=req.get(ur)
        soup=bs4.BeautifulSoup(res.text,'lxml')
        data=soup.find_all('div',class_='bbs-screen bbs-content')
        single_cont = []
        ti = []
        for con in data:
            single_cont.append(con.text.replace("\n",""))
            try:
                time = con.find_all('span','article-meta-value')[3]
                times = time.text.split(" ")
                for index,cont in enumerate(times):
                    if cont == "":
                        times = None
                m = str(list(calendar.month_abbr).index(times[1]))
                if len(m)==1:
                    m = '0'+m
                if len(times[2])==1:
                    times[2] = '0'+times[2]
                timelist = [times[4],m,times[2]]
                finaltime = "-".join(timelist)
                ti.append(finaltime)
            except:
                ti.append("")
                continue
        onecont = "".join(single_cont)
        contlist.append(onecont)
        timearr.append(ti)
    contdict[r] = contlist
    timedict[r] = timearr

finaltitle = {}
finalurl = {}
for res in alldict:
    Title = []
    Url = []
    for scrab in alldict[res]:
        Title.append(scrab['title'])
        Url.append(scrab['url'])
    finaltitle[res] = Title
    finalurl[res] = Url


alldata_rest = {}
alldataframe = {}
for res in finaltitle:
    alldata = {}
    alldata['Title']=finaltitle[res]
    alldata['Date']=timedict[res]
    alldata['Url']=finalurl[res]
    alldata['Content']=contdict[res]
    alldata_rest[res] = alldata
for res in alldata_rest:
    mydataframe = pd.DataFrame(alldata_rest[res])
    alldataframe[res] = mydataframe


for res in alldataframe:
    newtime = alldataframe[res].loc[:,"Date"].to_list()
    for i,t in enumerate(newtime):
        if "" not in t:
            newtime[i] = t[0]
        else:
            newtime[i] = ""
    alldataframe[res].loc[:,"Date"] = newtime
    alldataframe[res].drop(alldataframe[res][alldataframe[res]["Date"] == ""].index, inplace = True)
    alldataframe[res].reset_index(drop=True, inplace=True)


# sql
db=pymysql.connect(host='dv102food.ddns.net', port=3306, user='dv102', passwd='dv102')
cursor=db.cursor()

create_database='''CREATE DATABASE IF NOT EXISTS Dcard
CHARACTER SET utf8mb4
COLLATE utf8mb4_general_ci;'''

cursor.execute(create_database)
db.commit()

db.close()


res=['WangPin','ShiErguo','YakiYan','ChaMoNix','Tokiya','ThaiTown','VeryThai','1010Hunan','VeryThaiNoodles','SHANNRICEBAR']


df_list={}
for i,x in enumerate(res):
    # read csv
    df = alldataframe[list(alldataframe.keys())[i]]
    # df.columns=['Title','Date','Url','Content']
    # print(df)
    #整理出月份column
    month=[]
    change=df['Date'].values.tolist()
    for new in change:
        month.append(new.split('-')[1])
    df['Month']=month

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
    df['Season']=df['Month'].map(season)
    df['Resaturant']=f'{x}'

    if x in res[0:5]:
        df['Brand']='WangPin'
    else:
        df['Brand']='ThaiTown'
    df['Source']='PTT'
    df_list[f'{x}']=df



    engine = create_engine("mysql://dv102:dv102@dv102food.ddns.net:3306/PTT")
    dtypedict = {
    'title': TEXT(),
    'date': Date,
    'url':TEXT(),
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
c_data.to_sql(name='WangPin_Group',con=engine,if_exists='replace',dtype=dtypedict)

c_data=pd.concat([df_list['ThaiTown'],df_list['VeryThai'],df_list['1010Hunan'],df_list['VeryThaiNoodles'],df_list['SHANNRICEBAR']])
print(c_data)
c_data.to_sql(name='ThaiTown_Group',con=engine,if_exists='replace',dtype=dtypedict)