#coding: utf-8
import os
import re
import platform

from util import CSystem

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class WebElement:
    def __init__(self, driver):
        self.driver = driver
        self.element = 0
    def find(self, enum, arg):
        enum = enum.lower()
        try:
            if enum == 'name':
                self.element = self.driver.find_element_by_name(arg)
                # print self.element
            elif enum == 'xpath':
                self.element = self.driver.find_element_by_xpath(arg)
            elif enum == 'xpaths':
                self.element = self.driver.find_elements_by_xpath(arg)
            elif enum == 'id':
                self.element = self.driver.find_element_by_id(arg)
            elif enum == 'tagname':
                self.element = self.driver.find_element_by_tag_name(arg)
        except:
            pass
            # self.driver.Quit()
        return self
    def sendKeys(self, s):
        self.element.send_keys(s)
        return self

    @property
    def element(self):
        return self.element

class CWeb:
    def __init__(self, settings = {}, ws = '', cookie = ''):
        self.ss = CSystem()
        if ws != '':
            self.workSpace = ws
        else:
            self.workSpace = os.path.join(self.ss.GetDirName(self.ss.GetDirName(self.ss.GetRealPath(__file__))), '3rdTools')

        if settings != {}:
            self.driverType = settings['Driver'][settings['Driver']['use']].lower()
        else:
            self.driverType = 'phantomjs'
        self.initDriver(cookie)

    def initDriver(self, cookie):
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
            self.__class__.CU.runProcess('chmod +x ' + os.path.join(self.workSpace, 'phantomjs'), usepopen = True)
            self.driver = webdriver.PhantomJS(os.path.join(self.workSpace, 'phantomjs'), service_args = args)
            # self.driver = webdriver.Chrome()
            self.driverType = 'phantomjs'
        elif sysstr == 'Windows':
            if self.driverType == 'phantomjs':
                self.__driver = webdriver.PhantomJS(os.path.join(self.workSpace, 'phantomjs_win.exe'), service_args = args)
            elif self.driverType == 'chrome':
                print os.path.join(self.workSpace, 'chromedriver.exe')
                self.__driver = webdriver.Chrome(os.path.join(self.workSpace, 'chromedriver.exe'))
        elif sysstr == 'Darwin':
            # self.__class__.CU.runProcess('chmod +x ./phantomjs', usepopen = True)
            # self.driver = webdriver.PhantomJS(os.path.join(os.path.split(os.path.realpath(__file__))[0], 'phantomjs'))
            self.__driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.__driver, 5)

    def GetDriver(self, driver):
        driver = driver == '' and self.__driver or driver
        return driver

    def Goto(self, page, driver = ''):
        page = page.lower()
        if not re.match(r'http', page):
            page = 'http://' + page
        self.GetDriver(driver).get(page)
        return self.__driver

    def GoBack(self, driver = ''):
        self.GetDriver(driver).back()
    def Forward(self, driver = ''):
        self.GetDriver(driver).forward()

    def GetPageSource(self, driver = ''):
        driver = driver == '' and self.__driver or driver
        return driver.page_source

    def WaitUntil(self, condition, enum = '', arg = ''):
        enum = enum.lower()
        if condition == 'invisibility_of_element_located':
            if enum == 'xpath':
                return self.wait.until(EC.invisibility_of_element_located((By.XPATH, arg)))
        elif condition == 'element_to_be_clickable':
            if enum == 'xpath':
                return self.wait.until(EC.element_to_be_clickable((By.XPATH, arg)))
        elif condition == 'alert_is_present':
            return self.wait.until(EC.alert_is_present())

    def ExecScript(self, script, driver = ''):
        self.GetDriver(driver).execute_script(script)

    def Quit(self, driver = '', cookie = ''):
        self.GetDriver(driver).quit()
        if self.driverType != '':
            self.__class__.CU.killProcess([self.driverType], [cookie])
