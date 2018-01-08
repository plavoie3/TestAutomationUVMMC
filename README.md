# Test Automation for Web-Based UVMMC Apps using Selenium Webdriver and Python

Core files used to build and freeze automated test suite and a runner w/ HTML reports emailed

## File explanations

* [Applications Folder](https://github.uvmhealth.org/m306517/Automation/tree/master/Applications) - This folder contains each individual application's file which houses that application's test case(s) (groups of individual tests) and is where tests are defined (Browser configuration, WebDriver commands on DOM elements, assertions made, etc.)


* [Conf_Reader.py](https://github.uvmhealth.org/m306517/Automation/blob/master/Conf_Reader.py) - This file is used to read in test parameters from configuration .txt file (to avoid passwords being written into code). 
  Note: the repo does not include the configuration file. This will need to be created and managed. Keep in same directory as all other files.
        THIS FILE ALSO MUST BE ADDED TO THE TEST RUNNER .SPEC FILE'S ANALYSIS "DATAS" PARAMETER
        ex: 
        ```
        datas=[('H:\\MyDocuments\\PyCharmProjects\\Automation\\flash_config.txt', '.')]
        ```
      
    See below for format...

    Ex: config.txt
    ```
    *** Configuration file for test parameters ***
   
    --- KRONOS LOGIN CREDENTIALS ---
    
    KRONOS_LOGIN_USER=username
    KRONOS_LOGIN_PASSWORD=password
    
    
    --- TELETRACKING LOGIN CREDENTIALS ---
    
    TELETRACKING_LOGIN_USER=username
    TELETRACKING_LOGIN_PASSWORD=password
    
    --- EMAIL SETTINGS ---
    
    etc...
    ```

* [TestRunner_flash.py](https://github.uvmhealth.org/m306517/Automation/blob/master/TestRunner_flash.py) - This is file (specified in TestRunner_flash.spec) that is frozen by PyInstaller to be run as a standalone executable.

    Code to build test suite (add applications to runner):
    
    ```
    import unittest, HTMLTestRunner

    from Applications.applicationName import applicationName_TestCaseName
    from Applications.applicationName import application2Name_TestCaseName
    .
    .
    ...etc.
    
    outfile = open(self.label_text.get() + "/Test_Report_Name_" + date_time2 + ".html", "w")
    title = "Flash Testing Report " + date_time
        
    applicationName_suite = unittest.TestLoader().loadTestsFromTestCase(applicationName_TestCaseName)
    applicationName_suite = unittest.TestLoader().loadTestsFromTestCase(application2Name_TestCaseName)
    .
    .
    ...etc.
    
    run_suite = unittest.TestSuite([applicationName_suite, applicationName2_suite, ...etc.])
        
    runner = HTMLTestRunner.HTMLTestRunner(
            stream=outfile,
            title= title ,
            verbosity= 2 ,
            description='Flash testing report for Application and Application 2...'
            )
              
    runner.run(run_suite)
    ```

        



