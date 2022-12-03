from os.path import exists
from utils import get_addresses_json_files, create_address_metadata_csv, get_uniswap_addresses, add_uniswap_addresses_to_csv


if not exists('AddressMetaData.csv'):
    
    # get jsons of addresses metadata
    addresses_json_files = get_addresses_json_files()

    # generate csv file and add the jsons metadata
    create_address_metadata_csv(addresses_json_files)

# add new uniswap addresses and label to the csv file

uniswap_labels, uniswap_addresses = get_uniswap_addresses()
add_uniswap_addresses_to_csv(uniswap_labels, uniswap_addresses)

