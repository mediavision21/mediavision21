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
        package_list = []
        information_list = []
        campaign_list = []
        price_list = []
       
        driver = scrape.selenium_site(self.URL)
        time.sleep(2)
        # Accept button
        driver.find_elements(scrape.By.XPATH, "//span[text()='Accept all']/ancestor::button")[0].click()
        time.sleep(5)

        driver.find_elements(scrape.By.XPATH, "//a[text()='family or student plan']")[0].click()

        try: 
            # Scrapes parent elements
            individual = driver.find_element(scrape.By.XPATH, '//*[@id="yt-option-selection-flow-step-renderer"]/div[2]/ytm-option-item-renderer/div[2]').text
            family = driver.find_element(scrape.By.XPATH, '//*[@id="yt-option-selection-flow-step-renderer"]/div[3]/ytm-option-item-renderer/div[2]').text
            student = driver.find_element(scrape.By.XPATH, '//*[@id="yt-option-selection-flow-step-renderer"]/div[4]/ytm-option-item-renderer/div[2]').text
            
            #  Scrapes all the Package names
            individual_package = "individual"
            family_package = family.split("\n")[0] 
            student_package = student.split("\n")[0]
            package_list = [Youtube + ' '+ Premium + ' ' + individual_package, Youtube + ' '+ Premium + ' '+family_package, Youtube+ ' '+ Premium + ' ' + student_package]

            # Gets all the price information
        
            price_premium_individual = re.findall(r'\d+', individual)[1]
            price_premium_family = re.findall(r'\d+', family)[1]
            price_premium_student = re.findall(r'\d+', student)[1]
            price_list = [price_premium_individual, price_premium_family, price_premium_student]
    

            # Campaigns
            
            campaign_list = [" ".join(individual.split("\n")[0:2]) for i in range(0, 3)]
            

            # Scrapes all the information about the packages
            
            information_premium_individual = " ".join(individual.split("•")[1:])
            information_premium_family = " ".join(family.split("•")[1:])
            information_premium_student = " ".join(student.split("•")[1:])
            information_list = [information_premium_individual, information_premium_family,
                                information_premium_student]
            
                
        except selenium.common.exceptions.NoSuchElementException:
            # Youtube premium has two layouts, this block handles the second layout

            # Indivdual 
            individual = driver.find_element(scrape.By.CSS_SELECTOR, "yt-formatted-string.metadata-item").text
            package_list.append(Youtube + " " + Premium + " individual")
            campaign_list = 3* [individual.split("•")[0]]
            price_list.append(re.findall(r"\d+.\d+", individual)[0])
            information_list.append("")

            # Family
            family = driver.find_element(scrape.By.CSS_SELECTOR, "div#yt-unlimited-metadata").text
            package_list.append(Youtube + " " + Premium + " " + family.split("•")[0])
            price_list.append(re.findall(r"\d+.\d+", family)[0])
            information_list.append(family)

            # Student 
            student = driver.find_elements(scrape.By.CSS_SELECTOR, "div#yt-unlimited-metadata")[1].text
            package_list.append(Youtube + " " + Premium + " " + student.split("•")[0])
            price_list.append(re.findall(r"\d+.\d+", student)[0])
            information_list.append(student)


        driver.close()
        self.SE['Information'] = information_list
        self.SE['Campaign'] = campaign_list
        self.SE['Price'] = price_list
        self.SE['Package'] = package_list


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