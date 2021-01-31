import requests 
from bs4 import BeautifulSoup 
from selenium import webdriver 
import time
import numpy as np
import pandas as pd


links = []

x = 0

while(True):
	temp = len(links)

	URL = "https://exhibits.stanford.edu/oss-maps/browse/all-exhibit-items?page={}&per_page=96".format(x+1)
	r = requests.get(URL) 
	  
	soup = BeautifulSoup(r.content, 'html5lib')
	# print(soup.prettify()) 

	for link in soup.find_all('a'):
	    pos = link.get('href')
	    if(pos.find("catalog")!=-1):
	    	# links.append("https://exhibits.stanford.edu"+pos)
	    	links.append("https://purl.stanford.edu"+pos[-12:])

	if(len(links)==temp): break
	else: x += 1

print(len(links))

browser = webdriver.Chrome()

seen = []
fin_dic = []
keywords = ["description", "contributors", "subjects", "bibliography-info"]

# counter = 0;

for URL in links:
	
	if(URL in seen):
		continue

	print("Scraping: {}".format(URL)) 
	browser.get(URL)
	time.sleep(5)

	try:

		dic = {}
		title = browser.find_element_by_xpath("/html/body/div[1]/div/div/section/h1").text
		dic['TITLE'] = title
		dic['URL'] = URL
		for keyword in keywords:
				elem = browser.find_element_by_id(keyword)
				# lst = elem.find_element_by_tag_name("dl")
				curr = ""
				for item in elem.find_elements_by_xpath("div[@class='section-body']/dl/*"):
					# print(item.tag_name)
					if item.tag_name=="dt":
						curr = item.text
						dic[curr] = ""
					elif curr!="" and item.tag_name=="dd":
						dic[curr] += item.text+";"

				if(curr==""):
					for item in elem.find_elements_by_xpath("div[@class='section-body']/*"):
						# print(item.tag_name)
						if item.tag_name=="dt":
							curr = item.text
							dic[curr] = ""
						elif curr!="" and item.tag_name=="dd":
							dic[curr] += item.text+";"

		browser.switch_to.frame(browser.find_element_by_tag_name("iframe"))

		time.sleep(1)

		browser.find_element_by_xpath("/html/body/div/div/div/div/main/div[1]/div[1]/section/div[1]/header/nav/div/button[3]").click()

		time.sleep(1)

		browser.find_element_by_xpath("/html/body/div/div/div/div/main/div[3]/div[3]/ul/li[2]").click()

		time.sleep(1)

		browser.find_elements_by_xpath("/html/body/div/div/div/div/main/div[3]/div[3]/div/div[2]/ul/li")[-1].find_element_by_xpath("div/span/a").click()

		time.sleep(5)

		fin_dic.append(dic)

		# if(counter==10): break
		# else: counter += 1

	except:
		print("Badness")
		continue

	seen.append(URL)

df = pd.DataFrame(fin_dic)
with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(df)


df.to_csv("./output.csv",index=False)