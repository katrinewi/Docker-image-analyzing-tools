from selenium import webdriver
import time

urlpage = 'https://hub.docker.com/search/?q=&type=image&page={}'
page_count = 0
print("Scraping started")
image_names = open("./image-names.txt","w")
image_info = open("./image-info.csv", "w")

while page_count < 100:
    page_count +=1
    url = urlpage.format(page_count)
    #Run firefox webdriver
    driver = webdriver.Firefox(executable_path = '/usr/local/Cellar/geckodriver/geckodriver')
    #Get web page
    driver.get(url)
    #Sleep for 10s, to let the page fully load
    time.sleep(10)
    #Find elements by xpath
    results = driver.find_elements_by_xpath("//*[@class='imageSearchResult styles__searchResult___EBKah styles__clickable___2bfia']")

    print('Scraping page: ', page_count)
    for info in results:
        image_type = ""
        #Set the image type
        if('OFFICIAL' in info.text):
            image_type = "official"
        elif('Certified' in info.text):
            image_type = "certified"
        elif('VERIFIED' in info.text):
            image_type = "verified"
        else:
            image_type = "community"

        #Gather the image name from URL, different procedure for each image type
        image_link = info.get_attribute('href')
        if(image_type == "official"):
            tmp = image_link.split("/")[-1] + "," + image_type + "\n"
            image_names.write(image_link.split("/")[-1]+"\n")
            image_info.write(tmp)
        elif(image_type == "community"):
            tmp =  image_link.split("/")[-2] + "/" + image_link.split("/")[-1] + "," + image_type + "\n"
            image_names.write(image_link.split("/")[-2]+"/"+image_link.split("/")[-1] +"\n")
            image_info.write(tmp)
        else:
            tmp = image_link.split("/")[-1] + "," + image_type + "\n"
            image_names.write(image_link.split("/")[-1]+"\n")
            image_info.write(tmp)

    time.sleep(5)
    driver.close()
    
#Close driver
driver.quit()
#Close files
image_names.close()
image_info.close()
