#coding: utf-8
import os
import re
import platform
import attr

from util import CSystem

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class CWebElement:
    def __init__(self, driver):
        self.__driver = driver
        self.element = 0

    def Find(self, by, arg):
        # http://selenium-python.readthedocs.io/locating-elements.html
        by = by.lower()
        if by == 'xpaths':
            by = 'find_elements_by_xpath'
        else:
            by = 'find_element_by_' + by
        self.element = getattr(self.__driver, by)(arg)
        return self

    def Count(self):
        return len(self.element)

    def SendKeys(self, s):
        self.element.send_keys(s)
        return self

    def Keys(self, key):
        return getattr(Keys, key)

    def GetElements(self):
        return self.element

class CWeb:
    def __init__(self, settings = {}, ws = '', cookie = ''):
        self.__ss = CSystem()
        if ws != '':
            self.__workSpace = ws
        else:
            self.__workSpace = os.path.join(self.__ss.GetDirName(self.__ss.GetDirName(self.__ss.GetRealPath(__file__))), '3rdTools')

        if settings != {}:
            self.__driverType = settings['Driver'][settings['Driver']['use']].lower()
        else:
            self.__driverType = 'phantomjs'
        self.__InitDriver(cookie)

    def __InitDriver(self, cookie):
        args = []
        if cookie != '':
            args.append('--cookies-file=' + cookie)

        headers = { 'Accept':'*/*',
            'Accept-Encoding':'gzip, deflate, sdch',
            'Accept-Language':'en-US,en;q=0.8',
            'Cache-Control':'max-age=0',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
        }
        for key, value in enumerate(headers):
            webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.{}'.format(key)] = value

        sysstr = platform.system()
        if sysstr == 'Linux':
            self.__ss.RunProcess('chmod +x ' + os.path.join(self.__workSpace, 'phantomjs'), usepopen = True)
            self.__driver = webdriver.PhantomJS(os.path.join(self.__workSpace, 'phantomjs'), service_args = args)
            self.__driverType = 'phantomjs'
        elif sysstr == 'Windows':
            if self.__driverType == 'phantomjs':
                self.__driver = webdriver.PhantomJS(os.path.join(self.__workSpace, 'phantomjs_win.exe'), service_args = args)
            elif self.__driverType == 'chromedriver':
                self.__driver = webdriver.Chrome(os.path.join(self.__workSpace, 'chromedriver.exe'))
        elif sysstr == 'Darwin':
            # self.__class__.CU.runProcess('chmod +x ./phantomjs', usepopen = True)
            # self.driver = webdriver.PhantomJS(os.path.join(os.path.split(os.path.realpath(__file__))[0], 'phantomjs'))
            self.__driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.__driver, 5)

    def GetDriver(self, driver = ''):
        driver = driver == '' and self.__driver or driver
        return driver

    def Goto(self, page, driver = ''):
        page = page.lower()
        if not re.match(r'http', page):
            page = 'http://' + page
        driver = self.__driver.get(page)
        return self

    def GoBack(self):
        self.__driver.back()
    def Forward(self):
        self.__driver.forward()

    def GetPageSource(self):
        return self.__driver.page_source

    def WaitUntil(self, condition, by, arg, b = ''):
        # http://selenium-python.readthedocs.io/waits.html
        if b == '':
            elem = self.wait.until(getattr(EC, condition)((getattr(By, by), arg)))
        elif isinstance(b, bool):
            elem = self.wait.until(getattr(EC, condition)(arg, b))
        else:
            elem = self.wait.until(getattr(EC, condition)((getattr(By, by), arg), b))
        return [self, elem]

    def ExecScript(self, script, driver = ''):
        self.__driver.execute_script(script)

    def Quit(self, driver = '', cookie = ''):
        self.__driver.quit()
        if self.__driverType != '':
            self.__ss.KillProcess([self.__driverType + '*'], [cookie])
