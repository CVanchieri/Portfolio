---
layout: page
title: Deforestation Prediction Trends
image: null
nav-menu: false
description: null
show_tile: false
---

![Deforestation](/assets/images/WorldDeforestationPredictions/DFTHeader.jpg) <br>
## Using a randomforest regressor model to make deforestation predictions by country.


### Necessary installs.
```
!pip install category_encoders
```

#### Necessary imports.
```
import pandas as pd
import numpy as np
import requests
import category_encoders as ce
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import make_pipeline
pd.set_option('display.float_format', lambda x: '%.2f' % x)
```

#### Read in the train data set from the World Bank.
```
df_tr = pd.read_csv('https://raw.githubusercontent.com/CVanchieri/DataSets/master
                     /WorldBankDeforestation/WorldBank_1990_2018.csv')
```
```
train = df_tr.copy()
train = train.drop(columns=['Unnamed: 0'])
print(train.shape)
train.head()
```
![Deforestation](/assets/images/WorldDeforestationPredictions/DFM1.png) <br>

#### Set the target and features, split the data into train, val, test.
##### train_test_split
```
features = train.columns[:-1].tolist()
target = 'Forest area (% of land area)'

X = train.drop(columns=target)
y = train[target]
```
```
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=1)
print('X_train =', X_train.shape, 'y_train =', y_train.shape, 'X_val =', X_val.shape, 'y_val =', y_val.shape, 
'X_test =', X_test.shape, 'y_test =', y_test.shape)
```
![Deforestation](/assets/images/WorldDeforestationPredictions/DFM2.png) <br>

#### Create a pipeline for the randomforest regressor model.
##### Pipeline, OneHotEncoder, Randomforest Regressor
```
pipeline = make_pipeline(
    ce.OneHotEncoder(), 
    RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
)
pipeline.fit(X_train, y_train)

print ('Training Accuracy', pipeline.score(X_train, y_train))
print('Validation Accuracy', pipeline.score(X_val, y_val))
y_pred = pipeline.predict(X_val)
```
![Deforestation](/assets/images/DFM3.png) <br>

#### Read in the test predictions data frame.
##### Pandas 
```
df_te = pd.read_csv('https://raw.githubusercontent.com/CVanchieri/DataSets/master/WorldBankDeforestation
                     /WorldBank_2019_2120.csv')
```
```
test = df_te.copy()
test = test.drop(columns=['Unnamed: 0'])
print(test.shape)
test.head()
```
![Deforestation](/assets/images/WorldDeforestationPredictions/DFM4.png) <br>

#### Use the pipeline to make predictions on the test data.
##### Pipeline
```
features = test.columns[:-1].tolist()
target = 'Forest area (% of land area)'

X_test = test[features]
y_test = test[target]

pipeline.fit(X_test, y_test)
y_pred = pipeline.predict(X_test)

print ('Test Accuracy', pipeline.score(X_test, y_test))
y_pred
```
![Deforestation](/assets/images/WorldDeforestationPredictions/DFM5.png) <br>

#### Step 6: Add the test predictions to the test data frame.
##### Concat
```
test['Forest area (% of land area)'] = pd.Series(y_pred)
predictions = pd.concat([train, test])

print(predictions.shape)
predictions.head()
```
![Deforestation](/assets/images/WorldDeforestationPredictions/DFM6.png) <br>

#### Create a function to add in the country names.
```
def label_race(row):
   if row['Country Code'] == 'USA' :
      return 'United States of America'
   if row['Country Code'] == 'CHA' :
      return 'China'
   if row['Country Code'] == 'CAN' :
      return 'Canada'
   if row['Country Code'] == 'AUS' :
      return 'Australia'
   if row['Country Code'] == 'ARG' :
      return 'Argentina'
   if row['Country Code'] == 'BRA':
      return 'Brazil'
   if row['Country Code'] == 'BEL':
      return 'Belgium'   
   if row['Country Code'] == 'CHL':
      return 'Chile'
   if row['Country Code'] == 'DEU' :
      return 'Germany'
   if row['Country Code'] == 'ZAF' :
      return 'South Africa'
   if row['Country Code']  == 'NZL':
      return 'New Zealnd'
   if row['Country Code'] == 'GBR':
      return 'United Kingdom'
   if row['Country Code'] == 'IND' :
      return 'India'
   if row['Country Code'] == 'KHM' :
      return 'Cambodia'
   if row['Country Code']  == 'THA':
      return 'Thailand'
   if row['Country Code'] == 'VNM':
      return 'Vietnam'
   if row['Country Code'] == 'HIC' :
      return 'High Income Countries'
   if row['Country Code']  == 'MIC':
      return 'Middle Income Countries'
   if row['Country Code'] == 'LIC':
      return 'Low Income Countries'
   return 'Other'
```

#### Apply the country names to the dataframe with the function.
##### Lambda 
```
final.apply (lambda row: label_race(row), axis=1)
final['Country Name'] = final.apply (lambda row: label_race(row), axis=1)
final = final[['Country Name',
                                  'Country Code',
                                  'Year',
                                  'Agricultural land (sq. km)',
                                  'Electric power consumption (kWh per capita)',
                                  'GDP per capita growth (annual %)',
                                  'Livestock production index (2004-2006 = 100)',
                                  'Ores and metals exports (% of merchandise exports)',
                                  'Urban population',
                                  'Crop production index (2004-2006 = 100)',
                                  'Food production index (2004-2006 = 100)',
                                  'Forest area (% of land area)']]
```

#### Clean and organize the final data frame.
```
final = final[final['Country Name'] != 'Other']
final = final[['Country Name',
 'Country Code',
 'Year',
 'Agricultural land (sq. km)',
 'Electric power consumption (kWh per capita)',
 'GDP per capita growth (annual %)',
 'Livestock production index (2004-2006 = 100)',
 'Ores and metals exports (% of merchandise exports)',
 'Urban population',
 'Crop production index (2004-2006 = 100)',
 'Food production index (2004-2006 = 100)',
 'Forest area (% of land area)']]
final['Forest area (% of land area)'] = final['Forest area (% of land area)'].clip(lower=0)
```
```
print(final.shape)
final.tail()
```
![Deforestation](/assets/images/WorldDeforestationPredictions/DFM7.png) <br>

#### Deforestation prediction visualizations, % of forest area coverage.
##### Predictions by country.
![Deforestation](/assets/images/WorldDeforestationPredictions/DFT3.png) <br>

##### Predictions by country income.
![Deforestation](/assets/images/WorldDeforestationPredictions/DFT4.png) <br>

#### Summary
Since I had done my college studies in Environmental Studies working on deforestaion data sparked a lot of interest.  I found the toughest part of this project was collecting the different data and getting them all together is a clean data set to that could be used by the model.  I believe I used 6-8 different data set on different topics that all had some relation to deforestation in hopes that this additional info could help the models predictions.  Overall I think it all went well, with this project I state that we are predicting trends because the % of change in deforestation year by year is typically incredibly small, whether its going up or down.  I selected just a few countries so the graph is not overkill on the data but there are many more countries in the model notebook to view, I found that the income of the country low/med/high also graphed can typically determine which diretion the deforestation change trending.

Any suggestions or feedback is greatly appreciated, I am still learning and am always open to suggestions and comments.

GitHub file:
[Link]({{'https://github.com/CVanchieri/DSPortfolio/blob/master/posts/DeforestationPredictionsTrendsPost/DeforestationPredictionsModel.ipynb'}})




---
[[<< Back]](https://cvanchieri.github.io/DSPortfolio/TileA_MachineLearning.html)
