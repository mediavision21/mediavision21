# Importer
import time
import Scraper as scrape
from selenium.webdriver.support.ui import WebDriverWait

# Webscraping model - DISCOVERY PLUS SE
class Discoveryplus_SE:
    def __init__(self):
        self.SE = {'Package': [], 'ID': [109, 110, 111, 112, 113, 114], 'Price': [], 'Campaign': [], 'Information': []}
        self.URL_SE = "https://auth.discoveryplus.com/se/product?flow=purchase"

    # Method to scrape package name(s), prices, campaign and information about the packages.
    def scrape_site_SE(self, driver):
        Discoveryplus = str(self.URL_SE.split(".")[1].capitalize() + ' ')
        name_list = []
        package_list = []
        campaign_list = []
        random_list = []

        # Load the page
        WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(scrape.By.ID, 'onetrust-accept-btn-handler'))
        button = driver.find_element(scrape.By.ID, 'onetrust-accept-btn-handler')
        button.click()
        time.sleep(2)
        info_before_swipe = driver.find_elements(scrape.By.CSS_SELECTOR,
            "li.gwc-feature-list__item__9X1aN:not(.gwc-feature-list__item--unavailable__Wi3fW")
        # All package names
        package_names = driver.find_elements(scrape.By.TAG_NAME, 'h2')
        for name in package_names:
            if scrape.has_letters(name.text):
                name_list.append(name.text)
        # Package information
        for i in info_before_swipe:
            random_list.append(i.text)
        # Campaign information for the first packages campaigns
        campaign_information = driver.find_elements(scrape.By.CSS_SELECTOR,'div.gwc-product-card-price__additional-text__n4d0V')
        for campaign in campaign_information:
            if has_numbers(campaign.text):
                campaign_list.append(campaign.text)
            else:
                campaign_list.append('')

        # Prices for the first packages
        price_campaign = driver.find_elements(scrape.By.CLASS_NAME, 'gwc-product-card-price__old-price__dnVwn')
        price_list = []
        price_information = driver.find_elements(scrape.By.CLASS_NAME,'gwc-product-card-price__JZcyI')
        for price in price_campaign:
            if price.text[0:1].isdigit():
                price_list.append(price.text)
        for price in price_information:
            if price.text[0:1].isdigit():
                price_list.append(price.text)

        # Swipe to get all packages
        time.sleep(3)
        swiper_button = driver.find_element(scrape.By.CLASS_NAME,'swiper-button-next')
        swiper_button.click()
        driver.set_page_load_timeout(20)

        swiper_button.click()
        driver.set_page_load_timeout(20)

        swiper_button.click()
        driver.set_page_load_timeout(20)
        time.sleep(6)

        # All package names
        package_names = driver.find_elements(scrape.By.TAG_NAME,'h2')
        for name in package_names:
            if scrape.has_letters(name.text):
                name_list.append(name.text)
        for i in name_list:
            package_list.append(Discoveryplus + i)

        # Prices for packages to the right
        for i in price_information:
            price_list.append(i.text) if i.text not in price_list else price_list
        price_elems = []
        # Combine the prices for all the packages
        for price in price_list:
            if price[0:1].isdigit():
                price_elems.append(price[0:5] + ' kr/månad')
        price_elems = list(dict.fromkeys(price_elems))

        # Package information
        package_information = driver.find_elements(scrape.By.CSS_SELECTOR,
            "ul.gwc-feature-list__Ph3jY li.gwc-feature-list__item__9X1aN:not(.gwc-feature-list__item--unavailable__Wi3fW")
        random_information_list = []
        for info in package_information:
            if info.text != '':
                random_information_list.append(info.text)
        # Sort out all the information for each package
        information_list = [random_list[0], scrape.listToString(random_list[1:3]),
                            scrape.listToString(random_list[3:6]),
                            scrape.listToString(random_information_list[0:4]),
                            scrape.listToString(random_information_list[4:7]),
                            scrape.listToString(random_information_list[7:])]
        return package_list, price_elems, campaign_list, information_list


# Method to assign all scraped information to a dict
    def create_object(self):
        driver = scrape.selenium_site(self.URL_SE)
        self.SE['Package'], self.SE['Price'], self.SE['Campaign'], self.SE['Information'] = self.scrape_site_SE(driver)
        # --- Error-hadling --- check all lists same length
        if scrape.check_lists_lengths(self.SE['Package'], self.SE['Price'], self.SE['Campaign'],
                                      self.SE['Information']):
            print(self.URL_SE + ' works!')
        else:
            print(self.URL_SE + ' has no data!')
        driver.close()

# --- HELP FUNCTIONS ---
def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)
def has_letters(inputString):
    return any(char.isalpha() for char in inputString)

if __name__ == "__main__":
    discovery_obj = Discoveryplus_SE()
    discovery_obj.create_object()
    print(discovery_obj.SE['Package'])
    print(len(discovery_obj.SE['Campaign']))
    print(len(discovery_obj.SE['Package']))
    print(len(discovery_obj.SE['Price']))
    print(len(discovery_obj.SE['Information']))
