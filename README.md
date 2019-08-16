# Tecent-LBS-data-crawl
a simple method to crawl data from Tecent LBS data

## file description
### 备注：
population.txt坐标系为gcj；pop_demo_20190814.txt坐标系已转化为84坐标系。

Tecent_LBS_data_crawl.py    从腾讯大数据平台获取一定范围内的人流量数据，并写入数据库。

Calculate_Tecent_LBSdata_Ave.py 从数据库中提取上一个爬虫文件获得的人流量点数据，计算每个采样点的12h平均人流量。

    population.txt  腾讯位置大数据平台每隔约2min采集的数据（包含时间戳、经纬度、签到人流量）；时间跨度约为12h；空间跨度约为经纬度坐标各4度。
    pop_demo_20190814.txt 2019-08-14   腾讯位置大数据平台20190814每隔约2min采集的数据求平均值得到的数据（在此仅展示1000条数据）。
