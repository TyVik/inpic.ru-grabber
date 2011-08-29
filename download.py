#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import os
prefix = "http://www.inpic.ru"
beginPage = 1
endPage = 1000

def download(path, name):
    with open(name, 'w') as f:
        f.write(requests.get(prefix + path).content)

def loadImages():
    for i in xrange(beginPage, endPage):
        req = requests.get(prefix + '/image/' + str(i))
        if req.status_code == requests.codes.ok:
            soup = BeautifulSoup(req.content)
            # узнаем заголовок страницы
            name = soup.find("td", {"class": "post_title"}).contents[1].contents[0]
            name = name.replace('/', '_')
            print name

            mainImagePath = soup.find("img", {"class": "image last"})["src"]
            manyImages = soup.findAll("img", {"class": "image"})
            if manyImages:
                os.makedirs(name)
                name = os.path.join(name, name)
                download(mainImagePath, name + '_0.jpg')
                for i, src in enumerate(manyImages):
                    download(src["src"], name + '_' + str(i) + '.jpg')
            else:
                download(mainImagePath, name + '.jpg')

if __name__ == "__main__":
    loadImages()