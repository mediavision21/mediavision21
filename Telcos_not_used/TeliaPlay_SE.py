# Importer
import Scraper as scrape
import time
import re

# Webscraping model
class TeliaPlay:
    def __init__(self):
        self.URL = "https://www.telia.se/privat/tv/tvpaket"
        self.SE = {'Package': [], 'Price': [], 'Campaign': [], 'Information': []}

# Method to scrape package name(s), prices, campaigns and information.
    def scrape_all(self):
        driver = scrape.selenium_site(self.URL)
        telia = str(self.URL.split(".")[1]).capitalize()
        package_name = []
        all_prices = []
        price_list = []
        campaign_list = []
        information_list = []
        driver.find_element_by_id('cookie-preferences-accept-button').click()

        time.sleep(3)
        driver.execute_script("window.scrollTo(0, window.scrollY + 500)")
        time.sleep(3)
        names = driver.find_elements_by_css_selector('h3.service-product-card_telia-service-product-card__title__TiRio')
        prices_campaigns = driver.find_elements_by_css_selector('div.service-product-card_telia-service-product-card__price-container__MqpJM')
        information = driver.find_elements_by_css_selector('div.service-product-card_telia-service-product-card__rich-text__O8al5 ul')

        for name in names:
            print(name.text)
            package_name.append(telia + ' ' + name.text)

        for campaign_price in prices_campaigns:
            price_list.append(campaign_price.text)
            if len(campaign_price.text)>10:
                campaign_list.append(campaign_price.text)
            else:
                campaign_list.append('')
        for idx, price in enumerate(price_list):
            if len(price)>10:
                item = re.findall('[1-9]{1,3} kr/mån', price)
                if len(item)==2:
                    price_list[idx] = item[1]
                elif len(item) ==1:
                    price_list[idx] = item[0]
                else:
                    print('För kort')
        for info in information:
            information_list.append(info.text)
        driver.close()
        return package_name, price_list, campaign_list, information_list

# Method to assign all scraped information to a dict
    def create_object(self):
        self.SE['Package'], self.SE['Price'], self.SE['Campaign'], self.SE['Information']= self.scrape_all()

if __name__ == "__main__":
   TeliaPlay_obj = TeliaPlay()
   TeliaPlay_obj.create_object()
   print(TeliaPlay_obj.SE)
   print(TeliaPlay_obj.SE['Campaign'])
   print(len(TeliaPlay_obj.SE['Package']))
   print(len(TeliaPlay_obj.SE['Price']))
   print(len(TeliaPlay_obj.SE['Campaign']))
   print(len(TeliaPlay_obj.SE['Information']))