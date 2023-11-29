# Importer
import time
import selenium
import Scraper as scrape

# Webscraping model
class NordiskFilmPlus:
    def __init__(self):
        self.URL = "https://nordiskfilmplus.com/"
        self.DK = {'Package': [], 'ID':[428], 'Price': [], 'Campaign': [], 'Information': []}

# Method to scrape all information including:
    # Packages names
    # Prices
    # Campaigns
    # Information
    def scrape_information(self):
        Nordisk_film_plus = self.URL.split(".")[0].split('/')[2].capitalize()
        driver = scrape.selenium_site(self.URL)
        time.sleep(5)  # gives an implicit wait for 20 seconds
        # --- Package names ---
        package_list = [Nordisk_film_plus]
        # --- Prices ---
        price_information = driver.find_element(scrape.By.CSS_SELECTOR,'span.OfferButton_buttonSpan__01SVM.OfferButton_large__7gKda').text.split()
        price_list = [scrape.listToString(price_information[1:])]
        # --- Campaigns ---
        campaign_list = ['' for i in range(len(package_list))]
        # --- Information --- Do not scrape information, no information about packages on the website
        time.sleep(3)
        driver.find_element(scrape.By.CSS_SELECTOR,'button.coi-banner__accept').click()
        driver.execute_script("window.scrollTo(0, window.scrollY + 1500)")
        information_list = [i.text for i in driver.find_elements(scrape.By.CSS_SELECTOR, 'div.IntroScreen_Features__XiNpH')]
        information_list = [scrape.listToString(information_list)]
        driver.close()
        return package_list, price_list, campaign_list, information_list

# Method to assign all scraped information to a dict
    def create_object(self):
        self.DK['Package'], self.DK['Price'], self.DK['Campaign'], self.DK['Information'] = self.scrape_information()
        # --- Error-hadling --- check all lists same length
        if scrape.check_lists_lengths(self.DK['Package'], self.DK['Price'], self.DK['Campaign'],
                                      self.DK['Information']):
            print(self.URL + ' works!')
        else:
            print(self.URL + ' has no data!')

if __name__ == "__main__":
   NordiskFilmPlus = NordiskFilmPlus()
   NordiskFilmPlus.create_object()
   print(NordiskFilmPlus.DK)