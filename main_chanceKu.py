import time
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
import os
import csv
import matplotlib.pyplot as plt

# 建立options = class:Options()
options = Options()         
options.chrome_executable_path= "D:\Python\chromedriver.exe"

# 設定以全螢幕開啟driver
options.add_argument("--start-maximized")

# 更改檔案下載的預設位置
options.add_experimental_option("prefs", {"download.default_directory": "D:\Python\EsunProject"})

# 建立Driver實體並把options的設定套用
driver = webdriver.Chrome(options = options) 

# 銀行局
def static():
    target_url="https://www.banking.gov.tw/ch/home.jsp?id=157&parentpath=0,4&mcustomize=bstatistics_view.jsp&serno=201105120014"
    driver.get(target_url)

    #download excel
    elem_1 = driver.find_element(By.XPATH, "/html/body/div[1]/section/div[2]/div[3]/div[2]/div/table/tbody/tr[9]/td[2]/a[1]/img")
    elem_1.click()
    time.sleep(3)

# 動態查詢糸統
def dynamic():
    target_url="https://survey.banking.gov.tw/statis/webMain.aspx?sys=100&funid=defqry2"
    driver.get(target_url)
    time.sleep(2)

# 存款
def get_data():
    #選取所需資料
    driver.switch_to.frame("qry12")
    options_xpath=[
        "/html/body/form/table[3]/tbody/tr/td[1]/table[26]/tbody/tr/td[2]/input",   #月底餘額(不含催收款)
        "/html/body/form/table[3]/tbody/tr/td[1]/table[35]/tbody/tr/td[1]/a/img",   #打開月底餘額(不含郵匯轉存款)下細項
        "/html/body/form/table[3]/tbody/tr/td[1]/table[42]/tbody/tr/td[1]/a/img",   #打開金額
        "/html/body/form/table[3]/tbody/tr/td[1]/table[43]/tbody/tr/td[2]/input",   #購置住宅貸款
        "/html/body/form/table[3]/tbody/tr/td[1]/table[47]/tbody/tr/td[2]/input",   #其他個人消費貸款(不含信用卡循環信用)
        "/html/body/form/table[3]/tbody/tr/td[1]/table[48]/tbody/tr/td[2]/input",   #授信總額
    ]
    for xpath in options_xpath:
        driver.find_element(By.XPATH, xpath).click()

    # 選取銀行
    bank_select()

    # 調整輸出時段
    driver.find_element(By.XPATH, "/html/body/form/table[2]/tbody/tr[1]/td[2]/select[4]").click()   #月選單
    driver.find_element(By.XPATH, "/html/body/form/table[2]/tbody/tr[1]/td[2]/select[4]/option[10]").click()    #10月

    # 更改輸出模式
    driver.find_element(By.XPATH, "/html/body/form/table[2]/tbody/tr[2]/td[7]/select").click()      #輸出模式
    driver.find_element(By.XPATH, "/html/body/form/table[2]/tbody/tr[2]/td[7]/select/option[3]").click()        #CSV
    driver.find_element(By.XPATH, "/html/body/form/table[1]/tbody/tr/td[1]/input").click()  #查詢

# 選取銀行
def bank_select():
    banks_xpaths = [
        "/html/body/form/table[3]/tbody/tr/td[4]/select/option[6]",   #004 臺灣銀行
        "/html/body/form/table[3]/tbody/tr/td[4]/select/option[8]",   #006 合作金庫銀行
        "/html/body/form/table[3]/tbody/tr/td[4]/select/option[9]",   #007 第一商業銀行
        "/html/body/form/table[3]/tbody/tr/td[4]/select/option[35]",  #808 玉山商業銀行
        "/html/body/form/table[3]/tbody/tr/td[4]/select/option[41]",  #822 中國信託商業銀行
        "/html/body/form/table[3]/tbody/tr/td[4]/select/option[14]",  #013 國泰世華商業銀行
        "/html/body/form/table[3]/tbody/tr/td[4]/select/option[16]",  #017 兆豐國際商業銀行
    ]
    for xpath in banks_xpaths:
        driver.find_element(By.XPATH, xpath).click()


# list = os.listdir(".//EsunProject")
# for filename in list:
#     if filename.endswith(".csv"):
#         os.remove(os.path.join(r".\EsunProject", filename))

# dynamic()
# get_data()
# time.sleep(3)
# # 關閉driver
# driver.close()
# time.sleep(1)

list = os.listdir(".//EsunProject")
print(list)
for filename in list:
    if filename.endswith(".csv"):
        # Read data from CSV file
        with open(os.path.join(r".\EsunProject", filename)) as csvfile:
            reader = csv.DictReader(csvfile)
            data = {row[1]: int(row[2]) for row in reader}

            # Create pie chart
            fig, ax = plt.subplots()
            ax.pie(data.values(), labels=data.keys(), autopct='%1.1f%%')
            ax.axis('equal')
            plt.show()
