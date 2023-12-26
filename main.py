import requests as req
import re as re
from bs4 import BeautifulSoup as bs
import csv_file as csv
import time
import random as rand
from concurrent.futures import ThreadPoolExecutor

headers = [{
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134'},
           {
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 OPR/53.0.2907.97 Yowser/2.5 Safari/537.36'},
           {
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Vivaldi/1.96.1494.7 Safari/537.36'},
           {
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 OPR/53.0.2907.97 YaBrowser/21.6.0 Yowser/2.5 Safari/537.36'},
           {
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134'},
           {
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 OPR/53.0.2907.97 YaBrowser/21.6.0 Yowser/2.5 Safari/537.36'},
           {
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Vivaldi/1.96.1494.7 Safari/537.36'},
           {
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 OPR/53.0.2907.97 YaBrowser/21.6.0 Yowser/2.5 Safari/537.36'},
           {
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/9 Safari/537.36'},
           {
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/0 Safari/537.36'}]
url = 'https://www.guwenxue.cc'


def get(url):
    res = req.get(url, headers=headers[rand.randint(0, len(headers) - 1)])
    res.encoding = 'utf-8'
    return res.content


# 定义过滤器
def has_class_but_not_style(tag):
    return tag.has_attr('class') and not tag.has_attr('style')


def getDetil(var1, path):
    text = get(url + f'/shiwen_{var1}.html')
    soup = bs(text, 'html.parser')
    lines = soup.find_all("a", style=' font-size:15px;')
    datas = []
    for index, line in enumerate(lines):
        data = getInfo(index, line)
        datas.append(data)
    csv.arows(path, datas)
    return datas


# 获取信息
def getInfo(index, line):
    data = []
    var1 = var2 = var3 = var4 = var5 = ''
    try:
        resp = req.get(url + line['href'], headers=headers[index])
        resp.encoding = 'utf-8'
        print("{}:{}-{}".format(resp.request.method, resp.request.url, resp.status_code))
        soup2 = bs(resp.content, 'html.parser')
        var1 = line.get_text()
        var2 = soup2.find_all('p', attrs={'style': 'margin:0px; font-size:12px;line-height:160%;'})
        var3 = soup2.find('div', class_="son2", style=None).find_all('p')
        var4 = re.search('\((.*?)人评分\) (.*?) 分', soup2.find('div', class_='line1').get_text())
        var5 = var3[len(var3) - 1].get_text()
        if var5 == '原文：':
            var5 = soup2.find('div', class_="son2", style=None).stripped_strings
            var5 = "".join(var5).split("原文：", 1)[1]
    except AttributeError as ae:
        print("429错误，进行重试～")
        time.sleep(rand.random() + 0.5)
        data = getInfo(index, line)
        return data
    data.append(var1)
    data.append(var2[0].get_text().replace("朝代：", ''))
    data.append(var2[1].get_text().replace("作者：", ''))
    data.append(var5.replace('\r', "").replace('\n', '').strip())
    data.append(var4.group(1))
    data.append(var4.group(2))
    print(var1, '===> 添加成功')
    time.sleep(rand.random() + 0.5)
    return data

def main():
    file_path = 'data/data.csv'
    csv.wrow(file_path, ['诗词名', '朝代', '作者', '古诗', '评价数', '评分'])
    html = get(url + '/shiwen.html')
    soup = bs(html, 'html.parser')
    totals = soup.find('span', style='color:#65645F;').get_text().removeprefix('共').removesuffix('篇')
    pages = int(totals) // 10 if int(totals) % 10 == 0 else int(totals) // 10 + 1
    print("=======古诗文大全共{}条诗文, 共{}页=======".format(totals, pages))
    [getDetil(i, file_path) for i in range(1, pages)]

if __name__ == '__main__':
    main()
