# Importer
import time
import Scraper as scrape

# Webscraping model
class EurosportPlayer:
    def __init__(self):
        self.URL = "https://auth.eurosportplayer.com/product"
        self.SE = {'Package': [], 'ID': [134], 'Price': [], 'Campaign': [], 'Information': []}

# Method to scrape package name(s)
    def package_name(self, driver):
        Eurosport_player = str(self.URL.split(".")[1].capitalize() + ' ')
        package_names_list = []
        names = driver.find_elements(scrape.By.CLASS_NAME,'price-plan-title__3o5Ou')
        for name in names:
            package_names_list.append(Eurosport_player + name.text)
        return package_names_list

# Method to scrape price information
    def price(self, driver):
        price_list = []
        prices = driver.find_elements(scrape.By.CLASS_NAME,'price-plans-price__price-head__ExPCK')
        periods = driver.find_elements(scrape.By.CLASS_NAME,'price-plans-price__period__1VjcN.price-plans-price__period--big__2rBRp')
        for price, period in zip(prices, periods):
            price_list.append(price.text+' '+period.text)
        return price_list

# Method to scrape information about campaigns -- Do not scrape campaigns
    def campaign(self, driver):
        campaign_list_length = len(self.package_name(driver))
        campaign_list = []
        for i in range(campaign_list_length):
            campaign_list.append('')
        return campaign_list

# Method to scrape information about the packages
    def information(self, driver):
        information_list = []
        information_list_length = len(self.package_name(driver))
        information = driver.find_element(scrape.By.CLASS_NAME, 'pricePlansRow__item__3sq4-').text
        for i in range(information_list_length):
            information_list.append(information)
        return information_list

# Method to assign all scraped information to a dict
    def create_object_SE(self):
        driver = scrape.selenium_site(self.URL)
        time.sleep(6)
        self.SE['Package'] = self.package_name(driver)
        self.SE['Price'] = self.price(driver)
        self.SE['Campaign'] = self.campaign(driver)
        self.SE['Information'] = self.information(driver)
        driver.close()
        # --- Error-hadling --- check all lists same length
        if scrape.check_lists_lengths(self.SE['Package'], self.SE['Price'], self.SE['Campaign'],
                                      self.SE['Information']):
            print(self.URL + ' works!')
        else:
            print(self.URL + ' has no data!')

# Method to return all the scraped info for the other countries
    def create_object_DK_NO_FI(self):
        driver = scrape.selenium_site(self.URL)
        time.sleep(6)
        package_list = self.package_name(driver)
        price_list = self.price(driver)
        campaign_list = self.campaign(driver)
        information_list = self.information(driver)
        driver.close()
        # --- Error-hadling --- check all lists same length
        if scrape.check_lists_lengths(package_list, price_list, campaign_list, information_list):
            print(self.URL + ' works!')
        else:
            print(self.URL + ' has no data!')
        return package_list, price_list, campaign_list,information_list

if __name__ == "__main__":
   EurosportPlayer_obj = EurosportPlayer()
   EurosportPlayer_obj.create_object_SE()
   print(EurosportPlayer_obj.SE)