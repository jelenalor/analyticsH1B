from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time
import string
import json

""" Author Jelena Lor """

""" Constant variables """
url = "https://h1bdata.info/"

""" Support Function """


def scrap_data(url):
    try:
        browser = webdriver.Chrome(executable_path=r"chromedriver")
        # browser.set_page_load_timeout(30)
        browser.get(url)
        time.sleep(1)
        browser.delete_all_cookies()
        # Loop through employer search box in alphabetical order
        # to scrap data per employer name
        # Employer search box
        class_name = "//*[@id='employer']"
        employer_search_box = browser.find_element_by_xpath(class_name)
        list_of_companies = {}
        for letter in string.ascii_lowercase:
            print("Letter", letter)
            list_of_companies[letter] = []
            do = True
            while do:
                class_name = "//*[@id='employer']"
                employer_search_box = browser.find_element_by_xpath(class_name)
                employer_search_box.clear()
                employer_search_box.send_keys(letter)
                time.sleep(2)
                while True:
                    employer_search_box.send_keys(Keys.DOWN)
                    time.sleep(1)
                    element_attribute_value = employer_search_box.get_attribute('value')
                    if element_attribute_value not in list_of_companies[letter]:
                        list_of_companies[letter].append(element_attribute_value)
                        time.sleep(2)
                        continue
                    else:
                        do = False
                        break
        time.sleep(4)
        browser.quit()
        with open('data/list_of_companies.json', 'w') as fp:
            json.dump(list_of_companies, fp)
        print(list_of_companies)

    except Exception as e:
        print("Error occured", e)
        # browser.quit()

if __name__ == '__main__':
    scrap_data(url)
