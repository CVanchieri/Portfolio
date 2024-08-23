---
layout: page
title:
image: 
nav-menu: false
description: null
show_tile: false

---

![CryptoTokenBanner](/assets/images/EtherscanAddressScraper/EtherscanScraperheader.png) <br>
## Scraping Etherscan.io for hash address information.

---

#### Necessary imports.
```
from bs4 import BeautifulSoup
import cloudscraper
import pandas as pd
import dateparser
from IPython.display import HTML
import time
from datetime import datetime
```

#### Step 1: Taking in a user input 'ETH hash address'and set up the CloudScraper.
```
print('--- Etherscan.io Scraper ---')
print("----------------")
user_input = input("Enter your 'Ether' wallet address ->: ")
user_input = user_input.replace(' ', '-')
user_input = user_input.replace(' ', '')

scraper = cloudscraper.create_scraper()
```
![EtherscanScraper1](/assets/images/EtherscanAddressScraper/Etherscan1.png) <br>
(Take the users input.)

#### Step 2: Use the scraper and user input to scrape the hash address overview.
```
start = datetime.now()

### hash overview scraper ###
print('>>> pulling hash address overview')
print("----------------")
url_main = scraper.get(f'https://etherscan.io/address/{user_input}')

hash_scan = BeautifulSoup(url_main.text, 'lxml')
hash_title = hash_scan.title.text.strip()
hash_title = hash_title.replace('Address', '')
hash_title = hash_title.replace(' | Etherscan', '')
input_hash = hash_title.strip()
hash_overview = {}
print("-- wallet overview --")
print("-- hash address --")
hash_overview['address'] = hash_title
print(hash_title)

# get hash eth balance
overview = hash_scan.find('div', class_='row mb-4')
body = overview.find('div', class_='card-body')
balance_eth = body.select_one('div:nth-child(1)')
hash_eth_balance = balance_eth.text
split_string = hash_eth_balance. split(":", 1)
eth_balance = split_string[1].strip()
print("-- eth balance --")
hash_overview['eth balance'] = eth_balance
print(f'{eth_balance}')

# get hash usd balance
balance_usd = body.select_one('div:nth-child(3)')
hash_usd_balance = balance_usd.text
split_string = hash_usd_balance. split(":", 1)
usd_balance = split_string[1].strip()
print("-- usd balance --")
hash_overview['usd balance'] = usd_balance
print(f'{usd_balance}')
print("----------------")

```
![EtherscanScraper1](/assets/images/EtherscanAddressScraper/Etherscan2.png) <br>
(An overview of the hash address.)

#### Step 3: Scrape all the held assets for the hash address.
```
print('>>> pulling wallet assets')
print("----------------")
nft_body = body.find('ul', class_='list list-unstyled mb-0')
nfts = {}
nft_count = 0
for li in nft_body.find_all('li'):
    for a in li.find_all('a'):
        nft = {}
        hash = a['href']
        new_hash = hash.replace('/token/', '')
        nft['hash'] = hash
        name_quantity = a.div.text
        split_string = name_quantity. split(")", 1)
        name = split_string[0]+')'
        nft['name'] = name
        quantity = ''.join(i for i in split_string[1] if i.isdigit())
        nft['quantity'] = quantity
        nft_count = nft_count + 1
        nfts[nft_count] = nft
```
```
df_nfts = pd.DataFrame.from_dict(nfts, orient='index')
usd_floor = []
eth_floor = []
token_type = []
supply = []
holders = []
print('*** 5s pause ***')
print("----------------")
time.sleep(5)
print('>>> pulling wallet assets information')
print('>>> takes a few seconds')
print("----------------")
```
```
for x in df_nfts.hash.values:
    token_url_main = scraper.get(f'https://etherscan.io{x}')
    time.sleep(1)

    # get wallet overview
    hash_scan = BeautifulSoup(token_url_main.text, 'lxml')
    hash_title = hash_scan.title.text
    
    # # get wallet balances
    token_overview = hash_scan.find('div', id='ContentPlaceHolder1_divSummary')
    token_card = token_overview.find('div', class_='card h-100')
    tokentype = token_card.find('h2', class_='card-header-title').span.text
    tokentype = tokentype.replace("[",'')
    tokentype = tokentype.replace("]",'')
    card_body = token_card.find('div', class_='card-body')
    if card_body.find('div', class_='col-12') is None:
        usd_floor.append(0)
        eth_floor.append(0)
        token_type.append(tokentype)

    else:
        token_floor = card_body.find('div', class_='col-12')
        price_floor = token_floor.find('span', class_='d-block').text #
        split_string = price_floor. split("@", 1)
        usd = split_string[0].strip()
        usdfloor = usd.replace("$", '')
        usdfloor = usdfloor.replace(",", '')
        eth = split_string[1].strip()
        ethsplit = eth.split(" ", 1)
        ethfloor = ethsplit[0].strip()
        usd_floor.append(usdfloor)
        eth_floor.append(ethfloor)
        token_type.append(tokentype)
```
```
    token_supply = card_body.find('div', class_='row align-items-center')
    total_supply = token_supply.find('div', class_='col-md-8 font-weight-medium').text #
    split_string = total_supply. split(" ", 1)
    total_supply = split_string[0].replace(",", '')
    total_supply = total_supply.replace(" ", '0')
    if '.' in total_supply:
        total_supply = total_supply[:total_supply.index('.')]
    else:
        total_supply = total_supply
        
    df_nfts['total_supply'] = total_supply
    token_holders = card_body.find('div', id='ContentPlaceHolder1_tr_tokenHolders')
    total_holders = token_holders.find('div', class_='col-md-8').text.strip() #
    if '(' in total_holders:
        total_holders = total_holders[:total_holders.index('(')].strip()
    else:
        total_holders = total_holders
    holders.append(total_holders)
    supply.append(total_supply)
```
```
df_nfts['usd_floor'] = usd_floor
df_nfts['eth_floor'] = eth_floor
df_nfts['supply'] = supply
df_nfts.supply = df_nfts.supply.replace(r'^\s*$', 0, regex=True)
df_nfts['holders'] = holders
df_nfts['type'] = token_type
df_nfts = df_nfts.drop(['hash'], axis=1)
df_nfts.usd_floor = df_nfts.usd_floor.astype(float)
df_nfts.eth_floor = df_nfts.eth_floor.astype(float)
df_nfts.quantity = df_nfts.quantity.astype(int)
df_nfts['usd_holding'] = df_nfts['quantity'] * df_nfts['usd_floor']
df_nfts['eth_holding'] = df_nfts['quantity'] * df_nfts['eth_floor']
eth_sum = df_nfts['eth_holding'].sum()
usd_sum = df_nfts['usd_holding'].sum()
nfts_table = HTML(df_nfts.to_html(classes='table table-striped'))
nft_types = []
for x in df_nfts.type.unique():
    nft_types.append(x) 
print('-- assets types --')    
print(nft_types)
print('-- eth total --')
print(f'{eth_sum} eth')
print('-- usd total --')
print(f'${usd_sum}')
print(df_nfts.head(50))
```
![EtherscanScraper1](/assets/images/EtherscanAddressScraper/Etherscan3.png) <br>
(All assets owned by the hash address.)

#### Step 4: Seperate the assets and information into a dictionary.
```
dict_types = {}
for x in nft_types:
    df_type = df_nfts[df_nfts['type'] == x]
    dict_types[x] = df_type
    
assets_type_values = {}
for k, v in dict_types.items():
    df = pd.DataFrame.from_dict(dict_types[k])
    df['usd_holding'] = df['quantity'] * df['usd_floor']
    df['eth_holding'] = df['quantity'] * df['eth_floor']
    eth_sum = df['eth_holding'].sum()
    usd_sum = df['usd_holding'].sum()
    assets_type_values[k] = [f'eth total:  {eth_sum}', f'usd total:  {usd_sum}']
    
for k, v in assets_type_values.items():
    print("----------------")
    print(f'-- {k} tokens --')
    v[0] = v[0].replace('eth total:  ', '')
    print(f'{v[0]} eth')
    v[1] = v[1].replace('usd total:  ', '')
    print(f'${v[1]}')
```
``` 
nfts_overview = {}
# nft_list = nft_types
nft_list = ['ERC-721'] # enter type of tokens wanted
nfttoken = df_nfts[df_nfts['type'].isin(nft_list)]
nft_eth_sum = nfttoken['eth_holding'].sum()
nfts_overview['eth total'] = nft_eth_sum
nft_usd_sum = nfttoken['usd_holding'].sum()
nfts_overview['usd total'] = nft_usd_sum
nfttoken = nfttoken.reset_index(drop=True)
index_list = [] # enter 'index' of unwanted assets
nfttoken = nfttoken.drop(index_list)
print("----------------")
print(f'-- {nft_list} assets --')
print('-- eth total --')
print(f'{nft_eth_sum} eth')
print('-- usd total --')
print(f'${nft_usd_sum}')
print(nfttoken.head(50))
print("----------------")

```
![EtherscanScraper1](/assets/images/EtherscanAddressScraper/Etherscan4.png) <br>
(Single out specific asset types, 'ERC-721'.)


#### Step 5: Scrape all the coins information from the hash address.
```
print('>>> pulling coins information')
url_tokens = scraper.get(f'https://etherscan.io/tokenholdings?a={input_hash}')

# if url_tokens.status_code == 200:
#     print("connected to page")
# else:
#     print("unable to fetch page")
# get token overview
token_scan = BeautifulSoup(url_tokens.text, 'lxml')
token_title = token_scan.title.text
# get token usd balance
tokens_overview = token_scan.find('div', class_='wrapper')
token_body = tokens_overview.find('main', id='content')
token_overview = token_body.find('div', class_='container space-bottom-2')
token_usd_networth = token_overview.find('div', class_='row mx-gutters-md-2').div
# get token assets
token_asssets_overview = token_overview.find('div', id='assets-wallet')
print("----------------")
print("-- coin assets --")
token_assets_total = token_asssets_overview.h2.text
print(token_assets_total)
# get token assets card
token_asssets_card = token_overview.find('div', class_='card')
token_asssets_table = token_asssets_card.find('table', id='mytable').tbody
tokens = {}
token_count = 0
for td in token_asssets_table.find_all('tr'):
    token = {}
    token_name = td.select_one('td:nth-child(2)', style='text').text
    token_quantity = td.select_one('td:nth-child(4)', style='text').text
    token['quantity'] = token_quantity
    token_price = td.select_one('td:nth-child(5)', style='text').text
    token['eth_price'] = token_price
    token_24change = td.select_one('td:nth-child(6)', style='text').text
    token['24r_change'] = token_24change
    token_usdvalue = td.select_one('td:nth-child(7)', style='text').text
    token['usd_value'] = token_usdvalue
    tokens[token_name] = token
    token_count = token_count + 1
df_coins = pd.DataFrame.from_dict(tokens, orient='index')
coins_table = HTML(df_coins.to_html(classes='table table-striped'))
```
```
coins_overview = {}
# get coins eth balance
token_eth_networth = token_overview.find('div', class_='col-md col-md-auto u-ver-divider u-ver-divider--left u-ver-divider--none-md mb-md-4').div
eth_networth_total = token_eth_networth.text
eth_total = eth_networth_total.strip()
print("-- eth total --")
coins_overview['eth_total'] = eth_total
print(f'{eth_total} eth')
# get coins usd balance
token_usd_networth_total = token_usd_networth.text
split_string = token_usd_networth_total. split("$", 1)
usd_networth_total = '$' + split_string[1]
usd_total = usd_networth_total.strip()
coins_overview['usd_total'] = usd_total
print("-- usd total --")
print(usd_total)
print(df_coins.head())
print("----------------")
```
![EtherscanScraper1](/assets/images/EtherscanAddressScraper/Etherscan5.png) <br>
(All the coins and tokens from the address.)


#### Step 6: Scrape all the transaction history, put into downloadable database.
```
page_count = 0
transaction_count = 0
transactions = {}
print('>>> pulling transactions information')
print("----------------")
while page_count >= 0:
    time.sleep(1)
    url_transactions = scraper.get(f'https://etherscan.io/txs?a={input_hash}&p={page_count}')

    # get transactions overview
    hash_transactions = BeautifulSoup(url_transactions.text, 'lxml')
    hash_transactions_overview = hash_transactions
    hash_transactions_title = hash_transactions_overview.title.text

    hash_transactions_card = hash_transactions.find('div', class_='container space-bottom-2')
    hash_transactions_list = hash_transactions_card.find('div', class_='card-body')
    hash_transactions_table = hash_transactions_list.find('tbody')
    nomore_alert = hash_transactions_table.find('div', class_='alert alert-warning mb-0')

    if nomore_alert is None:
        for td in hash_transactions_table.find_all('tr'):
            transaction = {}
            transaction_hash = td.select_one('td:nth-child(2)', style='text').text
            transaction['hash'] = transaction_hash
            transaction_method = td.select_one('td:nth-child(3)', style='text').text
            transaction['method'] = transaction_method
            transaction_block = td.select_one('td:nth-child(4)', style='text').text
            transaction['block'] = transaction_block
            transaction_age = td.select_one('td:nth-child(6)', style='text').text
            transaction['age'] = transaction_age
            transaction_from = td.select_one('td:nth-child(7)', style='text').text
            transaction['sender'] = transaction_from
            transaction_direction = td.select_one('td:nth-child(8)', style='text').text
            transaction['direction'] = transaction_direction
            transaction_to = td.select_one('td:nth-child(9)', style='text').text
            transaction['reciever'] = transaction_to
            transaction_ethvalue = td.select_one('td:nth-child(10)', style='text').text
            transaction['eth_value'] = transaction_ethvalue
            transaction_ethfee = td.select_one('td:nth-child(11)', style='text').text
            transaction['eth_fee'] = transaction_ethfee
            transactions[transaction_count] = transaction
            transaction_count = transaction_count + 1
        page_count = page_count + 1
    else:
        break
```
```
df_transactions = pd.DataFrame.from_dict(transactions, orient='index')

df_transactions.eth_value = df_transactions.eth_value.str.rstrip(' Ether')
df_transactions.hash = df_transactions.hash.astype(object)
df_transactions.method = df_transactions.method.astype(object)
df_transactions.block = df_transactions.block.astype(int)
df_transactions.age = df_transactions.age.astype(object)
df_transactions.sender = df_transactions.sender.astype(object)
df_transactions.direction = df_transactions.direction.astype(object)
df_transactions.reciever = df_transactions.reciever.astype(object)
df_transactions.eth_value = df_transactions.eth_value.astype(float)
df_transactions.eth_fee = df_transactions.eth_fee.astype(float)

trans_dates = []
for s in df_transactions.age:
    date = dateparser.parse(s).strftime("%Y-%m-%d") 
    trans_dates.append(date)
df_transactions['date'] = trans_dates
df_transactions = df_transactions.drop(columns='age')
df_transactions.direction = df_transactions.direction.replace('\xa0IN\xa0', 'IN')
trans_table = HTML(df_transactions.to_html(classes='table table-striped'))
print('-- all transactions --')
print(df_transactions.shape)
print(df_transactions.head())
print("----------------")
print(f'number of transaction pages #{page_count}')
print(f'number of transactions total #{transaction_count}')
print("----------------")
```
```
direct_out = df_transactions[df_transactions['direction'] == 'OUT']
direct_in = df_transactions[df_transactions['direction'] == 'IN']
direct_self = df_transactions[df_transactions['direction'] == 'SELF']
trans_direction = {}
print('-- transactions metrics --')
print('-- eth spent --')
trans_eth_spent = direct_out['eth_value'].sum()
trans_direction['eth_spent'] = trans_eth_spent
print(f'{trans_eth_spent} eth')
print('-- gas spent --')
trans_gas_spent = df_transactions.eth_fee.sum()
trans_direction['gas_spent'] = trans_gas_spent
print(f'{trans_gas_spent} eth')
print('-- eth purchased --')
trans_eth_purchased = direct_in['eth_value'].sum()
trans_direction['eth_purchased'] = trans_eth_purchased
print(f'{trans_eth_purchased} eth')
print("----------------")

df_transactions.to_csv('df_transactions.csv',index=False)
df_nfts.to_csv('df_nfts.csv',index=False)
```
![EtherscanScraper1](/assets/images/EtherscanAddressScraper/Etherscan6.png) <br>
(All the transactions from the hash address.)

#### Summary
This was a lot of fun for me, I have had interest in Crypto and NFTs for a while now, and more specifically with NFTs your information is stored in the blockchain but its not easily accessible and tough to make sense of.  This is the beginning to trying to help solve that problem, the goal is to pull all the information from the wallet address and create dataframes that make sense for those that are in need of this info for tax purposes.  A little ways to go but this was a great start and I have a more clear understanding of what needs to come next in the project.  Let me know what you think, give it a go.

Any suggestions or feedback is greatly appreciated, I am still learning and am always open to suggestions and comments.




[[Link to repo]](https://github.com/CVanchieri/EtherscanScraper)






---
[[<< Back]](https://cvanchieri.github.io/Portfolio/Tile1_Projects.html)
