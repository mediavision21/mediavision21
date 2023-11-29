# Importer
import Scraper as scrape
from selenium.webdriver.common.by import By

# Webscraping model - HBO SE
class HBOMax_SE:
    def __init__(self):
        self.URL = "https://www.hbomax.com"
        self.SE = {'Package': [], 'ID':[117, 118], 'Price': [], 'Campaign': [], 'Information': []}

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
        price_list = [p.text.replace('/', '') for p in driver.find_elements(scrape.By.CSS_SELECTOR, 'div.text-center h3') if scrape.has_numbers(p.text) and len(p.text)<15]
        price_list = list(dict.fromkeys(price_list))
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
    def create_object(self):
        driver = scrape.selenium_site(self.URL)
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
   HBO_obj = HBOMax_SE()
   HBO_obj.create_object()
   print(HBO_obj.SE)