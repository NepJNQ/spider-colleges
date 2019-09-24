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

        # 学生总数
        if html.xpath(
                '//div[@class="data-item first"]//div[@class="t-slack sep"]/div[@class="t-dim"]/text()[.="Total '
                'number of students"]'):
            t1 = html.xpath('//div[@class="data-item first"]//div[@class="t-slack sep"]/div[@class="right '
                            't-strong"]/text()')
            t1 = t1[0].replace(' ', '').replace('\n', '')
        else:
            t1 = ''
        college_data.append(t1)

        # 国际学生数
        if html.xpath(
                '//div[@class="data-item first"]//div[@class="t-slack sep"]/div[@class="t-dim"]/text()[.="Number of '
                'international students"]'):
            t2 = html.xpath('//div[@class="data-item first"]//div[@class="t-slack sep"]/div[@class="right '
                            't-strong"]/text()')
            t2 = t2[0].replace(' ', '').replace('\n', '')
        else:
            t2 = ''
        college_data.append(t2)

        # 学术教职工
        if html.xpath(
                '//div[@class="data-item first"]//div[@class="t-slack sep"]/div[@class="t-dim"]/text()[.="Total number of academic staff"]'):
            t3 = html.xpath('//div[@class="data-item first"]//div[@class="t-slack sep"]/div[@class="right '
                            't-strong"]/text()')
            t3 = t3[0].replace(' ', '').replace('\n', '')
        else:
            t3 = ''
        college_data.append(t3)

        # 国际职工数
        if html.xpath(
                '//div[@class="data-item first"]//div[@class="t-slack sep"]/div[@class="t-dim"]/text()[.="Number of international staff"]'):
            t4 = html.xpath('//div[@class="data-item first"]//div[@class="t-slack sep"]/div[@class="right '
                            't-strong"]/text()')
            t4 = t4[0].replace(' ', '').replace('\n', '')
        else:
            t4 = ''
        college_data.append(t4)

        # 学士授予数
        if html.xpath(
                '//div[@class="data-item first"]//div[@class="t-slack sep"]/div[@class="t-dim"]/text()[.="Number of undergraduate degrees awarded"]'):
            t5 = html.xpath('//div[@class="data-item first"]//div[@class="t-slack sep"]/div[@class="right '
                            't-strong"]/text()')
            t5 = t5[0].replace(' ', '').replace('\n', '')
        else:
            t5 = ''
        college_data.append(t5)

        # 硕士授予数
        if html.xpath(
                '//div[@class="data-item first"]//div[@class="t-slack sep"]/div[@class="t-dim"]/text()[.="Number of master\'s degrees awarded"]'):
            t6 = html.xpath('//div[@class="data-item first"]//div[@class="t-slack sep"]/div[@class="right '
                            't-strong"]/text()')
            t6 = t6[0].replace(' ', '').replace('\n', '')
        else:
            t6 = ''
        college_data.append(t6)

        # 博士授予数
        if html.xpath(
                '//div[@class="data-item first"]//div[@class="t-slack sep"]/div[@class="t-dim"]/text()[.="Number of doctoral degrees awarded"]'):
            t7 = html.xpath('//div[@class="data-item first"]//div[@class="t-slack sep"]/div[@class="right '
                            't-strong"]/text()')
            t7 = t7[0].replace(' ', '').replace('\n', '')
        else:
            t7 = ''
        college_data.append(t7)

        # 专职科研数
        if html.xpath(
                '//div[@class="data-item first"]//div[@class="t-slack sep"]/div[@class="t-dim"]/text()[.="Number of research only staff"]'):
            t8 = html.xpath('//div[@class="data-item first"]//div[@class="t-slack sep"]/div[@class="right '
                            't-strong"]/text()')
            t8 = t8[0].replace(' ', '').replace('\n', '')
        else:
            t8 = ''
        college_data.append(t8)

        # 本科新生数
        if html.xpath(
                '//div[@class="data-item first"]//div[@class="t-slack sep"]/div[@class="t-dim"]/text()[.="Number of new undergraduate students"]'):
            t9 = html.xpath('//div[@class="data-item first"]//div[@class="t-slack sep"]/div[@class="right '
                            't-strong"]/text()')
            t9 = t9[0].replace(' ', '').replace('\n', '')
        else:
            t9 = ''
        college_data.append(t9)

        # 硕士新生数
        if html.xpath(
                '//div[@class="data-item first"]//div[@class="t-slack sep"]/div[@class="t-dim"]/text()[.="Number of new master\'s students"]'):
            t10 = html.xpath('//div[@class="data-item first"]//div[@class="t-slack sep"]/div[@class="right '
                             't-strong"]/text()')
            t10 = t10[0].replace(' ', '').replace('\n', '')
        else:
            t10 = ''
        college_data.append(t10)

        # 博士新生数
        if html.xpath(
                '//div[@class="data-item first"]//div[@class="t-slack sep"]/div[@class="t-dim"]/text()[.="Number of new doctoral students"]'):
            t11 = html.xpath('//div[@class="data-item first"]//div[@class="t-slack sep"]/div[@class="right '
                             't-strong"]/text()')
            t11 = t11[0].replace(' ', '').replace('\n', '')
        else:
            t11 = ''
        college_data.append(t11)

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
