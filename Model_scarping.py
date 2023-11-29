# Importer
import Scraper as scrape
import time

# Webscraping model
class NAME:
    def __init__(self):
        self.URL_SE = ""
        self.URL_NO = ""
        self.URL_DK = ""
        self.URL_FI = ""
        self.SE = {'Package': [], 'Price': [], 'Campaign': [], 'Information': []}
        self.NO = {'Package': [], 'Price': [], 'Campaign': [], 'Information': []}
        self.DK = {'Package': [], 'Price': [], 'Campaign': [], 'Information': []}
        self.FI = {'Package': [], 'Price': [], 'Campaign': [], 'Information': []}

    def scrape_information(self):
        driver = scrape.selenium_site(self.URL)
        driver.close()

# Method to scrape package name(s)
    def package_name(self):
        URL_scrape = str(self.URL.split(".")[1])
        soup = scrape.bs4_scrape(self.URL)
        pass

# Method to scrape price information
    def price(self):
        soup = scrape.bs4_scrape(self.URL)
        pass
# Method to scrape information about campaigns
    def campaign(self):
        soup = scrape.bs4_scrape(self.URL)

# Method to scrape information about the packages
    def information(self):
        soup = scrape.bs4_scrape(self.URL)

# Method to assign all scraped information to a dict
    def create_object(self):
        self.SE['Package'] = self.package_name()
        self.SE['Price'] = self.price()
        self.SE['Campaign'] = self.campaign()
        self.SE['Information'] = self.information()

if __name__ == "__main__":
   pass