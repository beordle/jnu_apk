#coding=utf-8
import urllib,urllib2,cookielib,base64,re,json,hashlib,StringIO,urlparse
from bs4 import *
from urlparse import *
global user
global pw
import requests

def login(username,password):
    #所有请求均使用本headers 这两个字段对方均会检查
    headers={'User-agent':'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        "Referer": "http://jwc.jnu.edu.cn/web/login.aspx"}
    #创建一个浏览器会话
    s = requests.session(headers=headers)

    #发起GET请求
    html=s.get("http://jwc.jnu.edu.cn/web/login.aspx").text

    #解析页面验证码并完成初始化cookie工作
    soup = BeautifulSoup(html)
    code = (soup.find('span', id='lblFJM').contents[0])#<span id="lblFJM'的正文为验证码
    dict = {}
    for i in soup.findAll("input"):#搜索表单,并填写
        if  i['name'] in ('__VIEWSTATE', '__EVENTVALIDATION', 'btnLogin'):
            dict[i['name']] = i['value'].encode('utf-8')
    dict['txtFJM'] = code
    dict['txtYHBS'] = username
    dict['txtYHMM'] = password

    #发起POST
    length=s.post(
        "http://jwc.jnu.edu.cn/web/login.aspx",
        data=dict,
        ).headers['Content-Length']

    if length == "7819":
        return None#密码不正确
    if length == "1325":
        #返回一个浏览器会话
        return s
    return None#当请求过于频繁，服务器过载时可能发生


#得到功课表文件
def get_xls(s,age, qx):
    #提供简单的第一学期第二学期的包装，可以将POST的string数据 像这样qxl(1) qxl(2)调用
    qxl                = ['', '', '']
    qxl[1]             = u"第一学期".encode('gbk')
    qxl[2]             = u"第二学期".encode('gbk')

    html  = s.get("http://jwc.jnu.edu.cn/web/Secure/PaiKeXuanKe/wfrm_xk_StudentKcb.aspx").text
    soup  = BeautifulSoup(html)
    dict = {}

    #搜索表单并填写
    for i in soup.findAll("input"):
        if  i['name'] in ('__VIEWSTATE', '__EVENTVALIDATION', 'btnExpKcb'):
            dict[i['name']] = i['value'].encode('utf-8')
    dict['dlstXndZ0'] = dict['dlstXndZ'] = str(age) + "-" + str(age + 1)
    dict['dlstNdxq']  = dict['dlstNdxq0'] = qxl[qx]
    #发起POST请求
    html = s.post(
        "http://jwc.jnu.edu.cn/web/Secure/PaiKeXuanKe/wfrm_xk_StudentKcb.aspx",
        data=dict
    ).text
    #原页面为多级iframe嵌套，所以这里可能难于理解
    nexturl = urljoin("http://jwc.jnu.edu.cn", BeautifulSoup(html).find('iframe')['src'])
    soup    = BeautifulSoup(s.get(nexturl).text)
    #其中第二个iframe是我们需要的，但是他不是iframe标签，没有i
    nexturl = urljoin("http://jwc.jnu.edu.cn", soup.findAll('frame')[1]['src'])
    html    = s.get(nexturl).text
    soup    = BeautifulSoup(html)
    #多级table嵌套
    table   = soup.find('table').find('table').findAll('table')[1].find('table')

    list = [([0] * 13) for i in range(7)]
    k = 0
    for tr in table.findAll('tr'):
        l = 0
        k = k + 1
        td = tr.findAll('td')
        for ele in td:
            l = l + 1
            if not ele.find('div') is None:
                if k - 3 > 0 and l - 2 > 0:  # 不显示时间

                    if k - 3 == 7:
                        list[0][l - 2] = unicode(
                            ele.find('div').contents[0]).encode('gbk')
                    else:
                        list[k - 3][l - 2] = unicode(
                            ele.find('div').contents[0]).encode('gbk')
                            #要输出可以用print unicode(ele.find('div').contents[0]).encode('gbk')
    print   eval('"""' + str(list) + '"""')

get_xls(login('2012052690','143217'),2012,1)