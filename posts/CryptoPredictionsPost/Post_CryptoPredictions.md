---
layout: page
title:
image: 
nav-menu: false
description: null
show_tile: false

---

![CryptoTokenBanner](https://cvanchieri.github.io/Portfolio/assets/images/CryptoTokenScraperPost/CryptoBanner.jpeg) <br>
## Making crypto predictions based on 1 year of compiled data.

---

#### Imports.

```
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.neural_network import MLPRegressor
from sklearn.ensemble import GradientBoostingRegressor
from statsmodels.tsa.arima.model import ARIMA
```

#### Get the data and organize it.
```
url = 'https://raw.githubusercontent.com/CVanchieri/CryptoThings/main/Data/CompiledCrypto/ALLDATA.csv'
df = pd.read_csv(url)
df.sort_values(by='Date', inplace=True)
df.fillna(0, inplace=True)

print(f"Things = {df['Name'].unique()}")
print(f"Dates = {df['Date'].iloc[0]} - {df['Date'].iloc[-1]}")
print(df.shape)
df.head()
```
![CryptoToken1](https://cvanchieri.github.io/Portfolio/assets/images/CryptoTokenScraperPost/crypto1.png) <br>
(Newly released tokens.)

#### Linear Regression.
```
names = ['GOLD', 'OIL', 'GAS', 'BTC', 'ETH', 'SOL', 'ADA', 'XRP'] # names to predict for
date = '09/01/2024' # pick a date

for name in names:

    name_df = df[df['Name'] == name] # filter the data for the given names
    if name_df.empty:
        print(f"No data found for {name} price. Check your dataset.")
        continue

    X = pd.to_datetime(name_df['Date']).astype(int).values.reshape(-1, 1)  # convert dates to numbers
    y = name_df['Close'].values # get the close values

    model = LinearRegression() # linear regression
    model.fit(X, y) # fit model

    # Predict the price for 09/01/2024 (date)
    future_date = pd.to_datetime(date).value  # get the number value of the given date
    predicted_price = model.predict([[future_date]]) # predict the model on the given date

    print(f"LR - Predicted {name} price on {date} (Linear Regression): {predicted_price[0]}")
```
![CryptoToken1](https://cvanchieri.github.io/Portfolio/assets/images/CryptoTokenScraperPost/crypto1.png) <br>
(Newly released tokens.)

#### Decision Tree.
```
names = ['GOLD', 'OIL', 'GAS', 'BTC', 'ETH', 'SOL', 'ADA', 'XRP'] # names to predict for
date = '09/01/2024' # pick a date

for name in names:

    name_df = df[df['Name'] == name] # filter the data for the given names
    if name_df.empty:
        print(f"No data found for {name} price. Check your dataset.")
        continue

    X = pd.to_datetime(name_df['Date']).astype(int).values.reshape(-1, 1) # convert dates to numbers
    y = name_df['Close'].values # get the close values

    model = DecisionTreeRegressor() # decision tree
    model.fit(X, y) # fit model

    # Predict the price for 09/01/2024 (date)
    future_date = pd.to_datetime(date).value  # get the number value of the given date
    predicted_price = model.predict([[future_date]]) # predict the model on the given date

    print(f"DT - Predicted {name} price on {date} (Decision Tree): {predicted_price[0]}")
```
![CryptoToken1](https://cvanchieri.github.io/Portfolio/assets/images/CryptoTokenScraperPost/crypto1.png) <br>
(Newly released tokens.)

#### Random Forest.
```
names = ['GOLD', 'OIL', 'GAS', 'BTC', 'ETH', 'SOL', 'ADA', 'XRP'] # names to predict for
date = '09/01/2024' # pick a date

for name in names:

    name_df = df[df['Name'] == name] # filter the data for the given names
    if name_df.empty:
        print(f"No data found for {name} price. Check your dataset.")
        continue

    X = pd.to_datetime(name_df['Date']).astype(int).values.reshape(-1, 1) # convert dates to numbers
    y = name_df['Close'].values # get the close values

    model = RandomForestRegressor() # random forest
    model.fit(X, y) # fit model

       # Predict the price for 09/01/2024 (date)
    future_date = pd.to_datetime(date).value  # get the number value of the given date
    predicted_price = model.predict([[future_date]]) # predict the model on the given date

    print(f"RF - Predicted {name} price on {date} (Random Forests): {predicted_price[0]}")
```
![CryptoToken1](https://cvanchieri.github.io/Portfolio/assets/images/CryptoTokenScraperPost/crypto1.png) <br>
(Newly released tokens.)

#### Support Vector Machine.
```
names = ['GOLD', 'OIL', 'GAS', 'BTC', 'ETH', 'SOL', 'ADA', 'XRP'] # names to predict for
date = '09/01/2024' # pick a date

for name in names:

    name_df = df[df['Name'] == name] # filter the data for the given names
    if name_df.empty:
        print(f"No data found for {name} price. Check your dataset.")
        continue

    X = pd.to_datetime(name_df['Date']).astype(int).values.reshape(-1, 1) # convert dates to numbers
    y = name_df['Close'].values # get the close values

    svm_model = SVR() # support vector machine
    svm_model.fit(X, y) # fit model
    svm_predicted_price = svm_model.predict([[future_date]]) # predict the model on the given date

    print(f"SVM - Predicted {name} price on {date} (Support Vector Machines): {svm_predicted_price[0]}")
```
![CryptoToken1](https://cvanchieri.github.io/Portfolio/assets/images/CryptoTokenScraperPost/crypto1.png) <br>
(Newly released tokens.)

#### Neural Network.
```
names = ['GOLD', 'OIL', 'GAS', 'BTC', 'ETH', 'SOL', 'ADA', 'XRP'] # names to predict for
date = '09/01/2024' # pick a date

for name in names:

    name_df = df[df['Name'] == name] # filter the data for the given names
    if name_df.empty:
        print(f"No data found for {name} price. Check your dataset.")
        continue

    X = pd.to_datetime(name_df['Date']).astype(int).values.reshape(-1, 1) # convert dates to numbers
    y = name_df['Close'].values # get the close values

    nn_model = MLPRegressor(hidden_layer_sizes=(100,), activation='relu', solver='adam', random_state=42, max_iter=500) # neural network
    nn_model.fit(X, y) # fit model
    nn_predicted_price = nn_model.predict([[future_date]])  # predict the model on the given date

    print(f"Neural Network - Predicted {name} price on {date} (Neural Networks): {nn_predicted_price[0]}")
```
![CryptoToken1](https://cvanchieri.github.io/Portfolio/assets/images/CryptoTokenScraperPost/crypto1.png) <br>
(Newly released tokens.)

#### Gradient Boosting Machine.
```
names = ['GOLD', 'OIL', 'GAS', 'BTC', 'ETH', 'SOL', 'ADA', 'XRP'] # names to predict for
date = '09/01/2024' # pick a date

for name in names:

    name_df = df[df['Name'] == name] # filter the data for the given names
    if name_df.empty:
        print(f"No data found for {name} price. Check your dataset.")
        continue

    X = pd.to_datetime(name_df['Date']).astype(int).values.reshape(-1, 1) # convert dates to numbers
    y = name_df['Close'].values # get the close values

    # Gradient Boosting Machine
    gbm_model = GradientBoostingRegressor() # gradient boost machine
    gbm_model.fit(X, y) # fit model
    gbm_predicted_price = gbm_model.predict([[future_date]])  # predict the model on the given date

    print(f"GBM - Predicted {name} price on {date} (Gradient Boosting Machines): {gbm_predicted_price[0]}")
```
![CryptoToken1](https://cvanchieri.github.io/Portfolio/assets/images/CryptoTokenScraperPost/crypto1.png) <br>
(Newly released tokens.)

#### Get the data and organize it.
```
names = ['GOLD', 'OIL', 'GAS', 'BTC', 'ETH', 'SOL', 'ADA', 'XRP'] # names to predict for
date = '09/01/2024' # pick a date

for name in names:

    name_df = df[df['Name'] == name].copy()  # Create an explicit copy
    if name_df.empty:
        print(f"No data found for {name} price. Check your dataset.")
        continue

    # Prepare data for time series analysis
    name_df['Date'] = pd.to_datetime(name_df['Date'])
    name_df.set_index('Date', inplace=True)
    y = name_df['Close'] # get the close values

    y = y.resample('D').last()  # 'D' for daily, adjust if needed

    # (p, d, q) are the model orders. You might need to tune these.
    model = ARIMA(y, order=(5, 1, 0)) # arima
    model_fit = model.fit() # fit model

    forecast_result = model_fit.forecast(steps=1) # predict the price for the next day after the end of your data
    predicted_price = forecast_result.iloc[0]  # access the first (and only) predicted value
    last_date = y.index[-1] # fet the last date in your data

    date_dt = pd.to_datetime(date) # convert the 'date' string to a datetime object
    prediction_date = date_dt + pd.DateOffset(days=0) # calculate the prediction date (next day)

    print(f"ARIMA - Predicted {name} price on {prediction_date.date()} (Time Series Analysis): {predicted_price}")
```
![CryptoToken1](https://cvanchieri.github.io/Portfolio/assets/images/CryptoTokenScraperPost/crypto1.png) <br>
(Newly released tokens.)




[[Link to repo]](https://github.com/CVanchieri/CryptoThings/blob/main/Notebooks/Data/CompiledDataPredictions.ipynb)




---
[[<< Back]](https://cvanchieri.github.io/Portfolio/Tile1_Projects.html)
