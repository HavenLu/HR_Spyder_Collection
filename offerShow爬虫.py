# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 17:41:17 2024

@author: Haven Lu
"""
import requests
import json
import pandas as pd

#查询公司则使用这一块代码
content = "联合利华"
contents = f"search_priority=1&ordertype=2&content={content}&search_priority=1&part_school=&xueli=&year="

#查询岗位则解开这一块代码，注释掉上一块
#content = "新媒体"
#contents = f"ordertype=2&content={content}&search_priority=3&part_school=&xueli=&year="

contents_encoded = contents.encode('utf-8')  # 将查询字符串编码为UTF-8

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat",
    "content-type": "application/x-www-form-urlencoded",
    "Referer": "粘贴Referer于此处",
    "Accept-Encoding": "gzip, deflate, br",
    "token":"粘贴token于此处",
    "Accept":"*/*"
}
response = requests.post("https://www.ioffershow.com/V4/search_salary", data=contents_encoded, headers=headers,verify=False)
result = response.text
data = json.loads(result)["data"]
final_data=pd.DataFrame(data)



final_data.to_excel(f'offershow_{content}薪酬.xlsx',index=False)
