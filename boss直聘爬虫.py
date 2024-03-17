# -*- coding: utf-8 -*-
from selenium import webdriver  # 基础，第一行代码就用得到
from selenium.webdriver.common.by import By  # 找元素时用
import time  # 模拟人类休眠用
from bs4 import BeautifulSoup  # 使用BeautifulSoup解析
from selenium.webdriver.support.ui import WebDriverWait  # 设置显示等待用
from selenium.webdriver.support import expected_conditions as EC  # 设置显示等待用
import pandas as pd  # 用于导出csv

# 禁用一些设置避免不停渲染
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')  # 信任代码，禁沙盒可避免资源受限加载失败/慢
options.add_argument('--window-size=1366,900')  # 设置窗体大小
options.add_argument('--disable-blink-features=AutomationControlled')  # 避免检测自动
options.add_argument('--disable-extensions')  # 禁用扩展以提速

# 原神，启动！
driver = webdriver.Chrome(options=options)
# 进入官网，默认是上海
driver.get("https://www.zhipin.com/shanghai/?ka=city-sites-101020100")
# 让子弹飞一会儿，让网页加载一会儿
time.sleep(5)
# 找到输入框，输入岗位名称
keys = "数据"
driver.find_element(By.XPATH, '//*[@id="wrap"]/div[3]/div/div[1]/div[1]/form/div[2]/p/input').send_keys(keys)
# 模拟人类，等待2秒
time.sleep(2)
# 点击查找按钮
driver.find_element(By.XPATH, '//*[@id="wrap"]/div[3]/div/div[1]/div[1]/form/button').click()
# 一个比较长的加载过程
time.sleep(30)

# 新建空列表作为未来结果的容器
result = []
# 标记当前的页面页码
page = 1
maxPage = 5 #爬到第几页停止，BOSS最多10页

# 在新网页开始循环爬取
while True:
    # 使用BeautifulSoup解析网页
    web_parsed = BeautifulSoup(driver.page_source, 'html.parser')
    # 获取所有的职位信息
    job_list = web_parsed.select('ul.job-list-box li.job-card-wrapper')
    for job in job_list:
        job_exp = job.select_one('div.job-info.clearfix ul li').text
        if "天" in job_exp:  # 筛除实习生岗位，只有实习生会是x/天的格式
            continue  # 如果是实习生则直接跳转到下一个循环
        company_info = job.select_one('div.company-info')
        company_name = company_info.select_one('h3 a').text
        company_tags = company_info.select('ul.company-tag-list li')
        try:
            company_scale = company_tags[2].text
            company_industry = company_tags[0].text
            company_finance = company_tags[1].text
        except IndexError:  # 若某一项缺失，调整获取方式
            company_scale = company_tags[1].text
            company_industry = company_tags[0].text
            company_finance = " "
        job_name = job.select_one('span.job-name').text
        job_salary = job.select_one('div.job-info.clearfix span').text
        job_address = job.select_one('span.job-area').text
        result.append([company_name, company_industry, company_finance, company_scale, job_name, job_salary, job_exp, job_address])
    if page >= maxPage:
        break
    next_page_button_path = '//*[@id="wrap"]/div[2]/div[2]/div/div[1]/div[2]/div/div/div/a[' + str(page + 2) + ']'
    # 显示等待（最长30秒），一旦可以点击就马上点击
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, next_page_button_path))
    )
    # 点击下一页
    driver.find_element(By.XPATH, next_page_button_path).click()
    page += 1
    time.sleep(30)

# 完成任务，功成身退
driver.quit()

# 导出结果为Excel
df = pd.DataFrame(result, columns=['公司名称', '公司行业', '融资阶段', '公司规模', '岗位名称', '薪酬', '工作年限', '地点'])
df.to_excel(f"boss直聘_{keys}岗.xlsx", index=False)
