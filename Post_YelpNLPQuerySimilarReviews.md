---
layout: page
title:
image: 
nav-menu: false
description: null
show_tile: false

---

![NLP](/assets/images/QuerySimilarYelpReviews/nlp.jpg) <br>

## Using natural language processing to query similar Yelp reviews by reviews text.

---

The goal here is to use create a fake review and then use Natural Language Processing on the text of the reivew to query similar reviews within the given Yelp data set. 

#### Necessary imports.
```
import pandas as pd
import re
import spacy 
from spacy.tokenizer import Tokenizer
from collections import Counter
import squarify
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from gensim.models import LdaMulticore
from gensim.corpora import Dictionary
from gensim import corpora
import pyLDAvis
import pyLDAvis.gensim
import seaborn as sns
from gensim.models.coherencemodel import CoherenceModel
```

#### Step 1: Read in the JSON file and got a visual of the data frame being worked with.
##### Pandas 
```
yelp = pd.read_json('review_sample.json', lines=True)
yelp = yelp[['business_id', 'review_id', 'text', 'cool', 'funny', 'useful', 'stars']]
```
```
print(yelp.shape)
yelp.head()
```
![yelp](/assets/images/QuerySimilarYelpReviews/yelp1.png) <br>
(Yelp data frame.)

#### Step 2: Clean up the text from the data frame reviews.
##### Regex
```
yelp['text'] = yelp['text'].apply(lambda x: re.sub(r'[^a-zA-Z ^0-9]', '', x))
yelp['text'] = yelp['text'].apply(lambda x: re.sub(r'(x.[0-9])', '', x))
yelp['text'] = yelp['text'].replace('/', ' ') 
yelp['text'] = yelp['text'].apply(lambda x: re.sub('  ', ' ', x))
yelp['text'] = yelp['text'].apply(lambda x: x.lower())
```
![yelp](/assets/images/QuerySimilarYelpReviews/yelp2.png) <br>
(Cleaned text.)

#### Step 3: Create a list of tokens from the reviews text and add to the dataframe.
##### Spacy | Tokenizer | Stop Words | Lemmatize
```
df = yelp.copy()
```
```
nlp = spacy.load("en_core_web_lg")
# set the tokenizer on nlp.vocab.
tokenizer = Tokenizer(nlp.vocab)
```
```
STOP_WORDS = nlp.Defaults.stop_words
```
```
tokens = []
for doc in tokenizer.pipe(df['text'], batch_size=500):
    doc_tokens = []
    for token in doc:
        if (token.lemma_ not in STOP_WORDS) & (token.text != ' '):
            doc_tokens.append(token.lemma_)
    tokens.append(doc_tokens)
```
```
df['tokens'] = tokens
df['tokens'].head()
```
![yelp](/assets/images/QuerySimilarYelpReviews/yelp3.png) <br>
(Review tokens.)

#### Step 4: Create a vectors and fit nearest neighbors model.
##### .vector | NearestNeighbors
```
vects = [nlp(doc).vector for doc in df['text']]
```
```
nn = NearestNeighbors(n_neighbors=10, algorithm='ball_tree')
nn.fit(vects)
```
![yelp](/assets/images/QuerySimilarYelpReviews/yelp4.png) <br>
(Nearest neighbors model.)

#### Step 5: Create a fake review, vector, and use the nn model.
##### .vector | .kneighbors
```
created_review = """
The indian food was magnificent! We will come back.
"""
created_review_vect = nlp(created_review).vector
```
```
created_review = '''
I love the gluten free food options and the service was really quick too!
'''
```
```
most_similiar = nn.kneighbors([created_review_vect])
yelp.iloc[most_similiar[1][0]]['text']
```
![yelp](/assets/images/QuerySimilarYelpReviews/yelp5.png) <br>
(most similar reviews.)

#### Step 6: Use Vectorizer, RandomForest, and GridSearch for the prediction model.
##### TfidVectorizer | RandomForestClassifier | GridSearchCV
```
vect = TfidfVectorizer(stop_words=STOP_WORDS)
rfc = RandomForestClassifier()
```
```
pipe = Pipeline([
                 ('vect', vect),
                 ('clf', rfc)                
                ])
```
```
parameters = {
    'vect__max_df': ( 0.5, 0.75, 1.0, 1.25, 1.50),
    'vect__min_df': (.01, .03, .05, .07, .09)
    }
grid_search = GridSearchCV(pipe, parameters, cv=5, n_jobs=-1, verbose=1)
grid_search.fit(df['text'], df['stars'])
```
```
grid_search.best_score_
```
![yelp](/assets/images/QuerySimilarYelpReviews/yelp6.png) <br>
(The goal was 51% and above.)

#### Step 7: Use the prediction model on the created reviews to predict star rating.
##### .predict 
```
created_review = [created_review]
pred = grid_search.predict(created_review)
created_review_stars = pd.DataFrame({'text': created_review, 'stars':pred})
created_review_stars['stars'] = created_review_stars['stars'].astype('int64')
created_review_stars['text'] = created_review_stars.text.replace('\n':'')
created_review_stars.head()                 
```
![yelp](/assets/images/QuerySimilarYelpReviews/yelp7.png) <br>
(created review with star review.)

#### Summary
The goal was to tokenize the yelp review data, query the most similar yelp reviews to the fake review created, create a classification model to give the fake review a star rating, and implement topic modeling.
I was very happy with my first go at NLP and the overall experience, I would consider it a success. I look forward to digging deeper and learning more.

Any suggestions or feedback is greatly appreciated, I am still learning and am always open to suggestions and comments.

GitHub file
[Link]({{'https://github.com/CVanchieri/DSPortfolio/blob/master/posts/YelpNLPQueryReviewsPost/YelpNLPQueryReviews.ipynb'}})






---
[[<< Back]](https://cvanchieri.github.io/DSPortfolio/Tile1_Projects.html)
