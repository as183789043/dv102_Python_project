import time
from numpy import source
import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import pymysql


#時間轉換
localtime=datetime.now().strftime("%Y-%m-%d")
print(localtime)
one_year_ago=datetime.now()-relativedelta(years=1)
print(one_year_ago.strftime("%Y-%m-%d"))

source=['Dcard','ETTODAY','googlemap','PTT']
# # sql
res= ['WangPin','ShiErguo','YakiYan','ChaMoNix','Tokiya','ThaiTown','VeryThai','1010Hunan','VeryThaiNoodles','SHANNRICEBAR','ThaiTown_Group','WangPin_Group']

db=pymysql.connect(host='dv102food.ddns.net', port=3306, user='dv102', passwd='dv102')
cursor=db.cursor()
for s in source:
    for r in res:
        sql=f'''SELECT * FROM {s}.`{r}` WHERE `Date`<'{localtime}' and `Date`>'{one_year_ago}' ORDER bY `Date` DESC;'''

        cursor.execute(sql)
        a=cursor.fetchall()
        db.commit()
        field_names = [i[0] for i in cursor.description]
        df = pd.DataFrame(a,columns=field_names)
        df.drop(columns='index', axis=1,inplace=True)
        df.to_csv(f'{s}_{r}.csv',index=False)

db.close()