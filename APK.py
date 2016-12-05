# coding: utf-8
import os
import struct
import logging
from ZipManager import *

class APK:
    def __init__(self):
        pass
    @staticmethod
    def isValidApk(apkPath):
        try:
            if not os.path.exists(apkPath):
                return False
            if not str(apkPath).lower().endswith(".apk"):
                return False

            contentManifest = ZipManager.extractFileContent(apkPath, "AndroidManifest.xml")
            contentDex = ZipManager.extractFileContent(apkPath, "classes.dex")
            if not contentDex or not contentManifest:
                return False
            if len(contentDex) <= 112 or len(contentManifest) <= 8:
                return False

            if APK.isValidDex(contentDex[0:4]) and APK.isValidManifest(contentManifest[0:4]):
                return True
        except Exception, e:
            logging.error(u"[isValidApk] 检测apk是否有效失败，原因：%s", e)
        return False

    @staticmethod
    def isWrapperAlready(apkPath):
        try:
            zipnamelist = ZipManager.getZipNameList(apkPath)
            if "assets/libsecexe.so" in zipnamelist or "assets/data.db" in zipnamelist:
                return True
        except Exception, e:
            logging.error(u"[isWrapperAlready] 检测apk是否加壳失败，原因:%s", e)
        return False

    @staticmethod
    def isValidManifest(magic):
        manifestMagic = struct.unpack('<L', magic)[0]
        # print hex(manifestMagic)
        if hex(manifestMagic) != "0x80003":
            return False
        return True

    @staticmethod
    def isValidDex(magic):
        if magic != "dex\n":
            return False
        return True