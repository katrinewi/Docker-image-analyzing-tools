import urllib.request, json
from urllib.error import HTTPError 

image_names = [line.rstrip('\n') for line in open("names.txt")]
results = open("./results.csv","w")
failed = open("./failed.txt","w")
results.write("image_name,pull_count,star_count,last_updated" + "\n")

for i in image_names:
    if ("/" in i):
        url_page = 'https://hub.docker.com/v2/repositories/{}'
    else:    
        url_page = 'https://hub.docker.com/v2/repositories/library/{}'
    try:
        with urllib.request.urlopen(url_page.format(i)) as url:
            data = json.loads(url.read().decode())
            results.write(i + "," + str(data['pull_count']) + "," + str(data['star_count'])+ "," + str(data['last_updated']) + "\n")
    except HTTPError as e:
        failed.write(i + "\n")           
        print(e.reason)
        continue

results.close()
failed.close()
