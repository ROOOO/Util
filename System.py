#coding: utf-8
import os
import time
import platform
import subprocess
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class CSystem:
    def __init__(self):
        pass

    def GetSystemFlag(self):
        return platform.system()

    def WalkPath(self, path):
        # dirPath, dirNames, fileNames
        try:
            os.walk(path)
        except:
            print 'Error path'
            return
        else:
            pass

    def GetFileTime(self, cm, filePath):
        if cm == 'c':
            return os.path.getctime(filePath)
        elif cm == 'm':
            return os.path.getmtime(filePath)

    def StrfTime(self, t):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t))

    def WriteFile(self, filePath, blocks):
        with open(filePath, 'w+') as file:
            file.write(blocks)

    def ReadFile(self, filePath):
        with open(filePath, 'r') as file:
            text = file.read()
        return text or ''

    def KillProcess(self, names, args = []):
        if not isinstance(names, list) or not isinstance(args, list):
            print 'Arg 2 and 3 must be a list'
            return
        sysstr = self.GetSystemFlag()
        for name in names:
            name = name.lower()
            print name
            if sysstr == 'Windows':
                os.system('start taskkill /f /im ' + name)
            else:
                os.system('ps aux | grep ' + name + ' | grep -v grep | cut -c 9-15 | xargs kill -s 9')
                if name == 'phantomjs':
                    os.popen('rm -f ' + args[names.index(name)])

    def RunProcess(self, path, usepopen = False):
        if usepopen:
            return os.popen(path).read()
        return subprocess.call(path, shell = False)

    def Sleep(self, s):
        time.sleep(s)

    def GetDirName(self, path):
        return os.path.dirname(path)

    def GetRealPath(self, file):
        return os.path.realpath(file)
