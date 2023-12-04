# Importer
import Scraper as scrape
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import re
import time

# Webscraping model - HBO SE
class HBOMax:
    def __init__(self):
        self.URL_SE = "https://www.hbomax.com"
        self.SE = {'Package': [], 'ID':[117, 118], 'Price': [], 'Campaign': [], 'Information': []}
        self.URL_DK = "https://www.hbomax.com/dk/da"
        self.DK = {'Package': [], 'ID':[407, 408], 'Price': [], 'Campaign': [], 'Information': []}


# Method to scrape package name(s)
    def package_name(self, driver):
        package_list = []
        HBOMax = str(self.URL.split(".")[1])
        HBOMax = HBOMax[:3].upper()+' '+ HBOMax[3:].capitalize() + ' '
        monthly_yearly = driver.find_elements(scrape.By.CSS_SELECTOR, 'div.text-center h2')
        package_list.append(HBOMax + monthly_yearly[0].text)
        package_list.append(HBOMax + monthly_yearly[1].text)
        return package_list

# Method to scrape price information
    def price(self, driver):
        price_list = [p.text.replace('/', '') for p in driver.find_elements(scrape.By.CSS_SELECTOR, 'div.text-center h3') if scrape.has_numbers(p.text) and len(p.text)<15][0:2]
        if price_list[0] == price_list[1]:
            # Checks if scraped monthly price is the same as the scraped yearly, happens for denmark currently
            # In which case we scroll down and check the price lower in the page
            element = driver.find_element(scrape.By.ID, "accordion-header-3")
            driver.execute_script("arguments[0].click(); window.scrollBy(0, 4000)", element) # clicks button and scrolls down
            time.sleep(2)
            price_info = driver.find_element(scrape.By.CSS_SELECTOR, "section#accordion-panel-3 p.text-left").text
            price_list = re.findall(r'\d+ kr', price_info)
        return price_list

# Method to scrape information about campaigns
    def campaign(self, driver):
        campaign_list = ['' for i in range(len(self.package_name(driver)))]
        return campaign_list

# Method to scrape information about the packages
    def information(self, driver, country):
        if country == 'SE':
            info = [i.text for i in driver.find_elements(scrape.By.CSS_SELECTOR, 'div.text-center h1')]
            information_list = [scrape.listToString2(info) for i in range(len(self.package_name(driver)))]
        elif country == 'FI':
            info = [i.text for i in driver.find_elements(scrape.By.CSS_SELECTOR,'div.text-center h1')]
            information_list = [scrape.listToString2(info) for i in range(len(self.package_name(driver)))]
        elif country == 'NO':
            info = [i.text for i in driver.find_elements(scrape.By.CSS_SELECTOR,'div.text-center h1')]
            information_list = [scrape.listToString2(info) for i in range(len(self.package_name(driver)))]
        elif country == 'DK':
            info = [i.text for i in driver.find_elements(scrape.By.CSS_SELECTOR,'div.text-center h1')]
            information_list = [scrape.listToString2(info) for i in range(len(self.package_name(driver)))]
        return information_list

# Method to assign all scraped information to a dict
    def create_object(self, country):
        driver = scrape.selenium_site(self.URL)
        time.sleep(3)
        try:
            driver.find_element(scrape.By.ID, "onetrust-accept-btn-handler").click()
        except NoSuchElementException:
            # If a cookie button doesn't show up => Do nothing
            pass

        self.SE['Package'] = self.package_name(driver)
        self.SE['Price'] = self.price(driver)
        self.SE['Campaign'] = self.campaign(driver)
        self.SE['Information'] = self.information(driver, 'SE')
        driver.close()
        if scrape.check_lists_lengths(self.SE['Package'],self.SE['Price'], self.SE['Campaign'], self.SE['Information']):
            print(self.URL + ' works!')
        else:
            print(self.URL + ' has no data!')

if __name__ == "__main__":
   HBO_obj = HBOMax()
   HBO_obj.create_object("DK")
   print(HBO_obj.DK)