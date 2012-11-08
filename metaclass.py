#coding=utf-8
import urllib
import urllib2
import cookielib
import base64
import re
import json
import hashlib
import urlparse
from bs4 import *
import re
from urlparse import *
import StringIO
global stuid
global pw


cj = cookielib.LWPCookieJar()
cookie_support = urllib2.HTTPCookieProcessor(cj)
opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
opener.addheaders = [('User-agent',
                      'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)')]
urllib2.install_opener(opener)


def get(str, i):
    #记录一下，如果不指定i的话会出现奇怪问题，经我分析应该是 不是函数中改变的的最新量，定义一下肯定行，但我不想改了
    try:
        return eval(str)
    except:
        return ""


#只负责登录,非常易于理解的。整个只是一个POST请求而已
def login(user, pw=''):
    cj.clear()  # 清除cookie，否则会受到限制的。但是他肯定是不基于IP限制的了，要不我怎么运行成功呢
    html = urllib2.urlopen("http://jwc.jnu.edu.cn/web/login.aspx").read()
    soup = BeautifulSoup(html)
    code = (soup.find('span', id='lblFJM').contents[0])
    dicta = {}
    for i in soup.findAll("input"):
        if  i['name'] in ('__VIEWSTATE', '__EVENTVALIDATION', 'btnLogin'):
            dicta[i['name']] = i['value'].encode('utf-8')
    dicta['txtFJM'] = code
    dicta['txtYHBS'] = user
    dicta['txtYHMM'] = pw
    req = urllib2.Request("http://jwc.jnu.edu.cn/web/login.aspx",
                          urllib.urlencode(dicta)
                          )
    req.add_header("Referer", "http://jwc.jnu.edu.cn/web/login.aspx")
    resp = urllib2.urlopen(req)
    length = resp.headers['Content-Length']
    if length == "7819":
        #print u"登录失败，密码不正确"
        pass
    elif length == "1325":
      print u"成功登入教务处"
      pass
    else:
        pass
     # print u"失败,可能是现在服务器忙" #
     # print resp.read()
#    raw_input()
#print html


#得到功课表文件
def get_xls(age, qx):
    html  = urllib2.urlopen("http://jwc.jnu.edu.cn/web/Secure/PaiKeXuanKe/wfrm_xk_StudentKcb.aspx").read()
    soup  = BeautifulSoup(html)
    dicta = {}
    for i in soup.findAll("input"):
#     if i.has_key('value'):
        if  i['name'] in ('__VIEWSTATE', '__EVENTVALIDATION', 'btnExpKcb'):
            dicta[i['name']] = i['value'].encode('utf-8')

    qxl                = ['', '', '']
    qxl[1]             = u"第一学期".encode('gbk')
    qxl[2]             = u"第二学期".encode('gbk')
    dicta['dlstXndZ0'] = dicta['dlstXndZ'] = str(age) + "-" + str(age + 1)
    dicta['dlstNdxq']  = dicta['dlstNdxq0'] = qxl[qx]
    req = urllib2.Request(
        "http://jwc.jnu.edu.cn/web/Secure/PaiKeXuanKe/wfrm_xk_StudentKcb.aspx",
        urllib.urlencode(dicta)
    )
    req.add_header("Referer", "http://jwc.jnu.edu.cn/web/Secure/PaiKeXuanKe/wfrm_xk_StudentKcb.aspx")
    resp = urllib2.urlopen(req)

    html = resp.read()
    """至此获得右框架"""
    soup = BeautifulSoup(html)

    nexturl = urljoin("http://jwc.jnu.edu.cn", soup.find('iframe')['src'])
    html    = urllib2.urlopen(nexturl).read()
    """至此获得右框架"""
    soup    = BeautifulSoup(html)
    
    nexturl = urljoin("http://jwc.jnu.edu.cn", soup.findAll('frame')[1]['src'])
    html    = urllib2.urlopen(nexturl).read()
    """至此获得右框架"""
    soup    = BeautifulSoup(html)
    table   = soup.find('table')
    table   = table.find('table')
    table   = table.findAll('table')[1]
    table   = table.find('table')
    list = [([0] * 13) for i in range(7)]
    k = 0
    l = 0
    for tr in table.findAll('tr'):
        l = 0
        k = k + 1
        td = tr.findAll('td')
        for ele in td:
            l = l + 1
            if not ele.find('div') is None:
                if k - 3 > 0 and l - 2 > 0:  # 不显示时间
                    print  (k - 3, l - 2)
                    if k - 3 == 7:
                        list[0][l - 2] = unicode(
                            ele.find('div').contents[0]).encode('gbk')
                    else:
                        list[k - 3][l - 2] = unicode(
                            ele.find('div').contents[0]).encode('gbk')
                    """星期(k-3) 第
          (l-1)节课       ----星期日为星期7 """
        #     import chardet
                    print unicode(ele.find('div').contents[0]).encode('gbk')
    print   eval('"""' + str(list) + '"""')
    """
[[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, '校本部教学大楼403室课程：综合英语Ⅰ(05021109)', 0,
 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, '校本部教学大楼604室  课程：大学语文(01030009)', '校本部教学大楼604室
 课程：大学语文(01030009)', 0, 0, '本部体育馆内羽毛球场
 课程：体育Ⅰ(01040001)', '本部体育馆内羽毛球场
 课程：体育Ⅰ(01040001)', 0, 0, 0, 0, 0], [0, '校本部教学大楼402室
 课程：综合英语Ⅰ(05021109)', '校本部南海楼608
 课程：问题求解与程序设计实验（全英）(60080004)', '校本部南海楼608
 课程：问题求解与程序设计实验（全英）(60080004)', 0, 0, '校本部教学大楼513室
 课程：计算机导论（全英）(60080002)', '校本部教学大楼513室
 课程：计算机导论（全英）(60080002)', '校本部教学大楼513室
 课程：计算机导论（全英）(60080002)', 0, 0, 0, 0], [0, 0, '校本部教学大楼1206室
 课程：英语口语(05023021)', '校本部教学大楼1206室
 课程：英语口语(05023021)', 0, 0, 0, 0, 0, 0, '校本部教学大楼513室
 课程：高等数学(信息类)Ⅰ（全英）(60080001)', '校本部教学大楼513室
 课程：高等数学(信息类)Ⅰ（全英）(60080001)', '校本部教学大楼513室
 课程：高等数学(信息类)Ⅰ（全英）(60080001)'], [0, 0, '校本部教学大楼505室
 课程：中国近现代史纲要(01010018)', '校本部教学大楼505室
 课程：中国近现代史纲要(01010018)', 0, 0, '校本部教学大楼512室
 课程：问题求解与程序设计（全英）(60080003)', '校本部教学大楼512室
 课程：问题求解与程序设计（全英）(60080003)', '校本部教学大楼512室
 课程：问题求解与程序设计（全英）(60080003)', 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0,0, 0, 0, 0, 0, 0]]
  """

    list = [
        "08:00-08:50",
        "09:00-09:50",
        "10:20-11:10",
        "11:20-12:10",
        "13:00-13:50",
        "14:00-14:50",
        "15:00-15:50",
        "16:00-16:50",
        "17:00-17:50",
        "18:00-18:50",
        "19:00-19:50",
        "20:00-20:50",
        "21:00-21:50",
    ]


"""
       -1 1 周
-1 2 节1
-1 3 节2
-1 4 节3
-1 5 节4
-1 6 节5
-1 7 节6
-1 8 节7
-1 9 节8
-1 10 节9
-1 11 节10
-1 12 节11
-1 13 节12
-1 14 节13
-1 15 节14
0 1
0 2 08:00-08:50
0 3 09:00-09:50
0 4 10:20-11:10
0 5 11:20-12:10
0 6 13:00-13:50
0 7 14:00-14:50
0 8 15:00-15:50
0 9 16:00-16:50
0 10 17:00-17:50
0 11 18:00-18:50
0 12 19:00-19:50
0 13 20:00-20:50
0 14 21:00-21:50
1 1 周一
1 2 校本部教学大楼403室
 课程：综合英语Ⅰ(05021109)
1 3 校本部教学大楼403室
 课程：综合英语Ⅰ(05021109)
2 1 周二
2 4 校本部教学大楼604室
 课程：大学语文(01030009)
2 5 校本部教学大楼604室
 课程：大学语文(01030009)
2 8 本部体育馆内羽毛球场
 课程：体育Ⅰ(01040001)
2 9 本部体育馆内羽毛球场
 课程：体育Ⅰ(01040001)
3 1 周三
3 2 校本部教学大楼402室
 课程：综合英语Ⅰ(05021109)
3 3 校本部教学大楼402室
 课程：综合英语Ⅰ(05021109)
3 4 校本部南海楼608
 课程：问题求解与程序设计实验（全英）(60080004)
3 5 校本部南海楼608
 课程：问题求解与程序设计实验（全英）(60080004)
3 8 校本部教学大楼513室
 课程：计算机导论（全英）(60080002)
3 9 校本部教学大楼513室
 课程：计算机导论（全英）(60080002)
3 10 校本部教学大楼513室
 课程：计算机导论（全英）(60080002)
4 1 周四
4 4 校本部教学大楼1206室
 课程：英语口语(05023021)
4 5 校本部教学大楼1206室
 课程：英语口语(05023021)
4 12 校本部教学大楼513室
 课程：高等数学(信息类)Ⅰ（全英）(60080001)
4 13 校本部教学大楼513室
 课程：高等数学(信息类)Ⅰ（全英）(60080001)
4 14 校本部教学大楼513室
 课程：高等数学(信息类)Ⅰ（全英）(60080001)
5 1 周五
5 4 校本部教学大楼505室
 课程：中国近现代史纲要(01010018)
5 5 校本部教学大楼505室
 课程：中国近现代史纲要(01010018)
5 8 校本部教学大楼512室
 课程：问题求解与程序设计（全英）(60080003)
5 9 校本部教学大楼512室
 课程：问题求解与程序设计（全英）(60080003)
5 10 校本部教学大楼512室
 课程：问题求解与程序设计（全英）(60080003)
6 1 周六
7 1 周日
"""


stuid = "2012052690"
pw = "143217"
login(stuid, pw)
get_xls(2012, 1)
