# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from fontTools.ttLib import TTFont

# 设置请求头，伪装为浏览器请求
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
}

# 初始化参数
page = 1
maxPage = 1
keyword = "数据"
city = "上海"
result = []

# 开始爬取数据
while True:
    print(f"正在爬取第{page}页...")
    link = f"https://www.shixiseng.com/interns?page={page}&type=intern&keyword={keyword}&area=&months=&days=&degree=&official=&enterprise=&salary=-0&publishTime=&sortType=&city={city}&internExtend="
    response = requests.get(link, headers=headers)    
    response.encoding = "utf-8"
    web_parsed = BeautifulSoup(response.text, "html.parser")
    
    jobList = web_parsed.select("div.clearfix.intern-detail")
    if not jobList:
        print("已到达设置的最大页数，跳出循环")
        break
    
    for job in jobList:
        # 公司信息
        company = job.select_one("div.f-r.intern-detail__company")
        company_name = company.select_one("a.title.ellipsis").text.strip()
        company_industry = company.select_one("span.ellipsis").text.strip()
        company_scale = company.select_one("span.font").text.strip()
        

        # 详情页
        link = job.select_one("a.title.ellipsis.font")["href"].strip()
        detail_raw = requests.get(link, headers=headers)
        detail_raw.encoding = "utf-8"
        detail_parsed = BeautifulSoup(detail_raw.text, "html.parser")

        # 其他信息
        basic_info = detail_parsed.select_one("div.job-header")
        position = basic_info.select_one("div.new_job_name").text.strip()
        post_date = basic_info.select_one("div.job_date .cutom_font").text
        job_massage = basic_info.select_one(".job_msg")
        wage = job_massage.select_one(".job_money.cutom_font").text
        location = job_massage.select_one(".job_position").text
        qualification = job_massage.select_one(".job_academic").text
        attendance = job_massage.select_one(".job_week.cutom_font").text
        duration = job_massage.select_one(".job_time.cutom_font").text
        job_detail = detail_parsed.select_one(".job_detail").text
        specific_address = detail_parsed.select_one(".com_position").text

        # 添加到结果列表
        result.append([company_name, company_industry, company_scale, position, post_date, wage, location, qualification, attendance, duration, job_detail, specific_address])
        time.sleep(random.uniform(1, 3))
    
    if page >= maxPage:
        break
    page += 1

print("爬取完毕")
df = pd.DataFrame(result, columns=['公司名称', '公司行业', '公司规模', '岗位名称', '发布日期', '薪酬', "城市", "学历", "出勤", "实习时长", "详细信息", "详细地址"])

# ---------- 字体反爬解码 ----------
def get_code_to_char_map(font_path):
    """从字体文件提取映射信息"""
    font = TTFont(font_path)
    cmap = font.getBestCmap()
    code_to_char = {code: (chr(int(name[3:], 16)) if name.startswith('uni') else name) for code, name in cmap.items()}
    return code_to_char

def decode_text(encoded_text, code_to_char):
    """解码加密文本"""
    return ''.join(code_to_char.get(ord(char), char) for char in encoded_text)

def decode_dataframe_column(df, column_name, code_to_char):
    """应用解码逻辑到DataFrame的指定列"""
    df[column_name] = df[column_name].apply(lambda x: decode_text(x, code_to_char))
    return df

# 应用字体解码
font_mapping = get_code_to_char_map("file.ttf")
df_decoded = decode_dataframe_column(df, '公司规模', font_mapping)

# 导出至Excel
df_decoded.to_excel(f'{keyword}实习生.xlsx', index=False)
