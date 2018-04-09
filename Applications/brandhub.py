from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import os
import unittest
import time
from __builtin__ import classmethod
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException


## Check download folder size (# of files) before any files are downloaded by test ##

path = "C:\Users\m306517\PycharmProjects\BrandHub\Downloads"
downloads_size = len(os.listdir(path))

## Test Class

class BrandHub_Office2016(unittest.TestCase):

## Test Class setup

    @classmethod
    def setUpClass(cls):
        profile = webdriver.FirefoxProfile()


        profile.set_preference("network.automatic-ntlm-auth.trusted-uris", "http://accweb02-pxy,http://tpkweb02-pxy,"
                                                                           "http://accweb01-pxy,http://tpkweb01-pxy,."
                                                                           "fahc.fletcherallen.org,.fahc.org,.fletcherallen.org,"
                                                                           ".uvmhealth.org,.uvmhn.org,.uvmmc.org,.uvmhealth.com,"
                                                                           ".uvmhealth.net,.uvmmedcenter.org,.uvmmedcenter.com,"
                                                                           ".uvmmedcenter.net,.uvmchildrens.org")

        profile.set_preference("browser.download.dir", "C:\Users\m306517\PycharmProjects\BrandHub\Downloads");
        profile.set_preference("browser.download.folderList", 2);
        profile.set_preference("browser.helperApps.neverAsk.saveToDisk",
                               "application/vnd.openxmlformats-officedocument.wordprocessingml.document, application/msword, application/csv,application/excel,application/vnd.msexcel,application/vnd.ms-excel,text/anytext,text/comma-separated-values,text/csv,application/vnd.ms-excel,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,application/octet-stream");
        profile.set_preference("browser.download.manager.showWhenStarting", False);
        profile.set_preference("browser.helperApps.neverAsk.openFile",
                               "application/vnd.openxmlformats-officedocument.wordprocessingml.document, application/msword, application/csv,application/excel,application/vnd.msexcel,application/vnd.ms-excel,text/anytext,text/comma-separated-values,text/csv,application/vnd.ms-excel,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,application/octet-stream");
        profile.set_preference("browser.helperApps.alwaysAsk.force", False);
        profile.set_preference("browser.download.manager.useWindow", False);
        profile.set_preference("browser.download.manager.focusWhenStarting", False);
        profile.set_preference("browser.download.manager.alertOnEXEOpen", False);
        profile.set_preference("browser.download.manager.showAlertOnComplete", False);
        profile.set_preference("browser.download.manager.closeWhenDone", True);
        profile.set_preference("pdfjs.disabled", True);

        profile.set_preference("browser.cache.disk.enable", False)
        profile.set_preference("browser.cache.memory.enable", False)
        profile.set_preference("browser.cache.offline.enable", False)
        profile.set_preference("network.http.use-cache", False)

        cls.driver = webdriver.Firefox(profile)
        cls.driver.maximize_window()

################################################################################################

    def sign_in(self):
        self.driver.get("http://intranet.fletcherallen.org/HR_CENTRAL/Pages/HRC_Home.aspx")
        self.driver.find_element_by_xpath(".//*[@id='zz8_CurrentNav']/div/ul/li[12]/a/span/span").click()
        self.driver.switch_to_window(self.driver.window_handles[-1])

        uvmmc = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
            (By.ID, "medical")))
        uvmmc.click()

        self.driver.switch_to_window(self.driver.window_handles[-1])

        user = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
            (By.XPATH, ".//*[@id='userNameInput']")))
        user.clear()
        user.send_keys("")   # get from config file
        password = self.driver.find_element_by_xpath(".//*[@id='passwordInput']")
        password.clear()
        password.send_keys("")   # get from config file
        self.driver.find_element_by_xpath(".//*[@id='submitButton']").click()
        time.sleep(2)
        try:
            self.brand = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
                (By.ID, "cuke_our_brand_top")))
        except NoSuchElementException:
            self.sign_in()

################################################################################################

    def test1_brand_hub_webpage(self):
        self.sign_in()

################################################################################################

    def test2_standards_summary(self):

        self.brand = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
            (By.ID, "cuke_our_brand_top")))

        self.hover = ActionChains(self.driver).move_to_element(self.brand).perform()

        time.sleep(1)

        self.standards = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
            (By.ID, "cuke_brand_standards_top")))
        self.standards.click()

        time.sleep(1)

        self.download = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
            (By.XPATH, ".//*[@id='content']/div/div[1]/div[1]/div/a")))
        self.download.click()

################################################################################################

    def test3_search(self):

        self.search = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
                              (By.ID, "js_prime_nav_keywordsearch_input")))
        self.search.send_keys("Template")
        time.sleep(1)
        self.search.send_keys(Keys.RETURN)
        time.sleep(1)
        self.result = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
            (By.XPATH, ".//*[@id='yui-gen0']/h6/a/span")))

################################################################################################

    def test4_file(self):

        self.driver.find_element_by_xpath(".//*[@id='yui-gen23']/ol/li[1]/div[1]/a/div/span[1]").click()
        self.driver.find_element_by_xpath(".//*[@id='yui-gen0']/h6/a/span").click()
        self.driver.find_element_by_id("js_download_no_popup").click()

################################################################################################

    def test5_print_ordering(self):
        self.driver.find_element_by_id("cuke_print_ordering_top").click()
        self.driver.find_element_by_xpath(".//*[@id='content']/div/p[4]/a").click()
        self.driver.find_element_by_xpath(".//*[@id='ContentMain_ContentMain_createProjectButton']/span").click()
        self.driver.find_element_by_id("ContentMain_ContentMain_jobTitleTextBox").send_keys("test")
        self.driver.find_element_by_id("ctl00_ctl00_ContentMain_ContentMain_jobTypeComboBox_Input").click()
        self.driver.find_element_by_xpath(".//*[@id='ctl00_ctl00_ContentMain_ContentMain_jobTypeComboBox_Input']").click()
        self.driver.find_element_by_xpath(".//*[@id='ctl00_ctl00_ContentMain_ContentMain_jobTypeComboBox_DropDown']/div/ul/li[2]").click()

################################################################################################

    def test6_email_sig(self):
        self.driver.get("https://www.uvmhealth-brandhub.org/en-GB")
        self.driver.find_element_by_xpath(".//*[@id='content']/div/div[1]/div/div/div[3]/div[2]/div[2]/a").click()

################################################################################################

    def test7_profile(self):
        self.driver.find_element_by_xpath(".//*[@id='header']/div/div[2]/div[1]/div/ul/li[2]/div/a/span").click()
        self.driver.find_element_by_xpath(".//*[@id='header']/div/div[2]/div[1]/div/ul/li[2]/div/div/ol/li[1]/a/span").click()
        self.driver.find_element_by_xpath(".//*[@id='content']/div/form/div[10]/button").click()
        self.update = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
                              (By.XPATH, "//*[contains(text(), 'Your profile has been updated')]")))

################################################################################################

    def test8_training_resources(self):

        self.resources = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
            (By.ID, "cuke_resources_top")))

        self.hover = ActionChains(self.driver).move_to_element(self.resources).perform()

        time.sleep(1)

        self.training_resources = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
            (By.XPATH, ".//*[@id='cuke_training_and_resources_top']/a")))
        self.training_resources.click()

        time.sleep(1)

        self.writing = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
            (By.XPATH, ".//*[@id='content']/div/p[4]/a")))
        self.writing.click()

        self.driver.find_element_by_xpath(".//*[@id='NavigationMenu']/ul/li[1]/ul/li[1]/a").click()

    ## Last test - Checks to make sure appropriate number of files downloaded successfully
    ## note: does not open downloaded files ##

    def test9_check_downloads(self):
        timeout = time.time() + 60 * 5
        while not os.path.exists(os.getcwd()):
            time.sleep(1)
            if os.path.exists(os.getcwd()) or time.time() > timeout:
                break
        new_downloads_size = len(os.listdir(path))
        self.assertEqual(new_downloads_size, downloads_size + 2)

################################################################################################

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2)

