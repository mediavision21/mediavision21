# Importer
import time

import Scraper as scrape
import re
from selenium.webdriver.support.ui import WebDriverWait
from YoutubePremium_SE import YoutubePremium_SE
from Eurosport_player import EurosportPlayer
from HBOMax_SE import HBOMax_SE

# Webscraping EurosportPlayer
class EurosportPlayerDK:
    def __init__(self):
        self.DK = {'Package': [], 'ID':[424], 'Price': [], 'Campaign': [], 'Information': []}

    def create_object(self):
        EurosportPlayer_obj = EurosportPlayer()
        self.DK['Package'], self.DK['Price'], self.DK['Campaign'], self.DK['Information'] = EurosportPlayer_obj.create_object_DK_NO_FI()


# Webscraping Youtube premium
class YoutubePremiumDK:
    def __init__(self):
        self.DK = {'Package': [], 'ID':[429, 430, 431], 'Price': [], 'Campaign': [], 'Information': []}

    def create_object(self):
        YoutubePremium_DK_obj = YoutubePremium_SE()
        self.DK['Package'], self.DK['Price'], self.DK['Campaign'], self.DK['Information'] = YoutubePremium_DK_obj.scrape_all()
        print(self.DK['Package'], self.DK['Price'], self.DK['Campaign'], self.DK['Information'])


# Webscraping with DANISH VPN
# AmazonPrime FI
class AmazonPrimeDK:
    def __init__(self):
        self.URL_DK = "https://www.primevideo.com/"
        self.AMAZON_DK = {'Package': [],  'ID':[413], 'Price': [], 'Campaign': [], 'Information': []}

    # Method to scrape package name(s)
    def package_name(self):
        AmazonPrime = str(self.URL_DK.split(".")[1].capitalize())
        return [AmazonPrime]

    # Method to scrape price information
    def price(self, driver):
        price_list = []
        price_info = driver.find_element(scrape.By.CLASS_NAME, 'dv-copy-body').text
        if any(i.isdigit() for i in price_info):
            price = re.findall(r'DKK [0-9]+', price_info)
            price_list.append(price[0] + '/month')
        return price_list

    # Method to scrape information about campaigns
    def campaign(self, driver):
        campaign_list = []
        campaign_list.append(driver.find_element(scrape.By.CLASS_NAME,'dv-content').text)
        return campaign_list

    # Method to scrape information about the packages
    def information(self, driver):
        information_list = []
        information = driver.find_elements(scrape.By.CLASS_NAME,'dv-copy-body')
        for i in information:
            information_list.append(i.text)
        information_list = [scrape.listToString(information_list)]
        return information_list

    # Method to assign all scraped information to a dict
    def create_object(self):
        driver = scrape.selenium_site(self.URL_DK)
        self.AMAZON_DK['Package'] = self.package_name()
        self.AMAZON_DK['Price'] = self.price(driver)
        self.AMAZON_DK['Campaign'] = self.campaign(driver)
        self.AMAZON_DK['Information'] = self.information(driver)
        driver.close()
        # --- Error-hadling --- check all lists same length
        if scrape.check_lists_lengths(self.AMAZON_DK['Package'], self.AMAZON_DK['Price'], self.AMAZON_DK['Campaign'],
                                      self.AMAZON_DK['Information']):
            print(self.URL_DK + ' works!')
        else:
            print(self.URL_DK + ' has no data!')

# Webscraping model - Danish VPN
class VPN_DK:
    def __init__(self):
        self.HBO_URL = "https://www.hbomax.com/dk/da"
        self.HBO_DK = {'Package': [], 'ID':[407, 408], 'Price': [], 'Campaign': [], 'Information': []}
        self.DISCO_URL = 'https://auth.discoveryplus.com/dk/product'
        self.DISCO_DK = {'Package': [], 'ID':[409, 410, 411, 412], 'Price': [], 'Campaign': [], 'Information': []}

# Method to scrape DISCO
    # name of the packages
    # price of the package
    # Campaigns
    # Information about the packages
    def scrape_site(self, driver):
        time.sleep(4)
        Discoveryplus = str(self.DISCO_URL.split(".")[1].capitalize() + ' ')
        name_list = []
        package_list = []
        campaign_list = []
        random_list = []

        # Load the page
        WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(scrape.By.ID, 'onetrust-accept-btn-handler'))
        button = driver.find_element(scrape.By.ID,'onetrust-accept-btn-handler')
        button.click()

        #Package information
        info_before_swipe = driver.find_elements(scrape.By.CSS_SELECTOR,
            "li.gwc-feature-list__item__9X1aN:not(.gwc-feature-list__item--unavailable__Wi3fW")
        # Package information
        for i in info_before_swipe:
            random_list.append(i.text)
        # Campaign information for the first packages campaigns
        campaign_information = driver.find_elements(scrape.By.CLASS_NAME,'gwc-product-card-price__additional-text__n4d0V')
        for campaign in campaign_information:
            if scrape.has_numbers(campaign.text):
                campaign_list.append(campaign.text)
            else:
                campaign_list.append('')

        # Prices for the first packages
        price_list = []
        price_information = driver.find_elements(scrape.By.CLASS_NAME,'gwc-product-card-price__JZcyI')
        for i in price_information:
            price_list.append(i.text)

        # Names for the first packages
        package_names = driver.find_elements(scrape.By.TAG_NAME, 'h2')
        for name in package_names:
            if name.text != '':
                package_list.append(Discoveryplus + name.text)
        swipe = driver.find_element(scrape.By.CLASS_NAME, 'swiper-button-next').click()
        time.sleep(3)
        # Prices for packages to the right
        for i in price_information:
            price_list.append(i.text) if i.text not in price_list else price_list
        price_elems = []
        # Combine the prices for all the packages
        for price in price_list:
            if price[0:1].isdigit():
                price_elems.append(price[0:5] + ' kr/månad')

        # All package names
        package_names = driver.find_elements(scrape.By.TAG_NAME,'h2')
        for name in package_names:
            if name.text != '':
                package_list.append(Discoveryplus + name.text)
        package_list = list(dict.fromkeys(package_list))

        # Package information
        package_information = driver.find_elements(scrape.By.CSS_SELECTOR,"li.gwc-feature-list__item__9X1aN:not(.gwc-feature-list__item--unavailable__Wi3fW")
        random_information_list = []
        for info in package_information:
            random_information_list.append(info.text)
        # Sort out all the information for each package
        information_list= [random_list[0], scrape.listToString(random_information_list[1:3]),
                            scrape.listToString(random_information_list[3:6]),
                                                scrape.listToString(random_information_list[6:])]

        print(package_list, price_elems, campaign_list, information_list)
        return package_list, price_elems, campaign_list, information_list

# Method to assign all scraped information to a dict
    def create_object(self):
        # --- Create HBO DK object ---
        driver = scrape.selenium_site(self.HBO_URL)
        HBOMax_DK = HBOMax_SE()
        self.HBO_DK['Package'] = HBOMax_DK.package_name(driver)
        self.HBO_DK['Price'] = HBOMax_DK.price(driver)
        self.HBO_DK['Campaign'] = HBOMax_DK.campaign(driver)
        self.HBO_DK['Information'] = HBOMax_DK.information(driver, 'DK')
        driver.close()
        # --- Error-hadling --- check all lists same length
        if scrape.check_lists_lengths(self.HBO_DK['Package'], self.HBO_DK['Price'], self.HBO_DK['Campaign'],
                                      self.HBO_DK['Information']):
            print(self.HBO_URL + ' works!')
        else:
            print(self.HBO_URL + ' has no data!')
        # --- Create DISCOVERY + DK object ---
        driver = scrape.selenium_site(self.DISCO_URL)
        self.DISCO_DK['Package'], self.DISCO_DK['Price'], self.DISCO_DK['Campaign'], self.DISCO_DK['Information'] = self.scrape_site(driver)
        driver.close()
        # --- Error-hadling --- check all lists same length
        if scrape.check_lists_lengths(self.DISCO_DK['Package'], self.DISCO_DK['Price'], self.DISCO_DK['Campaign'],
                                      self.DISCO_DK['Information']):
            print(self.DISCO_URL + ' works!')
        else:
            print(self.DISCO_URL + ' has no data!')


if __name__ == "__main__":
   VPN_DK_obj = VPN_DK()
   VPN_DK_obj.create_object()
   #print(VPN_DK_obj.HBO_DK)
   #print(VPN_DK_obj.DISCO_DK)
   #AmazonPrimeDK_obj = AmazonPrimeDK()
   #AmazonPrimeDK_obj.create_object()
   #print(AmazonPrimeDK_obj.AMAZON_DK)
   #ParamountPlusDK_obj = ParamountPlusDK()
   #ParamountPlusDK_obj.create_object()
   #print(ParamountPlusDK_obj.PARAMOUNT_DK)
   YoutubePremiumDK_obj = YoutubePremiumDK()
   YoutubePremiumDK_obj.create_object()
   print(YoutubePremiumDK_obj.DK)
   #EuropsportPlayer_obj = EurosportPlayerDK()
   #EuropsportPlayer_obj.create_object()
   #print(EuropsportPlayer_obj.DK)