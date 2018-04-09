import os
import time
import unittest
from __builtin__ import classmethod
import LabTrack

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver import ActionChains

cur_date = time.strftime("%m_%d_%Y")
cur_time = time.strftime("%I_%M_%S")
date_time = cur_date + " " + cur_time

## test_names = ["location","section","fridge","rule"]

## Test Case - Lab Track in IE browser

class LabTrack_IE_TestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        '''

        Set up for LabTrack tests

         For setting desired IE profile capabilites:

         caps = webdriver.DesiredCapabilities.INTERNETEXPLORER
         caps['enableFullPageScreenshot'] = False

         '''

        dir = os.getcwd()

        ie_driver_path = dir + "\IEDriverServer.exe"

        print ie_driver_path

        # for desired capabilities, add:    capabilities=caps   to webdriver.Ie arguments
        cls.driver = webdriver.Ie(ie_driver_path)
        cls.driver.maximize_window()

################################################################################################

    def test001_site_loads(self):

        '''Tests that site loads and page title is "LabTrack - Racks - LabTrack"'''

        self.driver.get("http://labtracktest.uvmhealth.org/")

        title = self.driver.title

        self.driver.save_screenshot(os.getcwd() + "\\Screenshots\\site_loads_" + date_time + ".png")

        assert title == "LabTrack - Racks - LabTrack"

    # LOCATIONS : CREATE, UPDATE

    def test002_create_location(self):

        '''Creates a location and verifies that it appears in the locations table'''

        LabTrack.create(self, "Locations")

        locations_list = self.driver.find_elements_by_xpath("/html/body/div/div[2]/table/tbody/tr")

        found = False
        for location in locations_list:
            location = location.text.replace(" Delete", "")
            if location == "TEST_LOCATION":
                found = True

        self.driver.save_screenshot(os.getcwd() + "\\Screenshots\\create_location_" + date_time + ".png")

        assert found == True

    def test003_update_location(self):

        '''Updates a location and verifies that changed name appears in the locations table'''

        LabTrack.update(self, "Locations")

        locations_list = self.driver.find_elements_by_xpath("/html/body/div/div[2]/table/tbody/tr")

        found = False
        for location in locations_list:
            location = location.text.replace(" Delete", "")
            if location == "TEST_LOC_UPDATE":
                found = True

        self.driver.save_screenshot(os.getcwd() + "\\Screenshots\\update_location_" + date_time + ".png")

        assert found == True

    # SECTIONS : CREATE, UPDATE

    def test004_create_section(self):

        '''Creates a section and verifies that it appears in the sections table'''

        LabTrack.create(self, "Sections")

        locations_list = self.driver.find_elements_by_xpath("/html/body/div/div[2]/table/tbody/tr")

        found = False
        for location in locations_list:
            location = location.text.replace(" Delete", "")
            if location == "TEST_SECTION":
                found = True

        self.driver.save_screenshot(os.getcwd() + "\\Screenshots\\create_section_" + date_time + ".png")

        assert found == True

    def test005_update_section(self):

        '''Updates a section and verifies that the changed name appears in the sections table'''

        LabTrack.update(self, "Sections")

        locations_list = self.driver.find_elements_by_xpath("/html/body/div/div[2]/table/tbody/tr")

        found = False
        for location in locations_list:
            location = location.text.replace(" Delete", "")
            if location == "TEST_SEC_UPDATE":
                found = True

        self.driver.save_screenshot(os.getcwd() + "\\Screenshots\\update_section_" + date_time + ".png")

        assert found == True

    # FRIDGES : CREATE, UPDATE

    def test006_create_fridge(self):

        '''Creates a fridge and verifies that it appears in the fridges table'''

        LabTrack.create(self, "Fridges")

        self.table_length = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
            (By.NAME, "frigsTable_length")))

        self.table_length.send_keys("All")

        fridges_list = self.driver.find_elements_by_xpath("/html/body/div/div[2]/table/tbody/tr")

        found = False
        for location in fridges_list:
            location = location.text.replace(" Delete", "")
            if location == "TEST_FRIDGE":
                found = True
                break

        self.driver.save_screenshot(os.getcwd() + "\\Screenshots\\create_fridge_" + date_time + ".png")

        assert found == True

    def test007_update_fridge(self):

        '''Updates a fridge and verifies that the changed name appears in the fridges table'''

        LabTrack.update(self, "Fridges")

        locations_list = self.driver.find_elements_by_xpath("/html/body/div/div[2]/table/tbody/tr")

        found = False
        for location in locations_list:
            location = location.text.replace(" Delete", "")
            if location == "TEST_FRIDGE_UPDATE":
                found = True
                break

        self.driver.save_screenshot(os.getcwd() + "\\Screenshots\\update_fridge_" + date_time + ".png")

        assert found == True

    # RACK TYPE / VALIDATION RULE TESTS #

    def test008_create_rack_type(self):

        LabTrack.admin_drop_down(self)
        time.sleep(1)

        LabTrack.rack_type_create_update(self, 0)

        rack_type_list = self.driver.find_elements_by_xpath('//*[@id="racktypesTable"]/tbody/tr/td[1]/a')

        found = False

        for rack_type in rack_type_list:
            rack_type = rack_type.text.replace("u", "")
            if rack_type == "TEST_RACK_TYPE":
                found = True
                break

        self.driver.save_screenshot(os.getcwd() + "\\Screenshots\\create_rack_type_" + date_time + ".png")

        assert found == True

    def test009_update_rack_type(self):

        LabTrack.rack_type_create_update(self, 1)

    def test010_create_validation_rule(self):

        LabTrack.admin_drop_down(self)

        LabTrack.create_validation_rule(self)

        validation_list = self.driver.find_elements_by_xpath('/html/body/div/table/tbody/tr/td[1]/a')

        found = False
        for rule in validation_list:
            rule = rule.text.replace(" Delete", "")
            if rule == "TWithLength4":
                found = True
                break

        self.driver.save_screenshot(os.getcwd() + "\\Screenshots\\create_validation_rule_" + date_time + ".png")

        assert found == True

    # RACK TESTS #

    def test011_create_rack(self):

        LabTrack.create_rack(self)

        self.newly_created = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="rowTEST_RACK_ID"]/td[1]/a')))

        try:
            assert self.newly_created.text == "TEST_RACK_ID"
        except AssertionError as e:
            self.driver.save_screenshot(os.getcwd() + "\\Screenshots\\create_rack_ERROR_" + date_time + ".png")
            print("Error creating and/or viewing new rack")
            raise e

        self.driver.save_screenshot(os.getcwd() + "\\Screenshots\\create_rack_" + date_time + ".png")

    # def test012_update_rack(self):
    #
    #     LabTrack.update_rack(self)
    #
    #     self.newly_created_2 = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
    #         (By.XPATH, "/html/body/div[1]/form/div/div/div[2]/div[3]")))
    #
    #     assert self.newly_created_2.text == "TES2"
    #
    #     comment = self.newly_created_2.get_attribute("data-comment")
    #
    #     assert comment == "TEST COMMENT"

    def test013_delete_location(self):

        self.driver.get("http://labtracktest.uvmhealth.org/Admin/Locations")

        links = self.driver.find_elements_by_tag_name('a')

        found = False
        for link in links:
            if link.text == "TEST_LOC_UPDATE":
                found = True
                break
        try:
            assert found == True
        except AssertionError as e:
            print("Test location to delete was not found")
            raise e

        LabTrack.delete_entry(self, 0)

        links = self.driver.find_elements_by_tag_name('a')

        found = False
        for link in links:
            if link.text == "TEST_LOC_UPDATE":
                found = True
                break
        try:
            assert found == False

        except AssertionError as e:
            self.driver.save_screenshot(os.getcwd() + "\\Screenshots\\delete_location_ERROR_" + date_time + ".png")
            print("Test location was not deleted")
            raise e

    def test014_delete_fridge(self):

        self.driver.get("http://labtracktest.uvmhealth.org/Admin/Frigs")
        links = self.driver.find_elements_by_tag_name('a')

        found = False
        for link in links:
            if link.text == "TEST_FRIDGE_UPDATE":
                found = True
                break
        try:
            assert found == True
        except AssertionError as e:
            print("Test fridge to delete was not found")
            raise e

        LabTrack.delete_entry(self, 1)

        links = self.driver.find_elements_by_tag_name('a')

        found = False
        for link in links:
            if link.text == "TEST_FRIDGE_UPDATE":
                found = True
                break
        try:
            assert found == False

        except AssertionError as e:
            print("Test fridge was not deleted")
            raise e


    def test015_delete_section(self):

        self.driver.get("http://labtracktest.uvmhealth.org/Admin/Sections")

        links = self.driver.find_elements_by_tag_name('a')

        found = False
        for link in links:
            if link.text == "TEST_SEC_UPDATE":
                found = True
                break
        try:
            assert found == True
        except AssertionError as e:
            print("Test section to delete was not found")
            raise e

        LabTrack.delete_entry(self, 2)

        links = self.driver.find_elements_by_tag_name('a')

        found = False
        for link in links:
            if link.text == "TEST_SEC_UPDATE":
                found = True
                break
        try:
            assert found == False

        except AssertionError as e:
            print("Test section was not deleted")
            raise e

    def test016_delete_rule(self):

        self.driver.get("http://labtracktest.uvmhealth.org/Admin/Rules")
        links = self.driver.find_elements_by_tag_name('a')

        found = False
        for link in links:
            if link.text == "LWithLength4":
                found = True
                break
        try:
            assert found == True
        except AssertionError as e:
            print("Test rule to delete was not found")
            raise e

        LabTrack.delete_entry(self, 3)

        links = self.driver.find_elements_by_tag_name('a')

        found = False
        for link in links:
            if link.text == "LWithLength4":
                found = True
                break
        try:
            assert found == False

        except AssertionError as e:
            print("Test rule was not deleted")
            raise e

    # def test017_delete_rack(self):



    ################################################################################################

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2)

