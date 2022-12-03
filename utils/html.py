""" HTML utils """
import constants as consts
import json
from bs4 import BeautifulSoup
import requests
from utils import csv

def fetch_html(url):
    """ fetch the html from url """
    reqs = requests.get(url)

    if reqs.status_code != 200:
        print("cant find url!")
        exit(1)

    return reqs.text

def get_html_parser(html):
    """ return html parser """
    return BeautifulSoup(html, 'html.parser')


def get_addresses_json_files():
    """ fetch addresses metadata html, extract links from html and return in json format """

    html = fetch_html(consts.ADDS_URL)
    soup = get_html_parser(html)

    links = []
    # Push all relevant addresses hrefs to links list
    [links.append(link.get('href')) for link in soup.findAll(class_='js-navigation-open Link--primary')]
        
    addresses_json_data = []

    for i in range(len(links)):
        full_url = consts.RAW_BASE_URL + links[i].replace('/blob', "")
        response = requests.get(full_url)
        data = json.loads(response.text)
        addresses_json_data.append(data)

    return addresses_json_data


def get_uniswap_addresses():
    """ Returns tupple of new uniswap labels and addresses """
    html = fetch_html(consts.UNISWAP_URL)
    soup = get_html_parser(html)

    uniswap_addresses_table = soup.find('table')
    uniswap_labels = []
    uniswap_addresses = []

    address_from_csv_dict = csv.convert_csv_address_column_to_dict()

    for address in uniswap_addresses_table.find_all('tbody'):
        rows = address.find_all('tr')
        for row in rows:
            val = (row.findAll('code'))
            if (not val[0].get_text() in address_from_csv_dict) and (not val[1].get_text() in address_from_csv_dict):
                uniswap_addresses.append([val[0].get_text(), val[1].get_text()])
                uniswap_labels.append(row.find('a').text)

    return uniswap_labels, uniswap_addresses
