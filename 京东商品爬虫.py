#京东商品信息爬虫
#爬取京东商品信息并保存到csv格式文件中
#2017-7-23


import os
import requests
import csv
from bs4 import BeautifulSoup

#获取url请求
def gethtml(kind,page):
    '''获取url请求'''
    pagenum = str(2 * page)
    try:
        r = requests.get('https://search.jd.com/Search?keyword=' + \
        kind + '&enc=utf-8&page=' + pagenum)#链接url
        r.raise_for_status()
        r.encoding = r.apparent_encoding#转码
        print('爬取第{}页：'.format(page))
        return r.text#返回html
    except:
        print('链接异常！！！')
        return ''

#获取定位资源
def findhtml(html,httplist):
    """寻找资源"""
    soup = BeautifulSoup(html,'lxml')
    links = soup.find_all('div', class_='gl-i-wrap')#寻找'div'标签
    for link in links:
        ui = []
        namediv = link.find('div', class_='p-name p-name-type-2')#寻找商品名称和链接
        title = namediv.a['title']
        href = namediv.a['href']
        ui.append(title)#名称加入到ui中
        pricediv = link.find('div', class_='p-price')#寻找商品价格
        try:
            price =  pricediv.strong['data-price'] 
            ui.append(price)#价格加入到ui中
        except:
            ui.append('')
        if 'https:' not in href:#添加链接
            ui.append('https:' + href)
        else:
            ui.append(href)
        aggressmentdiv = link.find('div', class_='p-commit')#寻找评论
        number = aggressmentdiv.strong.contents[1].string
        ui.append(number)#评论数添加到ui中
        httplist.append(ui)
        try:
            if price:
                print('{:^10s}:{:<}元'.format(title,price))
            else:
                print('{:^10s}'.format(title))
        except:
            print('{:^10s}'.format(title))


#保存资源
def savehtml(ul):
    path = 'D:/数据/'
    if not os.path.exists(path):
        os.mkdir(path)#创建一个文件
    with open(path + '京东商品信息爬虫.csv','w+') as f:
        writer = csv.writer(f)
        writer.writerow(['商品','价格','链接','评价数'])
        for u in range(len(ul)):
            if ul[u]:
                writer.writerow([ul[u][0],ul[u][1],ul[u][2],ul[u][3]])



#程序主体
if __name__ == '__main__':
    goods = input('请输入要搜索的物品：')
    yeshu = int(input('请输入要查询的页数:'))
    ulist = []
    for i in range(yeshu+1):
        try:
            if i != 0:
                text = gethtml(goods,i)
                findhtml(text,ulist)
            savehtml(ulist)
        except:
            break