#
# UVM MEDICAL CENTER INFORMATION SERVICES COPYRIGHT 2017
#
# Created by Phil Lavoie
# Contact: philip.lavoie@uvmhealth.org
#

'''
=========
Time Studies
=========

Description: Time Studies (https://timestudies.uvmhealth.org/) automated test script

Browser:     Firefox
'''


import os
import time
import unittest
import Conf_Reader
from __builtin__ import classmethod


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver import ActionChains
from selenium.webdriver import DesiredCapabilities

cur_date = time.strftime("%m_%d_%Y")
cur_time = time.strftime("%I_%M_%S")
date_time = cur_date + " " + cur_time

# Test Case - Time Studies in IE browser

class TimeStudiesFirefoxTestCase(unittest.TestCase):

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
                               "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,application/octet-stream")
        profile.set_preference("browser.download.manager.showWhenStarting", False);
        profile.set_preference("browser.helperApps.neverAsk.openFile",
                               "application/vnd.openxmlformats-officedocument.wordprocessingml.document, application/msword, "
                               "application/csv,application/excel,application/vnd.msexcel,application/vnd.ms-excel,text/anytext,text/comma-separated-values,text/csv,"
                               "application/vnd.ms-excel,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,application/octet-stream")
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
        profile.set_preference("browser.privatebrowsing.autostart", True)

        cls.driver = webdriver.Firefox(profile)

        cls.driver.maximize_window()

################################################################################################

    def test001_site_loads(self):

        '''Tests that user can login into site and reach index page'''

        # NOTE: All ensuing tests will fail if this test fails #

        self.driver.get("https://timestudies.uvmhealth.org/")

        self.email = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
            (By.ID, "i0116")))

        config_file = 'config.txt'

        user = Conf_Reader.get_value(config_file, 'USER')

        password = Conf_Reader.get_value(config_file, 'PASSWORD')

        self.email.send_keys(user)

        self.next_button = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
            (By.ID, "idSIButton9")))

        self.next_button.click()

        self.password = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
            (By.ID, "passwordInput")))

        self.password.send_keys(password)

        self.submit = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
            (By.ID, "submitButton")))

        self.submit.click()

        try:
            WebDriverWait(self.driver, 20).until(EC.title_is("Physician Time Studies"))
            assert self.driver.title == "Physician Time Studies"

        except AssertionError as e:
            self.driver.save_screenshot(os.getcwd() + "\\Screenshots\\site_loads_ERROR" + date_time + ".png")
            print("Could not sign into application")
            raise e

    # def test002_create_study_week(self):
    #
    #     '''C"'''
    #
    #     self.driver.get("https://timestudies.uvmhealth.org/Admin/StudyWeeks")
    #
    #     self.new_week_btn = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
    #         (By.LINK_TEXT, "Add New Study Week")))
    #
    #     self.new_week_btn.click()
    #
    #     self.start_date = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
    #         (By.ID, "StartDate")))
    #
    #     self.start_date.send_keys("01/09/2019")
    #     self.driver.find_element_by_id("EndDate").send_keys("01/16/2019")
    #
    #     self.driver.find_element_by_xpath("/html/body/div/form/div/div[4]/div/input").click()
    #



    ################################################################################################

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2)

