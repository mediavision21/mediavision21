# Importer
import Scraper as scrape
import time
import re
# Webscraping model - SE
# Changed name - Starts 20 sep.
# Sky show time fd. Paramount
class SkyShowTime:
    def __init__(self):
        self.URL = "https://www.skyshowtime.com/se/"
        self.URL_info = 'https://www.skyshowtime.com/se/plans'
        self.SE = {'Package': [], 'ID':[123, 124], 'Price': [], 'Campaign': [], 'Information': []}
        self.DK = {'Package': [], 'ID':[432, 433], 'Price': [], 'Campaign': [], 'Information': []}
        self.FI = {'Package': [], 'ID':[231, 232], 'Price': [], 'Campaign': [], 'Information': []}
        self.NO = {'Package': [], 'ID':[316, 317],'Price': [], 'Campaign': [], 'Information': []}

# Method to scrape package name(s)
    def package_name(self, driver, country):
        SkyShowTime_name = str(self.URL.split(".")[1].capitalize())
        monthly_yearly = [i.text for i in driver.find_elements(scrape.By.CSS_SELECTOR, 'span.eCwlci strong.richTextstyles__RTStrong-sc-1nxnh0u-13.gPhGkc')]
        if country == 'FI':
            package_names = [SkyShowTime_name, SkyShowTime_name + ' ' + monthly_yearly[1]]
        else:
            package_names = [SkyShowTime_name+ ' '+ monthly_yearly[0], SkyShowTime_name+' '+ monthly_yearly[1]]
        return package_names

# Method to scrape price information
    def price(self,driver, country):
        price_list_1 = [i.text for i in driver.find_elements(scrape.By.CSS_SELECTOR, 'p.jbKMNH')]
        price_list = []

        if country == "NO" or country == "DK":

            price_list.extend(
                [i.text for i in driver.find_elements(scrape.By.CSS_SELECTOR, "span.cQBhyK strong")],
            )
            return price_list
        for i in price_list_1:
            if country == 'SE':
                if re.search('[0-9]{1,3} kr/månad', i):
                    price_list.append(*re.findall('[0-9]{1,3} kr/månad', i))
            if country == 'DK':
                if re.search('[0-9]{1,2} kr./md.', i):
                    price_list.append(*re.findall(r'\d+', i))
            if country == 'FI':
                if re.search('[0-9]{1},[0-9]{1,2} €/kk', i):
                    price_list.append(*re.findall('[0-9]{1},[0-9]{1,2} €/kk', i))
                if re.search('[0-9]{1}.[0-9]{1,2} € kuussa', i):
                    price_list.append(*re.findall('[0-9]{1}.[0-9]{1,2} € kuussa', i))

        return price_list

# Method to scrape information about campaigns
    def campaign(self, driver, country):
        campaign_list = ['' for i in range(len(self.package_name(driver, country)))]
        return campaign_list

# Method to scrape information about the packages
    def information(self,driver):
        time.sleep(2)
        information_list = [
            i.text for i in driver.find_elements(scrape.By.CSS_SELECTOR, 'p.richTextstyles__RTParagraph-sc-1nxnh0u-4.jbKMNH')
        ]
        information_list = [scrape.listToString2(information_list[0:7]), scrape.listToString2(information_list[7:])]
        return information_list

# Method to assign all scraped information to a dict
    def create_object(self, country):
        driver = scrape.selenium_site(self.URL_info)
        driver.implicitly_wait(7)
        driver.find_element(scrape.By.ID, 'onetrust-accept-btn-handler').click()
        time.sleep(2)
        if country == 'SE':
            self.SE['Package'] = self.package_name(driver, country)
            self.SE['Price'] = self.price(driver,country)
            self.SE['Campaign'] = self.campaign(driver, country)
            self.SE['Information'] = self.information(driver)
        if country == 'NO':
            self.NO['Package'] = self.package_name(driver, country)
            self.NO['Price'] = self.price(driver, country)
            self.NO['Campaign'] = self.campaign(driver, country)
            self.NO['Information'] = self.information(driver)
        if country == 'DK':
            self.DK['Package'] = self.package_name(driver, country)
            self.DK['Price'] = self.price(driver, country)
            self.DK['Campaign'] = self.campaign(driver, country)
            self.DK['Information'] = self.information(driver)
        if country == 'FI':
            self.FI['Package'] = self.package_name(driver, country)
            self.FI['Price'] = self.price(driver,country)
            self.FI['Campaign'] = self.campaign(driver, country)
            self.FI['Information'] = self.information(driver)
        # --- Error-hadling --- check all lists same length
        if scrape.check_lists_lengths(self.package_name(driver, country), self.price(driver, country), self.campaign(driver, country), self.information(driver)):
            print(self.URL + ' works!')
        else:
            print(self.URL + ' has no data!')
        driver.close()



if __name__ == "__main__":
    SkyShowTime_obj = SkyShowTime()
    SkyShowTime_obj.create_object('DK')
    print(SkyShowTime_obj.DK)