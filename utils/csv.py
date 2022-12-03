""" CSV utils """
import csv
import pandas as pd

def create_address_metadata_csv(jsons):
    """ Generate address metadata csv with jsons data"""

    csv_columns = ['address', 'description', 'name']
    csv_file_name = "AddressMetaData.csv"
    try:
        with open(csv_file_name, 'w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
            writer.writeheader()
            for data in jsons:
                writer.writerow(data)
    except IOError:
        print("Failed to write to csv, exiting...")
        exit(1)

    # Convert csv file to dataframe to reformat as needed
    df = pd.read_csv('AddressMetaData.csv')
    df = df.drop("description", axis=1)
    df["chain"] = "ethereum"
    df.rename(columns={"name": "label"}, inplace=True)
    df.rename(columns={"address": "address1"}, inplace=True)
    df["address2"] = None
    df = df[['address1', 'address2', 'label', 'chain']]
    df.to_csv("AddressMetaData.csv")

def convert_csv_address_column_to_dict():
    with open('AddressMetaData.csv', mode='r') as csv_file:
        reader = csv.reader(csv_file)
        mydict = {}
        for rows in reader:
            mydict[rows[1]] = True

        return mydict

def add_uniswap_addresses_to_csv(unitswap_labels, uniswap_addresses):
    df = pd.read_csv('AddressMetaData.csv', index_col=0)

    for name, add in zip(unitswap_labels, uniswap_addresses):
        df = df.append({"address1": add[0], "address2": add[1], "label": name}, ignore_index=True)
        df["chain"] = "ethereum"

    df.to_csv('AddressMetaData.csv')