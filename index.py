import pandas as pd


""" Data -> was scraped for 2019 but as it turns out when request was made for 
the company that did not have any visa applications in 2019 - the code automatically 
scrapped the data for 2018 (or the last available data for that company) """
""" this is likely to impact only small companies, and therefore here we only analyse the
results from 2019 """
""" Future project ideas -> to scrap outstanding data and compare which companies/industries apply and get visa
e.g. how random is the random lottery """

df = pd.read_csv(r"data/h1b2019.csv")

print(df.head(5))