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
        
    applicationName_tests = unittest.TestLoader().loadTestsFromTestCase(applicationName_TestCaseName)
    applicationName2_tests = unittest.TestLoader().loadTestsFromTestCase(application2Name_TestCaseName)
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
    
    GUI asks user to enter test report output location and then run tests.
    Once run, the console is used to provide feedback on tests as they run, time elapsed when complete. 
    GUI displays result pass/fail totals of tests once completed.
    Closing GUI ends program (closes console window too)
    
    Email with full HTML report is saved to specified location and sent to preset email in this code:
    
  ```
  f = codecs.open(self.label_text.get() + "/Test_Report_Flash_" + date_time2 + ".html", 'r')
  for line in f:
    if "<p class='attribute'><strong>Status:</strong>" in line:
        status = line;
        break

  email_list = [elem.strip().split(',') for elem in recipients]

  msg = MIMEMultipart('alternative')
  msg['Subject'] = title
  msg['From'] = 'philip.lavoie@uvmhealth.org'
  msg['Reply-to'] = 'philip.lavoie@uvmhealth.org'
  msg['Cc'] = 'philip.lavoie@uvmhealth.org'

  msg.preamble = 'Multipart massage.\n'

  #############################################################

  html = """\
  <html>
            
  [EMAIL BODY]
            
  </html>
               
  """

  import os

  part = MIMEText(html, 'html')

  msg.attach(part)

  part = MIMEApplication(open(self.label_text.get() + "/Test_Report_Flash_" + date_time2 + ".html", "rb").read())
  part.add_header('Content-Disposition', 'attachment', filename=title+".html")
  msg.attach(part)

  server = smtplib.SMTP("email.fahc.org", 25)
  server.ehlo()
  server.starttls()

   credentials_file = os.getcwd() + '\\flash_config.txt'
   password = Conf_Reader.get_value(credentials_file, 'KRONOS_LOGIN_PASSWORD')

   server.login("m306517", password)

   server.sendmail(msg['From'], email_list, msg.as_string())

   status = status.replace("<p class='attribute'><strong>", "")
   status = status.replace("</strong>", "")
   status = status.replace("</p>", "")

   self.text_running = status + "\n Tests complete, full report has been emailed"
   self.label_text_running.set(self.text_running)
   
   
* [TestRunner_flash.spec](https://github.uvmhealth.org/m306517/Automation/blob/master/TestRunner_flash.spec) - Specification file for test runner executable (include necessary data files such as configuration.txt, icons, other desired settings)

    In cmd, navigate to location of the file and use this command:
    
    ```
    pyinstaller --onedir TestRunner_flash.spec
    ```
    
    This will create a dist and build folder in the directory of the spec file
    In the dist folder, there will be a folder with the name of the TestRunner, within this folder is where the exe will be.
     
    Zip the TestRunner folder, send to client, have them extract, create shortcut for exe. Double click to run.

 
    