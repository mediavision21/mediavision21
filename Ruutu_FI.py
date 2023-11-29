# Importer
import time

import Scraper as scrape
import re

# --- Finnish VPN not required ---
# Webscraping model - Ruutu FI
class Ruutu_FI:
    def __init__(self):
        self.URL = "https://www.ruutu.fi/plus"
        self.FI = {'Package': [], 'ID':[227, 228, 229, 230], 'Price': [], 'Campaign': [], 'Information': []}

# Method to scrape package name(s)
    def package_name(self):
        soup = scrape.bs4_scrape(self.URL)
        package_names = []
        packages = soup.find_all('h2', class_= 'cFwEfb')
        commercial = [i.text for i in
                          soup.find_all('li', class_= 'v1__LiCheckbox-sc-1rkdvyx-10') if
                          i.text != '' and scrape.has_numbers_check(i.text)]
        for i in packages:
            if 'Ruutu+' in i.text:
                package_names.append(i.text+ ' ' +commercial[0])
        for i in packages:
            if 'Ruutu+' in i.text:
                package_names.append(i.text)
        return package_names

# Method to scrape price information
    def price(self):
        soup = scrape.bs4_scrape(self.URL)
        price_list_double = []
        prices = soup.find_all('strong')
        for price in prices:
            price_list_double.append(re.findall('[0-9]+,[0-9]{2} €/kk', price.text))
        price_list = [item for sublist in price_list_double for item in sublist]
        return price_list

# Method to scrape information about campaigns
    def campaign(self):
        soup = scrape.bs4_scrape(self.URL)
        number_of_packages = len(self.package_name())
        campaign_list = list()
        for i in range(number_of_packages):
            campaign_list.append(soup.find('div', class_='eeONty').text)
        return campaign_list

# Method to scrape information about commercial packages
    def commerical(self):
        driver = scrape.selenium_site(self.URL)
        check_box = driver.find_elements(scrape.By.CLASS_NAME, 'chakra-checkbox.css-1lc114p')
        driver.execute_script('arguments[0].click();', check_box[0])
        driver.execute_script('arguments[0].click();', check_box[1])
        price_campaign = [i.text for i in driver.find_elements(scrape.By.CSS_SELECTOR,'strong') if i.text != '' and scrape.has_numbers_check(i.text)]
        price_list_double = []
        for price in price_campaign:
            price_list_double.append(re.findall('[0-9]+,[0-9]{2} €/kk', price))
        price_list = [item for sublist in price_list_double for item in sublist]
        self.FI['Price'].extend(price_list)
        driver.close()

# Method to scrape information about the packages
    def information(self):
        driver = scrape.selenium_site(self.URL)
        info1_list = []
        info2_list = []
        information1 = driver.find_elements(scrape.By.XPATH, '/html/body/div[1]/div/main/div/div/section[2]/div/div/div[1]/div/ul')
        information2 = driver.find_elements(scrape.By.XPATH,'/html/body/div[1]/div/main/div/div/section[2]/div/div/div[2]/div/ul')
        for info in information1:
            info1_list.append(info.text.replace('done\n', ''))
        for info in information2:
            info2_list.append(info.text.replace('done\n', ''))
        driver.close()
        return [scrape.listToString(info1_list), scrape.listToString(info2_list), scrape.listToString(info1_list), scrape.listToString(info2_list)]



# Method to assign all scraped information to a dict
    def create_object(self):
        self.FI['Package'] = self.package_name()
        self.FI['Price'] = self.price()
        self.FI['Campaign'] = self.campaign()
        self.FI['Information'] = self.information()
        self.commerical()
        # --- Error-hadling --- check all lists same length
        if scrape.check_lists_lengths(self.FI['Package'], self.FI['Price'], self.FI['Campaign'],
                                      self.FI['Information']):
            print(self.URL + ' works!')
        else:
            print(self.URL + ' has no data!')

if __name__ == "__main__":
   ruutu_FI = Ruutu_FI()
   ruutu_FI.create_object()
   print(ruutu_FI.FI)