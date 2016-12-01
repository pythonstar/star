# coding: utf-8
import os
import sys

# 返回当前脚本的全路径，末尾带\
def getthispath():
    return os.path.split(os.path.realpath(sys.argv[0]))[0] + '\\'

# 获取一个文件的大小
def getfilesize(f):
    return os.path.getsize(f)