print ("Compiling required modules...")

import time

import tkinter as tk
from tkinter.filedialog import askdirectory

print ("Done" + "\n")

print ("Wait for GUI window..." + "\n")

cur_date = time.strftime("%m_%d_%Y")
cur_time = time.strftime("%I:%M:%S")
cur_time2 = time.strftime("%I_%M_%S")
date_time = cur_date + " " + cur_time
date_time2 = cur_date + " " + cur_time2

class GUI:

    def __init__(self, master):

        self.master = master

        master.title("Test Automation")

        # Welcome label

        self.label_welcome = tk.Label(master, pady=10, padx=7, text="Welcome, select a destination for test reports to be saved to below, then click 'Run' to start tests")
        self.label_welcome.pack()

        # Separator

        self.separator = tk.Frame(height=2, bd=1, relief=tk.SUNKEN)
        self.separator.pack(fill=tk.X, padx=5, pady=5)

        # Leading label

        self.label_leading = tk.Label(master, text="Test reports will be saved to: ")
        self.label_leading.pack()

        # Destination label

        self.text = "No destination selected"
        self.label_text = tk.StringVar()
        self.label_text.set(self.text)

        self.label_destination = tk.Label(master, textvariable=self.label_text)
        self.label_destination.pack()

        # Separator

        self.separator = tk.Frame(height=2, bd=1, relief=tk.SUNKEN)
        self.separator.pack(fill=tk.X, padx=5, pady=5)

        # Button

        self.destination_button = tk.Button(master, pady=10, padx=7, text="Select destination", command=self.destination)
        self.destination_button.pack()

        # Separator

        self.separator = tk.Frame(height=2, bd=1, relief=tk.SUNKEN)
        self.separator.pack(fill=tk.X, padx=5, pady=5)

        # Warning label

        self.text_warning = ""
        self.label_text_warning = tk.StringVar()
        self.label_text_warning.set(self.text_warning)

        self.label_warning = tk.Label(master, pady=10, padx=7, textvariable=self.label_text_warning)
        self.label_warning.pack()

        # Run Button

        self.run_button = tk.Button(master, pady=10, padx=7, text="Run", command=self.run)
        self.run_button.pack()

        # Running label

        self.text_running = ""
        self.label_text_running = tk.StringVar()
        self.label_text_running.set(self.text_running)

        self.label_running = tk.Label(master, textvariable=self.label_text_running)
        self.label_running.pack()

        # Close Button

        self.close_button = tk.Button(master, pady=10, padx=7, text="Close", command=master.quit)
        self.close_button.pack()


    def destination(self):

        self.text = askdirectory()
        self.label_text.set(self.text)


    def run(self):

        recipients = ['philip.lavoie@uvmhealth.org']

        print "Running tests..."

        print "Report will be saved to: \n" + self.label_text.get() + "\n"
        print "Report will be emailed to: "

        for email in recipients:
            print email + "\n"


        if self.label_text.get() == "No destination selected":
            self.text_warning = "Destination must be selected before tests can be run"
            self.label_text_warning.set(self.text_warning)
            return

        else:
            self.destination_button.destroy()
            self.label_destination.destroy()
            self.label_text_warning
            self.label_welcome.destroy()
            self.label_leading.destroy()
            self.run_button.destroy()
            self.separator.destroy()

            from Applications.kronos import Kronos_TestCase
            from Applications.teletracking import Teletracking_TestCase
            import unittest, HTMLTestRunner

            outfile = open(self.label_text.get() + "/Test_Report_Flash_" + date_time2 + ".html", "w")
            title = "Flash Testing Report " + date_time

            kronos_tests = unittest.TestLoader().loadTestsFromTestCase(Kronos_TestCase)
            teletracking_tests = unittest.TestLoader().loadTestsFromTestCase(Teletracking_TestCase)

            run_suite = unittest.TestSuite([teletracking_tests, kronos_tests])

            runner = HTMLTestRunner.HTMLTestRunner(
                             stream=outfile,
                             title= title ,
                             verbosity= 2 ,
                             description='Flash testing report for Kronos and Teletracking Dashboard...'
                             )

            # run the suite using HTMLTestRunner

            runner.run(run_suite)

            self.text_running = "running"
            self.label_text_running.set(self.text_running)

            ########################################################################################################################

            outfile.close()

            import smtplib
            import codecs
            from email.mime.application import MIMEApplication
            from email.mime.multipart import MIMEMultipart
            from email.mime.text import MIMEText
            import Conf_Reader

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
              <head>
                <meta name="viewport" content="width=device-width">
                <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
                <title>Automated Test Results</title>
                <style>
                /* -------------------------------------
                    INLINED WITH htmlemail.io/inline
                ------------------------------------- */
                /* -------------------------------------
                    RESPONSIVE AND MOBILE FRIENDLY STYLES
                ------------------------------------- */
                @media only screen and (max-width: 620px) {
                  table[class=body] h1 {
                    font-size: 28px !important;
                    margin-bottom: 10px !important;
                  }
                  table[class=body] p,
                        table[class=body] ul,
                        table[class=body] ol,
                        table[class=body] td,
                        table[class=body] span,
                        table[class=body] a {
                    font-size: 16px !important;
                  }
                  table[class=body] .wrapper,
                        table[class=body] .article {
                    padding: 10px !important;
                  }
                  table[class=body] .content {
                    padding: 0 !important;
                  }
                  table[class=body] .container {
                    padding: 0 !important;
                    width: 100% !important;
                  }
                  table[class=body] .main {
                    border-left-width: 0 !important;
                    border-radius: 0 !important;
                    border-right-width: 0 !important;
                  }
                  table[class=body] .btn table {
                    width: 100% !important;
                  }
                  table[class=body] .btn a {
                    width: 100% !important;
                  }
                  table[class=body] .img-responsive {
                    height: auto !important;
                    max-width: 100% !important;
                    width: auto !important;
                  }
                }
                /* -------------------------------------
                    PRESERVE THESE STYLES IN THE HEAD
                ------------------------------------- */
                @media all {
                  .ExternalClass {
                    width: 100%;
                  }
                  .ExternalClass,
                        .ExternalClass p,
                        .ExternalClass span,
                        .ExternalClass font,
                        .ExternalClass td,
                        .ExternalClass div {
                    line-height: 100%;
                  }
                  .apple-link a {
                    color: inherit !important;
                    font-family: inherit !important;
                    font-size: inherit !important;
                    font-weight: inherit !important;
                    line-height: inherit !important;
                    text-decoration: none !important;
                  }
                  .btn-primary table td:hover {
                    background-color: #34495e !important;
                  }
                  .btn-primary a:hover {
                    background-color: #34495e !important;
                    border-color: #34495e !important;
                  }
                }
                </style>
              </head>
              <body class="" style="background-color: #f6f6f6; font-family: sans-serif; -webkit-font-smoothing: antialiased; font-size: 14px; line-height: 1.4; margin: 0; padding: 0; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%;">
                <table border="0" cellpadding="0" cellspacing="0" class="body" style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; width: 100%; background-color: #f6f6f6;">
                  <tr>
                    <!--<td style="font-family: sans-serif; font-size: 14px; vertical-align: top;">&nbsp;</td>-->
                    <td class="container" style="font-family: sans-serif; font-size: 14px; vertical-align: top; display: block; Margin: 0 auto; max-width: 580px; padding: 10px; width: 580px;">
                      <div class="content" style="box-sizing: border-box; display: block; Margin: 0 auto; max-width: 580px; padding: 10px;">
            
                        <!-- START CENTERED WHITE CONTAINER -->
                        <table class="main" style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; width: 100%; background: #ffffff; border-radius: 3px;">
            
                          <!-- START MAIN CONTENT AREA -->
                          <tr>
                            <td class="wrapper" style="font-family: sans-serif; font-size: 14px; vertical-align: top; box-sizing: border-box; padding: 20px;">
                              <table border="0" cellpadding="0" cellspacing="0" style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; width: 100%;">
                                <tr>
                                  <td style="font-family: sans-serif; font-size: 14px; vertical-align: top;">
                                    <p style="font-family: sans-serif; font-size: 14px; font-weight: normal; margin: 0; Margin-bottom: 15px;">Hello,</p>
                                    <p style="font-family: sans-serif; font-size: 14px; font-weight: normal; margin: 0; Margin-bottom: 15px;">Your automated tests are complete.</p>
                                    <p style="font-family: sans-serif; font-size: 14px; font-weight: normal; margin: 0; Margin-bottom: 15px;">""" + status + """</p>
                                    <p style="font-family: sans-serif; font-size: 14px; font-weight: normal; margin: 0; Margin-bottom: 15px;">Please view the attached file in a browser for full test results.</p>
                                    <p style="font-family: sans-serif; font-size: 14px; font-weight: normal; margin: 0; Margin-bottom: 15px;">Thank you,</p>
                                    <p style="font-family: sans-serif; font-size: 14px; font-weight: normal; margin: 0; Margin-bottom: 15px;">QA & Testing Department</p>
                                    
                                  </td>
                                </tr>
                              </table>
                            </td>
                          </tr>
                          
                          <table border="0" cellpadding="0" cellspacing="0" class="btn btn-primary" style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; width: 100%; box-sizing: border-box;">
                                      <tbody>
                                        <tr>
                                          <td align="left" style="font-family: sans-serif; font-size: 14px; vertical-align: top; padding-bottom: 15px;">
                                            <table border="0" cellpadding="0" cellspacing="0" style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; width: auto;">
                                              <tbody>
                                                <tr>
                                                  <td style="font-family: sans-serif; font-size: 14px; vertical-align: top; background-color: #3498db; border-radius: 5px; text-align: center;"> <a href="mailto:Steele, Kip <kip.steele@uvmhealth.org>" target="_blank" style="display: inline-block; color: #ffffff; background-color: #3498db; border: solid 1px #3498db; border-radius: 5px; box-sizing: border-box; cursor: pointer; text-decoration: none; font-size: 14px; font-weight: bold; margin: 0; padding: 12px 25px; text-transform: capitalize; border-color: #3498db;">Contact Us</a> </td>
                                                </tr>
                                              </tbody>
                                            </table>
                                          </td>
                                        </tr>
                                      </tbody>
            </table>
            
                        <!-- END MAIN CONTENT AREA -->
                        </table>
            
                        <!-- START FOOTER -->
                        <div class="footer" style="clear: both; Margin-top: 10px; text-align: center; width: 100%;">
                          <table border="0" cellpadding="0" cellspacing="0" style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; width: 100%;">
                            <tr>
                              <td class="content-block" style="font-family: sans-serif; vertical-align: top; padding-bottom: 10px; padding-top: 10px; font-size: 12px; color: #999999; text-align: center;">
                                <span class="apple-link" style="color: #999999; font-size: 12px; text-align: center;">UVM MEDICAL CENTER INFORMATION SERVICES | QA & TESTING DEPARTMENT</span>
                              </td>
                            </tr>
                       
                          </table>
                        </div>
                        <!-- END FOOTER -->
            
                      <!-- END CENTERED WHITE CONTAINER -->
                      </div>
                    </td>
                    <td style="font-family: sans-serif; font-size: 14px; vertical-align: top;">&nbsp;</td>
                  </tr>
                </table>
              </body>
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

root = tk.Tk()
my_gui = GUI(root)
root.mainloop()