# Importer
import time
import re
import Scraper as scrape

# Webscraping model
class TV2_NO:
    def __init__(self):
        self.URL = "https://play.tv2.no/pakker"
        self.NO = {'Package': [], 'ID':[324, 345, 346, 347, 327, 328], 'Price': [], 'Campaign': [], 'Information': []}

    def get_cards(self, driver):
        cards = driver.find_elements(scrape.By.CSS_SELECTOR, 'div.css-7qy3s')
        return cards
    
    def get_packages(self, cards):
        package_list = []
        for card in cards:
            package_type = card.find_element(scrape.By.CSS_SELECTOR, 'h3').text
            package_list.extend(["TV2 "+ package_type + " Uten reklame","TV2 " + package_type +" Med reklame" ])
        return package_list
    
    def get_prices(self, cards):
        price_list = []
        for card in cards:
            prices = card.find_elements(scrape.By.CSS_SELECTOR, "span.css-1k7sn2r span")
            for price in prices:
                price_list.append(price.text)
        return price_list
    
    def get_information(self, cards):
        information_list = []
        for card in cards:
            info = ", ".join([i.text for i in card.find_elements(scrape.By.CSS_SELECTOR, "li.css-1x91pt8")])
            information_list.extend([info, info])
        return information_list

    
    def get_campaigns(self, cards):
        return ["" for _ in self.NO["ID"]]

    # Method to assign all scraped information to a dict
    def create_object(self):
        driver = scrape.selenium_site(self.URL)
        time.sleep(4)
        cards = self.get_cards(driver)
        self.NO['Package'] = self.get_packages(cards)
        self.NO['Price'] = self.get_prices(cards)
        self.NO['Campaign'] = self.get_campaigns(cards)
        self.NO['Information'] = self.get_information(cards)
        driver.close()
        # --- Error-hadling --- check all lists same length
        if scrape.check_lists_lengths(self.NO['Package'], self.NO['Price'], self.NO['Campaign'],
                                      self.NO['Information']):
            print(self.URL + ' works!')
        else:
            print(self.URL + ' has no data!')


if __name__ == "__main__":
    TV2_NO_obj = TV2_NO()
    TV2_NO_obj.create_object()
    print(TV2_NO_obj.NO)
    print(len(TV2_NO_obj.NO['Package']))
    print(len(TV2_NO_obj.NO['Price']))
    print(len(TV2_NO_obj.NO['Campaign']))
    print(len(TV2_NO_obj.NO['Information']))