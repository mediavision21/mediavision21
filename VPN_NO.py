# Importer
import time
import Scraper as scrape
import re
from YoutubePremium_SE import YoutubePremium_SE
from Eurosport_player import EurosportPlayer
from HBOMax_SE import HBOMax_SE

# Webscraping EurosportPlayer
class EurosportPlayerNO:
    def __init__(self):
        self.NO = {'Package': [], 'ID':[338], 'Price': [], 'Campaign': [], 'Information': []}

    def create_object(self):
        EurosportPlayer_obj = EurosportPlayer()
        self.NO['Package'], self.NO['Price'], self.NO['Campaign'], self.NO['Information'] = EurosportPlayer_obj.create_object_DK_NO_FI()

# Webscraping Youtube premium
class YoutubePremiumNO:
    def __init__(self):
        self.NO = {'Package': [], 'ID':[335, 336, 337],'Price': [], 'Campaign': [], 'Information': []}

    def create_object(self):
        YoutubePremium_NO_obj = YoutubePremium_SE()
        self.NO['Package'], self.NO['Price'], self.NO['Campaign'], self.NO['Information'] = YoutubePremium_NO_obj.scrape_all()

# Webscraping with NORWEGIAN VPN
# AmazonPrime NO
class AmazonPrimeNO:
    def __init__(self):
        self.URL_NO = "https://www.primevideo.com/"
        self.AMAZON_NO = {'Package': [], 'ID':[315], 'Price': [], 'Campaign': [], 'Information': []}

    # Method to scrape package name(s)
    def package_name(self):
        AmazonPrime = str(self.URL_NO.split(".")[1].capitalize())
        return [AmazonPrime]

    # Method to scrape price information
    def price(self, driver):
        price_list = []
        price_info = driver.find_element(scrape.By.CLASS_NAME, 'dv-copy-body').text
        if any(i.isdigit() for i in price_info):
            price = re.findall(r'NOK [0-9]+', price_info)
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
        driver = scrape.selenium_site(self.URL_NO)
        self.AMAZON_NO['Package'] = self.package_name()
        self.AMAZON_NO['Price'] = self.price(driver)
        self.AMAZON_NO['Campaign'] = self.campaign(driver)
        self.AMAZON_NO['Information'] = self.information(driver)
        driver.close()
        # --- Error-hadling --- check all lists same length
        if scrape.check_lists_lengths(self.AMAZON_NO['Package'], self.AMAZON_NO['Price'], self.AMAZON_NO['Campaign'],
                                      self.AMAZON_NO['Information']):
            print(self.URL_NO + ' works!')
        else:
            print(self.URL_NO + ' has no data!')
# Webscraping model - NO VPN
class VPN_NO:
    def __init__(self):
        self.HBO_URL = "https://www.hbomax.com/no/no"
        self.HBO_NO = {'Package': [], 'ID': [310, 311], 'Package': [], 'Price': [], 'Campaign': [], 'Information': []}
        self.DISCO_URL = 'https://auth.discoveryplus.com/no/product'
        self.DISCO_NO = {'Package': [], 'ID': [304, 305, 306, 307], 'Price': [], 'Campaign': [], 'Information': []}

# Method to scrape DISCO
    # name of the packages
    # price of the package
    # Campaigns
    # Information about the packages
    def scrape_site(self, driver):
        time.sleep(10)
        Discoveryplus = str(self.DISCO_URL.split(".")[1].capitalize() + ' ')
        name_list = []
        package_list = []
        price_list = []
        campaign_list = []
        button = driver.find_element(scrape.By.CSS_SELECTOR, 'button#onetrust-accept-btn-handler').click()
        time.sleep(5)
        # Load the page
        # Campaign information for the first packages campaigns
        campaign_information = driver.find_elements(scrape.By.CSS_SELECTOR, 'div.gwc-product-card-price__additional-text__n4d0V')
        for campaign in campaign_information:
            if scrape.has_numbers(campaign.text):
                campaign_list.append(campaign.text)
            else:
                campaign_list.append('')
        # The first package names
        package_names = driver.find_elements(scrape.By.TAG_NAME, 'h2')
        for name in package_names:
            if name.text != '':
                package_list.append(Discoveryplus + name.text)
        # The first prices
        prices = []
        price_information = driver.find_elements(scrape.By.CLASS_NAME, 'gwc-product-card-price__JZcyI')
        for i in price_information:
            if i.text != '':
                prices.append(i.text)

        # Information for the first package
        information_list = []
        information_list.append(driver.find_element(scrape.By.CSS_SELECTOR,
            'ul.gwc-feature-list__Ph3jY li.gwc-feature-list__item__9X1aN:not(.gwc-feature-list__item--unavailable__Wi3fW)').text)

        # Swipe to get all packages
        swiper_button = driver.find_element(scrape.By.CLASS_NAME,'swiper-button-next').click()
        time.sleep(1)
        # Prices for the packages
        price_information = driver.find_elements(scrape.By.CLASS_NAME, 'gwc-product-card-price__JZcyI')
        for i in price_information:
            if i.text != '':
                prices.append(i.text)
        for price in prices:
            price_split = price.split('\n',1)
            price_list.append(price_split[0])
        price_list = list(dict.fromkeys(price_list))

        # All package names
        package_names = driver.find_elements(scrape.By.TAG_NAME, 'h2')
        for name in package_names:
            if name.text != '':
                package_list.append(Discoveryplus + name.text)
        package_list = list(dict.fromkeys(package_list))

        # Package information
        information = driver.find_elements(scrape.By.CSS_SELECTOR, 'ul.gwc-feature-list__Ph3jY li.gwc-feature-list__item__9X1aN:not(.gwc-feature-list__item--unavailable__Wi3fW)')
        for i in information:
            if i.text != '':
                information_list.append(i.text)
        information_list = [information_list[0], information_list[1],
                            scrape.listToString(information_list[2:4]), scrape.listToString(information_list[4:])]
        return package_list, price_list, campaign_list, information_list

# Method to assign all scraped information to a dict
    def create_object(self):
        # --- Create HBO FI object ---
        driver = scrape.selenium_site(self.HBO_URL)
        HBOMax_NO = HBOMax_SE()
        self.HBO_NO['Package'] = HBOMax_NO.package_name(driver)
        self.HBO_NO['Price'] = HBOMax_NO.price(driver)
        self.HBO_NO['Campaign'] = HBOMax_NO.campaign(driver)
        self.HBO_NO['Information'] = HBOMax_NO.information(driver, 'NO')
        driver.close()
        # --- Error-hadling --- check all lists same length
        if scrape.check_lists_lengths(self.HBO_NO['Package'], self.HBO_NO['Price'], self.HBO_NO['Campaign'],
                                      self.HBO_NO['Information']):
            print(self.HBO_URL + ' works!')
        else:
            print(self.HBO_URL + ' has no data!')
        # --- Create DISCOVERY + NO object ---
        driver = scrape.selenium_site(self.DISCO_URL)
        timeout = 30
        element_present = scrape.EC.presence_of_element_located((scrape.By.ID, 'onetrust-accept-btn-handler'))
        scrape.WebDriverWait(driver, timeout).until(element_present)
        self.DISCO_NO['Package'], self.DISCO_NO['Price'], self.DISCO_NO['Campaign'], self.DISCO_NO['Information'] = self.scrape_site(driver)
        driver.close()
        # --- Error-hadling --- check all lists same length
        if scrape.check_lists_lengths(self.DISCO_NO['Package'], self.DISCO_NO['Price'], self.DISCO_NO['Campaign'],
                                      self.DISCO_NO['Information']):
            print(self.DISCO_URL + ' works!')
        else:
            print(self.DISCO_URL + ' has no data!')


if __name__ == "__main__":
   VPN_NO_obj = VPN_NO()
   VPN_NO_obj.create_object()
   print('HBO')
   print(len(VPN_NO_obj.HBO_NO['Information']))
   print('DISCO')
   print(len(VPN_NO_obj.DISCO_NO['Package']))
   print(len(VPN_NO_obj.DISCO_NO['Information']))
   #AmazonPrimeNO_obj = AmazonPrimeNO()
   #AmazonPrimeNO_obj.create_object()
   #print('Amazon')
   #print(len(AmazonPrimeNO_obj.AMAZON_NO['Information']))
   #ParamountPlusNO_obj = ParamountPlusNO()
   #ParamountPlusNO_obj.create_object()
   #print('Paramount')
   #print(len(ParamountPlusNO_obj.PARAMOUNT_NO['Information']))
   YoutubePremiumNO_obj = YoutubePremiumNO()
   YoutubePremiumNO_obj.create_object()
   print(YoutubePremiumNO_obj.NO)
   #EuropsportPlayer_obj = EurosportPlayerNO()
   #EuropsportPlayer_obj.create_object()
   #print('Eurosport')
   #print(len(EuropsportPlayer_obj.NO['Information']))
