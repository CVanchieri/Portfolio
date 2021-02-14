---
layout: page
title: Liverpool's English Premier League Game Predictions
image: null
nav-menu: false
description: null
show_tile: false

---

![LiverpoolFootballClub](/assets/images/LiverPoolFCPredictions/LPFCTeam.png) <br>
## Making game predictions for the Liverpool using a Random Forest Classifier.

---

#### Necessary imports.
```
%matplotlib inline
import pandas as pd 
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns 
from sklearn.utils.multiclass import unique_labels
from sklearn.pipeline import make_pipeline
import category_encoders as ce
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
```

#### Step 1: Read in the data file.
```
df = pd.read_csv('https://raw.githubusercontent.com/CVanchieri/DataSets/master/EnglishPremierLeagueData/EPL_data.csv')
```
```
print('data frame shape:', df.shape)
print('--- data frame ---')
df.tail()
```
![LiverpoolFootballClub](/assets/images/LiverPoolFCPredictions/LPFC1.png){: .center-block :}

#### Step 2: Organize the data .
```
columns = ["Div", "GameDate", "HomeTeam", "AwayTeam", "FTHG", "FTAG", 
           "HTHG", "HTAG", "HTR", "HS", "AS", "HST", "AST", 
           "HC", "AC", "HF", "AF", "HY", "AY", "HR", "AR", "FTR"] 
df = df[columns]
df = df.rename(columns={"Div": "Division", "FTHG": "FullTimeHomeGoals", "FTAG": "FullTimeAwayGoals", 
                        "HTHG": "HalfTimeHomeGoals", "HTAG": "HalfTimeAwayGoals", "HTR": "HalfTimeResult", 
                        "HS": "HomeShots", "AS": "AwayShots", "HST": "HomeShotsOnTarget", "AST": "AwayShotsOnTarget", 
                        "HC": "HomeCorners", "AC": "AwayCorners", 
                        "HF": "HomeFouls", "AF": "AwayFouls", "HY": "HomeYellowCards", 
                        "AY": "AwayYellowCards", "HR": "HomeRedCards", "AR": "AwayRedCards", 
                        "FTR": "FullTimeResult"})

```
#### Step 3: Clean and rework the data.
```
def wrangle(X):
    X = X.copy()
    X['FullTimeResult'] = X['FullTimeResult'].fillna('Not Played')    
    X['FullTimeResult'] = X['FullTimeResult'].replace({'H':'Home', 'A': 'Away', 'D': 'Tied'}) 
    X['HalfTimeResult'] = X['HalfTimeResult'].astype(object)
    X['FullTimeResult'] = X['FullTimeResult'].astype(object)
    X['GameDate'] = pd.to_datetime(X['GameDate'], infer_datetime_format=True) 
    X['Year'] = X['GameDate'].dt.year
    X['Month'] = X['GameDate'].dt.month
    X['Day'] = X['GameDate'].dt.day
    X['GameDate'] = X.GameDate.astype(str)
    dropped_columns = ['FullTimeHomeGoals', 'FullTimeAwayGoals']
    X = X.drop(columns=dropped_columns)
    columns = ['GameDate', 'HomeTeam', 'AwayTeam','HalfTimeHomeGoals', 'HalfTimeAwayGoals',
               'HalfTimeResult', 'HomeShots', 'AwayShots', 'HomeShotsOnTarget',
               'AwayShotsOnTarget', 'HomeCorners', 'AwayCorners', 'HomeFouls',
               'AwayFouls', 'HomeYellowCards', 'AwayYellowCards', 'HomeRedCards',
               'AwayRedCards', 'FullTimeResult']
    X = X[columns]
    X = X.drop_duplicates()
    return X

df = wrangle(df)
```
#### Step 4: Split the data by date, 2021 season for val data.
```
X_train = df[df['GameDate'] < '2020-09-12']
y_train = X_train['FullTimeResult']
X_train = X_train.drop(columns=['FullTimeResult'])
X_val = df[df['GameDate'] > '2020-09-12']
y_val = X_val['FullTimeResult']
X_val = X_val.drop(columns=['FullTimeResult'])
```
```
print("X_train shape:", X_train.shape)
print("y_train shape:", y_train.shape)
print("X_val shape:", X_val.shape)
print("y_val shape:", y_val.shape)
```
![LiverpoolFootballClub](/assets/images/LiverPoolFCPredictions/LPFC2.png) <br>

#### Step 5: Save the 'GameDate' values from the data.
```
train_id = X_train['GameDate']
val_id = X_val['GameDate']
```
#### Step 6: Build the Randomforest model pipeline with an enocnder, imputer, and scalar.
```
model = make_pipeline(
                      ce.OrdinalEncoder(), 
                      SimpleImputer(strategy='median'),
                      StandardScaler(),
                      RandomForestClassifier(random_state=42, n_jobs=-1)
                      )
model.fit(X_train, y_train)
val_pred = model.predict(X_val)
```

#### Step 7: Generate a prediction data frame and model evaluation metrics.
```
val_pred_df = pd.DataFrame(val_pred, columns=["Predicted_Values" ])
v_test_df = pd.DataFrame(np.array(y_val), columns=["Real_Values"])
df_final = pd.concat([v_test_df , val_pred_df] , axis=1)
print('--- real values vs predicted values ---')
print(df_final.head())
print('--- model metrics ---')
print("model score:", model.score(X_val, y_val))
print("Precision Score:",metrics.precision_score(y_val, val_pred, 
                                           pos_label='positive',
                                           average='micro'))
print("Recall Score: ",metrics.recall_score(y_val, val_pred, 
                                           pos_label='positive',
                                           average='micro'))
print("f1 score Score:",metrics.f1_score(y_val, val_pred, 
                                           pos_label='positive',
                                           average='micro'))
```
```
print('--- confusion matrix ---')
print(metrics.confusion_matrix(y_val,val_pred))
print('--- classification report ---') 
print(metrics.classification_report(y_val,val_pred))
print('model accuracy score=', metrics.accuracy_score(y_val, val_pred))
```
![LiverpoolFootballClub](/assets/images/LiverPoolFCPredictions/LPFC3.png) <br>

#### Step 8: Use the saved 'GameDate' values to create a predictions vs actuals data frame.
```
val_predictions = pd.DataFrame({
                              'GameDate': val_id, 
                              'prediction': val_pred, 
                              'Actual': y_val
                              })
val_predictions = val_predictions.drop_duplicates()
val_predictions = val_predictions.merge( 
                                       X_val[['GameDate','HomeTeam', 'AwayTeam']],
                                       how='left'
                                       )
val_predictions = val_predictions.drop_duplicates(subset=['GameDate', 'HomeTeam'])
```
```
print('--- predictions vs actuals data frame ---')
print('data frame shape:', val_predictions.shape)
val_predictions.head(10)
```
![LiverpoolFootballClub](/assets/images/LiverPoolFCPredictions/LPFC4.png) <br>

#### Step 9: Check the importances of the features.
```
rf = model.named_steps['randomforestclassifier'] 
importances = pd.Series(rf.feature_importances_, X_val.columns)
n = 20
plt.figure(figsize=(20, 14))
plt.title(f'Top Features')
print('--- top features ---')
importances.sort_values()[-n:].plot.barh(color='red');
```
![LiverpoolFootballClub](/assets/images/LiverPoolFCPredictions/LPFC5.png) <br>

#### Step 10: Visualize a heatmap matrix of the model predictions.
```
def plot_confusion_matrix(y_true, y_pred):
    labels = unique_labels(y_true)
    columns = [f'Predicted {label}' for label in labels]
    index = [f'Actual {label}' for label in labels]
    table = pd.DataFrame(confusion_matrix(y_true, y_pred), 
                         columns=columns, index=index)
    return sns.heatmap(table, annot=True, fmt='d', cmap='Wistia')
```
```
print('--- prediction matrix ---')
plt.subplots(1, 1, figsize = (20, 14))
plot_confusion_matrix(y_val, val_pred);
plt.show()
```
![LiverpoolFootballClub](/assets/images/LiverPoolFCPredictions/LPFC6.png) <br>

#### Step 11: Adding a 'Correct?' column to the data frame.
```
val_predictions['Correct?'] = np.where(val_predictions['prediction'] == val_predictions['Actual'], 'Yes', 'No')
val_predictions['Correct?'][val_predictions.Actual == 'Not Played'] = "Not Played"
EPL_predictions = val_predictions.sort_values('GameDate')
```
```
print('--- predicted counts ---')
print(EPL_predictions['Correct?'].value_counts())
print('--- final predictions ---')
EPL_predictions = EPL_predictions.sort_values('GameDate')
EPL_predictions.head(50)
```
![LiverpoolFootballClub](/assets/images/LiverPoolFCPredictions/LPFC7.png) <br>

#### Step 12: Filter just Liverpool to create its own data frame.
```
LPFCH =  EPL_predictions[EPL_predictions['HomeTeam']=='Liverpool']
LPFCA =  EPL_predictions[EPL_predictions['AwayTeam']=='Liverpool']
liverpool_final = pd.concat([LPFCH, LPFCA], sort=False, ignore_index=True)
liverpool_final['GameDate'] = pd.to_datetime(liverpool_final['GameDate']).dt.date
```
#### Step 13: Show the final data frame for Liverpools game predictions vs actual results.
```
print('data frame shape:', liverpool_final.shape) # show the shape
print('--- predicted counts ---')
print(liverpool_final['Correct?'].value_counts())
print('--- Liverpool predictions ---')
liverpool_final.sort_values('GameDate')
```
![LiverpoolFootballClub](/assets/images/LiverPoolFCPredictions/LPFC8.png) <br>

#### Summary
Getting the data organized and put together the 23 files was the most time consuming portion of this project, I would have liked to find more data as making predicitons on these games without, lineups, weather, injury reports etc. will not generate very good accuracy for the predictions but working with what I had found this was fun and a good learning experience overall. 

GitHub file:
[Link]({{'https://github.com/CVanchieri/DSPortfolio/blob/master/posts/LiverpoolEPLPredictionsPost/LiverpoolEPLPredictions_RandomForestModel.ipynb'}})




---
[[<< Back]](https://cvanchieri.github.io/DSPortfolio/Tile1_Projects.html)

 
