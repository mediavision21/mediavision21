# Importer
import time

import Scraper as scrape

# Webscraping model
class TV2_DK:
    def __init__(self):
        self.URL = "https://play.tv2.dk/"
        self.DK = {'Package': [], 'ID':[414, 415, 416, 417, 418, 419], 'Price': [], 'Campaign': [], 'Information': []}

# Method to scrape package name(s)
    def package_name(self):
        soup = scrape.bs4_scrape(self.URL)
        tv2 = str(self.URL.split(".")[1].upper())
        package_list = []
        
        package_names = soup.find_all('div', class_='text-midnight')
        med_utan_reklam = soup.find_all('div', class_='text-button-label-xs')
        med_reklam = med_utan_reklam[0].text
        utan_reklam = med_utan_reklam[1].text
        for i in package_names:
            package_list.append(tv2 + ' ' + i.text + ' ' + med_reklam)
            package_list.append(tv2 + ' ' + i.text + ' ' + utan_reklam)
       
        return package_list[-6:]

# Method to scrape price information
    def price(self):
        soup = scrape.bs4_scrape(self.URL)
        price_list = []
        prices = soup.find_all('button', {'class':['flex','shrink-0', 'w-full']})
        for element in prices:
            if scrape.has_numbers_check(element.text):
                price_list.append(element.text)
        return price_list

# --- No campaigns scraped ---
    def campaign(self):
        soup = scrape.bs4_scrape(self.URL)
        campaign_list = []
        for i in range(len(self.price())):
            campaign_list.append('')
        return campaign_list

    # Method to scrape information about the packages
    def information(self):
        soup = scrape.bs4_scrape(self.URL)
        information_list = []
        information = soup.find_all('ul', class_='px-6')
        for i in information:
            information_list.append(i.text)
            information_list.append(i.text)
        return information_list

    # Method to assign all scraped information to a dict
    def create_object(self):
        self.DK['Package'] = self.package_name()
        self.DK['Price'] = self.price()
        self.DK['Campaign'] = self.campaign()
        self.DK['Information'] = self.information()
        # --- Error-hadling --- check all lists same length
        if scrape.check_lists_lengths(self.DK['Package'], self.DK['Price'], self.DK['Campaign'],
                                      self.DK['Information']):
            print(self.URL + ' works!')
        else:
            print(self.URL + ' has no data!')

if __name__ == "__main__":
    TV2_DK_obj = TV2_DK()
    TV2_DK_obj.create_object()
    print(len(TV2_DK_obj.DK['Package']))
    print(len(TV2_DK_obj.DK['Price']))
    print(len(TV2_DK_obj.DK['Information']))
    print(TV2_DK_obj.DK)