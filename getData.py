import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

""" Load a list of companies """
""" This list was scarped using Selenium """
""" The code is in getDataCompanies.py """

list_of_companies = []
with open("data/list_of_companies.json") as f:
    data = json.load(f)
    for k in data.keys():
        for i in data[k]:
            list_of_companies.append(i)


""" We store our scrapped data in dictionary """

my_dict = {"company": [],
           "job_title": [],
           "base_salary": [],
           "location": [],
           "submit_date": [],
           "start_date": [],
           "status": []}


""" Iterate over each company name from the list """
""" Find url for the company data """
""" I found that url changes each time there is a new company, 
which triggered me to use Requests (its is also faster) """
""" Apply Beautiful soup to look for tags and id to get the relevant data """
"""" The data is massive to it is likely to run into memory issues
that's why I break down into chunks, save and clear the df"""
""" I later accumulate all chunks into one df, which is having around 1m134k rows """

doc_counter = 7
COMPS = list_of_companies[800:]
for ind, i in enumerate(COMPS):
    try:
        url = "https://h1bdata.info/index.php?em={}&job=&city=&year=2019".format("+".join(i.split()))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find(id="myTable")
        for line in table.tbody.find_all("tr"):
            my_dict["company"].append(line.find_all("td")[0].string)
            my_dict["job_title"].append(line.find_all("td")[1].string)
            my_dict["base_salary"].append(line.find_all("td")[2].string)
            my_dict["location"].append(line.find_all("td")[3].string)
            my_dict["submit_date"].append(line.find_all("td")[4].string)
            my_dict["start_date"].append(line.find_all("td")[5].string)
            my_dict["status"].append(line.find_all("td")[6].string)

        # Built a print out checker - prints when we process new 50 companies
        if ind % 50 == 0:
            print(ind)
            time.sleep(200)

        # save and clear my_dict at every 100th company
        if ind % 100 == 0:
            """ Move the data from dict to dataframe and save in the 'data' folder """
            df = pd.DataFrame(my_dict)
            df.to_csv("data/h1b_data{}.csv".format(doc_counter), index=False)
            print("saved {}".format(doc_counter))
            doc_counter += 1
            # clear up memory
            del df
            del my_dict
            # create new instance of my_dict
            my_dict = {"company": [],
                       "job_title": [],
                       "base_salary": [],
                       "location": [],
                       "submit_date": [],
                       "start_date": [],
                       "status": []}
            time.sleep(500)

        # last round
        elif ind == len(COMPS)-1:
            df = pd.DataFrame(my_dict)
            df.to_csv("data/h1b_data{}.csv".format(doc_counter), index=False)
            print("saved {}".format(doc_counter))

    except Exception as e:
        print(e)