import urllib.request
from selenium import webdriver
import time
import pandas as pd


# specify the url
urlpage = 'https://hub.docker.com/search/?q=&type=image&page={}'
page_count = 0
print(urlpage)
data = []

while page_count < 41:
	page_count +=1
	url = urlpage.format(page_count)
	# run firefox webdriver
	driver = webdriver.Firefox(executable_path = '/home/katrinewi/Documents/scraper-testin/geckodriver')
	# get web page
	driver.get(url)
	# sleep for 10s, to let the page fully load
	time.sleep(10)
	# find elements by xpath
	results = driver.find_elements_by_xpath("//*[@class='imageSearchResult styles__searchResult___EBKah styles__clickable___2bfia']")

	print('Firefox Webdriver - Number of results', len(results)*page_count)

	for x in results:
    	info = x.text.split('\n')
    	image_type = ""
    	downloads = ""
    	stars = ""
    	last_updated = ""
    	#Set image type
    	if('OFFICIAL' in x.text):
        	image_type = "official"
        	downloads = info[1]
        	stars = info[3]
        	last_updated = info[6]
    	elif('VERIFIED' in x.text):
        	image_type = "verified"
        	last_updated = info[3]
    	else:
        	image_type = "community"
        	downloads = info[0]
        	stars = info[2]
        	#liste = info[5].split('•')
        	#last_updated = liste[1] if (len(liste)>0) else ""
    	image_link = x.get_attribute('href')
    	if(image_type != "community"):
        	data.append({"image" : image_link.split("/")[-1], "type" : image_type, "downloads" : downloads, "stars": stars, "last_updated":last_updated})
    	else:
        	data.append({"image" : image_link.split("/")[-2]+"/"+image_link.split("/")[-1], "type" : image_type, "downloads" : downloads, "stars": stars, "last_updated":last_updated})

	print(data)
	time.sleep(20)

# close driver
driver.quit()
# save to pandas dataframe
df = pd.DataFrame(data)
print(df)

