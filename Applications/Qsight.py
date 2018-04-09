#
# UVM MEDICAL CENTER INFORMATION SERVICES COPYRIGHT 2017
#
# Created by Phil Lavoie
# Contact: philip.lavoie@uvmhealth.org
#

'''
=========
QSight
=========

Description: Qsight (https://qsight.net/login.aspx?Domain=fahc) automated test script.

Browser:     Firefox 59.0.2
'''

import os
import time
import unittest
import Conf_Reader
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

# Get time of test case launch
cur_date = time.strftime("%m_%d_%Y")
cur_time = time.strftime("%I_%M_%S")
date_time = cur_date + " " + cur_time

# Test Class


class QSIGHTTestCase(unittest.TestCase):

    # Test Class setup

    @classmethod
    def setUpClass(cls):

        profile = webdriver.FirefoxProfile()

        # Enable Flash
        profile.set_preference("plugin.state.flash", 2)

        profile.set_preference("network.automatic-ntlm-auth.trusted-uris", "http://accweb02-pxy,http://tpkweb02-pxy,"
                                                                           "http://accweb01-pxy,http://tpkweb01-pxy,."
                                                                           "fahc.fletcherallen.org,.fahc.org,.fletcherallen.org,"
                                                                           ".uvmhealth.org,.uvmhn.org,.uvmmc.org,.uvmhealth.com,"
                                                                           ".uvmhealth.net,.uvmmedcenter.org,.uvmmedcenter.com,"
                                                                           ".uvmmedcenter.net,.uvmchildrens.org")

        # profile.set_preference("browser.download.dir", path);
        profile.set_preference("browser.download.folderList", 2)
        profile.set_preference("browser.helperApps.neverAsk.saveToDisk",
                               "application/vnd.openxmlformats-officedocument.wordprocessingml.document, "
                               "application/msword, application/csv,application/excel,application/vnd.msexcel,"
                               "application/vnd.ms-excel,text/anytext,text/comma-separated-values,text/csv,application/vnd.ms-excel,"
                               "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,application/octet-stream");
        profile.set_preference("browser.download.manager.showWhenStarting", False)
        profile.set_preference("browser.helperApps.neverAsk.openFile",
                               "application/vnd.openxmlformats-officedocument.wordprocessingml.document, "
                               "application/msword, application/csv,application/excel,application/vnd.msexcel,"
                               "application/vnd.ms-excel,text/anytext,text/comma-separated-values,text/csv,application/vnd.ms-excel,"
                               "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,application/octet-stream");
        profile.set_preference("browser.helperApps.alwaysAsk.force", False)
        profile.set_preference("browser.download.manager.useWindow", False)
        profile.set_preference("browser.download.manager.focusWhenStarting", False)
        profile.set_preference("browser.download.manager.alertOnEXEOpen", False)
        profile.set_preference("browser.download.manager.showAlertOnComplete", False)
        profile.set_preference("browser.download.manager.closeWhenDone", True)
        profile.set_preference("pdfjs.disabled", True)

        profile.set_preference("browser.cache.disk.enable", False)
        profile.set_preference("browser.cache.memory.enable", False)
        profile.set_preference("browser.cache.offline.enable", False)
        profile.set_preference("network.http.use-cache", False)

        cls.driver = webdriver.Firefox(profile)
        cls.driver.maximize_window()

    def test001_login(self):

        credentials_file = os.getcwd() + '\\flash_config.txt'

        user = Conf_Reader.get_value(credentials_file, 'QSIGHT_LOGIN_USER')
        password = Conf_Reader.get_value(credentials_file, 'QSIGHT_LOGIN_PASSWORD')

        self.driver.get("https://qsight.net/login.aspx?Domain=fahc")

        self.username = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
            (By.ID, "username")))

        self.username.send_keys(user)

        self.driver.find_element_by_id("password").send_keys(password)

        self.driver.find_element_by_id("btnsubmit").click()

        try:
            WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
                (By.ID, "logo")))
        except TimeoutException as e:
            self.driver.save_screenshot(os.getcwd() + "\\Screenshots\\login_ERROR" + date_time + ".png")
            print ("Could not verify successful login")
            raise e

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2)
