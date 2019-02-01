#! /usr/bin/python
# -*- coding: utf-8 -*-
import re
from urllib.parse import urlparse
from collections import OrderedDict
from httplib2 import Http
from bs4 import BeautifulSoup

def url_rewrite(url):
    """ Rewrite url from mobile into desktop """
    url = url.replace('_mobile.htm', '.htm')
    return url

def get_page(url, outfile=None):
    """ GET url and save result-html to outfile """
    url = url_rewrite(url)
    req = Http(timeout=5)
    headers  = {
        'Connection': 'keep-alive', 
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.65 Safari/534.24',
        'Content-type': 'application/x-www-form-urlencoded',
        'Accept': '*/*',
        'Accept-Charset': 'UTF-8,*;q=0.5',
        'Accept-Encoding': 'gzip,deflate,sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
    }
    try:
        rsp, content = req.request(url, "GET", headers=headers)
        #print(type(url), type(content), type(content.decode('utf8')))
        content = content.decode('utf8')
        if outfile is not None:
            with open(outfile, "w") as outf:
                outf.write(content)
    except Exception as e:
        print("Get %s error [%s]!" % (url, str(e)))
        return
    soup = BeautifulSoup(content, 'html.parser')
    parse_soup_imgs(url, soup)

def parse_soup_imgs(url, soup):
    website = urlparse(url).netloc
    print(website)
    print(soup.title.text)
    if website == 'www.wikiart.org':
        for link  in soup.findAll(name='img',attrs={"src":re.compile(r'^http')}):
            print(link.get('src'))
    elif website == 'www.artic.edu':
        img_url = soup.findAll(name='meta',attrs={"property":'og:image'})[0].get('content')
        img_title = soup.findAll(name='meta',attrs={"property":'og:description'})[0].get('content')
        print(img_url)
        print(img_title)
    elif website == 'www.namoc.org':
        img_url = re.search(r'var lm = \"(.*?)\";', soup.text)
        if img_url is not None:
            img_url = img_url.groups()[0].replace('/lm/', '/l/')
            img_title = soup.title.text
            print(img_url)
            print(img_title)
    else:
        print('not supported')

if __name__ == "__main__":
    #get_page("https://www.wikiart.org/en/grandma-moses/apple-butter-making-1947")
    #get_page("https://www.artic.edu/artworks/87479/the-assumption-of-the-virgin")
    get_page("http://www.namoc.org/zsjs/gczp/cpjxs/201304/t20130417_222410.htm")
