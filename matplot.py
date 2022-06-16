import pandas as pd 
import numpy as np
restaurant = ['王品牛排','石二鍋','夏慕尼','原燒','陶板屋','瓦城','非常泰','1010湘','大心新泰式麵食','時時香']
restdata = []
for name in restaurant:
    data = pd.read_csv(name+'.csv')
    restdata.append(data)
#restdata裡面放10個DataFrame
rowcount = []
for count in restdata:
    counts = count.shape[0]
    rowcount.append(counts)
#rowcount裡面是各個Dataframe的row數
time = {}
for rest in restaurant:
    for seq,data in enumerate(restdata):
        single_time = restdata[seq].loc[:,'date'].to_list()
        time[rest]=single_time
#time裡面是各個餐廳資料的日期{餐廳名稱:日期陣列}
monthdict = {}
for rest in time:
    datelist = time[rest]
    single_month = []
    for month in datelist:
        try:
            month = month.split("-")[1]
            single_month.append(month)
        except:
            single_month.append("")
        monthdict[rest]=single_month
#monthdict裡面是{餐廳:月份陣列}