---
layout: page
title:
image: 
nav-menu: false
description: null
show_tile: false

---

![twitter](/assets/images/TwitterBotHeader.png) <br>

## Automating a Tweepy Twitterbot that searches and stores data science related tweets.

---

I enjoy using Twitter for fun and to find information.  I thought that I would try to create a Twitterbot that will automate the collection and storage of data science information by searching, collecting, and storing tweets on the subject.

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
print("---> authenticate Twitter connection")
auth = tweepy.OAuthHandler(TWITconsumer_key, TWITconsumer_secret)
auth.set_access_token(TWITaccess_token, TWITaccess_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True,
wait_on_rate_limit_notify=True)
```

#### Step 2: Create the dictionary for storage and the start + end dates to be used.
##### Datetime
```
tweets = {} # store all ids and tweets
days = 3 # set the # of 'past' days to pull tweets from, end date
today = datetime.utcnow() # get todays date
end_date = today - timedelta(days=days) # <-- set the end date
end_str = end_date.strftime('%m/%d/%Y') # set the end date as str
start = datetime.now() # set the start date 
```

#### Step 3: Using Tweepy's Cursor api, loop through and search each hashtag storing tweets that pass the parameters.
##### Tweepy | Cursor
```
tags = ['datascience', 'machinelearning', 'artificialintelligence']
for tag in tags: # loop through hashtags
  try:
    print(f'---> hashtag: {tag}')
    for status in tweepy.Cursor(api.search,q=tag,
                                since=end_str,   
                                exclude_replies=True,    
                                lang='en', 
                                tweet_mode='extended').items(100):
      if status.full_text is not None:
        text = status.full_text.lower()

        id_s = status.id # store the tweet id 
        date = status.created_at # store the date created 
        name = status.user.name # store the user name 
        tweets[id_s] = [date, name, text] # add elements to dict

  ### handle errors ###
  except tweepy.TweepError as e: 
    print("Tweepy Error: {}".format(e))
```
#### Step 4: Locate and add a value to the dictionary that contains all the #hashtags used in the tweet.
##### Regex
```
for key, val in tweets.items(): # loop through dictionary key/values
  val0, val1, val2 = val # unpack all variables 
  tags = re.findall("[#]\w+", val2) # get all words starting with '#'.
  tweets[key] = [val0, val1, val2, tags] # add elements to the dictionary
```

#### Step 5: Convert the dictionary to a dataframe, remove duplicates, filter unwanted tweets.
##### Dataframe
```
df1 = DataFrame.from_dict(tweets, orient='index', columns=['date', 'name', 'text',  'tags']) # create a dataframe from for the tweets dict
df1.reset_index(inplace=True) # reset the index 
df1 = df1.rename(columns = {'index':'id'}) # rename columns 
df1 = df1.drop_duplicates(subset=['id'], keep='last') # drop duplicates
df1[['First','Last']] = df1.text.str.split(n=1, expand=True)  # split the text column into 2 
df1 = df1.drop_duplicates(subset=['First']) # drop duplicates ofr First column
df1 = df1.drop(columns=['First', 'Last']) # drop First and Last columns 
df1['retweet'] = 'NO' # add a retweet column, set to 'NO'
strings = ['rt', '@', 'trial', 'free', 'register', 'subscription'] # list of substrings 
df1 = df1[~df1.text.str.contains('|'.join(strings))] # remove any text values that contain a string from strings 
```

#### Step 6: Collect environmental variables and connect to the database.
##### Psycopg2 | AWS 
```
AWSdatabase = os.getenv("AWSDATABASE")
AWSuser = os.getenv("AWSUSER")
AWSpassword = os.getenv("AWSPASSWORD")
AWShost = os.getenv("AWSHOST")
AWSport = os.getenv("AWSPORT")
sql_AWS = os.getenv("AWSSQL")

## connect to AWS database ###
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
sql_select_Query = "select * from tweets_storage" # query all of database 
cur.execute(sql_select_Query)
records = cur.fetchall()
df2 = DataFrame(records)  # set as dataframe 
df2.columns = ['id', 'date', 'name', 'text', 'tags', 'retweet'] # label the columns 
```

#### Step 8: Merge to newly pulled tweets with the current SQL database and drop any duplicates.
##### Pandas | Concat
```
df3 = pandas.concat([df1, df2], axis = 0) # merge the old and new dataframes
df3 = df3.reset_index(drop=True) # reset the index 
df3 = df3.drop_duplicates(subset=['id'], keep='last') # drop duplicates
df3[['First','Last']] = df3.text.str.split(n=1, expand=True) # split the text value into 2 
df3 = df3.drop_duplicates(subset=['First']) # drop duplicates 
df3 = df3.drop(columns=['First', 'Last']) # remove First and Last columns 
```

#### Step 9: Push the updated tweets dataframe back to the AWS database.
##### SQL 
```
engine = create_engine(sql_AWS) # create engine
df3.to_sql('tweets_storage', con=engine, index=False, if_exists='replace') # push the dataframe to the database
```

#### Step 10: To check that its been updated SQL query the entire database again.
##### SQL | Dataframe
```
sql_select_Query = "select * from tweets_storage"  # query the whole database 
cur.execute(sql_select_Query)
records = cur.fetchall()
tweets_database = DataFrame(records) # set data as dataframe 
tweets_database.columns = ['id', 'date', 'name', 'text',  'tags', 'retweet'] # set the column names 
cur.close()
```

#### Summary
There was a lot of research and time that went into this project, connecting to tweepy and searching tweets was not very difficult and there is quite a bit of options for the api which is fun to mess around with.  I had never used AWS Lambda Functions before so setting the Lambda Function up properly with the connection to the AWS database took quite a bit of time, now that I have completed this one I am very happy to know how to use these automated functions.   I hope to in the future add on to this project with some analysis on the tweets but this was a great start and learning experience.

Any suggestions or feedback is greatly appreciated, I am still learning and am always open to suggestions and comments.

GitHub file
[Link]({{'https://github.com/CVanchieri/DSPortfolio/blob/master/posts/TwitterBotAWSLambdaFunctionPost/lambda_function.py'}})






---
[[<< Back]](https://cvanchieri.github.io/DSPortfolio/TileA_MachineLearning.html)
