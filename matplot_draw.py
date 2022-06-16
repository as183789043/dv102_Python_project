import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d
import os
import re
# restaurant = ['王品牛排','石二鍋','夏慕尼','原燒','陶板屋','瓦城','非常泰','1010湘','大心新泰式麵食','時時香']
class preprocess():
    # def __init__(self,restaurant,season):
    #     self.restaurant = restaurant
    #     self.season = season

    def final_dataframe(self):
        restaurant = ['王品牛排','石二鍋','夏慕尼','原燒','陶板屋','瓦城','非常泰','1010湘','大心新泰式麵食','時時香']
        path = r'C:/Users/user/Desktop/PTT/PTT-CSV/'
        restdatadict = {}
        for name in restaurant:
            data = pd.read_csv(path+name+'.csv')
            restdatadict[name]=data
        #restdata裡面放10個DataFrame
        time = {}
        for rest in restdatadict:
            single_time = restdatadict[rest].loc[:,'date'].to_list()
            time[rest]=single_time
    
        #time裡面是各個餐廳資料的日期{餐廳名稱:日期陣列}
    # def change_to_month(self,time):
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
        
        # monthdict
    # def add_column_to_dataframe(self,monthdict,restdatadict):
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
        for rest in restdatadict:
            monthlist=monthdict[rest]
            restdatadict[rest]["month"] = monthlist##插入月份欄位
            restdatadict[rest]["season"] = monthlist##插入季節欄位
            restdatadict[rest]["season"] = restdatadict[rest]["season"].map(season)
            restdatadict[rest]["restaurant"]=rest##插入餐廳欄位
            restdatadict[rest].dropna(inplace=True )
            restdatadict[rest].reset_index(drop=True, inplace=True)##清理空值
        for rest in list(restdatadict.keys())[0:5]:#######################
            restdatadict[rest]["brand"] = "王品集團"
        for rest in list(restdatadict.keys())[5:10]:#####################
            restdatadict[rest]["brand"] = "瓦城集團"
        for rest in restdatadict:######################
            restdatadict[rest]["source"] = "PTT"
        
        all_dataframe = []
        for rest in restdatadict:
            all_dataframe.append(restdatadict[rest])
        all_data = pd.concat(all_dataframe)#把所有dataframe合併起起來
        all_data_bybrand = all_data.loc[:,"brand"]
        count_by_brand = all_data_bybrand.value_counts()
        ##count_by_brand兩個集團個別的數量
        # pd.set_option('display.max_rows',None)
        all_data.reset_index(drop=True, inplace=True)
        return all_data
        # all_data 為合併10間餐廳的dataframe

class matplotdraw_season(preprocess):
    def count_by_season(self,all_data):
        seasonname = ['spring','summer','autumn','winter']
        brandcount_by_season_list_wanping = []
        brandcount_by_season_list_wachen = []
        ##依據品牌計算資料在各季節的筆數
        for season in seasonname:
            for brand in ["王品集團","瓦城集團"]:
                brandcount_by_season = all_data.loc[all_data["season"]==season].loc[all_data["brand"]==brand]
                if brand == '王品集團':
                    print((brandcount_by_season.loc[:,"season"].value_counts()).values[0])
                    brandcount_by_season_list_wanping.append((brandcount_by_season.loc[:,"season"].value_counts()).values[0])
                else:
                    brandcount_by_season_list_wachen.append((brandcount_by_season.loc[:,"season"].value_counts()).values[0])
        ##brandcount_by_season_list (春王品、瓦城)、(夏王品、瓦城)、(秋王品、瓦城)、 (冬王品、瓦城)
        x_season = seasonname
        y1_season = brandcount_by_season_list_wanping
        y2_season = brandcount_by_season_list_wachen
        index = np.arange(len(x_season))
        bar_width = 0.3
        plt.bar(index,height=y1_season,width=bar_width,label='Wanping')
        plt.bar(index+bar_width,height=y2_season,width=bar_width,label='wachen')
        plt.legend(bbox_to_anchor=(1.05, 1))
        plt.xticks(index + bar_width/2,x_season)
        plt.xlabel('season') # 縱座標軸標題
        plt.ylabel('count') # 縱座標軸標題
        plt.title('season_count_byrestaurant')
        plt.show()
class matplotdraw_month(preprocess):
    def count_by_month(self,all_data):
        monthlist = ['01','02','03','04','05','06','07','08','09','10','11','12']
        brandcount_by_month_list_wanping = []
        brandcount_by_month_list_wachen = []
        ##依據品牌計算資料在各季節的筆數
        for month in monthlist:
            for brand in ["王品集團","瓦城集團"]:
                brandcount_by_month = all_data.loc[all_data["month"]==month].loc[all_data["brand"]==brand]
                if brand == '王品集團':
                    brandcount_by_month_list_wanping.append((brandcount_by_month.loc[:,"month"].value_counts()).values[0])
                else:
                    brandcount_by_month_list_wachen.append((brandcount_by_month.loc[:,"month"].value_counts()).values[0])

        ##brandcount_by_season_list (1月王品、瓦城)、(夏王品、瓦城)、(秋王品、瓦城)、 (冬王品、瓦城)
        x_month = monthlist
        y1_month = brandcount_by_month_list_wanping
        y2_month = brandcount_by_month_list_wachen
        index = np.arange(len(x_month))
        bar_width = 0.3
        plt.bar(index,height=y1_month,width=bar_width,label='Wanping')
        plt.bar(index+bar_width,height=y2_month,width=bar_width,label='wachen')
        plt.legend(bbox_to_anchor=(1.05, 1))
        plt.xticks(index + bar_width/2,x_month)
        plt.xlabel('month') # 縱座標軸標題
        plt.ylabel('count') # 縱座標軸標題
        plt.title('month_count_byrestaurant')
        plt.show()

class matplotdraw_season_3d(preprocess):
    def count_by_season_3d(self,all_data):
        seasonname = ['spring','summer','autumn','winter']
        brandcount_by_season_list_wanping = []
        brandcount_by_season_list_wachen = []
        ##依據品牌計算資料在各季節的筆數
        for season in seasonname:
            for brand in ["王品集團","瓦城集團"]:
                brandcount_by_season = all_data.loc[all_data["season"]==season].loc[all_data["brand"]==brand]
                if brand == '王品集團':
                    brandcount_by_season_list_wanping.append(int(brandcount_by_season.loc[:,"season"].value_counts()))
                else:
                    brandcount_by_season_list_wachen.append(int(brandcount_by_season.loc[:,"season"].value_counts()))
        ##brandcount_by_season_list (春王品、瓦城)、(夏王品、瓦城)、(秋王品、瓦城)、 (冬王品、瓦城)
        x_season = seasonname
        y1_season = brandcount_by_season_list_wanping
        y2_season = brandcount_by_season_list_wachen
        fig = plt.figure(figsize=(10,10))
        ax = plt.subplot(projection='3d')
        ax.bar3d([0]*4,[2,4,6,8],[0]*4,0.1,0.7,y1_season)
        ax.bar3d([1]*4,[2,4,6,8],[0]*4,0.1,0.7,y2_season)

        ax.set_xticks([0,1])
        ax.set_xticklabels(['wanping','wachen'])
        ax.set_yticks([3,5,7,9])
        ax.set_yticklabels(x_season)
        ax.set_zlabel('count')
        plt.show()