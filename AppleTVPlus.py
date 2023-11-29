# Importer
import time
import Scraper as scrape
import re
from collections import OrderedDict
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# Webscraping model
class AppleTVPlus:
    def __init__(self):
       self.URL_SE = "https://www.apple.com/se/apple-tv-plus/"
       self.URL_one_SE = "https://www.apple.com/se/apple-one/"
       self.URL_FI = "https://www.apple.com/fi/apple-tv-plus/"
       self.URL_one_FI = "https://www.apple.com/fi/apple-one/"
       self.URL_NO = "https://www.apple.com/no/apple-tv-plus/"
       self.URL_one_NO = "https://www.apple.com/no/apple-one/"
       self.URL_DK = "https://www.apple.com/dk/apple-tv-plus/"
       self.URL_one_DK = "https://www.apple.com/dk/apple-one/"
       self.SE = {'Package': [], 'ID':[101, 102, 103], 'Price': [], 'Campaign': [], 'Information': []}
       self.FI = {'Package': [], 'ID':[201, 202, 203], 'Price': [], 'Campaign': [], 'Information': []}
       self.NO = {'Package': [], 'ID':[301, 302, 303], 'Price': [], 'Campaign': [], 'Information': []}
       self.DK = {'Package': [], 'ID':[420, 421, 423], 'Price': [], 'Campaign': [], 'Information': []}


    # Method to scrape package name(s)
    def package_name(self, soup_apple, soup_apple_one):
        # Apple TV
        package_name_list = list()
        apple_TV = soup_apple.find("div", class_='ac-ln-title').text.strip().replace(u'\xa0',' ')
        package_name_list.append(apple_TV)
        apple_one =soup_apple_one.find("div", class_='ac-ln-title').text.strip().replace(u'\xa0',' ') + ' '
        apple_one_names = soup_apple_one.find_all('h3', class_='typography-plan-headline')
        apple_one_names = list(OrderedDict.fromkeys(apple_one_names))
        for i in apple_one_names:
            package_name_list.append(apple_one + i.text)
        package_name_list= list(OrderedDict.fromkeys(package_name_list))
        return package_name_list

    # Method to scrape price information
    def price(self, soup_apple, soup_apple_one):
        # Apple TV +
        price_information = soup_apple.find_all("h3", class_='typography-offer-headline')
        price_list = []
        for p in price_information:
            if re.search('[0-9]{2,3}', p.text):
                price = p.text.replace(u'\xa0', u' ').replace('\n', '').replace('\t', '').strip()
                price_list.append(price)

        # Apple One
        apple_one_price = soup_apple_one.find_all('p', {'class': ['plan-individual', 'typography-plan-subhead']})
        for price in apple_one_price:
            if re.search('[0-9]{2,3}', price.text):
                apple_one_price = price.text.replace(u'\xa0', u' ').replace('\n', '').replace('\t', '').strip()
                if apple_one_price not in price_list:
                    price_list.append(apple_one_price)

        return price_list

    # Method to scrape information about campaigns - SE
    def campaign_SE(self, soup_apple):
        # Apple TV+ and Apple One
        campaign_list = []
        campaign2 = soup_apple.find_all("h3", class_='typography-offer-headline')
        for i in campaign2:
            if re.search('gratis', i.text):
                campaign_list.append(i.text.replace(u'\xa0', u' '))
        campaign1 = soup_apple.find_all("h2", class_='typography-offer-eyebrow')
        for c in campaign1:
            campaign_list.append(c.text.replace(u'\xa0', u' '))
        campaign_list.append(campaign_list[2])
        campaign_list[0:2] = [' & '.join(campaign_list[0:2])]
        campaign_list[0:2] = [', '.join(campaign_list[0:2])]
        return campaign_list

    # Method to scrape information about campaigns - FI
    def campaign_FI(self, soup_apple):
        # Apple TV+ and Apple One
        campaign_list = []
        campaign2 = soup_apple.find_all("h3", class_='typography-offer-headline')
        for i in campaign2:
            if re.search('ilmaista', i.text):
                campaign_list.append(i.text.replace(u'\xa0', u' '))
        campaign1 = soup_apple.find_all("h2", class_='typography-offer-eyebrow')
        for c in campaign1:
            campaign_list.append(c.text.replace(u'\xa0', u' '))
        campaign_list.append(campaign_list[2])
        campaign_list[0:2] = [' & '.join(campaign_list[0:2])]
        campaign_list[0:2] = [', '.join(campaign_list[0:2])]
        return campaign_list

# Method to scrape information about campaigns - DK
    def campaign_DK(self, soup_apple):
        # Apple TV+ and Apple One
        campaign_list = []
        campaign2 = soup_apple.find_all("h3", class_='typography-offer-headline')
        for i in campaign2:
            if re.search('gratis', i.text):
                campaign_list.append(i.text.replace(u'\xa0', u' '))
        campaign1 = soup_apple.find_all("h2", class_='typography-offer-eyebrow')
        for c in campaign1:
            campaign_list.append(c.text.replace(u'\xa0', u' '))
        campaign_list.append(campaign_list[2])
        campaign_list[0:2] = [' & '.join(campaign_list[0:2])]
        campaign_list[0:2] = [', '.join(campaign_list[0:2])]
        return campaign_list

    # Method to scrape information about campaigns - NO
    def campaign_NO(self, soup_apple):
        # Apple TV+ and Apple One
        campaign_list = []
        campaign2 = soup_apple.find_all("h3", class_='typography-offer-headline')
        for i in campaign2:
            if re.search('gratis', i.text):
                campaign_list.append(i.text.replace(u'\xa0', u' '))
        campaign1 = soup_apple.find_all("h2", class_='typography-offer-eyebrow')
        for c in campaign1:
            campaign_list.append(c.text.replace(u'\xa0', u' '))
        campaign_list.append(campaign_list[2])
        campaign_list[0:2] = [' & '.join(campaign_list[0:2])]
        campaign_list[0:2] = [', '.join(campaign_list[0:2])]
        return campaign_list

    # Method to scrape information about the packages
    def information(self, soup_apple, soup_apple_one):
        # Informaiton from Apple One
        information_one = soup_apple_one.find_all('div', class_='typography-plan-copy')
        information_one_list = []
        for info in information_one:
            information_one_list.append(info.text.replace(u'\xa0', u' '))
        # Information from Apple TV+
        information = soup_apple.find_all('p', class_='offer-copy')
        information_list_TV_plus= []
        for i in information:
            information_list_TV_plus.append(i.text.replace(u'\xa0', u' '))
        information_list_TV_plus.append(information_list_TV_plus[2])
        # Combine the information to final output
        information_list = [str(information_list_TV_plus[0]+information_list_TV_plus[1]),
                            str(information_list_TV_plus[2] + information_one_list[0]),
                            str(information_list_TV_plus[2] + information_one_list[1])]
        return information_list

# Method to assign all scraped information to a dict
    def create_object(self, country):
        if country == 'SE':
            soup_apple = scrape.bs4_scrape(self.URL_SE)
            soup_apple_one = scrape.bs4_scrape(self.URL_one_SE)
            self.SE['Package'] = self.package_name(soup_apple, soup_apple_one)
            self.SE['Price'] = self.price(soup_apple, soup_apple_one)
            self.SE['Campaign'] = self.campaign_SE(soup_apple)
            self.SE['Information'] = self.information(soup_apple, soup_apple_one)
            # --- Error-hadling --- check all lists same length
            if scrape.check_lists_lengths(self.SE['Package'], self.SE['ID'], self.SE['Price'], self.SE['Campaign'],
                                          self.SE['Information']):
                print(self.URL_SE + ' works!')
            else:
                print(self.URL_SE + ' has no data!')
        elif country == 'FI':
            soup_apple = scrape.bs4_scrape(self.URL_FI)
            soup_apple_one = scrape.bs4_scrape(self.URL_one_FI)
            self.FI['Package'] = self.package_name(soup_apple, soup_apple_one)
            self.FI['Price'] = self.price(soup_apple, soup_apple_one)
            self.FI['Campaign'] = self.campaign_FI(soup_apple)
            self.FI['Information'] = self.information(soup_apple, soup_apple_one)
            # --- Error-hadling --- check all lists same length
            if scrape.check_lists_lengths(self.FI['Package'], self.FI['Price'], self.FI['Campaign'],
                                          self.FI['Information']):
                print(self.URL_FI + ' works!')
            else:
                print(self.URL_FI + ' has no data!')
        elif country == 'DK':
            soup_apple = scrape.bs4_scrape(self.URL_DK)
            soup_apple_one = scrape.bs4_scrape(self.URL_one_DK)
            self.DK['Package'] = self.package_name(soup_apple, soup_apple_one)
            self.DK['Price'] = self.price(soup_apple, soup_apple_one)
            self.DK['Campaign'] = self.campaign_DK(soup_apple)
            self.DK['Information'] = self.information(soup_apple, soup_apple_one)
            # --- Error-hadling --- check all lists same length
            if scrape.check_lists_lengths(self.DK['Package'], self.DK['Price'], self.DK['Campaign'],
                                          self.DK['Information']):
                print(self.URL_DK + ' works!')
            else:
                print(self.URL_DK + ' has no data!')
        elif country == 'NO':
            soup_apple = scrape.bs4_scrape(self.URL_NO)
            soup_apple_one = scrape.bs4_scrape(self.URL_one_NO)
            self.NO['Package'] = self.package_name(soup_apple, soup_apple_one)
            self.NO['Price'] = self.price(soup_apple, soup_apple_one)
            self.NO['Campaign'] = self.campaign_NO(soup_apple)
            self.NO['Information'] = self.information(soup_apple, soup_apple_one)
            # --- Error-handling --- check all lists same length
            if scrape.check_lists_lengths(self.NO['Package'], self.NO['Price'], self.NO['Campaign'],
                                          self.NO['Information']):
                print(self.URL_NO + ' works!')
            else:
                print(self.URL_NO + ' has no data!')

if __name__ == "__main__":
    apple_obj = AppleTVPlus()
    apple_obj.create_object('SE')
    #apple_obj.create_object('FI')
    #apple_obj.create_object('DK')
    #apple_obj.create_object('NO')
    print(apple_obj.SE)
    print(len(apple_obj.SE['Package']))
    print(len(apple_obj.SE['Price']))
    print(len(apple_obj.SE['Campaign']))
    print(len(apple_obj.SE['Information']))
   #print(apple_obj.FI)
    #print(apple_obj.DK)
   # print(apple_obj.NO)