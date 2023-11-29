# Importer
import Scraper as scrape
import time

# Webscraping model
class YouSee_DK:
    def __init__(self):
        self.URL_DK = "https://yousee.dk/play/?icid=fp_HB_No_Salg_Tv_YouseePlay_YouseePlay_None_u3922#forside"
        self.DK = {'Package': [], 'ID':[434, 435, 436, 437, 438], 'Price': [], 'Campaign': [], 'Information': []}

# Method to scrape package name(s)
    def package_name(self, driver):
        YouSee_play = driver.find_element(scrape.By.CSS_SELECTOR, 'h2.image-box__aligned-title.image-box__aligned-title--hero').text + ' '
        package_list = [YouSee_play + i.text.replace('\n', ' ') for i in driver.find_elements(scrape.By.CSS_SELECTOR, 'div header.product-bs3-card__header h3.product-bs3-card__title')]
        return package_list

# Method to scrape price information
    def price(self, driver):
        price_list = [i.text for i in driver.find_elements(scrape.By.CSS_SELECTOR, 'h3.product-bs3-card__price')]
        return price_list

# Method to scrape information about campaigns
    # No campaigns at the moment
    def campaign(self, driver):
        campaign_list = ['' for i in range(len(self.package_name(driver)))]
        return campaign_list

# Method to scrape information about the packages
    def information(self, driver):
        information_list = [i.text.replace('\n', ' ') + '\n' + driver.find_element(scrape.By.CSS_SELECTOR, 'h3.product-bs3-overview__subtitle').text for i in driver.find_elements(scrape.By.CSS_SELECTOR, 'div header.product-bs3-card__header h3.product-bs3-card__title')]
        return information_list

# Method to assign all scraped information to a dict
    def create_object(self):
        driver = scrape.selenium_site(self.URL_DK)
        time.sleep(3)
        driver.find_element(scrape.By.ID, 'acceptButton').click()
        driver.execute_script("window.scrollTo(0, window.scrollY + 500)")
        self.DK['Package'] = self.package_name(driver)
        self.DK['Price'] = self.price(driver)
        self.DK['Campaign'] = self.campaign(driver)
        self.DK['Information'] = self.information(driver)
        driver.close()
        # --- Error-handling --- check all lists same length
        if scrape.check_lists_lengths(self.DK['Package'], self.DK['Price'], self.DK['Campaign'],
                                      self.DK['Information']):
            print(self.URL_DK + ' works!')
        else:
            print(self.URL_DK + ' has no data!')

if __name__ == "__main__":
   YouSee_DK_obj = YouSee_DK()
   YouSee_DK_obj.create_object()
   print(YouSee_DK_obj.DK)