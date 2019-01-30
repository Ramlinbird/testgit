#! /usr/bin/python
# -*- coding: utf-8 -*-
import re
from urlparse import urlparse
from collections import OrderedDict
from httplib2 import Http
from BeautifulSoup import BeautifulSoup

def get_page(url, outfile=None):
    """ GET url and save result-html to outfile """
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
        if outfile is not None:
            with open(outfile, "w") as outf:
                outf.write(content)
    except:
        print("Get %s error!" % url)
        return
    soup = BeautifulSoup(content)
    parse_soup_imgs(url, soup)

def parse_soup_imgs(url, soup):
    website = urlparse(url).netloc
    print(website)
    print(soup.title.text.encode("utf-8"))
    for link  in soup.findAll(name='img',attrs={"src":re.compile(r'^http')}):
        print link.get('src')

if __name__ == "__main__":
    get_page("https://www.wikiart.org/en/grandma-moses/apple-butter-making-1947")
    #get_page("https://www.artic.edu/artworks/87479/the-assumption-of-the-virgin")
