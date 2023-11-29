# Importer
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait


# Selenium webscraping
def selenium_site(webpage):
    # service = Service(executable_path=r'chromedriver.exe')
   
    options = Options()
    options.headless = False
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(
        #service=service,
        options=options)
    driver.get(webpage)
    driver.maximize_window()
    WebDriverWait(driver, 8)
    return driver

# BeautifulSoup
# bs4 Webscraping
def bs4_scrape(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup

# A helper function to create a class filter for scraping
def create_filter(tag_name, class_list):
    def class_filter(tag):
        return (
            tag.name == tag_name and
         set(tag.get('class', [])) == set(class_list)
        )
    return class_filter

# ----- HELP FUNCTIONS -----
# Function to convert
def listToString(s):
    # initialize an empty string
    str1 = " "
    # return string
    return (str1.join(s))

# Function to convert
def listToString2(s):
    # initialize an empty string
    str1 = "\n "
    # return string
    return (str1.join(s))

# Check length of list
def check_lists_lengths(*lists):
    non_empty_lists = []
    empty_lists = []

    # Check if all lists have the same length
    lengths = set(len(lst) for lst in lists)
    if len(lengths) > 1:
        print("Not all lists have the same length.")
        return False

    for lst in lists:
        if len(lst) > 0:
            non_empty_lists.append(lst)
        else:
            empty_lists.append(lst)

    if len(non_empty_lists) == len(lists):
        print("All lists have elements.")
        return True
    elif len(empty_lists) == len(lists):
        print("All lists are empty.")
        return False
    else:
        print("Some lists are empty.")
        return False


# --- HELP FUNCTIONS ---
def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)

def has_numbers_check(inputString):
    if any(char.isdigit() for char in inputString):
        return True
    else:
        return False

def has_letters(inputString):
    return any(char.isalpha() for char in inputString)

# Python3 code to remove whitespace
def remove(string):
    return string.replace(" ", "").replace('\n', "")