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

加解密操作模块

pycrypto https://www.dlitz.net/software/pycrypto/
'''
import os
import re
import sys
import uuid
import time
import shutil
import socket
import requests
import zlib
import gzip
import urllib
import urllib2
import cookielib
import base64
import hashlib
import logging
import string
import StringIO
import datetime
from random import choice
from bs4 import BeautifulSoup
from win32com.shell import shell
from win32com.shell import shellcon
# from Crypto.Cipher import AES

__all__ = ['path', 'file', 'net', 'zip', 'crypt']

###################################################
'''
调试相关
'''
###################################################

'''
示例：
star.initlogging()
logging.debug(u"%s %d", u"哈", 1)
'''
def initlogging(logfilename = u"log.txt"):
    '''
    binPath = os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), "bin")
    pid = '%d' % (os.getpid())
    logging.basicConfig(level=logging.DEBUG,
            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            filename=u'%s%swrap_%s.log' % (binPath, os.sep, pid),
            filemode='a')
    #################################################################################################
    #定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    #################################################################################################
    '''
    logging.basicConfig(stream=sys.stdout,
                        format = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt = '%Y-%m-%d %H:%M:%S',
                        filename = logfilename,
                        filemode = 'a',
                        level = logging.DEBUG)

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

# 命令行下暂停
def pause():
    os.system('pause')


"""
时间记录的函数和装饰器
"""
class TimeRecorder:
    def __init__(self, name):
        print(name + u" start")
        self.name = name
        self.startTime = time.time()
    def __del__(self):
        print(u"{0} end, time used: {1}".format(self.name, time.time() - self.startTime))

"""
def scan1():
    t = TimeRecorder(scan1.func_name)
    time.sleep(1)
    return 1

print scan1()
"""


# 函数装饰器，让函数打印耗时
def logtime(func):
    def wrapper(*args, **kwargs):
        print(func.func_name + u" start")
        startTime = time.time()
        ret = func(*args, **kwargs)
        print(u"{0} end, time used: {1}".format(func.func_name, time.time() - startTime))
        return ret
    return wrapper

# 指定一个名称
def logtimewithname(name = None):
    def wrapper(func):
        def wrapper2(*args, **kwargs):
            _name = name
            if name is None:
                _name = func.func_name
            else:
                _name = name
            print(_name + u" start")
            startTime = time.time()
            res = func(*args, **kwargs)
            print(u"{0} end, time used: {1}".format(_name, time.time() - startTime))
            return res
        return wrapper2
    return wrapper


# 函数限定时间运行
def timelimit(interval):
    def time_out():
        raise Exception("time out")

    def wrapper(func):
        def wrapper2(*args, **kwargs):
            print(func.func_name + u" start")
            timer = Timer(interval, time_out)
            timer.start()
            startTime = time.time()
            res = func(*args, **kwargs)
            timer.cancel()
            print(u"{0} end time: {1}".format(func.func_name, time.time() - startTime))
            return res
        return wrapper2
    return wrapper




class TimeoutException(Exception):
    pass

# 函数限定时间运行
def timelimited(timeout):
    def decorator(func):
        def decorator2(*args,**kwargs):
            class TimeLimited(Thread):
                def __init__(self):
                    Thread.__init__(self)
                    self._error = None
                    self._result = None

                def run(self):
                    try:
                        print(func.func_name + u" start")
                        startTime = time.time()
                        self._result = func(*args, **kwargs)
                        print(u"{0} end time: {1}".format(func.func_name, time.time() - startTime))
                    except Exception, e:
                        self._error = e

                def _stop(self):
                    if self.isAlive():
                        Thread._Thread__stop(self)

            t = TimeLimited()
            t.start()
            t.join(timeout)

            if t.isAlive():
                t._stop()
                raise TimeoutException('timeout for %s' % (repr(func)))

            if isinstance(t._error, TimeoutException):
                t._stop()
                raise TimeoutException('timeout for %s' % (repr(func)))

            if t._error is None:
                return t._result

        return decorator2
    return decorator

"""
@logtime
def scan1(p1, p2):
    time.sleep(1)
    return 1
print scan1(1, 2)

# @logtimewithname()
@logtimewithname(u"扫描")
def scan2(p1, p2):
    time.sleep(1)
    return 2

print scan2(1, 2)

@timelimited(2)
def scan3():
    time.sleep(3)

scan3()
"""
###################################################

###################################################
'''
系统相关
'''
###################################################
#获取本机IP
def getip():
    local_iP = socket.gethostbyname(socket.gethostname())
    return str(local_iP)
    # ip_lists = socket.gethostbyname_ex(socket.gethostname())
    # for ip_list in ip_lists:
    #     print ip_list
def getmac():
    return ':'.join(['{:02X}'.format((uuid.getnode() >> i) & 0xff) for i in range(0, 8 * 6, 8)][::-1])

# def setclipboard(s):
#     win32clipboard.OpenClipboard()
#     win32clipboard.EmptyClipboard()
#     win32clipboard.SetClipboardText(s)
#     win32clipboard.CloseClipboard()

#获取当前时间戳，10位
def gettime10():
    return str(int(time.time()))

#获取当前时间戳，13位
def gettime13():
    return "%d" % (time.time() * 1000)

#获取当前时间
def getcurrenttime():
    return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

def resetutf8():
    reload(sys)
    sys.setdefaultencoding('utf-8')

def resetgbk():
    reload(sys)
    sys.setdefaultencoding('GBK')

def run(args):
    if 'Windows' in platform.system():
        command = args.encode("utf-8")
        command = command.decode("utf-8").encode("gbk")
    if 'Linux'in platform.system():
        command = args
    p = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    # ret = p.wait() #该方法有问题
    ret = p.communicate()
    output = Utils.out2str(p.stdout.readlines())
    error = Utils.out2str(p.stderr.readlines())
    # return output if ret is 0 else error
    return star.commandResult2Str(ret)

def runJar(args):
    return Utils.run(args)

def commandResult2Str(text_seq):
    out = ''
    result = True
    try:
        out = str.strip(" ".join(text_seq).replace("\r", "").replace("\n", "")).decode('utf-8')
    except Exception, e:
        logging.warn(u"[out2str] 运行结果utf-8转码错误，将尝试gbk转码")
        result = False

    if not result:
        try:
            result = True
            out = str.strip(" ".join(text_seq).replace("\r", "").replace("\n", "")).decode('gbk')
        except Exception, e:
            logging.warn(u"[out2str] 运行结果gbk转码错误，将输出空字符")
            result = False

    if not result:
        out = ''
    return out
###################################################
'''
文件，路径相关
'''
###################################################

'''
返回桌面全路径，末尾带\
from win32com.shell import shell
from win32com.shell import shellcon
'''
def getdesktoppath():
    # return 'C:\\Users\\xxx\\Desktop\\'
    desktop_path = shell.SHGetPathFromIDList(shell.SHGetSpecialFolderLocation(0, shellcon.CSIDL_DESKTOP))
    return desktop_path + "\\"


# 返回当前脚本的全路径，末尾带\
def getthispath():
    path = sys.path[0]
    #判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
    if os.path.isdir(path):
        return path + '\\'
    elif os.path.isfile(path):
        return os.path.split(path)[0] + '\\'

# 获取路径的父目录，末尾不带\
def getparent(filepath):
    if not filepath:
        return None
    lsPath = os.path.split(filepath)
    # print(lsPath)
    # print("lsPath[1] = %s" %lsPath[1])
    if lsPath[1]:
        return lsPath[0]
    lsPath = os.path.split(lsPath[0])
    return lsPath[0]

# 获取一个文件的大小
def getfilesize(f):
    return os.path.getsize(f)

'''
一次性读取文本文件中的内容并返回。
file：文本文件的路径。
'''
def read(filename, binary=True):
    try:
        with open(filename, 'rb' if binary else 'r') as f:
            return f.read()
    except Exception as e:
        print e
        return None

def write(filename, buf, binary=True):
    try:
        with open(filename, 'wb' if binary else 'w') as f:
            return f.write(buf)
    except Exception as e:
        print e
        return None

# 创建多级目录，比如c:\\test1\\test2,如果test1 test2都不存在，都将被创建
def createdirs(to_create_path):
    path_create = to_create_path
    if os.sep == '\\':
        path_create = path_create.replace('/', os.sep)
    dirs = path_create.split(os.sep)
    path = ''
    for dir in dirs:
        dir += os.sep
        path = os.path.join(path, dir)
        if not os.path.exists(path):
            os.mkdir(path, 0o777)

    if not os.path.exists(to_create_path):
        return False
    return True

def deletedirs(to_del_dirs):
    if os.path.exists(to_del_dirs):
        shutil.rmtree(to_del_dirs)
        return os.path.exists(to_del_dirs) is False
    else:
        return True

# 目录下文件大小累加
def getdirsize(path):
    size = 0L
    for root, dirs, files in os.walk(path, True):
        size += sum([os.path.getsize(os.path.join(root, name)) for name in files])
        return size

def deletefile(to_del_file):
    if os.path.exists(to_del_file):
         os.remove(to_del_file)
         return os.path.exists(to_del_file) is False
    else:
        return True

def copyfile(sourceDir, destDir):
    if deletefile(destDir):
        shutil.copy(sourceDir, destDir)
        return os.path.exists(destDir)
    else:
        return False

def movefile(sourceDir, destDir):
    if deletefile(destDir):
        shutil.move(sourceDir, destDir)
        return os.path.exists(destDir)
    else:
        return False

# print star.file.isendwith(filename, "txt", "apk")
def isendwith(file, *endstring):
    return True in map(file.endswith, endstring)

# print star.file.isEndWith(filename, ["txt", "apk"])
# def isEndWith(file, endstring):
#     return True in map(file.endswith, endstring)

# filelist = Utils.getFileNameListFormDir(metainfPath, ['.rsa', '.dsa'])
def getfilenamelistformdir(path, endstringlist):
    retlist = []
    try:
        if os.path.exists(path):
            flist = os.listdir(path)
            for f in flist:
                if os.path.splitext(f)[1].lower() in endstringlist:
                    retlist.append(f)
    except Exception, e:
        logging.error(u"[getFileListFormDir] 获取特定后缀名%s的文件失败，路径:%s", str(endstringlist), path)
        return []
    return retlist

# smaliFileList = Utils.getFileListFromDir(outDir, '.smali')
def getfilelistfromdir(rootPath, endstring):
    fileList = []
    try:
        for root, dirs, files in os.walk(rootPath):
            for name in files:
                lowerName = name.lower()
                if lowerName.endswith(endstring):
                    fileList.append(os.path.join(root, name))
    except Exception, e:
        logging.error(u"[getFileListFromDir] 从目录%s获取特定后缀名%s的文件失败", rootPath, endstring)
        return []
    return fileList

def gbk2unicode(s):
    return s.decode('gbk', 'ignore')

# 脚本文件#coding:utf-8时默认不带u的字符串为utf8字符串：star.utf82unicode('我')
def utf82unicode(s):
    return s.decode('utf-8', 'ignore')

# 带u的字符串为unicode
# star.unicode2gbk(u'\u4e5f\u6709')
# star.unicode2gbk(u'也有')
def unicode2gbk(s):
    return s.encode('gbk')

# 带u的字符串为unicode
# star.unicode2utf8(u'\u4e5f\u6709')
# star.unicode2utf8(u'也有')
def unicode2utf8(s):
    return s.encode('utf-8')

# win下命令行参数为gbk编码：star.gbk2utf8(sys.argv[1]) + '也有'
def gbk2utf8(s):
    return s.decode('gbk', 'ignore').encode('utf-8')

def utf82gbk(s):
    return s.decode('utf-8', 'ignore').encode('gbk')
###################################################
'''
网络相关
'''
###################################################

#使用requests库封装一个简单的通过get方式获取网页源码的函数
def gethtml(url, decode = True):
    html = requests.get(url)
    # print html.encoding
    if decode is True:
        s = html.text.encode(html.encoding)
    else:
        s = html.text
    # s = BeautifulSoup(s, "lxml")
    return s

#简单的爬虫脚本，用来爬取网页gethtmlex('xxxxx', {'ip': '8.8.8.8'})
def gethtmlex(url, params = None):
    headers = {
           'Accept-Language': 'en-US,en;q=0.5',
           'Accept-Encoding': 'gzip, deflate',
           'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Connection' : 'keep-alive',
           }
    headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0" #USER_AGENTS[random.randint(0, len(USER_AGENTS)-1)]
    try:
        r = requests.get(url, params=params, headers=headers, timeout=10)
        r.raise_for_status()
    except requests.RequestException as e:
        logging.error(e)
        return None
    else:
       #   print r.encoding
        return r.content

# 获取网页源码，内部已设置浏览器引擎防止反爬虫。
def fetchurl(url):
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
        return None

# 下载网页源码到本地文件
def download(url, f):
    filename = None
    try:
        filename = urllib.urlretrieve(url, filename = f)
        # print filename[0], filename[1]
    except:
        print 'except: url miss http...'
        filename = None
    return filename

# star.quote("你好") 输出 %E4%BD%A0%E5%A5%BD
def quote(s):
    return urllib.quote(s)
# star.unquote("%E4%BD%A0%E5%A5%BD") 输出 你好
def unquote(s):
    return urllib.unquote(s)


# 解密网络数据中的gzip加密数据
def gzipdecode(data):
    s = StringIO.StringIO(data)
    gziper = gzip.GzipFile(fileobj = s)
    data = gziper.read()
    return data


# print star.post("http://www.ximalaya.com/tracks/19158075/play", {'played_secs': 0, "duration": 0})
def post(url, data, headers = None):
    h = headers
    if h is None:
        h = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36'}
    s = requests.session()
    r = s.post(url, data = data, headers = h)
    soup = BeautifulSoup(r.text, "lxml")
    return soup

# print star.postdata("http://www.ximalaya.com/tracks/19158075/play", {'played_secs': 0, "duration": 0})
def postdata(url, data, headers = None, isdecode = False):
    post_data = urllib.urlencode(data)  #duration=0&played_secs=0
    h = headers
    if h is None:
        h = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36'}
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    req = urllib2.Request(url, post_data, h)
    response = opener.open(req)
    # print response.geturl()
    # print response.info()
    content = response.read()
    if isdecode is True:
        content = gzipdecode(content)
    return content
###################################################
'''
加解密
'''
###################################################
#  生成随机密码
def genpasswd(length=8, chars = string.letters + string.digits):
    return ''.join([choice(chars) for i in range(length)])

# 计算字符串的MD5值，返回32个字符长度小写16进制符号
def md5hex(buf):
    if isinstance(buf, unicode):
        buf = buf.encode("utf-8")
    elif not isinstance(buf, str):
        buf = str(buf)
    m = hashlib.md5()
    m.update(buf)
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

# 获取文件的sha1值，大写
def sha1file(file_path):
    with open(file_path, "rb") as file:
        s = sha1()
        while True:
            strRead = file.read(1024 * 1024)
            if not strRead:
                break
            s.update(file.read())
    return s.hexdigest().upper()

def getcrc32(s):
    return zlib.crc32(s)

# key = '0123456789abcdef'
def aesencode(s, key):
    mode = AES.MODE_CBC
    encryptor = AES.new(key, mode)
    r = encryptor.encrypt(s)
    return r

def aesdecode(s, key):
    mode = AES.MODE_CBC
    decryptor = AES.new(key, mode)
    r = decryptor.decrypt(s)
    return r

def base64encode(s):
    return base64.b64encode(s)
def base64decode(s):
    return base64.b64decode(s)
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

'''
在content中查找规则为reg的字符串，如果指定捕获的结果列表，则按指定的序号(基数从1开始)返回。
如果未指定结果列表则直接返回命中结果，由调用者自行提取。
若未命中返回None，指定的多返回结果也均为None。

x, y = star.find('"(.*?)"(.*?)"(.*?)"', '"10"20"30"', [2,1])
print x, y  #20 10
x, y = star.find('"(.*?)"(.*?)"(.*?)"1', '"10"20"30"', [2,1])
print x, y  #None None
print star.find('"(.*?)"(.*?)"(.*?)"', '"10"20"30"')    #<_sre.SRE_Match object at 0x03123840>
print star.find('"(.*?)"(.*?)"(.*?)"1', '"10"20"30"')   #None
'''
def find(reg, content, group = None):
    pattern = re.compile(reg, re.U | re.S)
    result = pattern.search(content)
    if result is not None:
        if group is None:
            return result
        else:
            return (result.group(i) for i in group)
    else:
        if group is None:
            return None
        else:
            return (None for i in group)

def search(reg, content, group = None):
    star.find(reg, content, group)

'''
s = 'dd10aa20ccdd30aa40ccdd50aa60ccdd70aa80cc'
r = star.findall('dd(.*?)aa(.*?)cc', s)
[('10', '20'), ('30', '40'), ('50', '60'), ('70', '80')]

findall(r"<a.*?href=.*?<\/a>",ss,re.I)
'''
def findall(reg, content):
    r = re.findall(reg, content)
    return r

# 先抓大后抓小
# html = star.gethtml("https://github.com/pythonstar/star/wiki/%E8%AF%B4%E6%98%8E%E6%96%87%E6%A1%A3")
# result = star.find('"wiki-pages"(.*?)"wiki-more-pages-link"', html)
# print result
# if result is not None:
#     r = re.findall(r'href="(.*?)" class="wiki-page-link">(.*?)<', result.group(1))
#     for i in r:
#         s = '[' + i[1] + '](https://github.com' + i[0] + ')'
#         print s


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


