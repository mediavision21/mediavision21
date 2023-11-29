# Importer
import time
import Scraper as scrape
import re

# Webscraping model
class AmazonPrime_SE:
    def __init__(self):
        self.URL = "https://www.primevideo.com/"
        self.SE = {'Package': [], 'ID': [122, 142], 'Price': [], 'Campaign': [], 'Information': []}

# Method to scrape package name(s)
    def package_name(self):
        AmazonPrime = str(self.URL.split(".")[1].capitalize())
        return [AmazonPrime, AmazonPrime + " Årsplan"]

# Method to scrape price information
    def price(self, driver):
        price_list = []
        information = driver.find_element(scrape.By.CSS_SELECTOR,'div.dv-copy-body p').text
        return re.findall(r'\d+.\d+', information)

# Method to scrape information about campaigns
    def campaign(self, driver):
        campaign_list = []
        campaign_list.extend(2*[driver.find_element(scrape.By.CSS_SELECTOR,'span.dv-content').text])
        return campaign_list


# Method to scrape information about the packages
    def information(self, driver):
        information_list = []
        information = driver.find_elements(scrape.By.CSS_SELECTOR,'div.dv-copy-body p')
        for i in information:
            information_list.append(i.text)
        information_list = 2*[scrape.listToString(information_list)]
        return information_list

# Method to assign all scraped information to a dict
    def create_object(self):
        driver = scrape.selenium_site(self.URL)
        time.sleep(5)
        self.SE['Package'] = self.package_name()
        self.SE['Price'] = self.price(driver)
        self.SE['Campaign'] = self.campaign(driver)
        self.SE['Information'] = self.information(driver)
        driver.close()
        # --- Error-handling --- check all lists same length
        if scrape.check_lists_lengths(self.SE['Package'],self.SE['Price'], self.SE['Campaign'], self.SE['Information']):
            print(self.URL + ' works!')
        else:
            print(self.URL + ' has no data!')

if __name__ == "__main__":
   AmazonPrime_SE_obj = AmazonPrime_SE()
   AmazonPrime_SE_obj.create_object()
   print(AmazonPrime_SE_obj.SE)