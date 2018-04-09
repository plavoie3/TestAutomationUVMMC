#
# UVM MEDICAL CENTER INFORMATION SERVICES COPYRIGHT 2017
#
# created by philip.lavoie@uvmhealth.org
#
#

'''
=========
eLearn Sample
=========

Description: This is a sample script containing one website (class).
             Each function beginning with "test00x" is an individual test method - TESTS MUST BEGIN WITH "TEST"
             Tests will run sequentially by number (001...002...etc.) - WILL FOLLOW NUMBER ORDER (else alphbetically)
             RECOMMENDED NAMING CONVENTION: test###_name
             Each line or group of lines within a method generally represents a test step.
             setUpClass and tearDownClass functions will be run once at start and end of test sequence.

Browser:     Firefox  (designed using 54.0.1)
             (for cross browser testing see: BROWSERSTACK   )
'''


# IMPORT STATEMENTS #

import os, time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException


# Single website class (MyHealthOnline, BrandHub, etc..)

class eLearn_TestCase_1(unittest.TestCase):

    '''
    setUpClass is a class-level method that will be run once at start of website's test.
    Includes setup required for tests to follow.
    Tests (and tearDownClass) will not run if an exception is raised during setUpClass.
    '''
    @classmethod
    def setUpClass(cls):
        '''
                By default, a generic browser profile is used.
                Therefore, we will create a profile and set preferences for it.
                '''

        # Create Firefox profile for the WebDriver to use
        profile = webdriver.FirefoxProfile()

        # Set Firefox profile preferences #

        # Add UVM MC proxy servers to browser profile's auto-authentication/trusted list
        profile.set_preference("network.automatic-ntlm-auth.trusted-uris", "http://accweb02-pxy,http://tpkweb02-pxy,"
                                                                           "http://accweb01-pxy,http://tpkweb01-pxy,."
                                                                           "fahc.fletcherallen.org,.fahc.org,.fletcherallen.org,"
                                                                           ".uvmhealth.org,.uvmhn.org,.uvmmc.org,.uvmhealth.com,"
                                                                           ".uvmhealth.net,.uvmmedcenter.org,.uvmmedcenter.com,"
                                                                           ".uvmmedcenter.net,.uvmchildrens.org")

        # The second argument of this method is a list of MIME (file) types to download/save automatically
        # (browser will not bring up dialogue asking to save files)
        profile.set_preference("browser.helperApps.neverAsk.saveToDisk",
                               "application/vnd.openxmlformats-officedocument.wordprocessingml.document, application/msword, application/csv,application/excel,application/vnd.msexcel,application/vnd.ms-excel,text/anytext,text/comma-separated-values,text/csv,application/vnd.ms-excel,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,application/octet-stream");

        # The second argument of this method is a list of MIME (file) types to download/save automatically
        # (browser will not bring up dialogue asking to open files)
        profile.set_preference("browser.helperApps.neverAsk.openFile",
                               "application/vnd.openxmlformats-officedocument.wordprocessingml.document, application/msword, application/csv,application/excel,application/vnd.msexcel,application/vnd.ms-excel,text/anytext,text/comma-separated-values,text/csv,application/vnd.ms-excel,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,application/octet-stream");

        # (Various other preferences to enable automatic downloading/saving of files)
        profile.set_preference("browser.download.manager.showWhenStarting", False);
        profile.set_preference("browser.helperApps.alwaysAsk.force", False);
        profile.set_preference("browser.download.manager.useWindow", False);
        profile.set_preference("browser.download.manager.focusWhenStarting", False);
        profile.set_preference("browser.download.manager.alertOnEXEOpen", False);
        profile.set_preference("browser.download.manager.showAlertOnComplete", False);
        profile.set_preference("browser.download.manager.closeWhenDone", True);
        profile.set_preference("pdfjs.disabled", True);

        # Specify the directory where automatically downloaded files should be saved to
        profile.set_preference("browser.download.dir", os.getcwd());
        profile.set_preference("browser.download.folderList", 2);

        # Various preferences to allow for faster runtimes (disabling cache)
        profile.set_preference("browser.cache.disk.enable", False)
        profile.set_preference("browser.cache.memory.enable", False)
        profile.set_preference("browser.cache.offline.enable", False)
        profile.set_preference("network.http.use-cache", False)

        # Create Firefox webdriver instance with created profile (Open Firefox using profile)
        cls.driver = webdriver.Firefox(profile)
        # Maximize browser window
        cls.driver.maximize_window()

    # Test 1 - sign into patient portal
    def test001_sign_in(self):

        self.driver.get("http://intranet.fletcherallen.org/Pages/Home.aspx")
        time.sleep(1)
        result1 = self.driver.find_element_by_xpath(
            ".//*[@id='zz8_CurrentNav']/div/ul/li[2]/a/span/span").click()
        time.sleep(1)
        result2 = self.driver.find_element_by_xpath(".//*[@id='HRCentralPanel']/tbody/tr[4]/td[1]/a ")
        result2.click()
        time.sleep(1)


  ################################################################################################

    def test002_eLearn_upload(self):
        self.driver.switch_to_window(self.driver.window_handles[-1])

        manage = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
            (By.XPATH, ".//*[@id='navigation-container']/div[3]/ul/li[7]/a")))

        manage.click()
        time.sleep(5)


    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2)


