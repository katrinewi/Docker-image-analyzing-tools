import urllib.request, json
from urllib.error import HTTPError

names_file = open("./image_names.txt")
image_names = [line.rstrip('\n') for line in names_file]
names_file.close()
print("Finished reading image names")

results = open("./results_apiv1.csv","w")
failed = open("./failed_apiv1.txt","w")
results.write("image_name,pull_count,star_count,last_updated" + "\n")

print("Starting data gathering ...")
for i in image_names:
    print("Gathering data about: " + i)
    url_page = 'https://hub.docker.com/api/content/v1/products/images/{}'
    try:
        with urllib.request.urlopen(url_page.format(i)) as url:
            data = json.loads(url.read().decode())
            popularity =  str(data['popularity'])
            if(str(data['popularity']) == str(0)):
                popularity = ""
            results.write(i + "," + popularity + "," + "," + str(data['updated_at']) + "\n")
    except HTTPError as e:
        failed.write(i + "\n")
        print(e.reason)
        continue

results.close()
failed.close()      
