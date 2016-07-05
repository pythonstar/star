# coding: utf-8

'''
A Common Python Lib By Sing

path
路径操作模块

file
文件操作模块

net
网络操作模块

zip
压缩包操作模块

crypt
加解密操作模块
'''
import os
import re
import sys
import time
import socket
import requests
import urllib
import urllib2
import cookielib
import hashlib
import base64
import logging
import gzip
import StringIO
import datetime
from random import choice
import string
from bs4 import BeautifulSoup

__all__ = ['path', 'file', 'net', 'zip', 'crypt']

'''
把一段内容作为日志保存到当前目录下的log.txt文件中，每次重新创建，不追加！追加模式请使用loga函数。
s：      将要被输出到日志文件的内容
file：   默认为log.txt，也可以指定路径。
mode：   日志文件的打开方式，默认为读写重新创建，也可以重新指定。
'''
def log(s, file = 'log.txt', mode = os.O_RDWR | os.O_CREAT):
    result = False
    fd = os.open(file, mode)
    if fd > 0 :
        try:
            os.write(fd, s)
            result = True
        except:
            print 'can not access file: ' + file + ' open with os.O_RDWR?'
        finally:
            os.close(fd)
    else:
        print 'open file error: ' + file
        print fd
    return result

'''
追加的形式写日志，其他同log函数。
'''
def loga(s, file = 'log.txt'):
    return log(s, file, os.O_RDWR | os.O_APPEND)

'''
一次性读取文本文件中的内容并返回。
file：文本文件的路径。
'''
def readtxtfile(file):
    result = None
    fd = os.open(file, os.O_RDONLY)
    if fd > 0:
        try:
            result = os.read(fd, 999999999)
        except:
            print 'except: readtxtfile'
            result = None
        finally:
            os.close(fd)
    else:
        print 'open file error: ' + file
    return result

# 返回桌面全路径，末尾带\
def getdesktoppath():
    return 'C:\\Users\\xxx\\Desktop\\'

# 返回当前脚本的全路径，末尾带\
def getthispath():
    return os.path.split(os.path.realpath(sys.argv[0]))[0] + '\\'

# 获取一个文件的大小
def getfilesize(f):
    return os.path.getsize(f)

# 命令行下暂停
def pause():
    os.system('pause')

#使用requests库封装一个简单的通过get方式获取网页源码的函数
def gethtml(url, decode = True):
    html = requests.get(url)
    # print html.encoding
    if decode is True:
        s = html.text.encode(html.encoding)
    else:
        s = html.text
    # print s
    return s

# 获取网页源码，内部已设置浏览器引擎防止反爬虫。
def fetch(url):
    request = urllib2.Request(url)
    useragent =  "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0"
    try:
        request.add_header('User-Agent', useragent)
        request.add_header('Referer',url)
        #request.add_header('Cookie',cookie)
        response = urllib2.urlopen(request, timeout=5)
        data = response.read()
        # print '[step 1]get url OK'
        return data
    except :
        # print "NOT OK:%s"%(url)
        return "null"

# 下载网页源码到本地文件
def downloadhtml(url, f):
    filename = None
    try:
        filename = urllib.urlretrieve(url, filename = f)
        # print filename[0], filename[1]
    except:
        print 'except: url miss http...'
        filename = None
    return filename

def resetutf8():
    reload(sys)
    sys.setdefaultencoding('utf-8')

def resetgbk():
    reload(sys)
    sys.setdefaultencoding('GBK')

def quote(s):
    return urllib.quote(s)
def unquote(s):
    return urllib.unquote(s)

''''''''''''''''''''''''''''''''''''''''''
# 计算字符串的MD5值，返回小写的MD5值串
def md5(s):
    m2 = hashlib.md5()
    m2.update(s)
    return m2.hexdigest()

# MD5加密算法，返回32位小写16进制符号
def md5hex(word):

    if isinstance(word, unicode):
        word = word.encode("utf-8")
    elif not isinstance(word, str):
        word = str(word)
    m = hashlib.md5()
    m.update(word)
    return m.hexdigest()

# 计算文件的MD5值
def md5file(fname):
    def read_chunks(fh):
        fh.seek(0)
        chunk = fh.read(8096)
        while chunk:
            yield chunk
            chunk = fh.read(8096)
        else: #最后要将游标放回文件开头
            fh.seek(0)
    m = hashlib.md5()
    if isinstance(fname, basestring) and os.path.exists(fname):
        with open(fname, "rb") as fh:
            for chunk in read_chunks(fh):
                m.update(chunk)
    #上传的文件缓存 或 已打开的文件流
    elif fname.__class__.__name__ in ["StringIO", "StringO"] or isinstance(fname, file):
        for chunk in read_chunks(fname):
            m.update(chunk)
    else:
        return None
    return m.hexdigest()
''''''''''''''''''''''''''''''''''''''''''

def base64(s):
    return base64.b64encode(s)
def base64decode(s):
    return base64.b64decode(s)
''''''''''''''''''''''''''''''''''''''''''

# 解密网络数据中的gzip加密数据
def gzipdecode(data):
    s = StringIO.StringIO(data)
    gziper = gzip.GzipFile(fileobj = s)
    data = gziper.read()
    return data

# def getdata(url):
#     s = requests.session()
#     r = s.get(url)
#     soup = BeautifulSoup(r.text)
#     return soup
#
# def postdata():
#     #用户名和密码
#     login_data = {'username': '用户名', "userpwd":"密码", }
#     headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36'}
#     s = requests.session()
#     r = s.post("http://my.51job.com/my/My_Pmc.php", data=login_data, headers=headers)
#     soup = BeautifulSoup(r.text)
#     return soup

# post数据的示例代码，虽不可重用，但可快速复制修改使用，提高编码效率。
def postdata2():
    data = {'login_email':'xxxx','login_password':'xxxx'}
    post_data = urllib.urlencode(data)
    print post_data
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    headers = {
        'Host':'passport.jiayuan.com',\
        'User-Agent':'Mozilla/5.0 (Windows NT 6.3; rv:35.0) Gecko/20100101 Firefox/35.0',\
        'Accept':'*/*',\
        'Accept-Language':'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',\
        'Accept-Encoding':'gzip, deflate'
    }
    website = 'https://passport.jiayuan.com/dologin.php?pre_url=http://www.jiayuan.com/usercp'
    req = urllib2.Request(website, post_data, headers)
    response = opener.open(req)
    print response.geturl()
    print response.info()
    content = response.read()
    print gzipdecode(content)
    return
''''''''''''''''''''''''''''''''''''''''''
# 日志输出函数，使用示例：
# logger = star.logger().getlogger()
# logger.error('error')
class logger:
    def __init__(self, name = 'log'):
        self.log = logging.getLogger(name)
        self.log.setLevel(logging.DEBUG)

        fmt = '%(asctime)s %(thread)d|%(threadName)s %(filename)s:%(lineno)s %(levelname)s %(name)s :%(message)s'
        formatter = logging.Formatter(fmt)

        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        ch.setLevel(logging.DEBUG)
        fh = logging.FileHandler(name + '.log')
        fh.setFormatter(formatter)
        fh.setLevel(logging.DEBUG)

        self.log.addHandler(fh)
        self.log.addHandler(ch)
    def getlogger(self):
        return self.log

#获取当前时间戳，10位
def gettime10():
    return str(int(time.time()))

#获取当前时间戳，13位
def gettime13():
    return str(int(time.time())) + "000"

#获取当前时间
def getcurrenttime():
    return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

'''
时间记录者，使用示例：
timer = star.timer()
do something..
print u'耗时：' + str(timer.stop()) + ' s'
'''
class timer:
    def __init__(self):
        self.begintime = datetime.datetime.now()
        self.endtime = self.begintime
    def start(self):
        self.begintime = datetime.datetime.now()
    def stop(self):
        self.endtime = datetime.datetime.now()
        cost = self.endtime - self.begintime
        return cost.seconds

# u'<title>个人资料_(\w+)（ID:(\d+)）的个人空间</title>'
def find(reg, content):
    pattern = re.compile(reg, re.U | re.S)
    result = pattern.search(content)
    return result
    # if result is not None:
    #     self.nickname = result.group(1)
    #     self.uid = result.group(2)

# def getImg(html):
#     reg = r'src="(.+?\.jpg)" pic_ext'
#     imgre = re.compile(reg)
#     imglist = re.findall(imgre,html)
#     x = 0
#     for imgurl in imglist:
#         urllib.urlretrieve(imgurl,'%s.jpg' % x)
#         x+=1

""" 或者参考：http://www.phpxs.com/code/1009240

from django.core import mail
connection = mail.get_connection()

# 手动打开链接(connection)
connection.open()

# 使用该链接构造一个邮件报文
email1 = mail.EmailMessage('Hello', 'Body goes here', 'from@example.com',
                          ['to1@example.com'], connection=connection)
email1.send() # 发送邮件

# 构造其他两个报文
email2 = mail.EmailMessage('Hello', 'Body goes here', 'from@example.com',
                          ['to2@example.com'])
email3 = mail.EmailMessage('Hello', 'Body goes here', 'from@example.com',
                          ['to3@example.com'])

# 在一个调用中发送两封邮件
connection.send_messages([email2, email3])
# 链接已打开，因此 send_messages() 不会关闭链接
# 要手动关闭链接
connection.close()
"""

# 生成随机密码
def genpasswd(length=8,chars=string.letters+string.digits):
    return ''.join([ choice(chars) for i in range(length)])


#获取本机无线IP
def getip():
    local_iP = socket.gethostbyname(socket.gethostname())
    return str(local_iP)
    # ip_lists = socket.gethostbyname_ex(socket.gethostname())
    # for ip_list in ip_lists:
    #     print ip_list

#简单的爬虫脚本，用来爬取网页
def getURLContent(url):
        headers = {
               'Accept-Language': 'en-US,en;q=0.5',
               'Accept-Encoding': 'gzip, deflate',
               'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Connection' : 'keep-alive',
               }
        headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0" #USER_AGENTS[random.randint(0, len(USER_AGENTS)-1)]
        try:
            r = requests.get(url, params={'ip': '8.8.8.8'}, headers=headers, timeout=10)
            r.raise_for_status()
        except requests.RequestException as e:
            logging.error(e)
            return None
        else:
           #   print r.encoding
            return r.content
