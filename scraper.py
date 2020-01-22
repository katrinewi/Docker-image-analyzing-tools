import urllib.request
from selenium import webdriver
import time
import pandas as pd

# specify the url
urlpage = 'https://hub.docker.com/search/?q=&type=image&page={}'
page_count = 0
print("Scraping started")
data = ""
image_names = open("./scraper-files/image-names.txt","w")
image_info = open("./scraper-files/image-info.csv", "w")

while page_count < 60:
	page_count +=1
	url = urlpage.format(page_count)
	# run firefox webdriver
	driver = webdriver.Firefox(executable_path = '/home/maltrine/aevolume/Master-thesis-scripts/geckodriver')
	# get web page
	driver.get(url)
	# sleep for 10s, to let the page fully load
	time.sleep(10)
	# find elements by xpath
	results = driver.find_elements_by_xpath("//*[@class='imageSearchResult styles__searchResult___EBKah styles__clickable___2bfia']")

	print('Scraping page: ', page_count)

	for x in results:
		info = x.text.split('\n')
		image_type = ""
		downloads = ""
		stars = ""
		#Set image type
		if('OFFICIAL' in x.text):
			image_type = "official"
			downloads = info[1]
			stars = info[3]
		elif('VERIFIED' in x.text):
			image_type = "verified"
		else:
			image_type = "community"
			downloads = info[0]
			if(info[2].isdigit()):
				stars = info[2]
			else:
				stars = 0
		image_link = x.get_attribute('href')
		if(image_type == "official"):
			tmp = image_link.split("/")[-1] + ", " + image_type + ", " + downloads + ", "+stars +"\n"
			data += tmp
			image_names.write(image_link.split("/")[-1]+"\n")
			image_info.write(tmp)
		elif(image_type == "community"):
			tmp =  image_link.split("/")[-2]+"/"+image_link.split("/")[-1]  + ", " + image_type + ", " + downloads + ", "+stars+"\n"
			data += tmp
			image_names.write(image_link.split("/")[-2]+"/"+image_link.split("/")[-1] +"\n")
			image_info.write(tmp)
		else:
			tmp = image_link.split("/")[-1]+", " + image_type + "\n"
			data += tmp
			image_names.write(image_link.split("/")[-1]+"\n")
			image_info.write(tmp)

	time.sleep(5)
	driver.close()

# close driver
driver.quit()
# save to pandas dataframe
df = pd.DataFrame(data)
print(df)

