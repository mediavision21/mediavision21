# Importer
import Scraper as scrape
import time
import re
from selenium.common.exceptions import NoSuchElementException

# Webscraping model
class DisneyPlus_FI_NO_DK_SE:
    def __init__(self):
        self.URL_FI = "https://www.disneyplus.com/fi-fi"
        self.URL_NO = "https://www.disneyplus.com/en-no"
        self.URL_DK = "https://www.disneyplus.com/da-dk"
        self.URL_SE = "https://www.disneyplus.com/sv-se"
        self.URL_info = 'https://www.disneyplus.com/'
        self.FI = {'Package': [], 'ID':[217, 218], 'Price': [], 'Campaign': [], 'Information': []}
        self.NO = {'Package': [], 'ID':[341, 342, 308, 309, 343], 'Price': [], 'Campaign': [], 'Information': []}
        self.DK = {'Package': [], 'ID':[441, 442, 404, 405, 443], 'Price': [], 'Campaign': [], 'Information': []}
        self.SE = {'Package': [], 'ID':[139, 140, 115, 116, 141], 'Price': [], 'Campaign': [], 'Information': []}

# Method to scrape the monthly and yearly subscription
    # Package name
    # Price
    # Information
    # Campaign

    def get_package_names(self, premium, standard, standard_with_ads, disneyplus):
        premium_month = disneyplus + premium.split(" (")[0]
        premium_year = premium_month + " Annual"
        standard_month = disneyplus + standard.split(" (")[0]
        standard_year = standard_month + " Annual"
        standard_with_ads_month = disneyplus +  standard_with_ads.split(" (")[0]
        return [premium_month, premium_year, standard_month, standard_year, standard_with_ads_month]


    def monthly_yearly_subscription(self, country, url):
        driver = scrape.selenium_site(url)
        time.sleep(3)
        disneyplus = str(url.split(".")[1]).capitalize() + ' '

        try: 
            cookie_accept = driver.find_element(scrape.By.ID, 'onetrust-accept-btn-handler')
            cookie_accept.click()
        except NoSuchElementException:
            """Om cookie popup inte kommer, gör inget"""
            pass

        accordion_el = driver.find_elements(scrape.By.CSS_SELECTOR, 'div.accordion-container')[2]
        accordion_el.click() # Toggle för att kunna se priset
       
        if country == 'FI':
            time.sleep(1)
            info = accordion_el.find_elements(scrape.By.CSS_SELECTOR, 'span.medium')[0].text
            finnish_packages = [disneyplus + " monthly", disneyplus +" annual"]
            finnish_prices = re.findall(r'\d+,\d+', info)[0:2]
            finnish_info = [info, info]
            finnish_campaigns = ['', '']


        else:
            time.sleep(3)
            info = accordion_el.find_elements(scrape.By.CSS_SELECTOR, 'span.medium')[1:]
            premium = info[0].text
            standard = info[1].text
            standard_with_ads = info[2].text
            package_names = self.get_package_names(premium, standard, standard_with_ads, disneyplus)
            premium_prices = re.findall(r'\d+', premium.split("(")[1].split(")")[0])
            standard_prices = re.findall(r'\d+', standard.split("(")[1].split(")")[0])
            standard_with_ads_price = re.findall(r'\d+', standard_with_ads.split("(")[1].split(")")[0])[0]

            premium_info = premium.split(': ')[1]
            premium_info = [premium_info, premium_info]
            standard_info = standard.split(': ')[1]
            standard_info = [standard_info, standard_info]
            standard_with_ads_info = standard_with_ads.split(': ')[1]

        driver.close()

        if country == 'FI':
            self.FI['Package'] = finnish_packages
            self.FI['Price'] = finnish_prices
            self.FI['Campaign'] = finnish_campaigns
            self.FI['Information'] = finnish_info
            # --- Error-hadling --- check all lists same length
            if scrape.check_lists_lengths(self.FI['Package'], self.FI['Price'], self.FI['Campaign'],
                                          self.FI['Information']):
                print(self.URL_FI + ' works!')
            else:
                print(self.URL_FI + ' has no data!')
        elif country == 'DK':
            self.DK['Package'] = package_names
            self.DK['Price'] = [*premium_prices, *standard_prices, standard_with_ads_price]
            self.DK['Campaign'] = ['' for i in range(5)]
            self.DK['Information'] = [*premium_info, *standard_info, standard_with_ads_info]
            # --- Error-hadling --- check all lists same length
            if scrape.check_lists_lengths(self.DK['Package'], self.DK['Price'], self.DK['Campaign'],
                                          self.DK['Information']):
                print(self.URL_DK + ' works!')
            else:
                print(self.URL_DK + ' has no data!')
        elif country == 'NO':
            self.NO['Package'] = package_names
            self.NO['Price'] = [*premium_prices, *standard_prices, standard_with_ads_price]
            self.NO['Campaign'] = ['' for i in range(5)]
            self.NO['Information'] = [*premium_info, *standard_info, standard_with_ads_info]
            # --- Error-hadling --- check all lists same length
            if scrape.check_lists_lengths(self.NO['Package'], self.NO['Price'], self.NO['Campaign'],
                                          self.NO['Information']):
                print(self.URL_NO + ' works!')
            else:
                print(self.URL_NO + ' has no data!')
        elif country == 'SE':
            self.SE['Package'] = package_names
            self.SE['Price'] = [*premium_prices, *standard_prices, standard_with_ads_price]
            self.SE['Campaign'] = ['' for i in range(5)]
            self.SE['Information'] = [*premium_info, *standard_info, standard_with_ads_info]
            # --- Error-hadling --- check all lists same length
            if scrape.check_lists_lengths(self.SE['Package'], self.SE['Price'], self.SE['Campaign'],
                                          self.SE['Information']):
                print(self.URL_SE+ ' works!')
            else:
                print(self.URL_SE + ' has no data!')

# Create information lists for each country
    def create_object(self, country):
        if country =='FI':
            self.monthly_yearly_subscription('FI', self.URL_FI)
        elif country == 'NO':
            self.monthly_yearly_subscription('NO', self.URL_NO)
        elif country == 'DK':
            self.monthly_yearly_subscription('DK', self.URL_DK)
        elif country == 'SE':
            self.monthly_yearly_subscription('SE', self.URL_SE)


if __name__ == "__main__":
   disney_obj = DisneyPlus_FI_NO_DK_SE()
   disney_obj.create_object('NO')
   print(disney_obj.NO)