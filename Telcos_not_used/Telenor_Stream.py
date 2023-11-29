# Importer
import Scraper as scrape
import time

# Webscraping model - Telenor Stream SE
class Telenor_Stream_SE:
    def __init__(self):
        self.URL = "https://www.telenor.se/handla/stream/#paket"
        self.SE = {'Package': [], 'Price': [], 'Campaign': [], 'Information': []}

# Method to scrape all information including:
    # Package names
    # Prices
    # Campaigns
    # Information
    def scrape_information(self):
        Telenor = str(self.URL.split(".")[1]).capitalize() + ' '
        package_list = []
        price_list = []
        campaign_list = []
        information_list = []
        driver = scrape.selenium_site(self.URL)
        #driver.find_element_by_id('onetrust-accept-btn-handler').click()
        time.sleep(3)
        driver.execute_script("window.scrollTo(0, window.scrollY + 300)")
        package_information = driver.find_elements_by_css_selector('div.image-with-text-block__text__heading h2 span.font-h2')
        price_information = driver.find_elements_by_css_selector('div.image-with-text-block__text__body.tnse-editorial.trailer p')
        campaign_information = driver.find_elements_by_css_selector('div.image-with-text-block__text__body.tnse-editorial.trailer ul li:nth-of-type(2')
        information = driver.find_elements_by_css_selector('div#imageWithTextBlockText div.image-with-text-block__text__body.tnse-editorial.trailer ul')
        for name in package_information:
            package_list.append(Telenor + name.text)
        for price, campaign in zip(price_information, campaign_information):
            if price.text[0:3].isdigit():
                print(price.text)
                price_list.append(price.text[0:3] + 'kr/mån')
                if len(price.text[4:])<12 and 'priset' in campaign.text:
                    campaign_list.append(price.text[4:] + ' ' + campaign.text)
                else:
                    campaign_list.append(price.text[4:])
            elif scrape.has_numbers(price.text):
                price_list.append(price.text)
                campaign_list.append('')
        for i in information:
            information_list.append(i.text)
        driver.close()
        return package_list, price_list, campaign_list, information_list[:len(package_list)]

# Method to assign all scraped information to a dict
    def create_object(self):
        self.SE['Package'], self.SE['Price'], self.SE['Campaign'], self.SE['Information'] = self.scrape_information()

if __name__ == "__main__":
   Telenor_Stream_SE_obj = Telenor_Stream_SE()
   Telenor_Stream_SE_obj.create_object()
   print(Telenor_Stream_SE_obj.SE)
   print(len(Telenor_Stream_SE_obj.SE['Price']))
   print(len(Telenor_Stream_SE_obj.SE['Campaign']))
   print(len(Telenor_Stream_SE_obj.SE['Package']))
   print(len(Telenor_Stream_SE_obj.SE['Information']))