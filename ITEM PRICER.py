from bs4 import BeautifulSoup
import requests
import numpy as np
import csv
from datetime import datetime

LINK = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p4432023.m570.l1311&_nkw=4090+rtx&_sacat=0"

def get_prices_by_link(link):
    r = requests.get(link)
    page_parse = BeautifulSoup(r.text, 'html.parser')
    # find all list items form search results
    search_results = page_parse.find("ul",{"class":"srp-results"}).find_all("li",{"class":"s-item"})

    item_prices =[]

    for result in search_results:
        price_as_text = result.find("span",{"class":"s-item__price"}).text
        if "to" in price_as_text:
            continue
        price = float(price_as_text[1:].replace(",",""))
        item_prices.append(price)
    return item_prices

def get_average(prices):
    return np.mean(prices)
    
# creates a new file to save the average of that days item
def save_to_file(prices):
    fields = [datetime.today().strftime("%B-%D-%Y"),np.around(get_average(prices),2)]
    with open('prices.csv.','a',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(fields)

if __name__ == "__main__":
    prices = (get_prices_by_link(LINK))
    save_to_file(prices)
