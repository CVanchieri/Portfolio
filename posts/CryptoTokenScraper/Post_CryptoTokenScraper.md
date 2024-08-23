---
layout: page
title:
image: 
nav-menu: false
description: null
show_tile: false

---

![CryptoTokenBanner](/assets/images/CryptoTokenScraper/CryptoBanner.jpeg) <br>
## Scraping websites and pulling data from APIs to gather crypto token information.

---

#### Necessary imports.
```
import os
import pandas
import psycopg2
import requests
from datetime import datetime, timedelta
import re
from bs4 import BeautifulSoup
import tweepy
```

#### Step 1: Scraping newly released tokens from the CoinMarketCap website.
```
start = datetime.now()
source_new = requests.get(f'https://coinmarketcap.com/new/').text
soup_4 = BeautifulSoup(source_new, 'lxml')
card_5 = soup_4.find('tbody')
print('--- New Release Tokens ---')
new_tokens = {}
for td in card_5.find_all('tr')[0:10]:
    token = {}
    new_num = td.select_one('td:nth-child(2)', style='text').text
    new_name = td.select_one('td:nth-child(3)', style='text').a.div.div.p.text
    token['name'] = new_name
    new_symbol = td.select_one('td:nth-child(3)', style='text').a.div.div.div.p.text
    token['symbol'] = new_symbol
    new_img = td.select_one('td:nth-child(3)', style='text').a.div.img['src']
    token['image'] = new_img
    new_release = td.select_one('td:nth-child(10)', style='text').text
    token['release date'] = new_release
    new_price = td.select_one('td:nth-child(4)', style='text').text
    token['price'] = new_price
    new_change1hr = td.select_one('td:nth-child(5)', style='text').span.text
    token['change 1hr'] = new_change1hr
    new_change24hr = td.select_one('td:nth-child(6)', style='text').span.text
    token['change 24hr'] = new_change24hr
    new_volume = td.select_one('td:nth-child(8)', style='text').text
    token['volume'] = new_volume
    new_chain = td.select_one('td:nth-child(9)', style='text').div.text
    token['blockchain'] = new_chain
    cmc_url = td.select_one('td:nth-child(3)', style='text').a['href']
    token['cmc url'] = 'https://coinmarketcap.com' + cmc_url
    new_tokens[new_num] = token
```
![CryptoToken1](/assets/images/CryptoTokenScraper/crypto1.png) <br>
(Newly released tokens.)

#### Step 2: Take a user input and gather token info from the CoinMarketCap API.
```
user_input = input ("Enter the token name:")
```
```
x_query = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
x_latest = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
x_meta = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/info'
apikey = os.getenv("CMC_APIKEY")
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY' : apikey,
    }
params = {
    'symbol' : user_input,
    }
```
```
source_stats = requests.get(x_query, params=params , headers=headers).json()
coins_stats = source_stats['data']
token_info = {}
for key, value in coins_stats.items():
    name = value['name']
    token_info['name'] = name
    symbol = value['symbol']
    token_info['symbol'] = symbol
    slug = value['slug']
    token_info['slug'] = slug
    date_added = value['date_added'][:10]
    token_info['date added'] = date_added
    is_active = value['is_active']
    if is_active != 1:
        token_info['active'] = 'no'
    else:
        token_info['active'] = 'yes'
    total_supply = value['total_supply']
    token_info['total supply'] = "{:,}".format(total_supply)
    circulating_supply = value['circulating_supply']
    token_info['circulating supply'] = "{:,}".format(circulating_supply)
    market_cap = value['quote']['USD']['market_cap']        
    token_info['market cap'] = "{:,}".format(market_cap)
    price = value['quote']['USD']['price']
    token_info['price'] = "{:,}".format(price)
    volume_24h = value['quote']['USD']['volume_24h']
    token_info['volume'] = "{:,}".format(volume_24h)
    change_1h = value['quote']['USD']['percent_change_1h']
    token_info['change 1hr'] = "{:,}".format(change_1h)
    change_24h = value['quote']['USD']['percent_change_24h']
    token_info['change 24hr'] = "{:,}".format(change_24h)
    change_7d = value['quote']['USD']['percent_change_7d']
    token_info['change 7d'] = "{:,}".format(change_7d)
    change_30d = value['quote']['USD']['percent_change_30d']
    token_info['change 30d'] = "{:,}".format(change_30d)
    change_60d = value['quote']['USD']['percent_change_60d']
    token_info['change 60d'] = "{:,}".format(change_60d)
    change_90d = value['quote']['USD']['percent_change_90d']
    token_info['change 90d'] = "{:,}".format(change_90d)
```
```
    source_urls = requests.get(x_meta, params=params , headers=headers).json()
    coins_urls = source_urls['data']
    token_urls = []
    for key, value2 in coins_urls.items():
        if value['name'] == value2['name']:
            logo = value2['logo']
            for x in value2['urls']['explorer']:
                token_urls.append(x)
    token_info['source urls'] = token_urls
```
#### Step 3: Scrape the CoinMarketCap website for more token stats information.
```
    url_name = name.replace(' ', '-')
    source_stats2 = requests.get(f'https://coinmarketcap.com/currencies/{url_name}').text
    coin_stats2 = BeautifulSoup(source_stats2, 'lxml')
    coin_scrape_stats = coin_stats2.find('div', class_='sc-16r8icm-0 jIZLYs container___E9axz')
    if coin_scrape_stats != None:
        body = coin_scrape_stats.find('tbody')
        chang24r = body.select_one('tr:nth-child(3)')
        chang24r_numbers = chang24r.td.text
        token_info['24hr low / high'] = chang24r_numbers
        market_dominance = body.select_one('tr:nth-child(6)')
        market_dominance_numbers = market_dominance.td.text
        token_info['market dominance'] = market_dominance_numbers
```
``` 
    token_hash = []
    hash_url = []
    platform = []
    source_hash = requests.get(f'https://coinmarketcap.com/currencies/{url_name}').text
    coins_hash = BeautifulSoup(source_hash, 'lxml')
    for head in coins_hash.find_all('div', class_='sc-16r8icm-0 dOJIkS container___2dCiP contractsRow'):
        if 'Con' in head.div.text:
            content = head.find('div', class_= 'content___MhX1h')
            thash = content.div.a['href']
            hash_url.append(thash)
            plat  = content.div.a.span.text
            platform.append(plat)
            if 'Eth' in plat:
                token_hash.append(thash[27:])
            else:
                token_hash.append(thash[26:])
    if len(token_hash) == 0:
        token_info['hash'] = 'No data'
        token_info['hash_url'] = 'No data'
        token_info['platform'] = 'No data'
    else:
        token_info['hash'] = token_hash[0]
        token_info['hash_url'] = hash_url[0]
        token_info['platform'] = platform[0]
        
    token_description = []
    if coins_hash.find_all('div', class_='sc-1lt0cju-0 srvSa') != None:
        for desc in coins_hash.find_all('div', class_='sc-1lt0cju-0 srvSa'):
                des = desc.div
                if des != None:
                    token_description.append(des.text)
        if len(token_description) > 0:
            token_info['description'] = token_description[0]
```
![CryptoToken2](/assets/images/CryptoTokenScraper/crypto2.png) <br>
(Token stats.)

#### Step 4: If the token is on the Binance Smart Chain, scrape the bscscan website for holders information.
```
token_holder_info = {}
top_holders = {}
if 'bsc' in token_info['hash_url']:
    source_info = requests.get(f'https://bscscan.com/token/{token_info["hash"]}').text
    source_holders = requests.get(f'https://bscscan.com/token/tokenholderchart/{token_info["hash"]}').text
    source_description = requests.get(f'https://bscscan.com/token/{token_info["hash"]}#tokenInfo').text
    soup_1 = BeautifulSoup(source_info, 'lxml')
    soup_2 = BeautifulSoup(source_holders, 'lxml')
    soup_3 = BeautifulSoup(source_description, 'lxml')
    overview = soup_1.find('div', class_='row mb-4')
    card_4 = soup_3.find('div', id='ContentPlaceHolder1_maintab')
    token = overview.find('div', class_='font-weight-medium').b.text
    description = card_4.find('div', id='tokenInfo').div.text
    description = description.split('MarketVolume', 1)
    description = description[0]
    description = description[9:]
    supply = overview.find('span', class_='hash-tag text-truncate').text
    c_supply = overview.find('span', class_='text-secondary ml-1').text
    num_holders = overview.find('div', class_='mr-3').text
    num_holders = num_holders[1:-3]
```
```
    url = []
    for card in soup_1.find_all('div', class_='col-md-6'):
        if card.find('h2', class_='card-header-title') != None and card.find('div', class_='col-md-4').text == 'Contract:':
            contract = card.find('a', class_='text-truncate d-block mr-2').text
            url_t = card.find('div', id='ContentPlaceHolder1_tr_officialsite_1')
            url_t = url_t.find('div', class_='col-md-8').a['href']
            url.append(url_t)

    card_2 = soup_2.find('div', id='ContentPlaceHolder1_resultrows')
    ta = soup_2.find('div', class_='mb-0').p.text[1:-1]
    ta = ta.replace('token', 'tokens')
    desc_1 = ta.replace('tokenss', 'tokens')
    card_3 = soup_2.find('div', class_='card-header py-4')
    token_holder_info[token] = [num_holders, url[0], description, desc_1]

    for addre in card_2.find_all('tr')[:6]:
        rank = []
        holder = []
        hash = []
        holder_hash = []
        holder_hash_url = []
        exchange = []
        quantity = []
        percentage = []

        if addre.select_one('td:nth-child(1)') != None:
            rank.append(addre.select_one('td:nth-child(1)').contents[0])
            holder_name = addre.select_one('td:nth-child(2)').span
            hash_t = holder_name.a['href']
            hash.append(re.sub(r'^.*?=', '=', hash_t))
            holder_hash_t = hash[0][1:]
            holder_hash.append(holder_hash_t)
            holder_hash_url.append('https://bscscan.com/address/' + holder_hash[0])

            if ': ' in holder_name.a.text:
                exch, nam = holder_name.a.text.split(':')
                exchange.append(exch)
                holder.append(nam)
                quant = addre.select_one('td:nth-child(3)').contents[0]
                quantity.append(quant)
                perc = addre.select_one('td:nth-child(4)').contents[0]
                percentage.append(perc)

                top_holders[rank[0]] = [holder[0], holder_hash[0], holder_hash_url[0], quantity[0], percentage[0], exchange[0]]
            else:
                no_exchange = 'Exchange: Missing'
                exchange.append(no_exchange)
                nam = holder_name.a.text
                holder.append(nam)
                quant = addre.select_one('td:nth-child(3)').contents[0]
                quantity.append(quant)
                perc = addre.select_one('td:nth-child(4)').contents[0]
                percentage.append(perc)
                
                top_holders[rank[0]] = [holder[0], holder_hash[0], holder_hash_url[0], quantity[0], percentage[0], exchange[0]]
```
![CryptoToken3](/assets/images/CryptoTokenScraper/crypto5.png) <br>
(Holder info.)

#### Step 5: Connect to the Twitter API and pull the most recent hashtags for the token.
```
TWITconsumer_key = os.getenv("TWITCONSUMER_KEY")
TWITconsumer_secret = os.getenv("TWITCONSUMER_SECRET")
TWITaccess_token = os.getenv("TWITACCESS_TOKEN")
TWITaccess_token_secret = os.getenv("TWITACCESS_TOKEN_SECRET")
auth = tweepy.OAuthHandler(TWITconsumer_key, TWITconsumer_secret)
auth.set_access_token(TWITaccess_token, TWITaccess_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True,
wait_on_rate_limit_notify=True)
```
```
tweets = {}
days = 2 
today = datetime.utcnow() 
end_date = today - timedelta(days=days) 
end_str = end_date.strftime('%m/%d/%Y') 
token_symbol = token_info['symbol']
token_slug = token_info['slug'].replace('-', '')
tags = []
if token_symbol.lower() == token_slug:
    token_tags = [token_symbol, token_symbol+'news', token_symbol+'updates']
    for val in token_tags:
        tags.append(val)
else:
    token_tags = [token_symbol, token_symbol+'news', token_symbol+'updates',
                token_slug, token_slug+'news', token_slug+'updates']
    for val in token_tags:
        tags.append(val)
for tag in tags: 
    try:
        print(f'---> hashtag: {tag}')
        for status in tweepy.Cursor(api.search,q=tag,
                                    since=end_str,   
                                    exclude_replies=True,    
                                    lang='en', 
                                    tweet_mode='extended').items(100):
            if status.full_text is not None:
                text = status.full_text.lower()

                id_s = status.id 
                date = status.created_at 
                name = status.user.name
                tweets[id_s] = [date, name, text]

    except tweepy.TweepError as e: 
        print("Tweepy Error: {}".format(e))
```
```
tweets_temp = {}
for key, val in tweets.items():
    if 'rt' not in val[2]:
        val[2] = val[2].split('http', 1)[0]
        if ':' in val[2] == 1:
            val[2] = val[2].split(': ', 1)[1]
            val[2] = re.sub(r'[!@#$]', '', val[2])
            val[2] = "".join(val[2].splitlines())
            tweets_temp[val[1]] = val[0], val[2]
        else:
            val[2] = re.sub(r'[!@#$]', '', val[2])
            val[2] = "".join(val[2].splitlines())
            tweets_temp[val[1]] = val[0], val[2]
temp = []
tweets_res = {}
for key, val in tweets_temp.items():
    if (val[0], val[1][10:20])  not in temp:
        temp.append((val[0], val[1][10:20]))
        tweets_res[key] = val
    else:
        continue
```
![CryptoToken4](/assets/images/CryptoTokenScraper/crypto4.png) <br>
(Twitter tweets.)

#### Step 6: Connect to the Reddit API and pull the most recent posts for the token.
```
REDclient_id = os.getenv("RED_CLIENT_ID")
REDsecret_key = os.getenv("RED_SECRET_KEY")
auth = requests.auth.HTTPBasicAuth(REDclient_id, REDsecret_key)
data = {
        'grant_type': 'password',
        'username': ''########',',
        'password': '########',
        }
headers = {'User-Agent': 'MyAPI/0.0.1'}
res = requests.post('https://www.reddit.com/api/v1/access_token', 
                    auth=auth, data=data, headers=headers)
TOKEN = res.json()['access_token']
headers = {**headers, **{'Authorization': f'bearer {TOKEN}'}}
```
```
sub_posts = {}
sub_res2 = requests.get('https://oauth.reddit.com/r/' + token_slug + '/new', 
                headers=headers)
if sub_res2.json() != None:
    for post in sub_res2.json()['data']['children'][:10]:
        title = post['data']['title']
        for k, v in post.items():
            if 'selftext' in v:
                text = post['data']['selftext']
                text = "".join(text.splitlines())
                text = re.sub(r'[&@#]', '', text)
                score = post['data']['score']
                sub_posts[title] = [text, score]
```
![CryptoToken5](/assets/images/CryptoTokenScraper/crypto5.png) <br>
(Reddit posts.)

#### Summary
Working...

Any suggestions or feedback is greatly appreciated, I am still learning and am always open to suggestions and comments.


[[Link to live site]](https://portfolioprojects.herokuapp.com/coinscraper)


[[Link to repo]](https://github.com/CVanchieri/CryptoTokenScraper)






---
[[<< Back]](https://cvanchieri.github.io/DSPortfolio/Tile1_Projects.html)
