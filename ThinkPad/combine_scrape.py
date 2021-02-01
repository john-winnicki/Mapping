import requests #HTML Downloader
from bs4 import BeautifulSoup #HTML Parser

from selenium.webdriver import Firefox #Web driver, which also will serve as our parser
import time #For waiting
import numpy as np
import pandas as pd #Data frame used to convert list of dictionaries to CSV


links = []

x = 0

"""This first block scrapes all the 
pages of the "all exhibit items"
section, and compiles a list of URLs"""
while(True):
	temp = len(links) #take initial length of lists scraped

	"""Webpage to scrape ^^. This is 
	simply the above URL with X+1 inserted
	between the {} brackets."""  
	URL = "https://exhibits.stanford.edu/oss-maps/browse/all-exhibit-items?page={}&per_page=96".format(x+1)

	"""Download the HTML of the page 
	and place it in a BeautifulSoup object. 
	This allows us to parse the page.""" 
	r = requests.get(URL) 
	soup = BeautifulSoup(r.content, 'html5lib')

	"""Search the page for links that contain the
	word "catalog". These items in the catalog, 
	and hence items of interest.""" 
	for link in soup.find_all('a'):
	    pos = link.get('href')
	    if(pos.find("catalog")!=-1):
	    	# links.append("https://exhibits.stanford.edu"+pos)
	    	links.append("https://purl.stanford.edu"+pos[-12:])
	    	"""Note that here we take the link that we scraped.
	    	We then append the last 12 characters of the link to purl.stanford.edu.
	    	This is Stanford's web repository and the new URL points to the same
	    	data, but on the main archive (as opposed to the exihibit site). 
	    	Here, we are able to scrape both the metadata and the 
	    	images at the same time."""
	
	if(len(links)==temp): break #If we didn't add any new links from our scrape (AKA we reached the last webpage), break. 
	else: x += 1

print("Number of links: " + str(len(links))) #There will be double the number of maps, since each link is scraped twice in the above process


browser = Firefox() #Opens a web browser our computer can interact with

"""Seen will be used to scrape any duplicate links. As mentioned earlier, 
the above code scrapes duplicates of everything. Fin_Dic will be used to
hold all the data of a webpage. It is a list of dictionaries, where each
dictionary maps a keyword to a piece of data (e.g. Title -> Map of Japan). 
Keywords denote the sections of the metadata that we would like to search.
This is mainly useful for our scraper to know where the metadata in the
program is being stored on the page (more on this later)."""
seen = []
fin_dic = []
keywords = ["description", "contributors", "subjects", "bibliography-info"]

#Set constants for printing status
counter = -1;
length = len(links)

for URL in links:
	counter += 1
	print(str(counter)+"/"+str(length))

	if(URL in seen): #If the URL has already been scraped, then do nothing. 
		continue

	print("Scraping: {}".format(URL)) 
	browser.get(URL) #Navigate the browser to the URL
	time.sleep(5) #Wait for the page to load. 

	try:

		dic = {} #Create the metadata dictionary for this specific webpage
		title = browser.find_element_by_xpath("/html/body/div[1]/div/div/section/h1").text #This is the XPath to the title
		dic['TITLE'] = title
		dic['URL'] = URL

"""
This piece of code is probably the most confusing. We search the webpage's HTML
for elements with the ID of the keywords we listed above. We then search the page
for description list elements (DL). These contain tables of metadata with words
describing the metadata (such as "contributors") and their associated data. 
And so the DL elements look something like this. 
<dl>Meta Data Section Name                       <----- Overarching data container
	<dt>Meta Data Title</dt>                     <----- Data name
	<dl>Meta Data</dl>                           <----- Some data has multiple pieces of information
	<dl>More Meta Data under the same title</dl>
	<dt>New Meta Data Title</dt>                 <----- New name
<dl>

Sometimes, however, the metadata are not all organized under a dl. This is why we check if
the anything has been scraped using curr=="" (more on that later). The structure is the 
same as described above, but we don't bother looking for a dl container. 

The way this scrape actually works is, we parse through the web web element containing
the meta data and its associated title. If the tag name is dt, then we know it is a title, 
and we map that title to an empty string. For each following element that is a dd element, 
we know it is the metadata associated with that title, and add it to the mapping. 
Note that because we start out with curr="", if no title has been scraped, then it will stay
as "". Apart from checking if curr is "" when looking for dd elements, we also use this to
check there even is a dl container, or if we should scrape assuming there isn't one.  
"""
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


"""
This final part of the program interacts with the web app on the page, and downloads the image. 
We start by switching iframes. Effectively, this means there is a web app on the page and it
tells our program to scrape that web app, rather than that page, which allows us to know what
is happening inside of it, and in turn interact with it. 

We periodically tell the program to wait a second in order to allow the page to load. 

We then move through a series of clicks on the page to download the image. In this case it is
Share and Download Button -> Download -> Lowest Link on the set of options (this is the highest resolution)

"""

		browser.switch_to.frame(browser.find_element_by_tag_name("iframe"))

		time.sleep(1)
		#Share and Download Button
		browser.find_element_by_xpath("/html/body/div/div/div/div/main/div[1]/div[1]/section/div[1]/header/nav/div/button[3]").click()

		time.sleep(1)
		#Select Download
		browser.find_element_by_xpath("/html/body/div/div/div/div/main/div[3]/div[3]/ul/li[2]").click()

		time.sleep(1)
		#Click on lowest link of the set of options (this is the "original image" option, AKA the highest resolution). This downloads the image. 
		browser.find_elements_by_xpath("/html/body/div/div/div/div/main/div[3]/div[3]/div/div[2]/ul/li")[-1].find_element_by_xpath("div/span/a").click()

		time.sleep(5)
		#Add metadata to list after downloading image
		fin_dic.append(dic)

		# if(counter==10): break
		# else: counter += 1

	except:
		#In case the map doesn't exist on the page, an NoSuchElementExists exception will be thrown from the above code.
		#We choose to just ignore this error and continue on with our scrape.  
		print("Badness")
		continue

	#Add URL to list of URLs seen
	seen.append(URL)

"""
Initializing a Pandas Dataframe with a List of Dictionaries 
will automatically format the data nicely to export to a CSV file. 
"""
df = pd.DataFrame(fin_dic)
df.to_csv("./output.csv",index=False)
# with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
#     print(df)