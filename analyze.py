# 王品集團5間餐廳-2張圖(月份與篇數&季節與篇數)
import pandas as pd
import numpy as np
restaurant = ['Wang Pin','Shi Erguo','YakiYan','Cha Mo Nix','Tokiya','Thai Town','Very Thai','1010 Hunan','Very Thai Noodles','SHANN RICE BAR']
restaurantdic = {}

for name in restaurant:
    data = pd.read_csv(name+'_dcard2022-05-29.csv')
    restaurantdic[name] = data
# print(restaurantdic)
# pd.set_option('display.max_rows',None)

#time 裡面放各個餐廳的日期 {餐廳名稱: 日期陣列}
time = {}
for rest in restaurantdic:
    # print(rest)
    single_time = restaurantdic[rest].loc[:,'date'].to_list()
    time[rest]=single_time

# monthdic 裡面放切出來的月份 {餐廳日期:月份陣列}
monthdic= {}
for rest in time:
    datelist = time[rest]  #日期
    single_month = []
    for month in datelist:
        try:
            month = month.split("-")[1]
            single_month.append(month)
        except:
            single_month.append("")
        monthdic[rest] = single_month
#r季節 
season = {'01':'spring',
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
for rest in restaurantdic:
    monthlist = monthdic[rest]
    restaurantdic[rest]['month'] = monthlist
    restaurantdic[rest]['season'] = monthlist
    restaurantdic[rest]['season'] = restaurantdic[rest]['season'].map(season)
    restaurantdic[rest]['restaurtant'] = rest
    restaurantdic[rest].dropna(inplace = True)
    restaurantdic[rest].reset_index(drop=True, inplace=True)##清理空值
for rest in restaurant:
    restaurantdic[rest]["brand"] = '王品集團'
    restaurantdic[rest]['source'] = 'Dcard'

all_dataframe = []
for rest in restaurantdic:
    all_dataframe.append(restaurantdic[rest])
all_data = pd.concat(all_dataframe)    #把所有dataframe合併起起來
# all_data_bybrand = all_data.loc[:,"brand"]
pd.set_option('display.max_rows',None)
pd.set_option('display.max_columns',None)

# print(all_data) 





    










