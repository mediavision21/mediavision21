# Importer
import Scraper as scrape
import re
import pandas as pd
import time
from collections import OrderedDict

# Webscraping model - TV4 Play SE
class TV4PLAY_SE:
    def __init__(self):
        self.URL = "https://www.tv4play.se/paket"
        self.SE = {'Package': [], 'ID':[104, 105, 106, 107, 108], 'Price': [], 'Campaign': [], 'Information': []}

    # Packages names
    # Prices
    # Campaigns
    # Information
    def scrape_all(self):
        driver = scrape.selenium_site(self.URL)
        package_names = []
        price_list = []
        time.sleep(5)

        accept_button = driver.find_element(scrape.By.ID, 'onetrust-accept-btn-handler')
        accept_button.click()
        time.sleep(4)

        # Packages names
        find_package_names = driver.find_elements(scrape.By.CSS_SELECTOR,'div.cayqxF')

        for i in find_package_names:
            if i.text != '':
                package_names.append(i.text)

        # Prices
        find_price_information = driver.find_elements(scrape.By.CSS_SELECTOR,'div.icNrHF')
        for elem in find_price_information:
            i = elem.text
            if re.search('[0-9]{1,3} kr/månad', i):
                price_list.append(*re.findall('[0-9]{1,3} kr/månad', i))
       
        # Campaigns
        campaign_list = ['' for i in range(len(package_names))]


        # Information

        ad = [i.text for i in driver.find_elements(scrape.By.CSS_SELECTOR, 'div.jvLMHW')]
        
        information_list = [scrape.listToString2(ad[0:3]),
                            scrape.listToString2(ad[3:8]),
                            scrape.listToString2(ad[8:15]),
                            scrape.listToString2(ad[15:23]),
                            scrape.listToString2(ad[23:])]

        driver.close()
        return package_names, price_list, campaign_list, information_list

# Method to assign all scraped information to a dict
    def create_object(self):
        self.SE['Package'], self.SE['Price'], self.SE['Campaign'], self.SE['Information'] = self.scrape_all()
        # --- Error-handling --- check all lists same length
        if scrape.check_lists_lengths(self.SE['Package'],self.SE['Price'], self.SE['Campaign'], self.SE['Information']):
            print(self.URL + ' works!')
        else:
            print(self.URL + ' has no data!')

if __name__ == "__main__":
    tv4_play = TV4PLAY_SE()
    tv4_play.create_object()
    print(len(tv4_play.SE['Package']))
    print(len(tv4_play.SE['Information']))
    print(len(tv4_play.SE['Campaign']))
    print(len(tv4_play.SE['Price']))
    print(tv4_play.SE)