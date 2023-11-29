# Importer
import Scraper as scrape
import re

# Viaplay Webscaping - SE, FI, NO, DK
class Viaplay:

    def __init__(self):
        self.URL_SE = 'https://viaplay.se/se-sv/'
        self.URL_NO = 'https://checkout.viaplay.no/?countryCode=no'
        self.front_page_NO = 'https://viaplay.no/no-nb'
        self.URL_FI = 'https://viaplay.fi/'
        self.URL_DK = 'https://viaplay.dk/'
        self.SE = {'Package': [], 'ID':[128, 129, 130], 'Price':[], 'Campaign': [], 'Information': []}
        self.NO = {'Package': [], 'ID':[332, 333, 334],'Price':[], 'Campaign': [], 'Information': []}
        self.FI = {'Package': [], 'ID':[219, 220], 'Price':[], 'Campaign': [], 'Information': []}
        self.DK = {'Package': [], 'ID':[439, 440], 'Price':[], 'Campaign': [], 'Information': []}

    # Package names SE DK
    def package_names_SE_DK(self, driver):
        # namn
        package_names = [i.text for i in driver.find_elements(scrape.By.CSS_SELECTOR,"h3.text-lg.font-bolder.mb-5.text-center")]
        return package_names

    # Package names FI
    def package_names(self, driver):
        package_names = [i.text for i in driver.find_elements(scrape.By.CSS_SELECTOR,"h3.text-lg.font-bolder.mb-5.text-center")]
        return package_names


    # Package Name NO
    def package_names_NO(self, URL, URL_front_page):
        soup = scrape.bs4_scrape(URL)
        soup1 = scrape.bs4_scrape(URL_front_page)
        # namn
        package_names = []
        for i in soup.find_all("h3", class_="package__title"):
            if 'Viaplay' in i.text:
                package_names.append(i.text)
            else:
                package_names.append(soup1.find('h3', {'class': ['text-lg', 'font-bolder', 'mb-5', 'text-center']}).text)
        names = list(dict.fromkeys(package_names))
        return names

    # Works only to get package prices from Sweden
    def price_se(self,driver):
        prices = [i.text for i in driver.find_elements(scrape.By.CSS_SELECTOR,'div.text-center div.mb-2')]
        price_list = re.findall('[1-9]{1,3} kr/mån', scrape.listToString(prices))
        return price_list

    # Works only to get package prices from Norway
    def price_no(self, driver):
        price_list = [i.text for i in driver.find_elements(scrape.By.CSS_SELECTOR,'span.price.value')]
        return price_list

    # Works only to get package prices from Finland
    def price_fi(self, driver):
        price_paragraph = [i.text for i in driver.find_elements(scrape.By.CSS_SELECTOR,'div p.text-lg.font-bolder.mb-1')]
        return price_paragraph

    # Works only to get package prices from Finland
    def price_dk(self, driver):
        prices = [i.text for i in driver.find_elements(scrape.By.CSS_SELECTOR,'div.text-center div.mb-2')]
        price_list = re.findall(r'\d{3} kr/md',scrape.listToString(prices))
        return price_list

# COUNTRY - SE
# A method to take out the campaign.
# Returns an empty list if no campaign.
    def campaign_SE(self, driver):
        campaign_list =[]
        package_wrapper = driver.find_elements(scrape.By.CSS_SELECTOR,'div.text-center div a')
        for element in package_wrapper:
            if not element.text is None:
                if any(i.isdigit() for i in element.text):
                    campaign_list.append(element.text)
                else:
                    campaign_list.append('')
        return campaign_list

    # COUNTRY - NO
    # A method to take out the campaign.
    # Returns an empty list if no campaign.
    def campaign_NO(self, URL):
        soup = scrape.bs4_scrape(URL)
        campaign_list = []
        for element in soup.find_all('div', class_='btn-block-v2'):
            if any(i.isdigit() for i in element.text):
                campaign_list.append(element.text)
            else:
                campaign_list.append('')
        return campaign_list

    # COUNTRY - DK
    # A method to take out the campaign.
    # Returns an empty list if no campaign.
    def campaign_DK(self, URL):
        soup = scrape.bs4_scrape(URL)
        campaign_list = []
        for element in soup.find_all('p', class_='text-lg'):
            if 'gratis' in element.text:
                campaign_list.append(element.text)
            else:
                campaign_list.append('')
        return campaign_list

    # COUNTRY - FI
    # A method to take out the campaign.
    # Returns an empty list if no campaign.
    def campaign_FI(self,driver):
        campaign_list = []
        test_list = [i.text for i in driver.find_elements(scrape.By.CSS_SELECTOR,'div.flex.flex-col.items-center a.btn')]
        for i in test_list:
            if scrape.has_numbers_check(i):
                campaign_list.append(i)
            else:
                campaign_list.append('')
        return campaign_list

# COUNTRY - SE
# A method to take out package information.
# Returns a lists with information about all the packages
    # The list is sorted in the following order: Viaplay Film & Serier, Viaplay Medium, Viaplay Total
    def package_information_SE(self,driver):
        # information
        package_information = [i.text for i in driver.find_elements(scrape.By.CSS_SELECTOR,'li.grid.gap-x-3.gap-y-1.items-center')]
        package_list = [scrape.listToString(package_information[0:3]), scrape.listToString(package_information[5:9]), scrape.listToString(package_information[0:5])]
        return package_list

# COUNTRY - DENMARK
# A method to take out package information.
# Returns a lists containing information about all the packages
# The list is sorted in the following order:Viaplay Film & Serier, Viaplay Total
    def package_information_DK(self, driver):
        information_list_1 = [i.text.split('\n') for i in driver.find_elements(scrape.By.CSS_SELECTOR,'ul.py-6.flex.flex-col')]
        information_list = [scrape.listToString2(information_list_1[0][2:]), scrape.listToString2(information_list_1[1])]
        return information_list

# COUNTRY - FINLAND
# A method to take out package information.
# Returns a lists containing information about all the packages
# The list is sorted in the following order:Viaplay Film & Serier, Viaplay Total
    def package_information_FI(self, driver):
        # information
        package_list = [i.text for i in driver.find_elements(scrape.By.CSS_SELECTOR,'ul.py-6.flex.flex-col.gap-6')]
        return package_list

# COUNTRY - NORWAY
# A method to take out package information.
# Returns a lists containing information about all the packages
# The list is sorted in the following order:Viaplay Film & Serier, Viaplay Total, Viaplay Nyheter
# Note: Comes in a different order on the website: Viaplay total, Viaplay Film & Serier, Viaplay Nyheter
    def package_information_NO(self, driver):

        information_list = []

        packages = driver.find_elements(scrape.By.CSS_SELECTOR, ".package")
        for package in packages:
            information_list.append(
                scrape.listToString([i.text for i in package.find_elements(scrape.By.CSS_SELECTOR,'div.item:not(.disabled)')])
            )
        
        return information_list

    def create_objects_viaplay(self, country):
        if country == 'SE':
            driver = scrape.selenium_site(self.URL_SE)
            self.SE['Package'] = self.package_names_SE_DK(driver)
            self.SE['Price'] = self.price_se(driver)
            self.SE['Campaign'] = self.campaign_SE(driver)
            self.SE['Information'] = self.package_information_SE(driver)
            driver.close()
            # --- Error-hadling --- check all lists same length
            if scrape.check_lists_lengths(self.SE['Package'], self.SE['Price'], self.SE['Campaign'],
                                          self.SE['Information']):
                print(self.URL_SE + ' works!')
            else:
                print(self.URL_SE + ' has no data!')
        elif country == 'NO':
            driver = scrape.selenium_site(self.URL_NO)
            self.NO['Package'] = self.package_names_NO(self.URL_NO, self.front_page_NO)
            self.NO['Price'] = self.price_no(driver)
            self.NO['Campaign'] = self.campaign_NO(self.URL_NO)
            self.NO['Information'] = self.package_information_NO(driver)
            driver.close()
            # --- Error-handling --- check all lists same length
            if scrape.check_lists_lengths(self.NO['Package'], self.NO['Price'], self.NO['Campaign'],
                                          self.NO['Information']):
                print(self.URL_NO + ' works!')
            else:
                print(self.URL_NO + ' has no data!')
        elif country == 'FI':
            driver = scrape.selenium_site(self.URL_FI)
            self.FI['Package'] = self.package_names(driver)
            self.FI['Price'] = self.price_fi(driver)
            self.FI['Campaign'] = self.campaign_FI(driver)
            self.FI['Information'] = self.package_information_FI(driver)
            driver.close()
            # --- Error-hadling --- check all lists same length
            if scrape.check_lists_lengths(self.FI['Package'], self.FI['Price'], self.FI['Campaign'],
                                          self.FI['Information']):
                print(self.URL_FI + ' works!')
            else:
                print(self.URL_FI + ' has no data!')
        elif country == 'DK':  # DK
            driver = scrape.selenium_site(self.URL_DK)
            driver.execute_script("window.scrollTo(0, window.scrollY + 800)")
            self.DK['Package'] = self.package_names_SE_DK(driver)
            self.DK['Price'] = self.price_dk(driver)
            self.DK['Information'] = self.package_information_DK(driver)
            self.DK['Campaign'] =self.campaign_DK(self.URL_DK)
            driver.close()
            # --- Error-hadling --- check all lists same length
            if scrape.check_lists_lengths(self.DK['Package'], self.DK['Price'], self.DK['Campaign'],
                                          self.DK['Information']):
                print(self.URL_DK + ' works!')
            else:
                print(self.URL_DK + ' has no data!')


if __name__ == "__main__":
    viaplay = Viaplay()
    viaplay.create_objects_viaplay('NO')
    print(viaplay.NO)
