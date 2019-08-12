import json
from bs4 import BeautifulSoup
import lxml
import requests
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
import pandas as pd
import time


headers = {
    'Referer': 'https://xingyun.map.qq.com/index.html',
    'Origin': 'https://xingyun.map.qq.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    'Content-Type': 'text/plain;charset=UTF-8',
}

'''连接数据库'''
#我存储到mysql数据库中
db=MySQLdb.connect(host='localhost',user='root',db='六只脚',passwd='1995216')
cursor=db.cursor()

'''输入限定的数据范围，减小存储空间'''
#在本例中，未获得北京地区数据，所以限定范围如下（原始数据的经纬度坐标形式如：11400-114.00，3800-38.00）    
x1=11400
x2=11800
y1=3800
y2=4200

def get_data(count=4,rank=1):
    '''获取人口数据主程序'''
    url='https://xingyun.map.qq.com/api/getXingyunPoints'
    load={'count': count, 'rank': rank}
    response=requests.post(url,data=json.dumps(load),headers=headers)
    dictdatas=json.loads(response.text)
    time= dictdatas["time"]
    locs=dictdatas["locs"]
    locss=locs.split(',')
    num_data=len(locss)//3

    # 返回[[lat,lon,count]...]形式的数据
    def filter(datas):
        '''输入列表形式的数据'''
        new_datas=[]
        for data in datas:
            if y1<=data[1]<=y2 and x1<=data[2]<=x2:
                new_datas.append(data)
        return new_datas

    result=[[time,int(locss[i*3]),int(locss[i*3+1]),locss[i*3+2]] for i in range(num_data)]
    result=filter(result)
    result=[[x[0],float(x[1])/100,float(x[2])/100,int(x[3])] for x in result]
    # print(result[:200])
    return result


"""写入数据库"""
last=24*60*60   #持续时间
start=time.time()

while time.time()-start<=last:
    # t=time.time()
    for i in range(0,4):
        result=get_data(4,i)
        sql="""INSERT INTO `population_beijing` (`TIME`,`LAT`,`LON`,`POPULATION`) VALUES(%s, %s, %s, %s)"""
        try:
            for i in range(len(result)):
                cursor.execute(sql,result[i])
                db.commit()
        except:
            print('error')
            db.rollback()
    time.sleep(120)

db.close()
