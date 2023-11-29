# Importer
import time
import Scraper as scrape

# Webscraping model
class Strim_NO:
    def __init__(self):
        self.URL_signup = 'https://www.strim.no/bli-kunde/velg'
        self.NO = {'Package': [], 'ID':[318, 319, 320, 321, 322, 323], 'Price': [], 'Campaign': [], 'Information': []}
        self.list_of_links = []
        self.subscription_packages = []

    # --- Basic packages Strim ---
    def Strim(self, driver):
        # Strim Mye
        time.sleep(4)
        self.NO['Package'] = [i.text for i in driver.find_elements(scrape.By.CSS_SELECTOR, 'h2.rds-title-2._title_1ses4_21')]
        price_list = [i.text for i in driver.find_elements(scrape.By.CSS_SELECTOR, 'div._price_1meul_1 span[data-testid="total-price"]')]
        for i in range(len(self.NO['Package'])):
            self.NO['Price'].append(price_list[i])
        for i in range(len(self.NO['Package'])):
            self.NO['Campaign'].append('')
        self.NO['Information'] = [i.text for i in driver.find_elements(scrape.By.CSS_SELECTOR, 'div._description_1ses4_79')]

# --- Sport packages, addon ---
    def sport_paket(self, driver):
        sport_paket = []
        Strim = str(self.URL_signup.split(".")[1].capitalize())
        for i in driver.find_elements(scrape.By.CSS_SELECTOR, 'h2.rds-title-2'):
            if not 'Strim' in i.text:
                sport_paket.append(i.text)
                self.NO['Package'].append(Strim + ' '+ i.text)
        price_list = [i.text for i in driver.find_elements(scrape.By.CSS_SELECTOR, 'div._price_1meul_1 span[data-testid="total-price"]')]
        price_list.pop(0)
        price_list.pop(0)
        self.NO['Price'] = self.NO['Price'] + price_list
        for i in range(len(sport_paket)):
            self.NO['Campaign'].append('')
        for i in driver.find_elements(scrape.By.CSS_SELECTOR, 'ul.rds-list'):
            if i.text[0].isdigit():
                self.NO['Information'].append(i.text)

# Method to create object and call methods
    def create_object(self):
        driver = scrape.selenium_site(self.URL_signup)
        time.sleep(2)
        self.Strim(driver)
        self.sport_paket(driver)
        driver.close()
        # --- Error-hadling --- check all lists same length
        if scrape.check_lists_lengths(self.NO['Package'], self.NO['Price'], self.NO['Campaign'],
                                      self.NO['Information']):
            print(self.URL_signup + ' works!')
        else:
            print(self.URL_signup + ' has no data!')

if __name__ == "__main__":
   Strim_NO_obj = Strim_NO()
   Strim_NO_obj.create_object()
   print(Strim_NO_obj.NO)
   print(len(Strim_NO_obj.NO['Package']))
   print(len(Strim_NO_obj.NO['Information']))
   print(len(Strim_NO_obj.NO['Price']))
   print(len(Strim_NO_obj.NO['Campaign']))