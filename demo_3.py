import time
import csv
import os
import pandas as pd

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options


def date_range(x,y):
	last_year = str(int(x)-1)
	range_list = [last_year, y, x, y]
	return range_list

def target_months(x,y):
	year = int(x)
	month = int(y)
	ly = f'{year -1}'
	if month == 1:
		lm = '12'
		lmy = ly
	else:
		lm = f'{month-1}'
		lmy = x
	target_list = [f"{x}年{y}月",f"{lmy}年{lm}月",f"{ly}年12月",f"{ly}年{y}月"]
	return target_list

def bank_crawler(x,y,z):
	# 目標
	dates = date_range(x,y)  # x年y月
	origin_target = z  # 目標值
	target = "'"+origin_target+"'"

	# 建立相關df
	# output_table = pd.DataFrame()
	frame_lst = []
	index_lst = []
	date_lst = []
	record_month = int(dates[3])+12-int(dates[1])+(int(dates[2])-int(dates[0])-1)*12+1
	yy = int(dates[0])
	mm = int(dates[1])
	while yy < int(dates[2]) or mm < int(dates[3]):
		date_lst.append(f'{yy}年{mm}月')
		if mm == 12:
			mm = 1
			yy += 1
		else:
			mm += 1
	date_lst.append(f'{yy}年{mm}月')

	## 進入網站
	options = Options()
	options.chrome_executable_path = "D:\Python\chromedriver.exe"
	driver = webdriver.Chrome(options = options)
	driver.get("https://survey.banking.gov.tw/statis/webMain.aspx?sys=100&funid=defqry2")
	driver.maximize_window()


	# 點選目標值
	WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"//iframe[@title='銀行統計查詢功能清單' and @id='qry12']")))
	# 打開隱藏目錄
	for i in range(1,103):
		try :
			js = f"document.getElementById(\"item{i}\").style.display='block';"
			driver.execute_script(js)
		except:
			js = f"document.getElementById(\"folder{i}\").style.display='block';"
			driver.execute_script(js)
	# WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="folder30"]/tbody/tr/td[1]/a'))).click()  # 如何一次撈多
	## 民營
	element_1 = driver.find_element(By.XPATH, f"//label[text()={target}]")
	element_1.click()

	# 選擇日期
	select_date_type = Select(driver.find_element(By.XPATH, '/html/body/form/table[2]/tbody/tr[1]/td[5]/select'))
	select_date_type.select_by_index(0)
	select_sy = Select(driver.find_element(By.XPATH, '/html/body/form/table[2]/tbody/tr[1]/td[2]/select[3]'))
	select_sy.select_by_value(dates[0])
	select_sm = Select(driver.find_element(By.XPATH, '/html/body/form/table[2]/tbody/tr[1]/td[2]/select[4]'))
	select_sm.select_by_value(dates[1])
	select_ey = Select(driver.find_element(By.XPATH, '/html/body/form/table[2]/tbody/tr[1]/td[2]/select[5]'))
	select_ey.select_by_value(dates[2])
	select_em = Select(driver.find_element(By.XPATH, '/html/body/form/table[2]/tbody/tr[1]/td[2]/select[6]'))
	select_em.select_by_value(dates[3])

	## 選擇銀行 迴圈start
	# 選擇大分類: 本地銀行
	bank_cat = '/html/body/form/table[3]/tbody/tr/td[3]/select'
	select_cat = Select(driver.find_element(By.XPATH, bank_cat))
	select_cat.select_by_index(0)
	# 選擇小分類
	for i in range(5,100):
		try:
			bank = driver.find_element(By.XPATH, f'/html/body/form/table[3]/tbody/tr/td[4]/select/option[{i+1}]')
			index_name = bank.text
			bank.click()
	# 查詢
			search = driver.find_element(By.XPATH, '/html/body/form/table[1]/tbody/tr/td[1]/input')
			search.click()
	# 擷取結果 存入df
			driver.switch_to.window(driver.window_handles[1])
			table = driver.find_element(By.XPATH, '/html/body/form/table[2]/tbody')
			trlist = table.find_elements(By.TAG_NAME, 'tr')
			lst =[]
			for row in trlist[1:]:
				tdlist = row.find_elements(By.TAG_NAME,'td')
				for col in tdlist:
					num = col.text
					try:
						num = num.replace(",",'')
						num = int(num)
					except:
						num = 0
					lst.append(num)
			frame_lst.append(lst)
			index_lst.append(index_name)

	# 關閉分頁 迴圈end
			driver.close()
			driver.switch_to.window(driver.window_handles[0])
			WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"//iframe[@title='銀行統計查詢功能清單' and @id='qry12']")))
			WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form/table[3]/tbody/tr/td[5]/div/a'))).click() 
		except:
			break

	driver.quit()
	# 將爬下來的資料存入dataframe
	full_data = pd.DataFrame(frame_lst, columns = date_lst, index = index_lst)
	return full_data

def bank_table(x,y,w,z):
	## 建立欲輸出的df
	df = pd.DataFrame()

	target_month = target_months(x,y)
	df = z[target_month] 

	# 若有重複月份
	for i in range(0,4):
		for j in range(i+1,4):
			if target_month[i] == target_month[j]:
				target_month[j] = f'{target_month[j]}_1'
	df.columns = target_month

	# 計算前20與總額
	month_total = []
	top_twenty = []
	for column in df:
		total = df[column].sum()
		top = df.nlargest(20, column)[column].sum()
		month_total.append(total)
		top_twenty.append(top)

	df.loc['前20'] = top_twenty
	df.loc['總額'] = month_total

	# 計算市占率&排名
	for column in range(0, df.shape[1] *3, 3):
		market_share = []
		for row in range(df.shape[0]):
			share = df.iloc[row, column] / df.iloc[df.shape[0] - 1, column]
			market_share.append(share)

		ranking = df[target_month[column // 3]].iloc[:-2].rank(ascending=False)
	
		# print(column)
		# print(market_share)
		df.insert(column + 1 , column=f'{target_month[column // 3]}市占率', value = market_share)
		df.insert(column + 2, column=f'{target_month[column // 3]}排名', value = ranking)

	# 與前__比較
	new_target = ['上月增量', '去年年底增量', '去年同期增量']
	[target_month.append(i) for i in new_target]

	df['上月增量'] = df[target_month[0]] - df[target_month[1]]
	df['去年年底增量'] = df[target_month[0]] - df[target_month[2]]
	df['去年同期增量'] = df[target_month[0]] - df[target_month[3]]

	for column in range(12, 21, 3):
		ranking = df[target_month[column // 3]].iloc[:-2].rank(ascending=False)
		rate = df[target_month[column // 3]]/df[target_month[0]]
		df.insert(column + 1 , column=f'{target_month[column // 3]}成長率', value = rate)
		df.insert(column + 2, column=f'{target_month[column // 3]}排名', value = ranking)

	# 寫入csv(1): dataframe
	out = df.sort_values(by = target_month[0], ascending = False)
	out = out.head(22)
	out = out.sort_values(by = [f'{target_month[0]}排名', f'{target_month[0]}市占率'])

	# print(df)
	col = out.columns.values.tolist()
	col.insert(0, '')
	bank_name = out.index.values.tolist()

	py_path = os.path.abspath('.')
	file_path = os.path.join(py_path, f'{w}_{x}年{y}月.csv')

	with open(file_path, 'w', encoding='utf-8', newline='') as f:
		writer = csv.writer(f)
		writer.writerow(col)
		for i in range(out.shape[0]):
			inform = out.iloc[i].tolist()
			inform.insert(0,bank_name[i])
			writer.writerow(inform)
		f.close()

	# 寫入csv(2): 玉山
	main_file = os.path.join(py_path, "esun.csv")
	# col = out.columns.values.tolist()
	# col.insert(0, '')
	esun = out.loc['808 玉山商業銀行'].tolist()
	esun.insert(0,w)

	if os.path.isfile(main_file):
		with open(main_file, 'a', encoding='utf-8', newline='') as f:
		    writer = csv.writer(f)
		    writer.writerow(esun)
		    f.close()

	else:
		with open(main_file, 'a', encoding='utf-8', newline='') as f:
		    writer = csv.writer(f)
		    writer.writerow(col)
		    writer.writerow(esun)
		    f.close()



## 進入網站
options = Options()
options.chrome_executable_path = "D:\Python\chromedriver.exe"
driver = webdriver.Chrome(options = options)
driver.get("https://survey.banking.gov.tw/statis/webMain.aspx?sys=100&funid=defqry2")
driver.maximize_window()

# 點選目標值
WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"//iframe[@title='銀行統計查詢功能清單' and @id='qry12']")))
WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="folder30"]/tbody/tr/td[1]/a'))).click()  # 如何一次撈多

lst = []
for i in range(1,103):
	try :
		js = f"document.getElementById(\"item{i}\").style.display='block';"
		driver.execute_script(js)
		label_name = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, f"item{i}"))).text
	except:
		js = f"document.getElementById(\"folder{i}\").style.display='block';"
		driver.execute_script(js)
		label_name = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, f'folder{i}'))).text
	lst.append(label_name)
print(lst)

lst = ['月底餘額(不含郵匯轉存款)', '活期性存款', '外匯存款', '月底餘額(不含催收款)', '對民營事業', '對中小企業',  '金額', '購置住宅貸款',  '其他個人消費貸款(不含信用卡循環信用)', '流通金融卡數', '裝設台數', '本月交易次數', '稅前損益(累計數)', '收益(累計數)', '利息收入(累計數)', '手續費收入(累計數)', '透過損益按公允價值衡量\n之金融資產及負債利益(累計數)', '其他收益(累計數)']

for i in lst:
	try:
		target_value = bank_crawler('112','1',i) 
		bank_table('112','1',i,target_value)
	except:
		pass



# target_value = bank_crawler('112','1','定期性存款') 
# bank_table('112','1','定期性存款',target_value)


