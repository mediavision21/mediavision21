# Importer
import time
import selenium
import Scraper as scrape
import re

# Webscraping MTV
# Works with Swedish VPN
class MTV:
    def __init__(self):
        self.URL = "https://www.mtv.fi/tuotteet"
        self.FI = {'Package': [], 'ID':[239, 240, 204, 241, 205], 'Price': [], 'Campaign': [], 'Information': []}

# Method to scrape package name(s)
    def get_package_name(self, card):
        return card.find_element(
                    scrape.By.CSS_SELECTOR,
                    "div.cayqxF"
        ).text

# Method to scrape price information
    def get_price(self, card):
        try: 
            price = card.find_element(
                scrape.By.CSS_SELECTOR,
                "div.icNrHF"
            ).text   
        except selenium.common.exceptions.NoSuchElementException:
            price = card.find_element(
                scrape.By.CSS_SELECTOR,
                "div.bBwVck"
            ).text   

        decimal_num = re.findall(r'\d+,\d+', price)
        if len(decimal_num) != 0:
            return decimal_num[0]
        else:
            num = re.findall(r'\d+,\d+', price)
            num_without_comma = re.findall(r'\d+', price)
            if len(num) == 0 and len(num_without_comma) == 0:
                raise ValueError("Not a number in price")
            if len(num) == 1:
                return num[0]
            if len(num_without_comma) == 1:
                return num_without_comma[0]
        return price


    def get_information(self, card):
        information_elements = card.find_elements(
                scrape.By.CSS_SELECTOR,
                "div.jvLMHW"
            )
        return " ".join([info.text for info in information_elements])
        

    def get_campaign(self, card):

        try:
            campaign = card.find_element(scrape.By.CSS_SELECTOR, "div.kIYumG")
            return campaign.text
        except selenium.common.exceptions.NoSuchElementException:
            return ""

        
    def collect_data(self, driver):
        package_list = []
        price_list = []
        information_list = []
        campaign_list = []
        cards = driver.find_elements(scrape.By.CSS_SELECTOR, "div.eWOtsA")
        for card in cards:

            # Packages
            package_list.append(
                self.get_package_name(card)
            )
            # Prices
            price_list.append(
                self.get_price(card) 
            )

            # Information
            information_list.append(
                self.get_information(card)
            )

            campaign_list.append(
                self.get_campaign(card)
            )


        return package_list, price_list, information_list, campaign_list


# Method to assign all scraped information to a dict
    def create_object(self):
        driver = scrape.selenium_site(self.URL)
        time.sleep(3)

        driver.find_element(scrape.By.ID, "onetrust-accept-btn-handler").click()
        time.sleep(3)
    
        self.FI['Package'], self.FI['Price'], self.FI['Information'], self.FI['Campaign'] = self.collect_data(driver)
        driver.close()

        # --- Error-hadling --- check all lists same length
        if scrape.check_lists_lengths(self.FI['Package'], self.FI['Price'], self.FI['Campaign'],
                                      self.FI['Information']):
            print(self.URL + ' works!')
        else:
            print(self.URL + ' has no data!')
        

if __name__ == "__main__":
    mtv_obj = MTV()
    mtv_obj.create_object()
    print(mtv_obj.FI)
    print(len(mtv_obj.FI['Information']))
    print(len(mtv_obj.FI['Package']))