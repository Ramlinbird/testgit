#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from flask import Flask, render_template, request
app = Flask(__name__)

import re
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
        return OrderedDict()
    soup = BeautifulSoup(content)
    return parse_soup_imgs(soup)

def parse_soup_imgs(soup):
    ret_dict = OrderedDict()
    ret_dict['title'] = soup.title.text.encode("utf-8")
    #link_formatted = '<img src="{src}"  alt="{title}" />'
    link_formatted = """
    <a href="{url}">
    <img src="{url}" width="200" alt="{title}" />
    <figcaption>{title}</figcaption>
    </a>
    """
    for ind, link in enumerate(soup.findAll(name='img', attrs={"src":re.compile(r'^http')})):
        #ret_dict['link_%d' % ind] = link.get('src')
        ret_dict['link_%d' % ind] = link_formatted.format(url=link.get('src', 'url'), \
                title=link.get('title', 'None')).replace('\n', '')
    return ret_dict

@app.route('/')
def main_index():
    return render_template('index.html')

@app.route('/url_parse', methods=['POST', 'GET'])
def url_parse():
    if request.method == 'POST':
        result = request.form
        fill = OrderedDict()
        fill['src_url'] = result['url']
        if 'imgurl' in result:
            ret = get_page(fill['src_url'].encode('utf8'))
            if not ret:
                fill['status'] = 'failed'
            else:
                fill['status'] = 'succeed'
                fill.update(ret)
        else:
            fill['status'] = 'failed'
        return render_template("result.html", result=fill)

if __name__ == '__main__':
    #app.run(debug = True)
    #print get_page('https://www.wikiart.org/en/grandma-moses/apple-butter-making-1947')
    app.run(host='0.0.0.0', port=8082)
