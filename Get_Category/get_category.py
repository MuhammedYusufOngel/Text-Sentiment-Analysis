from os import system
import requests
from bs4 import BeautifulSoup
import json

system("CLS")

categoryAll = []

#I only bought a few categories for trial purposes
for i in range(4):

    url = f"https://www.hepsiburada.com/api/v1/navigation/{1719+i}"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'Referer': 'https://www.hepsiburada.com/'
    }

    #We send requests and get response
    response = requests.get(url, headers=headers)
    #We convert to html
    html_content = response.content
    #We create soup object. We will use to get data
    soup = BeautifulSoup(html_content, 'html.parser')
    #We convert more readable with prettify
    string = soup.prettify()
    #Convert to json
    json_request = json.loads(string)

    categoryLevel1 = []
    categoryLevel2 = []
    categoryLevel3 = []
    categoryLevel4 = []
    empty = []

    #We cycle through all items with this loop
    for item in json_request['data']['items']:
        for child in item['children']:
            
            try:
                categoryLevel1.append(child['url'])
            except:
                empty.append("")

            for child2 in child['children']:
                
                try:
                    categoryLevel2.append(child2['url'])
                except:
                    empty.append("")

                for child3 in child2['children']:
                    try:
                        categoryLevel3.append(child3['url'])
                    except:
                        empty.append("")
                    
                    for child4 in child3['children']:
                        try:
                            categoryLevel4.append(child4['url'])
                        except:
                            empty.append("")

    categoryAll.append(categoryLevel1)
    categoryAll.append(categoryLevel2)
    categoryAll.append(categoryLevel3)
    categoryAll.append(categoryLevel4)

categoryLast = []

#We combine all categories into one list
for categories in categoryAll:
    for category in categories:
        categoryLast.append(category.split("?")[0])

#We save all categories to text file
with open("output.txt","w") as txt_file:
    for line in categoryLast:
        txt_file.write(line + "\n")