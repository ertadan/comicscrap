# pip3 install lxml bs4 requests fpdf
import random
import os
from time import sleep
from fpdf import FPDF
from bs4 import BeautifulSoup
import requests


headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0",
    "Cookie": "ageRestrict=17",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
}

# Initially get html and save it to file
# req = requests.get(url, headers=headers)
# src = req.text
# print(src)
# with open("site/index.html", "w") as file:
#     file.write(src)

# load HTML from file
# with open("site/index.html") as file:
#     src = file.read()

# TODO: make pdf according to  actual image size.


def savePDF(fileList):
    pdf = FPDF()
    for image in fileList:
        pdf.add_page()
        pdf.image(image)
    pdf.output("result.pdf", "F")


def download_img(name, link):
    # print(link)
    savedFile = str(name) + link[link.rfind('.'):]
    r = requests.get(link)
    if r.status_code == 200:
        with open(f"img/{savedFile}", "wb") as file:
            file.write(r.content)
            del r
            print(f"[+] Download {savedFile}")
            return savedFile
    return ""


def getImgLink(url):
    ''' Extract Image Link
    <img id="mainImage" src="/upload/!c/koriandr/.../000144-6vhr8t5q2u.jpg"
    alt="Комикс ....: выпуск №144" width="1000" height="4573">
    '''
    # print(soup.find('div', {"class": 'serial-nomargin'}
    #                 ).find('img')['src'])
    return BeautifulSoup(requests.get(url, headers=headers).text, "lxml").find(
        'div', {"class": 'serial-nomargin'}).find('img')['src']


def get_data(url):
    # All needed logic

    # check download path
    if not os.path.exists(f"img"):
        os.mkdir(f"img")
    # get pages count
    req = requests.get(url, headers=headers)
    src = req.text
    soup = BeautifulSoup(src, "lxml")
    last_page = int(soup.find('span', class_='issueNumber').text.split('/')[1])
    # save from last to  first
    imagelist = []
    for page in range(last_page, 0, -1):
        address = url + str(page)
        # print(address)
        link = getImgLink(address)
        imagelist.append(download_img(page, url[:url.find('ru') + 2] + link))
        sleep(random.randrange(2, 5))
    #revert order to make correct pdf
    imagelist.reverse()
    # savePDF(imagelist)
    print('Done')


def main():
    #url = "https://acomics.ru/~old-harmony/"
    url = input('Enter comic URL: ')
    if url:
        get_data(url)


if __name__ == '__main__':
    main()
