# Importer
import Scraper as scrape
import re

# Webscraping model - NETFLIX: SE, FI, DK and NO.
class Netflix:
    def __init__(self):
        self.URL_SE = "https://help.netflix.com/sv/node/24926?ui_action=kb-article-popular-categories"
        self.URL_FI = "https://help.netflix.com/sv/node/24926/fi"
        self.URL_DK = "https://help.netflix.com/sv/node/24926/dk"
        self.URL_NO = "https://help.netflix.com/sv/node/24926/no"
        self.SE = {'Package': [], 'ID':[119, 120, 121], 'Price': [], 'Campaign': [], 'Information': []}
        self.FI = {'Package': [], 'ID':[223, 224, 225], 'Price': [], 'Campaign': [], 'Information': []}
        self.DK = {'Package': [], 'ID':[401, 402, 403], 'Price': [], 'Campaign': [], 'Information': []}
        self.NO = {'Package': [], 'ID':[312, 313, 314], 'Price': [], 'Campaign': [], 'Information': []}

# Method to scrape package name(s)
# Fill the campaign list with empty strings - do not scrape any campaigns for Netflix
    def package_name_campaign(self, driver):
        Netflix = str(self.URL_SE.split(".")[1].capitalize() + ' ')
        package_list =[Netflix + i.text for i in driver.find_elements(scrape.By.CSS_SELECTOR, 'div.c-wrapper div ul li p strong')]
        campaign_list = []
        for i in range(len(package_list)):
            campaign_list.append('')
        return package_list, campaign_list


# Method to scrape price information
    def price(self, driver, country):
        information = driver.find_elements(scrape.By.CSS_SELECTOR,'div ul li p')
        price_list = []
        for i in information:
            if re.search('[0-9]{2,3}', i.text):
                if country == 'SE':
                    price_list.append(re.findall('[0-9]{2,3} kr/månad', i.text)[0])
                elif country == 'FI':
                    price_list.append(re.findall('[0-9]{1,2}.[0-9]{1,2}€ / month', i.text)[0])
                elif country == 'DK':
                    price_list.append(re.findall('[0-9]{2,3} kr / month', i.text)[0])
                elif country == 'NO':
                    price_list.append(re.findall('[0-9]{2,3} / month', i.text)[0])
        return price_list

# Method to scrape information about the packages
    def information(self, driver):
        information1 = driver.find_element(scrape.By.CSS_SELECTOR, 'tbody').text
        information = information1.split('\n')
        information_list = [scrape.listToString(information[:5]),
                            scrape.listToString(information[5:11]),
                            scrape.listToString(information[11:])]
        return information_list

# Method to assign all scraped information to a dict
    def create_object(self, country):
        if country == 'SE':
            driver = scrape.selenium_site(self.URL_SE)
            self.SE['Package'], self.SE['Campaign'] = self.package_name_campaign(driver)
            self.SE['Price'] = self.price(driver, country)
            self.SE['Information'] = self.information(driver)
            driver.close()
            # --- Error-handling --- check all lists same length
            if scrape.check_lists_lengths(self.SE['Package'], self.SE['Price'], self.SE['Campaign'],
                                          self.SE['Information']):
                print(self.URL_SE + ' works!')
            else:
                print(self.URL_SE + ' has no data!')
        elif country == 'FI':
            driver = scrape.selenium_site(self.URL_FI)
            self.FI['Package'], self.FI['Campaign'] = self.package_name_campaign(driver)
            self.FI['Price'] = self.price(driver, country)
            self.FI['Information'] = self.information(driver)
            driver.close()
            # --- Error-hadling --- check all lists same length
            if scrape.check_lists_lengths(self.FI['Package'], self.FI['Price'], self.FI['Campaign'],
                                          self.FI['Information']):
                print(self.URL_FI + ' works!')
            else:
                print(self.URL_FI + ' has no data!')
        elif country =='DK':
            driver = scrape.selenium_site(self.URL_DK)
            self.DK['Package'], self.DK['Campaign'] = self.package_name_campaign(driver)
            self.DK['Price'] = self.price(driver, country)
            self.DK['Information'] = self.information(driver)
            driver.close()
            # --- Error-handling --- check all lists same length
            if scrape.check_lists_lengths(self.DK['Package'], self.DK['Price'], self.DK['Campaign'],
                                          self.DK['Information']):
                print(self.URL_DK + ' works!')
            else:
                print(self.URL_DK + ' has no data!')
        elif country == 'NO':
            driver = scrape.selenium_site(self.URL_NO)
            self.NO['Package'], self.NO['Campaign'] = self.package_name_campaign(driver)
            self.NO['Price'] = self.price(driver, country)
            self.NO['Information'] = self.information(driver)
            driver.close()
            # --- Error-handling --- check all lists same length
            if scrape.check_lists_lengths(self.NO['Package'], self.NO['Price'], self.NO['Campaign'],
                                          self.NO['Information']):
                print(self.URL_NO + ' works!')
            else:
                print(self.URL_NO + ' has no data!')

if __name__ == "__main__":
   netflix_obj = Netflix()
   netflix_obj.create_object('SE')
   print(netflix_obj.SE)