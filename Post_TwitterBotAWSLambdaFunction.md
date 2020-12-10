---
layout: page
title:
image: 
nav-menu: false
description: null
show_tile: false

---

![twitter](/assets/images/TwitterBotHeader.png) <br>

## Using a AWS Lambda Function to automate a Twitterbot that searches and stores data science related tweets.

---

I enjoy using Twitter for fun and to find information.  I thought that I would try to create a Twitterbot that will automate the collection and storage of data science information by searching, collecting, and storing tweets on the subject.  

If you need assistance getting started with Tweepy api or AWS Lambda Function connections, this is the blog I followed for those connections. --> [Link]({{'https://dylancastillo.co/how-to-make-a-twitter-bot-for-free/'}})


#### Necessary imports.
```
import os
from pathlib import Path
from datetime import datetime, timedelta
import pandas
from pandas import DataFrame 
import regex as re
import tweepy
import psycopg2
from sqlalchemy import create_engine
```

#### Step 1: Collect the environmental variables and build connection to Tweepy.
##### .env | Tweepy 
```
TWITconsumer_key = os.getenv("TWITCONSUMER_KEY")
TWITconsumer_secret = os.getenv("TWITCONSUMER_SECRET")
TWITaccess_token = os.getenv("TWITACCESS_TOKEN")
TWITaccess_token_secret = os.getenv("TWITACCESS_TOKEN_SECRET")
auth = tweepy.OAuthHandler(TWITconsumer_key, TWITconsumer_secret)
auth.set_access_token(TWITaccess_token, TWITaccess_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
```

#### Step 2: Create the dictionary for storage and the start + end dates to be used.
##### Datetime
```
tweets = {}
days = 3
today = datetime.utcnow()
end_date = today - timedelta(days=days)
end_str = end_date.strftime('%m/%d/%Y')
start = datetime.now()
```

#### Step 3: Using Tweepy's Cursor api to loop through and search each hashtag while storing tweets that pass the parameters.
##### Tweepy | Cursor
```
tags = ['datascience', 'machinelearning', 'artificialintelligence']
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
    
print('--- hashtags tweets ---')
print(f'pulled tweets count: {len(tweets)}')
```
![twitter](/assets/images/TwitterBot1.png) <br>

#### Step 4: Locate and add a value to the dictionary that contains all the #hashtags used in the tweet.
##### Regex
```
for key, val in tweets.items():
val0, val1, val2 = val
tags = re.findall("[#]\w+", val2)
tweets[key] = [val0, val1, val2, tags]

tweets
```
![twitter](/assets/images/TwitterBot2.png) <br>

#### Step 5: Convert the dictionary to a dataframe, remove duplicates, filter unwanted tweets.
##### Dataframe
```
df1 = DataFrame.from_dict(tweets, orient='index', columns=['date', 'name', 'text',  'tags'])
df1.reset_index(inplace=True)
df1 = df1.rename(columns = {'index':'id'})
df1 = df1.drop_duplicates(subset=['id'], keep='last')
df1[['First','Last']] = df1.text.str.split(n=1, expand=True)
df1 = df1.drop_duplicates(subset=['First'])
df1 = df1.drop(columns=['First', 'Last'])
df1['retweet'] = 'NO' # add a retweet column, set to 'NO'
strings = ['rt', '@', 'trial', 'free', 'register', 'subscription'] 
df1 = df1[~df1.text.str.contains('|'.join(strings))]

df1['text'].values
```
![twitter](/assets/images/TwitterBot3.png) <br>

#### Step 6: Collect environmental variables and connect to the database.
##### Psycopg2 | AWS 
```
AWSdatabase = os.getenv("AWSDATABASE")
AWSuser = os.getenv("AWSUSER")
AWSpassword = os.getenv("AWSPASSWORD")
AWShost = os.getenv("AWSHOST")
AWSport = os.getenv("AWSPORT")
sql_AWS = os.getenv("AWSSQL")

connection = psycopg2.connect(database=AWSdatabase,
                              user=AWSuser,
                              password=AWSpassword,
                              host=AWShost,
                              port=AWSport)

cur = connection.cursor()
```

#### Step 7: SQL query all of the database and convert to a dataframe.
##### SQL | Dataframe 
```
sql_select_Query = "select * from tweets_storage"
cur.execute(sql_select_Query)
records = cur.fetchall()
df2 = DataFrame(records)
df2.columns = ['id', 'date', 'name', 'text', 'tags', 'retweet']
```

#### Step 8: Merge the newly pulled tweets with the current SQL database and drop any duplicates.
##### Pandas | Concat
```
df3 = pandas.concat([df1, df2], axis = 0)
df3 = df3.reset_index(drop=True)
df3 = df3.drop_duplicates(subset=['id'], keep='last')
df3[['First','Last']] = df3.text.str.split(n=1, expand=True)
df3 = df3.drop_duplicates(subset=['First'])
df3 = df3.drop(columns=['First', 'Last'])

df3.head()
```
![twitter](/assets/images/TwitterBot4.png) <br>

#### Step 9: Push the updated tweets dataframe back to the AWS database.
##### SQL 
```
engine = create_engine(sql_AWS)
df3.to_sql('tweets_storage', con=engine, index=False, if_exists='replace')
```

#### Summary
There was a lot of research and time that went into this project a little more than expected, connecting to Tweepy and searching for tweets was not very difficult and there is quite a bit of options for the api which is fun to mess around with.  I had never used AWS Lambda Functions before so setting the Lambda Function up with proper triggers and properly connection to the AWS database took quite a bit of time, but now that I have completed this I am very happy to know how to use these Lambda Functions which are great for automation.   I hope to in the future add on to this project with some analysis on the tweets but this was a great start and learning experience.

Any suggestions or feedback is greatly appreciated, I am still learning and am always open to suggestions and comments.

LambdaFunction file
[Link]({{'https://github.com/CVanchieri/DSPortfolio/blob/master/posts/TwitterBotAWSLambdaFunctionPost/lambda_function.py'}})
GitHub repo
[Link]({{'https://github.com/CVanchieri/DSPortfolio'}})
Tweepy/AWS connection support
[Link]({{'https://dylancastillo.co/how-to-make-a-twitter-bot-for-free/'}})







---
[[<< Back]](https://cvanchieri.github.io/DSPortfolio/TileA_MachineLearning.html)
