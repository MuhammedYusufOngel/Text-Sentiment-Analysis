from os import system
from bs4 import BeautifulSoup
import requests
import re

system("CLS")

url = "https://www.hepsiburada.com"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
}

counter = 0
products = set()

#We open our categories links
f = open("../Get_Category/output.txt","r")
lines = f.read().split("\n")

for line in lines:
    counter = counter + 1

    if(counter == 30):
        print("break")
        break

    new_url = url + line

    
    htmlStr = requests.get(new_url, headers=headers).text

    #We try to find max page number. So we try to take total product.
    wanted = '<span class="totalProductCount-NGwtj4MUJQB5Zmv2FajZ">(.*?)</span>'
    pages = re.findall(wanted, htmlStr)

    #If page is "10.000+" max page is fifty
    if pages[0] == "10.000+":
        maxPageNumber = 50

    #We divide the total number of products by 24 because there are 24 products on one page 
    else:
        maxPageNumber = int(int(pages[0]) / 24)
    
    if maxPageNumber > 0:
        
        #The maximum number of pages on Hepsiburada.com generally does not exceed 50.
        if maxPageNumber > 50:
            maxPageNumber = 50

        #We loop between 1 to 51 but 51 is not included.
        for page in range(1, maxPageNumber+1):
            
            #We change the url to navigate pages
            url2 = new_url + '?sayfa=' + str(page)

            htmlStr2 = requests.get(url2, headers=headers)
            soup = BeautifulSoup(htmlStr2.text, 'html.parser')

            #We find product link and add products variable
            for div in soup.find_all('li'):
                for a in div.find_all('div'):
                    for link in a.find_all('a'):
                        result = link.get('href')
                        products.add(result)
                        print(page)
                        print(result)

    else:
        #We don't need to add "?sayfa" because there is one page.
        url2 = new_url

        htmlStr2 = requests.get(url2, headers=headers)
        soup = BeautifulSoup(htmlStr2.text, 'html.parser')

        for div in soup.find_all('li'):
            for a in div.find_all('div'):
                for link in a.find_all('a'):
                    result = link.get('href')
                    products.add(result)

    print(new_url)


with open("product_list.txt","w") as txt_file:
    for line in products:
        txt_file.write(line + "\n")
    