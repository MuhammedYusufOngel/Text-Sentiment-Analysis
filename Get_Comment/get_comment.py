from os import system
import requests
from bs4 import BeautifulSoup
import re

system("CLS")

url = "https://www.hepsiburada.com"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
}

#For loop
maxPage = 0
numberOfStars = 0
counter = 0

commentsAll = set()

#We open product list
f = open("../Get_Product/product_list.txt","r")
lines = f.read().split("\n")

for line in lines:
    #Sometimes they just specify stars in the comments. 
    #In this case, program brings back the comments on the first page.
    #It usually happens on the last pages. That variables is to prevent this.
    isLoopOver = False
    first_comment = ""
    
    
    maxPage = 0
    
    #When you received the links to the products, you also received advertisements. 
    #With this decision structure, the program will skip this link.
    if "https://adservice.hepsiburada.com" in line:
        continue
    
    counter = counter + 1

    print(counter) 

    #After around 1300, the program gives a connection out error.
    #So we put break
    if counter == 1000:
        break
    
    #Classic BeautifulSoup structures
    comment_url = url + line + "-yorumlari"
    htmlStr = requests.get(comment_url, headers=headers)
    soup = BeautifulSoup(htmlStr.text, 'html.parser')

    #With this loop, we find max page number
    for pageNumber in soup.find_all('span', class_="hermes-PageHolder-module-mgMeakg82BKyETORtkiQ"):
        tempNewPageNumber = re.sub('<span class="hermes-PageHolder-module-mgMeakg82BKyETORtkiQ">', '', str(pageNumber))
        newPageNumber = re.sub('</span>', '', str(tempNewPageNumber))
    
        if newPageNumber.isdigit():
            if maxPage < int(newPageNumber):
                maxPage = int(newPageNumber)
    
    #If the comments are collected on one page, we just make one loop
    if maxPage == 0:

        #Classic BeautifulSoup structures
        new_url = comment_url
        htmlStr = requests.get(new_url, headers=headers)
        soup = BeautifulSoup(htmlStr.text, 'html.parser')

        print(new_url)

        #We try to access the comment div
        for commentFull in soup.find_all('div', class_="hermes-ReviewCard-module-BJtQZy5Ub3goN_D0yNOP"):
            
            numberOfStars = 0
            
            #We find number of stars
            for star in commentFull.find_all('div', class_="star"):
                numberOfStars = numberOfStars + 1

            for comment in commentFull.find_all('span', itemprop="description"):
                tempNewComment = re.sub('<span itemprop="description">', '', str(comment))
                newComment = re.sub('</span>', '', str(tempNewComment))
                #We add number of stars and comment
                commentsAll.add(str(numberOfStars) + "\t" + newComment)


    for i in range(1, maxPage+1):
        
        #Classic BeautifulSoup structures. With "?sayfa=", we can access all comments. (sayfa = page)
        new_url = comment_url + "?sayfa=" + str(i)
        htmlStr = requests.get(new_url, headers=headers)
        soup = BeautifulSoup(htmlStr.text, 'html.parser')

        print(new_url)

        #We try to access the comment div
        for commentFull in soup.find_all('div', class_="hermes-ReviewCard-module-BJtQZy5Ub3goN_D0yNOP"):
            
            numberOfStars = 0
            
            #We find number of stars
            for star in commentFull.find_all('div', class_="star"):
                numberOfStars = numberOfStars + 1

            for comment in commentFull.find_all('span', itemprop="description"):
                tempNewComment = re.sub('<span itemprop="description">', '', str(comment))
                newComment = re.sub('</span>', '', str(tempNewComment))
                
                #If newComment == first_comment it means that the program returned to the first page.
                if first_comment == newComment:
                    print("-----------------------------------------------------")
                    #Loop must be over
                    isLoopOver = True
                    break
                    
                if isLoopOver:
                    break
                
                #We find first comment because as I said, we don't want to repeat comments.
                if first_comment == "":
                    first_comment = newComment
            
                commentsAll.add(str(numberOfStars) + "\t" + newComment)

            if isLoopOver:
                break

        if isLoopOver:
            break


with open("comments_4.txt","w", encoding="utf-16") as txt_file:
    for line in commentsAll:
            txt_file.write(line + "\n")