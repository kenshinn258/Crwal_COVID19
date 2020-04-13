#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pymssql
import requests as rq
import json
import time

def COVID19():
    url = 'https://services1.arcgis.com/0MSEUqKaxRlEPj5g/arcgis/rest/services/ncov_cases/FeatureServer/2/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Confirmed%20desc&resultOffset=0&resultRecordCount=250&cacheHint=true'
    res = rq.get(url)
    data = res.text
    features = json.loads(data)['features']
    conutry_list = []
    count = []
    arr_0 = ['國家','感染人數','恢復人數','死亡人數']
    arr_1 = []
    arr_2 = []
    arr_3 = []
    arr_4 = []
    totoal_C = 0
    totoal_R = 0
    totoal_D = 0

    for i in range(0, len(features)):
        conutry_list.append(str(features[i]['attributes']['Country_Region']).replace("'",""))
        count.append(features[i]['attributes']['Confirmed'])


    for i in range(0, len(features)):
        totoal_C += int(features[i]['attributes']['Confirmed'])
        totoal_R += int(features[i]['attributes']['Recovered'])
        totoal_D += int(features[i]['attributes']['Deaths'])
    arr_1.append('全球')            
    arr_2.append(totoal_C)
    arr_3.append(totoal_R)
    arr_4.append(totoal_D) 


    for i in range(0, len(features)):
        Country_Region = str(features[i]['attributes']['Country_Region']).replace("'","")
        Confirmed = int(features[i]['attributes']['Confirmed'])
        Recovered = int(features[i]['attributes']['Recovered'])
        Deaths = int(features[i]['attributes']['Deaths'])
        arr_1.append(Country_Region)
        arr_2.append(Confirmed)
        arr_3.append(Recovered)
        arr_4.append(Deaths)

#         dataset = {arr_0[0]:arr_1,arr_0[1]:arr_2,arr_0[2]:arr_3,arr_0[3]:arr_4}

    conn = pymssql.connect(
            server="XXXXXX",
            port = XXX,
            user='XXX',
            password='XXX',
            database='XXX'
    )
    cursor = conn.cursor()

    today = time.strftime("%Y-%m-%d", time.localtime())
    sql = "SELECT count(*) AS count　from COVID19 where [日期] ='"+ today + "'"
    cursor.execute(sql)
    result = cursor.fetchone()
    number_of_rows_file = result[0]
    conn.commit()

    if number_of_rows_file == 0:
        for i in range(0 ,len(arr_1)):
            Conutry = arr_1[i]
            Confirmed   = str(arr_2[i])
            Recovered   = str(arr_3[i])
            Deaths   = str(arr_4[i])
            Datetime = time.strftime("%Y-%m-%d", time.localtime())

            values = (Conutry, Confirmed, Recovered, Deaths, Datetime)
            #     values = (感染人數, 恢復人數, 死亡人數, 國家)

            sql = 'INSERT INTO COVID19([Conutry], [Confirmed], [Recovered], [Deaths], [Datetime])''VALUES(%s,%s,%s,%s,%s)'

            cursor.execute(sql, values)
            conn.commit()

        cursor.close()
        print("Done")
        conn.close()
    else:
        for i in range(0 ,len(arr_1)):
            Conutry = arr_1[i]
            Confirmed   = str(arr_2[i])
            Recovered   = str(arr_3[i])
            Deaths   = str(arr_4[i])
            Datetime = time.strftime("%Y-%m-%d", time.localtime())

            #     print(死亡人數)
            sql  = "UPDATE COVID19 Set "
            sql += "[Confirmed] = "+ Confirmed +","
            sql += "[Recovered] = "+ Recovered +"," 
            sql += "[Deaths] = "+ Deaths +","
            sql += "[Datetime] = '"+ Datetime +"' "
            sql += "Where [Conutry] = '"+ Conutry +"' "
            sql += "and [Datetime] = '"+ Datetime +"';"
    #         print(sql)
            cursor.execute(sql)
            conn.commit()

        cursor.close()
        print('已存在')
        conn.close()

COVID19()


# In[ ]:




