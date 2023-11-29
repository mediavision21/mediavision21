# Importer
import time
import re
import Scraper as scrape
import selenium

# Webscraping Youtube
class YoutubePremium_SE:
    def __init__(self):
        self.URL = 'https://www.youtube.com/premium/offers?app=desktop&ybp=OgIIAUoNCAYSCXVubGltaXRlZHosGAIiDQgGEgl1bmxpbWl0ZWQiFAgGEhB1bmxpbWl0ZWQtQi1ydWJ5KgMBAgM%253D'
        self.URL_enskild = 'https://www.youtube.com/premium/offers?ybp=OgIIAUoNCAYSCXVubGltaXRlZHosGAIiDQgGEgl1bmxpbWl0ZWQiFAgGEhB1bmxpbWl0ZWQtQi1ydWJ5KgMBAgOSARcYASITNjYwMTg2OTAyMzc1MzIwNjgxNQ%253D%253D'
        self.URL_family = 'https://www.youtube.com/premium/family?ybp=IgoIBBIGZmFtaWx5OgIIAUoNCAYSCXVubGltaXRlZA%253D%253D'
        self.SE = {'Package': [], 'ID':[131, 132, 133], 'Price': [], 'Campaign': [], 'Information': []}


# Method to scrape all information
    def scrape_all(self):
        Youtube = str(self.URL.split(".")[1].capitalize())
        Premium = str(self.URL.split("/")[3].capitalize())
       
        driver = scrape.selenium_site(self.URL)
        time.sleep(2)
        # Accept button
        driver.find_elements(scrape.By.XPATH, "//span[text()='Accept all']/ancestor::button")[0].click()
        time.sleep(5)

        driver.find_elements(scrape.By.XPATH, "//a[text()='family or student plan']")[0].click()

        # Scrapes parent elements
        individual = driver.find_element(scrape.By.XPATH, '//*[@id="yt-option-selection-flow-step-renderer"]/div[2]/ytm-option-item-renderer/div[2]').text
        family = driver.find_element(scrape.By.XPATH, '//*[@id="yt-option-selection-flow-step-renderer"]/div[3]/ytm-option-item-renderer/div[2]').text
        student = driver.find_element(scrape.By.XPATH, '//*[@id="yt-option-selection-flow-step-renderer"]/div[4]/ytm-option-item-renderer/div[2]').text
        
        #  Scrapes all the Package names
        individual_package = "individual"
        family_package = family.split("\n")[0] 
        student_package = student.split("\n")[0]
        package_list = [Youtube + ' '+ Premium + ' ' + individual_package, Youtube + ' '+ Premium + ' '+family_package, Youtube+ ' '+ Premium + ' ' + student_package]
        self.SE['Package'] = package_list


        # Gets all the price information
    
        price_premium_individual = re.findall(r'\d+', individual)[1]
        price_premium_family = re.findall(r'\d+', family)[1]
        price_premium_student = re.findall(r'\d+', student)[1]
        price_list = [price_premium_individual, price_premium_family, price_premium_student]
        self.SE['Price'] = price_list

        # Campaigns
        
        campaign_list = [" ".join(individual.split("\n")[0:2]) for i in range(0, 3)]
        self.SE['Campaign'] = campaign_list

        # Scrapes all the information about the packages
        
        information_premium_individual = " ".join(individual.split("•")[1:])
        information_premium_family = " ".join(family.split("•")[1:])
        information_premium_student = " ".join(student.split("•")[1:])
        information_list = [information_premium_individual, information_premium_family,
                            information_premium_student]
        self.SE['Information'] = information_list
        driver.close()
            
        # --- Error-hadling --- check all lists same length
        if scrape.check_lists_lengths(package_list, price_list, campaign_list,
                                      information_list):
            print(Youtube + ' works!')
        else:
            print(Youtube + ' has no data!')
        return package_list, price_list, campaign_list, information_list

if __name__ == "__main__":
   YoutubePremium_SE_obj = YoutubePremium_SE()
   print(YoutubePremium_SE_obj.scrape_all())
   print(YoutubePremium_SE_obj.SE)