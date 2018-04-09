import time
from random import randint
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


cur_date = time.strftime("%m_%d_%Y")
cur_time = time.strftime("%I_%M_%S")
date_time = cur_date + " " + cur_time

def create(self, to_create):

    '''Called when creating a new section, location or fridge.
    :param self: the test case in which this test is part of. (see labtrack_test_script.py)
    :param to_create: table to add a new entry to - "Sections", "Locations", or "Fridges"
    '''

    if to_create.lower() == "sections":
        text = "TEST_SECTION"
        create_new_obj = "Create New Section"

    if to_create.lower() == "locations":
        text = "TEST_LOCATION"
        create_new_obj = "Create New Location"

    if to_create.lower() == "fridges":
        text = "TEST_FRIDGE"
        create_new_obj = "Create New Fridge/Shelf"
        fridge_text = "FrigShelf"

    admin_drop_down(self)

    self.target = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
        (By.LINK_TEXT, to_create)))

    self.target.click()

    self.create_new_button = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
        (By.LINK_TEXT, create_new_obj.title())))

    self.create_new_button.click()

    if to_create.lower() == "fridges":
        self.text_input = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
            (By.ID, fridge_text)))
    else:
        self.text_input = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
            (By.ID, to_create.title()[:-1])))

    self.text_input.send_keys(text)

    self.save_button = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
        (By.XPATH, "/html/body/div/div[2]/div/form/div[3]/input")))

    self.save_button.click()
    time.sleep(1)

    if to_create.lower() == "fridges":
        self.table_length = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
            (By.NAME, "frigsTable_length")))
    else:
        self.table_length = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
            (By.NAME, "locationsTable_length")))

    self.table_length.send_keys("All")

def update(self, to_update):

    '''Called when updating a new section, location or fridge.
    :param self: the test case in which this test is part of. (see labtrack_test_script.py)
    :param to_update: table of item to update. Corresponds to Link Text in Admin Dropdown - "Sections", "Locations", or "FrigShelf"
    '''

    if to_update.lower() == "sections":
        text = "TEST_SECTION"
        update_text = "TEST_SEC_UPDATE"

    if to_update.lower() == "locations":
        text = "TEST_LOCATION"
        update_text = "TEST_LOC_UPDATE"

    if to_update.lower() == "fridges":
        text = "TEST_FRIDGE"
        update_text = "TEST_FRIDGE_UPDATE"
        fridge_text = "FrigShelf"

    if to_update.lower() == "fridges":
        self.table_length = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
            (By.NAME, "frigsTable_length")))
    else:
        self.table_length = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
            (By.NAME, "locationsTable_length")))

    self.table_length.send_keys("All")

    self.test_location = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
        (By.LINK_TEXT, text)))

    self.test_location.click()

    if to_update.lower() == "fridges":
        self.text_input = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
            (By.ID, fridge_text)))
    else:
        self.text_input = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
            (By.ID, to_update.title()[:-1])))

    self.text_input.clear()
    self.text_input.send_keys(update_text)

    self.save_location_button = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
        (By.XPATH, "/html/body/div/div[2]/div/form/div[3]/input")))

    self.save_location_button.click()
    time.sleep(1)

    if to_update.lower() == "fridges":
        self.table_length = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
            (By.NAME, "frigsTable_length")))
    else:
        self.table_length = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
            (By.NAME, "locationsTable_length")))

    self.table_length.send_keys("All")

def delete(self, to_delete):

    '''Called when updating a new section, location or fridge.
    :param self: the test case in which this test is part of. (see labtrack_test_script.py)
    :param to_update: table of item to update. Corresponds to Link Text in Admin Dropdown - "Sections", "Locations", or "FrigShelf"
    '''

    self.driver.get("http://labtracktest.uvmhealth.org/Admin/Locations")

    self.table_length = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
        (By.NAME, "locationsTable_length")))

    self.table_length.send_keys("All")

    links = self.driver.find_elements_by_tag_name('a')

    for link in links:
        if link.text == "TEST_LOC_UPDATE":
            href = link.get_attribute("href")

    loc_id = ""
    for char in href:
        if char.isdigit():
            loc_id = loc_id + char

    for link in links:
        href = link.get_attribute("href")
        if href == "http://labtracktest.uvmhealth.org/Admin/DeleteLocation/" + loc_id:
            link.click()
            break

    self.delete_location_button = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
        (By.XPATH, "/html/body/div/div[2]/form/input[1]")))

    self.delete_location_button.click()


def create_validation_rule(self):

    self.validation_rules = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
        (By.LINK_TEXT, "Validation Rules")))

    self.validation_rules.click()

    self.create_new = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
        (By.LINK_TEXT, "Create New Validation Rule")))

    self.create_new.click()

    self.rule_name = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
        (By.ID, "RuleName")))

    self.rule_name.send_keys("TWithLength4")

    self.length = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
        (By.ID, "AllowedLength")))

    self.length.clear()

    self.length.send_keys("4")

    self.char = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
        (By.ID, "FirstChar")))

    self.char.send_keys("T")

    self.create = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
        (By.XPATH, "/html/body/div/div[2]/div/form/div[5]/input")))

    self.create.click()
    time.sleep(1)


def rack_type_create_update(self, mode):

    if mode == 0:

        self.rack_types = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable(
            (By.XPATH, "/html/body/nav/div/div[2]/ul/li[1]/ul/li[1]/a")))

        self.rack_types.click()

        self.rack_button = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
            (By.LINK_TEXT, "Create New Rack Type")))

    else:

        self.rack_button = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
            (By.LINK_TEXT, "TEST_RACK_TYPE")))

    self.rack_button.click()

    if mode == 0:
        self.rack_type = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
            (By.ID, "RackType_RackType")))

    self.total_rows = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
        (By.ID, "RackType_RackRows")))

    self.total_cols = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
        (By.ID, "RackType_RackCols")))

    self.rack_duration = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
        (By.ID, "RackType_RackDuration")))

    self.rack_duration = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
        (By.ID, "RackType_RackDuration")))

    self.default_location = Select(self.driver.find_element_by_id("RackType_LocationId"))
    self.default_section = Select(self.driver.find_element_by_id("RackType_SectionId"))
    self.default_fridge = Select(self.driver.find_element_by_id("RackType_FrigId"))

    if mode == 1:
        self.default_location.select_by_value("1")
        self.default_section.select_by_value("1")
        self.default_fridge.select_by_value("1")

        self.total_rows.send_keys(randint(1, 10))
        self.total_cols.send_keys(randint(1, 10))
        self.rack_duration.send_keys(randint(1, 50))

    else:
        self.rack_type.clear()
        self.rack_type.send_keys("TEST_RACK_TYPE")

        self.default_location.select_by_visible_text("TEST_LOC_UPDATE")
        self.default_section.select_by_visible_text("TEST_SEC_UPDATE")
        self.default_fridge.select_by_visible_text("TEST_FRIDGE_UPDATE")

        self.total_rows.clear()
        self.total_cols.clear()
        self.rack_duration.clear()

        self.total_rows.send_keys(randint(1, 10))
        self.total_cols.send_keys(randint(1, 10))
        self.rack_duration.send_keys(randint(1, 50))

    self.submit_create = self.driver.find_element_by_xpath("/html/body/div/div[2]/div/form/div[9]/input")
    self.submit_create.click()
    time.sleep(1)

    self.table_length = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
        (By.NAME, "racktypesTable_length")))

    self.table_length.send_keys("All")


def create_rack(self):

    self.home = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
        (By.LINK_TEXT, "LabTrack")))

    self.home.click()

    self.home = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable(
        (By.LINK_TEXT, "Create New Rack")))

    self.home.click()
    time.sleep(1)

    self.rack_type = Select(self.driver.find_element_by_id("Rack_RackTypeId"))

    self.rack_type.select_by_visible_text("TEST_RACK_TYPE")

    self.rack_id = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
        (By.ID, "Rack_Rack")))

    self.rack_id.send_keys("TEST_RACK_ID")

    self.rack_date = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
        (By.ID, "Rack_ExpireDate")))

    self.rack_location = Select(self.driver.find_element_by_id("Rack_LocationId"))
    self.rack_location.select_by_visible_text("TEST_LOC_UPDATE")

    self.rack_section = Select(self.driver.find_element_by_id("Rack_SectionId"))
    self.rack_section.select_by_visible_text("TEST_SEC_UPDATE")

    self.rack_fridge = Select(self.driver.find_element_by_id("Rack_FrigId"))
    self.rack_fridge.select_by_visible_text("TEST_FRIDGE_UPDATE")

    self.create_button = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
        (By.XPATH, "/html/body/div/div[2]/div/form/div[10]/input")))

    self.create_button.click()

    self.back = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
        (By.XPATH, "/html/body/div[1]/div[2]/a")))

    self.back.click()


def update_rack(self):

    self.to_update = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
        (By.LINK_TEXT, "TEST_RACK_ID")))

    self.to_update.click()

    self.cell_1 = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
        (By.XPATH, "/html/body/div[1]/form/div/div/div[2]/div[2]")))

    ActionChains(self.driver).move_to_element(self.cell_1).send_keys("TES1").perform()
    ActionChains(self.driver).send_keys(Keys.ENTER).perform()

    self.cell_2 = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
        (By.XPATH, "/html/body/div[1]/form/div/div/div[2]/div[3]")))

    ActionChains(self.driver).move_to_element(self.cell_2).send_keys("TES2").perform()
    ActionChains(self.driver).send_keys(Keys.ENTER).perform()

    ActionChains(self.driver).move_to_element(self.cell_2).double_click().perform()

    self.comment_box = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
        (By.ID, "comment")))

    self.comment_box.send_keys("TEST COMMENT")

    self.save_button = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
        (By.ID, "btnSaveComment")))

    self.save_button.click()

    # self.back = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
    #     (By.XPATH, "/html/body/div[1]/div[2]/a")))
    #
    # self.back.click()


def admin_drop_down(self):

    self.admin = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
        (By.XPATH, "/html/body/nav/div/div[2]/ul/li[1]/a")))

    self.admin.click()
    time.sleep(1)


def delete_entry(self, to_delete):

    # 0 for location, 1 for fridge, 2 for section, 3 for rules
    if to_delete == 0 or to_delete == 2:
        self.table_length = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
             (By.NAME, "locationsTable_length")))

        self.table_length.send_keys("All")
        links = self.driver.find_elements_by_tag_name('a')

    if to_delete == 1:
        self.table_length = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
            (By.NAME, "frigsTable_length")))

        self.table_length.send_keys("All")

    links = self.driver.find_elements_by_tag_name('a')
    href_tar = ""

    if to_delete == 0:
        for link in links:
            if link.text == "TEST_LOC_UPDATE":
                href_tar = link.get_attribute("href")
                break

        loc_id = ""
        for char in href_tar:
            if char.isdigit():
                loc_id = loc_id + char

        for link in links:
            href = link.get_attribute("href")
            if href == "http://labtracktest.uvmhealth.org/Admin/DeleteLocation/" + loc_id:
                link.click()
                break

    elif to_delete == 1:
        for link in links:
            if link.text == "TEST_FRIDGE_UPDATE":
                href_tar = link.get_attribute("href")
                break

        loc_id = ""
        for char in href_tar:
            if char.isdigit():
                loc_id = loc_id + char

        for link in links:
            href = link.get_attribute("href")
            if href == "http://labtracktest.uvmhealth.org/Admin/DeleteFrig/" + loc_id:
                link.click()
                break

    elif to_delete == 2:
        for link in links:
            if link.text == "TEST_SEC_UPDATE":
                href_tar = link.get_attribute("href")
                break

        loc_id = ""
        for char in href_tar:
            if char.isdigit():
                loc_id = loc_id + char

        for link in links:
            href = link.get_attribute("href")
            if href == "http://labtracktest.uvmhealth.org/Admin/DeleteSection/" + loc_id:
                link.click()
                break

    elif to_delete == 3:
        for link in links:
            if link.text == "TWithLength4":
                href_tar = link.get_attribute("href")
                break

        loc_id = ""
        for char in href_tar:
            if char.isdigit():
                loc_id = loc_id + char

        for link in links:
            href = link.get_attribute("href")
            if href == "http://labtracktest.uvmhealth.org/Admin/DeleteRule/" + loc_id:
                link.click()
                break
    if href_tar:
        self.delete_location_button = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
            (By.XPATH, "/html/body/div/div[2]/form/input[1]")))

        self.delete_location_button.click()




