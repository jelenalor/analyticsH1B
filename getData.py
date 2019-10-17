from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from optparse import OptionParser
from selenium.webdriver.common.action_chains import ActionChains

import numpy as np
import pandas as pd
import time
import string
import json

list_of_companies = []
with open("data/list_of_companies.json") as f:
    data = json.load(f)
    for k in data.keys():
        for i in data[k]:
            list_of_companies.append(i)

print(len(list_of_companies))

# if __name__ == '__main__':
#     scrap_data(url)
