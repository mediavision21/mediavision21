# Importer
import Scraper as scrape
import re
import time

# Webscraping model
class DNA_TV_FI:
    def __init__(self):
        self.URL = "https://kauppa4.dna.fi/Sovellukset-ja-palvelut/DNA-TV/p/VMTV00302"
        self.FI = {'Package': [], 'ID':[210], 'Price': [], 'Campaign': [], 'Information': []}

# Method to scrape package name(s)
    def package_name(self):
        soup = scrape.bs4_scrape(self.URL)
        package_name = [soup.find('h1', class_='product-name').text]
        return package_name

# Method to scrape price information
    def price(self):
        soup = scrape.bs4_scrape(self.URL)
        price = soup.find('div', class_= 'continuous-price').text
        price = ' '.join(price.split())
        price_list = re.findall(r'\d{1},\d{2} €/kk', price)
        return price_list

# Method to scrape information about campaigns
    def campaign(self):
        soup = scrape.bs4_scrape(self.URL)
        campaign = soup.find('div', class_='price sale').text
        campaign_list = [' '.join(campaign.split())]
        return campaign_list

# Method to scrape information about the packages
    def information(self):
        driver = scrape.selenium_site(self.URL)
        time.sleep(2)
        information_list = []
        information = driver.find_element(scrape.By.CSS_SELECTOR, 'div.ingress div.summary').text
        information_list.append(information)
        driver.close()
        return information_list


# Method to assign all scraped information to a dict
    def create_object(self):
        self.FI['Package'] = self.package_name()
        self.FI['Price'] = self.price()
        self.FI['Campaign'] = self.campaign()
        self.FI['Information'] = self.information()
        if scrape.check_lists_lengths(self.FI['Package'], self.FI['Price'], self.FI['Campaign'],
                                      self.FI['Information']):
            print(self.URL + ' works!')
        else:
            print(self.URL + ' has no data!')

if __name__ == "__main__":
   DNA_TV_FI_obj = DNA_TV_FI()
   DNA_TV_FI_obj.create_object()
   print(DNA_TV_FI_obj.FI)
   print(len(DNA_TV_FI_obj.FI['Information']))