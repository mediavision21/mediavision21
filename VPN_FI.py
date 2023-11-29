# Importer
import time
import Scraper as scrape
import re
from selenium.webdriver.support.ui import WebDriverWait
from YoutubePremium_SE import YoutubePremium_SE
from Eurosport_player import EurosportPlayer
from HBOMax_SE import HBOMax_SE

# Webscraping EurosportPlayer
class EurosportPlayerFI:
    def __init__(self):
        self.FI = {'Package': [], 'ID':[236], 'Price': [], 'Campaign': [], 'Information': []}

    def create_object(self):
        EurosportPlayer_obj = EurosportPlayer()
        self.FI['Package'], self.FI['Price'], self.FI['Campaign'],self.FI['Information'] = EurosportPlayer_obj.create_object_DK_NO_FI()

# Webscraping Youtube premium
class YoutubePremiumFI:
    def __init__(self):
        self.FI = {'Package': [], 'ID':[233, 234, 235],  'Price': [], 'Campaign': [], 'Information': []}

    def create_object(self):
        YoutubePremium_FI_obj = YoutubePremium_SE()
        self.FI['Package'], self.FI['Price'], self.FI['Campaign'], self.FI['Information'] = YoutubePremium_FI_obj.scrape_all()

# Webscraping model - Finnish VPN
# AmazonPrime FI
class AmazonPrimeFI:
    def __init__(self):
        self.URL_FI = "https://www.primevideo.com/"
        self.AMAZON_FI = {'Package': [], 'ID':[226], 'Price': [], 'Campaign': [], 'Information': []}

    # Method to scrape package name(s)
    def package_name(self):
        AmazonPrime = str(self.URL_FI.split(".")[1].capitalize())
        return [AmazonPrime]

    # Method to scrape price information
    def price(self, driver):
        price_list = []
        price_info = driver.find_element(scrape.By.CLASS_NAME, 'dv-copy-body').text
        if any(i.isdigit() for i in price_info):
            price = re.findall(r'[$€£]{1}\d+\.?\d{0,2}', price_info)
            price_list.append(price[0])
        return price_list

    # Method to scrape information about campaigns
    def campaign(self, driver):
        campaign_list = []
        campaign_list.append(driver.find_element(scrape.By.CLASS_NAME, 'dv-content').text)
        return campaign_list

    # Method to scrape information about the packages
    def information(self, driver):
        information_list = []
        information = driver.find_elements(scrape.By.CLASS_NAME, 'dv-copy-body')
        for i in information:
            information_list.append(i.text)
        information_list = [scrape.listToString(information_list)]
        return information_list

    # Method to assign all scraped information to a dict
    def create_object(self):
        driver = scrape.selenium_site(self.URL_FI)
        self.AMAZON_FI['Package'] = self.package_name()
        self.AMAZON_FI['Price'] = self.price(driver)
        self.AMAZON_FI['Campaign'] = self.campaign(driver)
        self.AMAZON_FI['Information'] = self.information(driver)
        driver.close()
        # --- Error-hadling --- check all lists same length
        if scrape.check_lists_lengths(self.AMAZON_FI['Package'], self.AMAZON_FI['ID'], self.AMAZON_FI['Price'], self.AMAZON_FI['Campaign'],
                                      self.AMAZON_FI['Information']):
            print(self.URL_FI + ' works!')
        else:
            print(self.URL_FI + ' has no data!')


class VPN_FI:
    def __init__(self):
        self.HBO_URL = "https://www.hbomax.com/fi/fi"
        self.HBO_FI = {'Package': [], 'ID':[221, 222], 'Price': [], 'Campaign': [], 'Information': []}
        self.DISCO_URL = 'https://auth.discoveryplus.com/fi/product'
        self.DISCO_FI = {'Package': [], 'ID':[211, 212, 213, 214], 'Price': [], 'Campaign': [], 'Information': []}

# Method to scrape DISCO
    # name of the packages
    # price of the package
    # Campaigns
    # Information about the packages
    def scrape_site(self, driver):
        Discoveryplus = str(self.DISCO_URL.split(".")[1].capitalize() + ' ')
        name_list = []
        package_list = []
        campaign_list = []
        random_list = []

        # Load the page
        time.sleep(10)
        WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(scrape.By.ID, 'onetrust-accept-btn-handler'))
        button = driver.find_element(scrape.By.ID, 'onetrust-accept-btn-handler')
        button.click()
        time.sleep(2)
        #Package information
        info_before_swipe = driver.find_elements(scrape.By.CSS_SELECTOR,
            "li.gwc-feature-list__item__9X1aN:not(.gwc-feature-list__item--unavailable__Wi3fW")
        #Package name before swipe
        name_list =[i.text for i in driver.find_elements(scrape.By.TAG_NAME,'h2') if i.text != ""]

        # Package information
        for i in info_before_swipe:
            if i.text != '':
                random_list.append(i.text)
        # Campaign information for the first packages campaigns
        campaign_information = driver.find_elements(scrape.By.CLASS_NAME,'gwc-product-card-price__additional-text__n4d0V')
        for campaign in campaign_information:
            if scrape.has_numbers(campaign.text):
                campaign_list.append(campaign.text)
            else:
                campaign_list.append('')
        # Swipe to get all packages
        swiper_button = driver.find_element(scrape.By.CLASS_NAME, 'swiper-button-next')
        swiper_button.click()
        driver.set_page_load_timeout(20)

        # Prices for the first packages
        price_list = []
        price_information = driver.find_elements(scrape.By.CLASS_NAME,'gwc-product-card-price__JZcyI')
        for i in price_information:
            if i.text[0:1].isdigit():
                price_list.append(i.text)
        price_list = [*price_list[0:3], price_list[-1]] # Ignoring duplicates
        price_list = [re.findall(r'\d+,\d+', price)[0] for price in price_list] # Remove text

        # All package names
        package_names = driver.find_elements(scrape.By.TAG_NAME, 'h2')
        for name in package_names:
            if name.text != "":
                name_list.append(name.text)
        package_list = list(dict.fromkeys(name_list))

        

        # Package information
        package_information = driver.find_elements(scrape.By.CSS_SELECTOR,"li.gwc-feature-list__item__9X1aN:not(.gwc-feature-list__item--unavailable__Wi3fW")
        random_information_list = []
        for info in package_information:
            if info.text != '':
                random_information_list.append(info.text)
        # Sort out all the information for each package
        information_list = [random_list[0], random_list[1],
                            scrape.listToString(random_list[2:5]),
                            scrape.listToString(random_information_list[4:])]
        return package_list, price_list, campaign_list, information_list

# Method to assign all scraped information to a dict
    def create_object(self):
        # --- Create HBO FI object ---
        driver = scrape.selenium_site(self.HBO_URL)
        HBOMax_FI = HBOMax_SE()
        self.HBO_FI['Package'] = HBOMax_FI.package_name(driver)
        self.HBO_FI['Price'] = HBOMax_FI.price(driver)
        self.HBO_FI['Campaign'] = HBOMax_FI.campaign(driver)
        self.HBO_FI['Information'] = HBOMax_FI.information(driver, 'FI')
        driver.close()
        # --- Error-hadling --- check all lists same length
        if scrape.check_lists_lengths(self.HBO_FI['Package'], self.HBO_FI['Price'], self.HBO_FI['Campaign'],
                                      self.HBO_FI['Information']):
            print(self.HBO_URL + ' works!')
        else:
            print(self.HBO_URL + ' has no data!')
        # --- Create DISCOVERY + FI object ---
        driver = scrape.selenium_site(self.DISCO_URL)
        self.DISCO_FI['Package'], self.DISCO_FI['Price'], self.DISCO_FI['Campaign'], self.DISCO_FI['Information'] = self.scrape_site(driver)
        driver.close()
        # --- Error-hadling --- check all lists same length
        if scrape.check_lists_lengths(self.DISCO_FI['Package'], self.DISCO_FI['Price'], self.DISCO_FI['Campaign'],
                                      self.DISCO_FI['Information']):
            print(self.DISCO_URL + ' works!')
        else:
            print(self.DISCO_URL + ' has no data!')



if __name__ == "__main__":
   VPN_FI_obj = VPN_FI()
   VPN_FI_obj.create_object()
   #print(VPN_FI_obj.HBO_FI)
   print(VPN_FI_obj.DISCO_FI)
   print(VPN_FI_obj.DISCO_FI['Price'])
   print(len(VPN_FI_obj.DISCO_FI['Campaign']))
   print(VPN_FI_obj.DISCO_FI['Campaign'])
   print(len(VPN_FI_obj.DISCO_FI['Campaign']))
   AmazonPrimeFI_obj = AmazonPrimeFI()
   AmazonPrimeFI_obj.create_object()
   print(AmazonPrimeFI_obj.AMAZON_FI)
   YoutubePremiumFI_obj = YoutubePremiumFI()
   YoutubePremiumFI_obj.create_object()
   print(YoutubePremiumFI_obj.FI)
   EuropsportPlayerFI_obj = EurosportPlayerFI()
   EuropsportPlayerFI_obj.create_object()
   print(EuropsportPlayerFI_obj.FI)