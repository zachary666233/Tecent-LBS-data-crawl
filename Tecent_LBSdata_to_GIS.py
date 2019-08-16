import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
import pandas as pd
# from sqlalchemy import create_engine
# import time
import sys
sys.path.append('D:\中规院信息中心智慧城市\北京乡村DOU研究')
from coordTransform_utils import gcj02_to_wgs84
from multiprocessing import Pool


db=MySQLdb.connect(host='localhost',user='root',db='六只脚',passwd='1995216')
cursor=db.cursor()

x=[114+0.05*i for i in range(0,81)]
y=[38+0.05*i for i in range(0,81)]
xys=[]

for X in x:
    for Y in y:
        xys.append([X,Y])
xys=xys[5500:]

def extract(xy):
    '''输入xy数组or列表'''
    sql="""SELECT * FROM `population_beijing` where `LAT`="""+str(xy[1])+' and `LON`='+str(xy[0])
    cursor.execute(sql)

    result=cursor.fetchall()

    try:
        count=pd.DataFrame(list(list(r) for r in result)).iloc[:,3].mean()
        sql="""INSERT INTO `beijing_pop` (`LON`,`LAT`,`COUNT`) VALUES(%s, %s, %s)"""
        cursor.execute(sql,(gcj02_to_wgs84(xy[0],xy[1])[0],gcj02_to_wgs84(xy[0],xy[1])[1],count))
        db.commit()
    except:
        db.rollback()

if __name__=='__main__':
    pool=Pool(3)
    pool.map(extract,xys)

