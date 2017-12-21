from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import os
import Conf_Reader
import unittest
import base64
import time
from __builtin__ import classmethod
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException


# ## Check download folder size (# of files) before any files are downloaded by test ##
#
# path = os.getcwd() + "\downloads"
# downloads_size = len(os.listdir(path))

## Test Class



class Kronos_TestCase(unittest.TestCase):


## Test Class setup

    @classmethod
    def setUpClass(cls):
        profile = webdriver.FirefoxProfile()

        # Enable Flash
        profile.set_preference("plugin.state.flash", 2);


        profile.set_preference("network.automatic-ntlm-auth.trusted-uris", "http://accweb02-pxy,http://tpkweb02-pxy,"
                                                                           "http://accweb01-pxy,http://tpkweb01-pxy,."
                                                                           "fahc.fletcherallen.org,.fahc.org,.fletcherallen.org,"
                                                                           ".uvmhealth.org,.uvmhn.org,.uvmmc.org,.uvmhealth.com,"
                                                                           ".uvmhealth.net,.uvmmedcenter.org,.uvmmedcenter.com,"
                                                                           ".uvmmedcenter.net,.uvmchildrens.org")

        # profile.set_preference("browser.download.dir", path);
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

    def test001_sign_in(self):

        credentials_file = os.path.join(os.path.dirname(__file__), 'login.credentials.txt')
        self.username = Conf_Reader.get_value(credentials_file, 'LOGIN_USER')
        self.password = Conf_Reader.get_value(credentials_file, 'LOGIN_PASSWORD')

        self.driver.get("https://kronos.uvmmedcenter.org/wfc/navigator/logon")

        username = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
            (By.ID, "username")))

        username.send_keys(self.username)

        self.driver.find_element_by_id("passInput").send_keys(self.password)

        self.driver.find_element_by_id("loginSubmit").click()

        try:
            self.driver.find_element_by_id("Navigator")
        except NoSuchElementException as e:
            print("Unable to verify successful login by finding navigation bar.")
            raise e

################################################################################################

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2)
