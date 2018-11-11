import os
import urllib.request
import requests
import re
import zipfile


def getHTML(offset):
    url = 'https://github.com/Python3WebSpider?page=' + str(offset)
    r = requests.get(url)
    try:
        if r.status_code == 200:
            return (r.text)
    except:
        print('链接失败!')

def parsePage(html,urllist):
    pattern = re.compile('<h3>.*?<a itemprop="name codeRepository".*?>(.*?)</a>.*?</h3>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        zipurl = 'https://github.com/Python3WebSpider/' + item[11:-1] + '/archive/master.zip'
        urllist.append(zipurl)

def downloadZip(urllist):
    for item in urllist:
        itemName = re.search('WebSpider/(.*?)/archive', item).group(1)
        codesPath = 'codes' + os.path.sep + itemName + '.zip'
        if not os.path.exists(codesPath):
            try:
                print('正在下载' + itemName)
                urllib.request.urlretrieve(item,codesPath)
            except:
                continue

def unZip():
    fileList = os.listdir('codes')
    for fileName in fileList:
        filePath = 'codes' + os.path.sep + fileName
        if os.path.splitext(fileName)[1] == '.zip':
            print('正在尝试解压' + fileName)
            file_zip = zipfile.ZipFile(filePath, 'r')
            for file in file_zip.namelist():
                file_zip.extract(file, 'codes') #选择保存路径 codes
            file_zip.close()
            os.remove(filePath)

def main():
    urllist = []
    html = getHTML(1)
    parsePage(html, urllist)
    downloadZip(urllist)
    unZip()


if __name__ == '__main__':
    if not os.path.exists('codes'):
        os.mkdir('codes')
    main()