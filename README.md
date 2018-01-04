# Test Automation for Web-Based UVMMC Apps using Selenium Webdriver and Python

Core files used to build and freeze automated test suite and a runner w/ HTML reports emailed

## File explanations

* [Conf_Reader.py](https://github.uvmhealth.org/m306517/Automation/blob/master/Conf_Reader.py) - Used to read in test parameters from configuration .txt file (to avoid passwords being written into code). 
  Note: the repo does not include the configuration file. This will need to be created and managed. Keep in same directory as all other files. See below for format...

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
* [kronos.py](https://github.uvmhealth.org/m306517/Automation/blob/master/kronos.py) - Application file


TEST CHANGE