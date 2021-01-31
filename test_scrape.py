import requests 
from bs4 import BeautifulSoup 

links = []

for x in range(10):
	URL = "https://exhibits.stanford.edu/oss-maps/browse/all-exhibit-items?page={}&per_page=96".format(x+1)
	r = requests.get(URL) 
	  
	soup = BeautifulSoup(r.content, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib 
	# print(soup.prettify()) 

	for link in soup.find_all('a'):
	    pos = link.get('href')
	    if(pos.find("catalog")!=-1):
	    	links.append("https://exhibits.stanford.edu"+pos)

for link in links:
	print(link)

print(len(links))