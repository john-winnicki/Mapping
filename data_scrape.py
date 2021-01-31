from selenium import webdriver                    # Import module 
from selenium.webdriver.common.keys import Keys   # For keyboard keys 
import time                                       # Waiting function  
import numpy as np
import pandas as pd

URL = 'https://purl.stanford.edu/mr870gt3467'      # Define URL 
browser = webdriver.Chrome()                       # Create driver object means open the browser 

browser.get(URL)
# time.sleep(5)

# browser.switch_to.frame(browser.find_element_by_tag_name("iframe"))

# time.sleep(1)

dic = {}

title = browser.find_element_by_xpath("/html/body/div[1]/div/div/section/h1").text
dic['TITLE'] = title

dic['URL'] = URL

keywords = ["description", "contributors", "subjects", "bibliography-info"]


for keyword in keywords:
		elem = browser.find_element_by_id(keyword)
		# lst = elem.find_element_by_tag_name("dl")
		curr = ""
		for item in elem.find_elements_by_xpath("div[@class='section-body']/dl/*"):
			print(item.tag_name)
			if item.tag_name=="dt":
				curr = item.text
				dic[curr] = ""
			elif curr!="" and item.tag_name=="dd":
				dic[curr] += item.text+";"

		if(curr==""):
			for item in elem.find_elements_by_xpath("div[@class='section-body']/*"):
				print(item.tag_name)
				if item.tag_name=="dt":
					curr = item.text
					dic[curr] = ""
				elif curr!="" and item.tag_name=="dd":
					dic[curr] += item.text+";"


fin_dic = {}
for key in dic:
	if(not key in fin_dic): fin_dic[key] = []
	fin_dic[key].append(dic[key])

df = pd.DataFrame.from_dict(fin_dic)
with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(df)


df.to_csv("./output.csv",index=False)
# for keyword in keywords:
# 	elem = browser.find_element_by_id(keyword)
# 	temp = elem.find_elements_by_tag_name("dt")
# 	for dt_elem in temp:
# 		dic[dt_elem.text] = []
# 		for small_elem in elem.find_elements_by_tag_name("dd"):
# 			dic[dt_elem.text].append(small_elem.text)

# for keyword in keywords:
# 	elem = browser.find_element_by_id(keyword)
# 	temp = elem.find_elements_by_tag_name("dt")
# 	for dt_elem in temp:
# 		dic[dt_elem.text] = []
# 		# for small_elem in elem.find_elements_by_tag_name("dd"):
# 		# 	dic[dt_elem.text].append(small_elem.text)
# 		print("here")
# 		counter = 1
# 		while(True): 
# 			# print(dt_elem.find_element_by_xpath("following-sibling::dd[1]").getTagName())
# 			# print(dt_elem.text + ": " + dt_elem.find_element_by_xpath("following-sibling::dd[1]").text)
# 			# break
# 			try:
# 				dd_elem = dt_elem.find_element_by_xpath("following-sibling::dd[{}]".format(counter))
# 				print(dt_elem.text + ": " + dd_elem.text)
# 				counter += 1
# 			except:
# 				break
		# print(dt_elem.find_element_by_xpath("following-sibling::dd").text)

# elem = browser.find_element_by_id("contributors")
# contributor = elem.find_elements_by_tag_name("dd")
# contributors = ""
# for conman in contributor:
# 	contributors += conman.text + ";"
# contributors = contributors[:-1]


# elem = browser.find_element_by_id("description")
# temp = elem.find_elements_by_tag_name("dt")
# for dt_elem in temp:
# 	elem.find_elements_by_tag_name("dd")

# print(dic)