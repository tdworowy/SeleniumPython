import random

import requests
from bs4 import BeautifulSoup


def getSongs():
    f= open('file.txt', 'w')
    for i in range(25):
        response = requests.get('http://www.last.fm/pl/user/TotaledThomas/loved?page='+str(i)).text
        soup = BeautifulSoup(response)
        titles = soup.find_all("a", class_="link-block-target")
        titles = str(titles).split(">")
        #print(titles)
        for text in titles:
            #print(text)
           if "—" in text:
               i = text.index("—")+1
               print(text[i:-1])
               print(text[i:-1], file=f)

    f.close()

getSongs()