import pandas as pd
from selenium.webdriver.common.by import By


class Patient():
    def __init__(self, patient_id, name=None, sex=None, birth_date=None):
        self.name = name
        self.id = patient_id
        self.sex = sex
        self.birth_date = birth_date

    def has_opd(self, driver, opd_no:list, return_detail=True):
        url_opd = 'https://web9.vghtpe.gov.tw/emr/qemr/qemr.cfm?action=findOpd&histno={}'.format(self.id)
        try:
            driver.get(url_opd)
            opd_html = driver.find_element(By.ID, 'opdlist').get_attribute('outerHTML')
        except:
            return print("Fail to retrieve opd list for {}".format(self.id))

        opd_df = pd.read_html(opd_html, flavor='html5lib')[0]
        for i in range(opd_df.shape[0]):
            opd = opd_df.iloc[i]
            if opd['科別'][0:3] in opd_no:
                return (True, opd) if return_detail else True
            else:
                # Proceed to check next OPD encounter
                continue
        #No matched encounter

        return (False, None) if return_detail else False