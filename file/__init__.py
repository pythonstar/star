# coding: utf-8
import os
import sys

# 返回当前脚本的全路径，末尾带\
def getthispath():
    return os.path.split(os.path.realpath(sys.argv[0]))[0] + '\\'

# 获取一个文件的大小
def getfilesize(f):
    return os.path.getsize(f)

def createDirs(to_create_path):
    #创建多级目录，比如c:\\test1\\test2,如果test1 test2都不存在，都将被创建
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

def deleteDirs(to_del_dirs):
    if os.path.exists(to_del_dirs):
        shutil.rmtree(to_del_dirs)

def deleteFile(to_del_file):
    if os.path.exists(to_del_file):
         os.remove(to_del_file)
    else:
        return True

    if not os.path.exists(to_del_file):
        return True
    else:
        return False

def copyFile(sourceDir, destDir):
    if deleteFile(destDir):
        shutil.copy(sourceDir, destDir)
        if os.path.exists(destDir):
            return True

    return False

def moveFile(sourceDir, destDir):
    if deleteFile(destDir):
        shutil.move(sourceDir, destDir)
        if os.path.exists(destDir):
            return True

    return False

# print star.file.isEndWith(filename, "txt", "apk")
def isEndWith(file, *endstring):
    return True in map(file.endswith, endstring)

# print star.file.isEndWith(filename, ["txt", "apk"])
# def isEndWith(file, endstring):
#     return True in map(file.endswith, endstring)

# filelist = Utils.getFileNameListFormDir(metainfPath, ['.rsa', '.dsa'])
def getFileNameListFormDir(path, endstringlist):
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
def getFileListFromDir(rootPath, endstring):
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
