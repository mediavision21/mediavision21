# Importer
import re
import Scraper as scrape
import time

# Webscraping Hayu
# Sweden
# Finland - requires Finish VPN
# Denmark - requires Danish VPN
# Norway - requires Norwegian VPN

class Hayu:
    def __init__(self):
        self.URL = "https://www.hayu.com/signup"
        self.URL_hayu = "https://www.hayu.com"
        self.URL_NO = 'https://get.hayu.com/welcome?geo=NO'
        self.SE = {'Package': [], 'ID':[135, 136, 137],'Price': [], 'Campaign': [], 'Information': []}
        self.NO = {'Package': [], 'ID':[339, 340], 'Price': [], 'Campaign': [], 'Information': []}
        self.FI = {'Package': [], 'ID':[237],'Price': [], 'Campaign': [], 'Information': []}
        self.DK = {'Package': [], 'ID':[425, 426, 427], 'Price': [], 'Campaign': [], 'Information': []}

# Method to scrape all information for Sweden and Norway
    # Package names
    # Prices
    # Campaigns
    # Information
    def scrape_all_SE_DK(self):
        driver = scrape.selenium_site(self.URL)
        time.sleep(5)
        driver.implicitly_wait(5)
        package_list = []
        price_list = []
        campaign_list = []
        information_list = []
        while True:
            # Accept cookies
            try:
                button = driver.find_element(scrape.By.ID, 'onetrust-accept-btn-handler')
                button.click()
                time.sleep(5)
                Hayu_name = str(self.URL.split(".")[1]).capitalize() + ' '
                # Package names
                package_names = driver.find_elements(scrape.By.CLASS_NAME,'heaLJo')
                
                for name in package_names:
                    if not name.text == '':
                        package_list.append(Hayu_name + name.text)

                # Prices
                prices = driver.find_elements(scrape.By.CLASS_NAME,'gLvytZ')
    
                for price in prices:
                    if scrape.has_numbers(price.text):
                        price_list.append(price.text)

                # Campaigns
                for i in range(len(package_list)):
                    campaign_list.append(" ".join([c.text for c in driver.find_elements(scrape.By.CLASS_NAME, 'cbwlhb')]))
                # Information
                for i in range(len(package_list)):
                    information_list.append("")
            except:
                break
                driver.close()
                self.scrape_all_SE()

        driver.close()
        return package_list, price_list, campaign_list, information_list


# Method to scrape all information for Norway
    def scrape_all_NO(self):
        information_list = []
        Hayu_name = str(self.URL.split(".")[1]).capitalize()
        driver = scrape.selenium_site(self.URL_NO)
        time.sleep(3)
        driver.find_element(scrape.By.ID,'onetrust-accept-btn-handler').click()
        driver.execute_script("window.scrollTo(0, window.scrollY + 300)")
        package_list = []
        price_list = [i.text for i in driver.find_elements(scrape.By.CSS_SELECTOR, 'span h3') if scrape.has_numbers(i.text) and 'kr' in i.text]
        temp = price_list[1].split(' ')
        price_list[1] = scrape.listToString(temp[1:])
        for i in price_list:
            package_list.append(Hayu_name +str(i.split('|')[1]))
        campaign_list = [driver.find_element(scrape.By.XPATH, '/html/body/div[2]/div/div[3]/div/div[1]/div[1]/div/div/div/span/p[2]').text,
                         driver.find_element(scrape.By.XPATH,'/html/body/div[2]/div/div[3]/div/div[2]/div[1]/div/div/div/span/p[2]').text]
        information_list = [driver.find_element(scrape.By.CSS_SELECTOR, 'span.h4').text for i in range(len(package_list))]
        driver.close()
        return package_list, price_list, campaign_list, information_list

# Method to scrape all information for Finland and Denmark
    # Package names
    # Prices
    # Campaigns
    # Information
    def scrape_all_FI(self):
        driver = scrape.selenium_site(self.URL)
        time.sleep(10)
        driver.implicitly_wait(5)
        while True:
            # Accept cookies
            try:
                button = driver.find_element(scrape.By.ID,'onetrust-accept-btn-handler')
                button.click()
                time.sleep(5)
                Hayu_name = str(self.URL.split(".")[1]).capitalize()
                package_list = [Hayu_name]
                price_list = []
                campaign_list = []
                information_list = []

                # Campaigns
                campaign_list.append(driver.find_element(scrape.By.CLASS_NAME,
                    'cbwlhb').text)

                # Prices
                prices = scrape.listToString(campaign_list).split(' ')
                for price in prices:
                    if re.search('[0-9]{2}', price):
                        price_list.append(price)
                price_list = list(dict.fromkeys(price_list))
                # Information
                information_list.append(" ".join([i.text for i in driver.find_elements(scrape.By.CLASS_NAME,
                    'cbwlhb')]))
            except:
                break
                driver.close()
                self.scrape_all_FI_DK()

        driver.close()
        return package_list, price_list, campaign_list, information_list

    # Method to assign all scraped information to a dicts
    # country: SE, NO, FI, DK
    def create_object(self, country):
        if country == 'SE':
            self.SE['Package'], self.SE['Price'], self.SE['Campaign'], self.SE['Information'] = self.scrape_all_SE_DK()
            # --- Error-hadling --- check all lists same length
            if scrape.check_lists_lengths(self.SE['Package'], self.SE['Price'], self.SE['Campaign'],
                                          self.SE['Information']):
                print(self.URL + ' works!')
            else:
                print(self.URL + ' has no data!')
        elif country == 'NO':
            self.NO['Package'], self.NO['Price'], self.NO['Campaign'], self.NO['Information'] = self.scrape_all_NO()
            # --- Error-hadling --- check all lists same length
            if scrape.check_lists_lengths(self.NO['Package'], self.NO['Price'], self.NO['Campaign'],
                                          self.NO['Information']):
                print(self.URL + ' works!')
            else:
                print(self.URL + ' has no data!')
        elif country == 'FI':
            self.FI['Package'], self.FI['Price'], self.FI['Campaign'], self.FI['Information'] = self.scrape_all_FI()
            # --- Error-hadling --- check all lists same length
            if scrape.check_lists_lengths(self.FI['Package'], self.FI['Price'], self.FI['Campaign'],
                                          self.FI['Information']):
                print(self.URL + ' works!')
            else:
                print(self.URL + ' has no data!')
        elif country == 'DK':
            self.DK['Package'], self.DK['Price'], self.DK['Campaign'], self.DK['Information'] = self.scrape_all_SE_DK()
            # --- Error-hadling --- check all lists same length
            if scrape.check_lists_lengths(self.DK['Package'], self.DK['Price'], self.DK['Campaign'],
                                          self.DK['Information']):
                print(self.URL + ' works!')
            else:
                print(self.URL + ' has no data!')

if __name__ == "__main__":
   Hayu_obj = Hayu()
   Hayu_obj.create_object('SE')
   #Hayu_obj.create_object('NO')
   #Hayu_obj.create_object('DK')
   #Hayu_obj.create_object('FI')
   print(Hayu_obj.SE)

   #print(Hayu_obj.NO)
   #print(Hayu_obj.DK)
   #print(Hayu_obj.FI)