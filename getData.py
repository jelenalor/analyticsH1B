from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from optparse import OptionParser

import numpy as np
import pandas as pd
import time
import datetime
from datetime import timedelta


""" Author Jelena Lor """


""" Constant variables """
url = "https://h1bdata.info/"

""" Support Function """



def scrap_data(url):
    try:
        browser = webdriver.Chrome(executable_path=r"chromedriver")
        browser.get(url)
        time.sleep(10)
        browser.quit()

    except Exception as e:
        print("Error occured", e)
        # browser.quit()


if __name__ == '__main__':
    scrap_data(url)
