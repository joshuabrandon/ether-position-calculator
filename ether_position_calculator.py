# Import packages

import pandas as pd
import urllib.request, json

# Powered by Etherscan.io APIs

def es_data(es_address, es_key):
    """ Pulls Ether balance from a specified address (es_address) using the Etherscan API. Requires a user-specific API key (es_key) """
    
    es_url = "https://api.etherscan.io/api?module=account&action=balance&address=%s&tag=latest&apikey=%s" % (es_address, es_key)
    with urllib.request.urlopen(es_url) as url:
        output = json.loads(url.read().decode())
    return output

# CoinMarketCap API call
# Powered by CoinMarketCap APIs

def cmc_data(cmc_key):
    """ Pulls Ether price information """
    
    cmc_url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol=ETH&convert=CAD&CMC_PRO_API_KEY=%s" % (cmc_key)
    with urllib.request.urlopen(cmc_url) as url:
        output = json.loads(url.read().decode())
    return output

# Get quantity of ETH held by specified address

def get_quantity():
    """ Returns the ETH balance of address from Etherscan """
    
    try:
        if int(es_output["status"]) != 1:
            raise ValueError("Error: API call was unsuccessful. Message: {}".format(es_output["message"]))
    except ValueError as ve:
        quantity = "Error"
        print(ve)
    else:
        quantity = float(es_output["result"]) / 1.0e18
    return quantity

# Get latest price and update time for ETH

def get_price_info():
    """ Returns the latest ETH price and the time the price was last updated """
    
    try:
        if int(cmc_output["status"]["error_code"]) != 0:
            raise ValueError("Error: API call was unsuccessful. Message: {}".format(cmc_output["status"]["error_message"]))
    except ValueError as ve:
        price = "Error"
        updated_time = "Error"
        print(ve)
    else:
        price = float(cmc_output["data"]["ETH"]["quote"]["CAD"]["price"])
        update_time = cmc_output["data"]["ETH"]["quote"]["CAD"]["last_updated"] 
    return (price, update_time)

# Calculate value of ETH holding

def holding_value(quantity, price):
    """ Calculates the dollar value of ETH position based on quantity and price """
    
    holding_value = round(quantity * price, 2)
    return holding_value

# Create DataFrame to be exported to Excel spreadsheet

def create_df():
    """ Creates a DataFrame with holding data """
    
    df = pd.DataFrame({"Symbol":cmc_output["data"]["ETH"]["symbol"],
                       "Quantity":quantity,
                       "Price":price,
                       "Value":holding_value
                      }, index=[update_time])
    return df

# Append DataFrame result to CSV

def df_to_csv(df):
    """ Append DataFrame to CSV """
    
    file_name = "output.csv"
    with open(file_name, "a") as f:
        df.to_csv(f, header=False)

# Run the code

es_address = input("EtherScan Address: ")
es_key = input("EtherScan API key: ")
cmc_key = input("CoinMarketCap API key: ")

es_output = es_data(es_address, es_key)
cmc_output = cmc_data(cmc_key)

quantity = get_quantity()
price, update_time = get_price_info()
holding_value = holding_value(quantity, price)

df = create_df()
df_to_csv(df)