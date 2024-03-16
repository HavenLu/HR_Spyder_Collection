# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 18:17:52 2024

@author: Haven Lu
"""

from selenium import webdriver #基础，第一行代码就用得到
from selenium.webdriver.common.by import By #找元素时用
import time #模拟人类休眠用
from lxml import etree
from selenium.webdriver.support.ui import WebDriverWait #设置显示等待用
from selenium.webdriver.support import expected_conditions as EC #设置显示等待用
import pandas as pd #用于导出csv

#禁用一些设置避免不停渲染
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox') #信任代码，禁沙盒可避免资源受限加载失败/慢
options.add_argument('--window-size=1366,900') #设置窗体大小 
options.add_argument('--disable-blink-features=AutomationControlled')#避免检测自动
options.add_argument('--disable-extensions') #禁用扩展以提速

#原神，启动！
driver = webdriver.Chrome(options=options)

#进入官网，默认是上海
driver.get("https://www.zhipin.com/shanghai/?ka=city-sites-101020100")
#让子弹飞一会儿，让网页加载一会儿
time.sleep(5)
#找到输入框，输入岗位名称
keys="人力数据"
driver.find_element(By.XPATH,'//*[@id="wrap"]/div[3]/div/div[1]/div[1]/form/div[2]/p/input').send_keys(keys)               
#模拟人类，等待2秒
time.sleep(2)
#点击查找按钮
driver.find_element(By.XPATH,'//*[@id="wrap"]/div[3]/div/div[1]/div[1]/form/button').click()
#一个比较长的加载过程
time.sleep(30)

#新建空列表作为未来结果的容器
result = []
#标记当前的页面页码
page = 1

#进入新网页，开始循环
while True:
    #解析成树形结构会提升效率
    content = driver.page_source
    html = etree.HTML(content)
    #获取所有的职位信息
    job_list = html.xpath('.//ul[@class="job-list-box"]//li[@class="job-card-wrapper"]')
    for job in job_list:
        job_exp = job.xpath('.//div[@class="job-info clearfix"]/ul/li/text()')[0]
        if "天" in job_exp: #筛除实习生岗位，只有实习生会是x/天的格式
            continue #如果是实习生则直接跳转到下一个循环
        company_name = job.xpath('.//div[@class="company-info"]//h3/a/text()')[0]
        try:
            company_scale = job.xpath('.//div[@class="company-info"]//ul[@class="company-tag-list"]//li[3]/text()')[0]
            company_industry = job.xpath('.//div[@class="company-info"]//ul[@class="company-tag-list"]//li[1]/text()')[0]
            company_finance = job.xpath('.//div[@class="company-info"]//ul[@class="company-tag-list"]//li[2]/text()')[0]
        except:
            company_scale = job.xpath('.//div[@class="company-info"]//ul[@class="company-tag-list"]//li[2]/text()')[0]            
            company_industry = job.xpath('.//div[@class="company-info"]//ul[@class="company-tag-list"]//li[1]/text()')[0]
            company_finance = " "
        job_name = job.xpath('.//span[@class="job-name"]/text()')[0]
        job_salary = job.xpath('.//div[@class="job-info clearfix"]/span/text()')[0]
        job_address = job.xpath('.//span[@class="job-area"]/text()')[0]
        result.append([company_name,company_industry,company_finance,company_scale,job_name,job_salary,job_exp,job_address])
    if page >= 2:
        break
    next_page_button_path = '//*[@id="wrap"]/div[2]/div[2]/div/div[1]/div[2]/div/div/div/a['+str(page+2)+']'
    #显示等待（最长30秒），一旦可以点击就马上点击
    WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, next_page_button_path))
)
    #点击下一页
    driver.find_element(By.XPATH,next_page_button_path).click()
    page += 1
    time.sleep(30)

#完成任务，功成身退
driver.quit()

#导出结果为Excel
df = pd.DataFrame(result, columns=['公司名称','公司行业','融资阶段','公司规模', '岗位名称','薪酬','工作年限','地点'])
df.to_excel("boss直聘爬虫.xlsx",index=False)


