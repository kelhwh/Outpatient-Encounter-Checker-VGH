import time
import pandas as pd
import getpass
from selenium import webdriver
from selenium.webdriver.common.by import By
from pyfiglet import figlet_format
from patient import Patient
from verification import (verify_length_strict, verify_date)

URL_LOGIN = 'https://eip.vghtpe.gov.tw/login.php'
URL_REGISTRATION = 'https://web9.vghtpe.gov.tw/emr/qemr/qemr.cfm?action=findReg'
URL_EMR = 'https://web9.vghtpe.gov.tw/emr/qemr/qemr.cfm?action=findEmr'

class App():
    def __int__(self):
        return

    def run(self, test_run=False):
        print(figlet_format('VGHTPE\nRadOnc', font='3-d'))
        print("This app helps you check whether the patients who've booked appointments on the given day are new to RO.")

        USERNAME = input('Web9 Username:')
        PASSWORD = getpass.getpass('Password: ')
        OPD_DATE = input('Date (ex.20230220): ')
        verify_date(OPD_DATE)
        OPD_NO = input('OPD Code (ex. 042): ')
        verify_length_strict(OPD_NO, 3)
        OPD_ROOM = input('OPD Room (ex. 17): ')
        verify_length_strict(OPD_ROOM, 2)

        # Initialize chromedriver
        print("Starting...")
        options = webdriver.ChromeOptions()
        options.add_argument('headless') #With browser hidden
        options.add_argument('log-level=3') #Show only fatal message
        driver = webdriver.Chrome('chromedriver', options=options)

        # Login
        print("Logging in...")
        driver.get(URL_LOGIN)
        time.sleep(2)
        username = driver.find_element(By.ID, 'login_name')
        password = driver.find_element(By.ID, 'password')
        login_button = driver.find_element(By.ID, 'loginBtn')

        username.send_keys(USERNAME)
        password.send_keys(PASSWORD)
        login_button.click()
        time.sleep(2)

        print("Checking patients on {} for OPD:{} Room:{}...".format(OPD_DATE, OPD_NO, OPD_ROOM))
        driver.get(URL_REGISTRATION + '&dt={}&ect={}&room={}'.format(OPD_DATE, OPD_NO, OPD_ROOM))
        time.sleep(2)
        registration_html = driver.find_element(By.ID, 'regdetail').get_attribute('outerHTML')
        patient_df = pd.read_html(registration_html, flavor='html5lib')[0]
        patient_list = patient_df['病歷號']

        if len(patient_list)==0 or patient_list[0]=='無資料':
            return print("No patients on {}.".format(OPD_DATE))

        if test_run:
            patient_list = patient_list[:1]

        driver.get(URL_EMR + '&histno={}'.format(str(patient_list[0]))) # Visit the EMR homepage first to avoid error

        num_new_patient = 0
        for id in patient_list:
            p = Patient(patient_id=id)
            has_opd, opd = p.has_opd(driver, ['0RR', '0RA', '042', '142'])
            if has_opd:
                print("{} has recent appointment with {} on {}.".format(id, opd['門診醫師'],opd['門診日期']))
            elif not has_opd:
                num_new_patient += 1
                print("NEW!! {} has no recent RO appointment history.".format(id))
            time.sleep(1)

        driver.close()

        print("A total of {} patients, with {} new patients on {}.".format(len(patient_list), num_new_patient, OPD_DATE))
        print("-"*10 + "Finished" + "-"*10)
        input("Press ENTER to leave")

if __name__ == "__main__":
    app = App()
    app.run(test_run=False)