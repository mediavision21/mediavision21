# Importer
import time
import Scraper as scrape
import re

# Tele2PlayPlus Webscraping
class Tele2PlayPlus:
    def __init__(self):
        self.URL = "https://www.tele2play.se/"
        self.SE = {'Package': [], 'ID':[125, 126, 127], 'Price': [], 'Campaign': [], 'Information': []}

# Method to scrape package name(s)
    def package_name(self, driver):
        Tele2 = str(self.URL.split(".")[1].capitalize() + ' ')
        package_name_list = []
        package_name = driver.find_elements(scrape.By.CSS_SELECTOR, 'h4.PromoTeaser_title__wn8j_')
        for i in package_name:
            package_name_list.append(Tele2 + i.text)
        return package_name_list

# Method to scrape package price(s)
    def price(self, driver):
        package_price_list = [i.text for i in driver.find_elements(scrape.By.CSS_SELECTOR,'p.PromoTeaser_regularPrice__1CpXF')]
        for i in driver.find_elements(scrape.By.CSS_SELECTOR,'p.PromoTeaser_price__mJU2s'):
            package_price_list.append(i.text)
        return package_price_list

# Method to scrape information about campaigns
    # Cannot find any campaigns at the moment
    def campaign(self, driver):
        campaign_list = []
        campaigns = driver.find_elements(scrape.By.CSS_SELECTOR,'div.PromoTeaser_priceContainer__AVIUG')
        for i in campaigns:
            if '0' in i.text:
                campaign_list.append(i.text)
            else:
                campaign_list.append('')
        return campaign_list

# Method to scrape information about the packages
    def information(self, driver):
        information_list = [i.text for i in driver.find_elements(scrape.By.CSS_SELECTOR,'div.PromoTeaser_container__ZAjcA div.RichText_richText__kieMP')]
        return information_list

# Method to assign all scraped information to a dict
    def create_object(self):
        driver = scrape.selenium_site(self.URL)
        time.sleep(3)
        self.SE['Package'] = self.package_name(driver)
        self.SE['Campaign'] = self.campaign(driver)
        self.SE['Price'] = self.price(driver)
        self.SE['Information'] = self.information(driver)
        driver.close()
        # --- Error-hadling --- check all lists same length
        if scrape.check_lists_lengths(self.SE['Package'], self.SE['Price'], self.SE['Campaign'],
                                      self.SE['Information']):
            print(self.URL + ' works!')
        else:
            print(self.URL + ' has no data!')


if __name__ == "__main__":
    tele2playplus_obj = Tele2PlayPlus()
    tele2playplus_obj.create_object()
    print(tele2playplus_obj.SE)

