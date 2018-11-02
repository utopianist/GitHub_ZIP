import os
import urllib.request
import requests
import re
from bs4 import BeautifulSoup
import zipfile


def getHTML(offset):
    url = 'https://github.com/Python3WebSpider?page=' + str(offset)
    r = requests.get(url)
    try:
        if r.status_code == 200:
            return (r.text)
    except:
        print('链接失败!')


def parsePage1(html,urllist,namelist):
    pattern = re.compile('<h3>.*?<a href=.*?itemprop="name codeRepository">(.*?)</a>.*?</h3>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        zipurl = 'https://github.com/Python3WebSpider/' + item[9:] + '/archive/master.zip'
        urllist.append(zipurl)
        namelist.append(item[9:])


def parsePage2(html, urllist, namelist):
    soup = BeautifulSoup(html, 'html.parser')
    data = soup.find_all('h3')
    for item in data:
        a = item('a')
        for item in a:
            print(item.string)
            zipurl = 'https://github.com/Python3WebSpider/' + item[9:] + '/archive/master.zip'
            urllist.append(zipurl)
            namelist.append(item[9:])



def downloadZip(urllist, namelist):
    count = 0
    dir = os.path.abspath('.')
    for item in urllist:
        if os.path.exists(os.path.join(dir, namelist[count] + '.zip')):
            count = count +1
        else:
            try:
                print('正在下载' + namelist[count])
                work_path = os.path.join(dir, namelist[count] + '.zip')
                urllib.request.urlretrieve(item,work_path)
                count = count + 1
            except:
                continue

def unZip():
    file_list = os.listdir(r'.')
    for file_name in file_list:
        if os.path.splitext(file_name)[1] == '.zip':
            try:
                print('正在尝试解压' + file_name)
                file_zip = zipfile.ZipFile(file_name, 'r')
                for file in file_zip.namelist():
                    file_zip.extract(file, r'.')
                file_zip.close()
                os.remove(file_name)
            except:
                name = os.path.splitext(file_name)[0]
                os.remove(file_name)
                zipurl = 'https://github.com/Python3WebSpider/' + name + '/archive/master.zip'
                try:
                    print('正在下载' + name)
                    work_path = os.path.join(dir, name + '.zip')
                    urllib.request.urlretrieve(zipurl, work_path)
                except:
                    continue


def main():
    urllist = []
    namelist = []
    html = getHTML(1)
    parsePage1(html, urllist, namelist)
    downloadZip(urllist, namelist)
    unZip()


main()