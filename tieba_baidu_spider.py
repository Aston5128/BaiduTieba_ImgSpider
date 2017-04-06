# Catching BaiduTieba images

import requests
import Download
from bs4 import BeautifulSoup
import re
import os


class tieba:
    def __init__(self):
        self.start_url = 'http://tieba.baidu.com'
        if os.path.exists('/Users/yton/Documents/百度贴吧'):
            print('[Folder exist]。。。百度贴吧')
            os.chdir('/Users/yton/Documents/百度贴吧')
        else:
            print('[Creating folder]。。。百度贴吧')
            os.mkdir('/Users/yton/Documents/百度贴吧')
            os.chdir('/Users/yton/Documents/百度贴吧')

    def GetMaxSpan(self, keyword):
        html = Download.dl.GetHtml(self.start_url + '/f?ie=utf-8&kw=' + keyword)
        href = BeautifulSoup(html, 'lxml').find('a', class_='last pagination-item ')['href']
        return int(re.findall('&pn=([0-9]*)', href)[0])

    def StoreImg(self, href, name):
        print('[Creating folder]。。。' + name)
        os.mkdir(name)
        html = Download.dl.GetHtml(href)
        img_href_list = BeautifulSoup(html, 'lxml').find_all('img', class_='BDE_Image')
        i = 0
        for img_href in img_href_list:
            img_url = img_href['src']
            img = requests.get(img_url)
            img_fp = open(name + '/' + str(i) + '.jpg', 'ab')
            img_fp.write(img.content)
            img_fp.close()
            i += 1

    def GetDetailHref(self, pn, keyword):
        url = self.start_url + '/f?ie=utf-8&kw=' + keyword + '&pn=' + str(pn)
        print('[Catching]。。。url：' + url)
        html = Download.dl.GetHtml(url)
        detail_href_list = list(BeautifulSoup(html, 'lxml').find_all('a', class_='j_th_tit '))
        for item in detail_href_list:
            name = item.text
            href = self.start_url + item['href']
            print('[Catching]。。。' + name + ' url：' + href)
            self.StoreImg(href, name)

    def Get(self, keyword):
        for pn in range(0, self.GetMaxSpan(keyword)+1, 50):
            self.GetDetailHref(pn, keyword)

a = tieba()
a.Get('坦克世界')
