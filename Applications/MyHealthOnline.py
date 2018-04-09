#
# UVM MEDICAL CENTER INFORMATION SERVICES COPYRIGHT 2017
#
# Created by philip.lavoie@uvmhealth.org
#
#

'''
=========
MyHealthOnline
=========

Description: This is a sample script containing one website (class).
             Each function beginning with "test00x" is an individual test method - TESTS MUST BEGIN WITH "TEST"
             Tests will run sequentially by number (001...002...etc.) - WILL FOLLOW NUMBER ORDER (else alphbetically)
             RECOMMENDED NAMING CONVENTION: test###_name
             Each line or group of lines within a method generally represents a test step.
             setUpClass and tearDownClass functions will be run once at start and end of test sequence.

Browser:     Firefox  (designed using 54.0.1)

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

class MyHealthOnline_TestCase(unittest.TestCase):

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
        profile.set_preference("browser.download.dir", "C:\Users\m306517\PycharmProjects\BrandHub\Downloads");
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

        user_name = ""  # read in from config file

        # Tell webdriver (browser) to get MyHealthOnline Login Page
        self.driver.get("https://myhealthonline.uvmmedcenter.org/Account/LogIn?ReturnUrl=%2f")

        # Make webdriver wait explicitly until UserName text input is visible (will wait 20 seconds before failing)
        # Set user_name variable to UserName text field element once visible
        user_name_input = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
            (By.ID, "UserName")))

        # Fill in UserName text field element
        user_name_input.send_keys(user_name)

        # Locate and fill in Password text field element
        self.driver.find_element_by_id("Password").send_keys("")   # read in from config file

        # Locate and click 'Login' button
        self.driver.find_element_by_xpath(".//*[@id='LoginForm']/form/div[4]/button").click()

        # Wait until login welcome box is visible. Set verify_login to that element
        verify_login = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
            (By.XPATH, "html/body/div[4]/h1")))

        # Verify that correct user was signed in by checking element's text
        assert verify_login.text == "Welcome, " + user_name


    # Test 2 - navigate to Medical Information using menu/banner link
    def test002_med_info(self):

        # Locate and click on 'View Medical Information' tile button link
        self.driver.find_element_by_xpath(".//*[@id='MyChart']/div/a[2]").click()

        # Wait until the new page loads to locate and set user record tab to verify variable
        verify_user_medinfo = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
            (By.XPATH, ".//*[@id='proxyTabs']/li/a/span")))

        # Verify that displayed text for pulled user's record matches the signed in user's name
        try:
            assert verify_user_medinfo.text != ""
        except AssertionError as e:
            self.driver.save_screenshot(os.getcwd())  # get these photos in report!!!
            print("Bill != expected user name...displaying wrong record?")
            raise e

    #
    # tearDownClass is a class-level method that will be run once at the end of website's test.
    # Simply closes down the browser
    #
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

# If interpreter is running this file
if __name__ == '__main__':
    # call main method of the test case and pass the verbosity argument (controls amount of test result details displayed on console)
    unittest.main(verbosity=2)