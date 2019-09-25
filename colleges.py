import requests
from lxml import etree
from lxml.etree import ParseError
from requests import RequestException
import csv


# 单页url
def get_one_page_url(url, URLlist):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/76.0.3809.132 Safari/537.36 '
    }

    try:
        response = requests.get(url, headers=headers)
        body = response.text
    except RequestException as e:
        print("request is error", e)
    try:
        html = etree.HTML(body, etree.HTMLParser())
        result = html.xpath('//div[@class="maincontent"]//div[@class="sep"]/div[@class="block unwrap"]/h2/a/@href')
        for item in result:
            URLlist.append(item)
    except ParseError as e:
        print(e.position)


# 所有url
def get_all_urls(page, URLlist):
    if page != 1:
        url = "https://www.usnews.com/education/best-global-universities/search?country=china&region=asia&page=" + str(
            page)
        get_one_page_url(url, URLlist)
    else:
        url = "https://www.usnews.com/education/best-global-universities/search?country=china&region=asia"
        get_one_page_url(url, URLlist)


# 进入每个url获取数据
def get_one_detail(url, college_data):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/76.0.3809.132 Safari/537.36 '
    }

    try:
        response = requests.get(url, headers=headers)
        body = response.text
    except RequestException as e:
        print("request is error", e)
    try:
        html = etree.HTML(body, etree.HTMLParser())
        school_name = html.xpath('//h1[@class="h-biggest"]/text()')
        for item in school_name:
            college_data.append(item)

        paths = ['Total number of students',
                 'Number of international students',
                 'Total number of academic staff',
                 'Number of international staff',
                 'Number of undergraduate degrees awarded',
                 'Number of master\'s degrees awarded',
                 'Number of doctoral degrees awarded',
                 'Number of research only staff',
                 'Number of new undergraduate students',
                 'Number of new master\'s students',
                 'Number of new doctoral students']

        for item in paths:
            # 通过兄弟节点判断数据存在:加入列表,去除多于空格
            if html.xpath(
                    '//div[@class="data-item first"]//div[@class="t-slack sep"]/div[@class="t-dim" and text()=$val]',
                    val=item):
                text = html.xpath(
                    '//div[@class="data-item first"]//div[@class="t-slack sep"]/div[@class="t-dim" and text()=$val]/preceding-sibling::*[1]/text()',
                    val=item)
                text = text[0].replace(' ', '').replace('\n', '')
            # 否则:列表中加入空元素占位
            else:
                text = ''
            college_data.append(text)

    except ParseError as e:
        print(e.position)


# 入口
if __name__ == '__main__':
    college_list = []
    URLlist = []
    for i in range(1, 5):
        get_all_urls(page=i, URLlist=URLlist)
    print(URLlist)

    for url in URLlist:
        college_data = []
        get_one_detail(url, college_data)
        college_list.append(college_data)
    print(college_list)
    with open('data.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            ['学校', '学生总数', '国际学生数', '学术教职工', '国际教职工', '学士学位授予数', '硕士学位授予数', '博士学位授予数', '专职科研人员数', '本科新生总数', '硕士新生总数',
             '博士新生总数'])
        for item in college_list:
            writer.writerow(item)
