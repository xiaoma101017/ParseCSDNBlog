'''
@Author Caso_卡索
@Date 2020-8-25 22:14
@Func Python爬虫CSDN博客文章数据，并写入excel表中
      使用 re 模块正则匹配要获取的 url地址
'''
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import re
from config import Host, User_Agent, Source, EachSource,OUTPUT

results = [] # 存储全部数据

def parseEachBlog(link):
    referer = "Referer: " + link
    headers = {"Referer": referer, "User-Agent": User_Agent}
    r = requests.post(link, headers=headers)
    html = r.text
    with open(EachSource, 'w', encoding='UTF-8') as f:
        f.write(html)
    soup = BeautifulSoup(open(EachSource, 'r', encoding='UTF-8'), features="html.parser")
    readcontent = soup.select('.bar-content .read-count')
    collection = soup.select('.bar-content .get-collection')
    readcounts = re.sub(r'\D', "", str(readcontent[0]))
    collections = re.sub(r'\D', "", str(collection[0]))
    blogname = soup.select('.title-article')[0].text
    time = soup.select('.bar-content .time')[0].text
    eachBlog = [blogname, link, readcounts, collections, time]
    return eachBlog

def getBlogList(blogID, pages):
    listhome = "https://" + Host + "/" + blogID + "/article/list/"
    pagenums = [] # 转换后的pages页数
    for i in range(1, int(pages)+1):
        pagenums.append(str(i))

    for number in pagenums:
        url = listhome + number + "?t=1"
        headers = {"Referer": url, "Host": Host, "User-Agent": User_Agent}
        response = requests.post(url, headers=headers)
        html = response.text
        with open(Source, 'a', encoding='UTF-8') as f:
            f.write(html)
    # 获取全部博客的链接
    soup = BeautifulSoup(open(Source, 'r', encoding='UTF-8'), features="html.parser")
    hrefs = []
    re_patterm = "^https://blog.csdn.net/" + blogID + "/article/details/\d+$"
    for a in soup.find_all('a', href=True):
        if a.get_text(strip=True):
            href = a['href']
            if re.match(re_patterm, href):
                if hrefs.count(href) == 0:
                    hrefs.append(href)
    return hrefs

def parseData():
    dataframe = pd.DataFrame(data=results)
    dataframe.columns = ['文章标题', '文章链接', '浏览量', '收藏量', '发布时间']
    dataframe.to_csv(OUTPUT, index=False, sep=',')

def delTempFile():
    if os.path.exists(Source):
        os.remove(Source)
    if os.path.exists(EachSource):
        os.remove(EachSource)

if __name__ == '__main__':
    blogID = input("输入你要爬去的博客名: ")
    pages = input("输入博客列表页数: ")
    print("获取全部博客链接...")
    linklist = getBlogList(blogID, pages)
    print("开始获取数据...")
    for i in linklist:
        print("当前获取: %s"%(i))
        results.append(parseEachBlog(i))
    print("结束获取数据...")
    # 开始解析并存储 .csv 文件
    print("开始解析并存储数据...")
    parseData()
    print("删除临时文件...")
    delTempFile()