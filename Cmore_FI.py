# Importer
import time

import Scraper as scrape
import re

# Webscraping Cmore FI
# Works with Swedish VPN
class CmoreFI:
    def __init__(self):
        self.URL = "https://www.cmore.fi/"
        self.FI = {'Package': [], 'ID':[204, 205, 206, 207, 208, 209], 'Price': [], 'Campaign': [], 'Information': []}

# Method to scrape package name(s)
    def package_name(self, driver):
        package_names_list = []
        package_names = driver.find_elements(scrape.By.CSS_SELECTOR,'h4.sc-7xehqg-3.sc-34h7td-1.bkPPga.jmUsvh')
        for name in package_names:
            package_names_list.append(name.text)
        return package_names_list

# Method to scrape price information
    def price(self, driver):
        time.sleep(2)
        price_list = [i.text for i in driver.find_elements(scrape.By.CSS_SELECTOR,'p.sc-34h7td-3.dySuew')]
        return price_list

# Method to scrape information about campaigns and information
    def campaign_information(self, driver, telia):
        # list for all the campaigns
        campaign_list = []
        # "check button" for each package
        check_button = driver.find_elements(scrape.By.CSS_SELECTOR, 'div.sc-34h7td-4.Mwjww')
        for b in check_button:
            time.sleep(2)
            driver.execute_script("arguments[0].click();", b)
            time.sleep(2)
            campaign = driver.find_element(scrape.By.CSS_SELECTOR,'button.sc-pbmgs6-0.gggiBh').text
            information_list = [i.text for i in driver.find_elements(scrape.By.CSS_SELECTOR,'h4.sc-7xehqg-3.sc-vqvt09-1.bkPPga.idFjSj')]
            if scrape.has_numbers(campaign):
                campaign_list.append(campaign)
            else:
                campaign_list.append('')
            time.sleep(3)
        c_more = scrape.listToString(information_list[0:3])
        c_more_total_plus = scrape.listToString(information_list)
        if telia == True:
            cmore_tv = information_list[0]+ ', '+ information_list[1]
            total_information_list = [c_more, c_more_total_plus, cmore_tv]
        else:
            cmore_sport = scrape.listToString(information_list[2:4])
            total_information_list = [c_more,c_more_total_plus, cmore_sport]
        return campaign_list,total_information_list


# Method to assign all scraped information to a dict
    def create_object(self):
        driver = scrape.selenium_site(self.URL)
        time.sleep(3)
        driver.find_element(scrape.By.ID, 'onetrust-accept-btn-handler').click()
        time.sleep(3)
        driver.execute_script("window.scrollTo(0, window.scrollY + 500)")
        self.FI['Package'] = self.package_name(driver)
        self.FI['Price'] = self.price(driver)
        self.FI['Campaign'], self.FI['Information'] = self.campaign_information(driver, False)
        # --- Telia packages ---
        driver.find_element(scrape.By.CSS_SELECTOR, 'label div.sc-vxp6y7-15.kxXSmZ').click()
        time.sleep(3)
        pack_list = self.package_name(driver)
        price_list = self.price(driver)
        camp_list, info_list = self.campaign_information(driver, True)
        self.FI['Package'].extend(pack_list)
        self.FI['Price'].extend(price_list)
        self.FI['Campaign'].extend(camp_list)
        self.FI['Information'].extend(info_list)
        driver.close()

        # --- Error-hadling --- check all lists same length
        if scrape.check_lists_lengths(self.FI['Package'], self.FI['Price'], self.FI['Campaign'],
                                      self.FI['Information']):
            print(self.URL + ' works!')
        else:
            print(self.URL + ' has no data!')


if __name__ == "__main__":
    cmore_obj = CmoreFI()
    cmore_obj.create_object()
    print(cmore_obj.FI)
    print(len(cmore_obj.FI['Information']))
    print(len(cmore_obj.FI['Package']))