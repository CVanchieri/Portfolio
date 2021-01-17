---
layout: page
title:
image: 
nav-menu: false
description: null
show_tile: false

---

![Covid19Header2](/assets/images/Covid19USALineGraph/PLGCovidHeader2.jpg) <br>

## Visualizing the COVID-19 virus impact on the USA in a plotly line graph.

Line graphs are not always very engaging or eye catching on their own, I have been enjoying using Plotly to add a 
little bit of engagement with the user.  Plotly gives you easy ability to add data information into the graph that a 
user can find themselves and locate by engaging with the visualization.

#### Necessary installs.
```
!pip install chart_studio  
```

#### Necessary imports.
```
import pandas as pd
import requests
from pandas import DataFrame
import plotly.graph_objs as go
import chart_studio.plotly as py
import plotly.offline
from plotly.offline import iplot, init_notebook_mode
```

#### Step 1: Pull in the COVID19.com API daily counts for USA.
##### Requests | Json
```
response = requests.get("https://covidtracking.com/api/us/daily")
covid_cs = response.json()
data = pd.json_normalize(covid_cs)
```
```
print(data.shape)
data.head()
```
![Covid19LineGraph](/assets/images/Covid19USALineGraph/PLG1.png) <br>
(COVID-19 daily dataframe.)

#### Step 2: Clean, filter and organize data.
##### Pandas
```
df = data.copy()
```
```
df = df.drop(columns=['hash', 'pending', 'dateChecked', 'lastModified', 'total', 'posNeg', 'hospitalized'])
df = df.rename(columns={'date' : 'Date', 'states' : 'States', 'positive' : 'TotalPositives', 
'positiveIncrease' : 'PositivesToday', 'negative' : 'TotalNegatives', 'negativeIncrease' : 'NegativesToday', 'hospitalizedCurrently' : 'HospitalizedCurrently', 'hospitalizedIncrease' : 'HospitalizedToday', 'hospitalizedCumulative' : 'TotalHospitalized', 'inIcuCurrently' : 'IcuCurrently', 
'inIcuCumulative': 'TotalIcu', 'onVentilatorCurrently' : 'VentilatorsCurrently', 'onVentilatorCumulative' : 'TotalVentilators', 'death' : 'TotalDeaths', 'deathIncrease' : 'DeathsToday', 'recovered' : 'TotalRecovered', 'totalTestResults' : 'TotalTests', 'totalTestResultsIncrease' : 'TestsToday'})
df['Date'] = pd.to_datetime(df['Date'].astype(str), format='%Y%m%d')
df['Date'] = df.Date.astype(str)
df = df.sort_values('Date')
df = df.fillna(0)
df['IcuToday'] = df['IcuCurrently'].diff()
df['VentilatorsToday'] = df['VentilatorsCurrently'].diff()
df['RecoveredToday'] = df['TotalRecovered'].diff()
df['TestsDailyChange'] = df['TestsToday'].diff()
df['PostiviesDailyChange'] = df['PositivesToday'].diff()
df['NegativesDailyChange'] = df['NegativesToday'].diff()
df['HospitalizedDailyChange'] = df['HospitalizedToday'].diff()
df['IcuDailyChange'] = df['IcuToday'].diff()
df['VentilatorsDailyChange'] = df['VentilatorsToday'].diff()
df['DeathsDailyChange'] = df['DeathsToday'].diff()
df['RecoveredDailyChange'] = df['RecoveredToday'].diff()
df = df[['Date', 'States', 'TestsToday', 'TestsDailyChange', 'TotalTests', 'PositivesToday', 'PostiviesDailyChange', 'TotalPositives', 'NegativesToday', 'NegativesDailyChange', 'TotalNegatives',
'HospitalizedToday', 'HospitalizedDailyChange', 'HospitalizedCurrently', 'TotalHospitalized', 
'IcuToday', 'IcuDailyChange', 'IcuCurrently', 'TotalIcu', 'VentilatorsToday', 'VentilatorsDailyChange',                           'VentilatorsCurrently', 'TotalVentilators', 'DeathsToday', 'DeathsDailyChange', 'TotalDeaths', 'RecoveredToday', 'RecoveredDailyChange', 'TotalRecovered']]
df = df.sort_values('Date', ascending=False)
df.loc[df.Date == '2020-05-01', 'HospitalizedToday'] = 4000
df.loc[df.Date == '2020-05-08', 'HospitalizedToday'] = 3000
df.loc[df.Date == '2020-05-26', 'HospitalizedToday'] = 3000
df.loc[df.Date == '2020-06-04', 'HospitalizedToday'] = 700
df.loc[df.Date == '2020-07-11', 'HospitalizedToday'] = 2500
df.loc[df.Date == '2020-08-07', 'HospitalizedToday'] = 4000
df.loc[df.Date == '2020-10-06', 'HospitalizedToday'] = 650
df.loc[df.Date == '2020-10-23', 'HospitalizedToday'] = 2000
```
```
print(df.shape)
df.head()
```
![Covid19LineGraph](/assets/images/Covid19USALineGraph/PLG2.png) <br>
(Reworked data frame.)

#### Step 3: Function to configure the browser to display plotly charts properly.
##### IPython | Plotly
```
def configure_plotly_browser_state():
  import IPython
  display(IPython.core.display.HTML('''
        <script src='/static/components/requirejs/require.js'></script>
        <script>
          requirejs.config({
            paths: {
              base: '/static/base',
              plotly: 'https://cdn.plot.ly/plotly-latest.min.js?noext',
            },
          });
        </script>
        '''))
```

#### Step 4: Configure the data, design, and layout for the graph.
##### Scatter | Layout | Figure
```
configure_plotly_browser_state()
init_notebook_mode(connected=True)
trace1 = go.Scatter(
    x=df['Date'],
    y=list(df['TotalHospitalized']),
    name="TotalHospitalized",
    mode='lines+markers',
    line=dict(color="#f4fc03", width = 1, dash = 'dash'),
    )
trace2 = go.Scatter(
    x=df['Date'],
    y=list(df['TotalIcu']),
    name="Total ICU",
    mode='lines+markers',
    line=dict(color="#fca503", width = 1, dash = 'dash')
    )
trace3 = go.Scatter(
    x=df['Date'],
    y=list(df['TotalVentilators']),
    name="Total Ventilators",
    mode='lines+markers',
    line=dict(color="#c603fc", width = 1, dash = 'dash')
    )
trace4 = go.Scatter(
    x=df['Date'], 
    y=list(df['TotalDeaths']),
    name="Total Deaths",
    mode='lines+markers',
    line=dict(color="#fc0303", width = 1, dash = 'dash')
    )
data = [trace1,trace2, trace3, trace4]
layout = go.Layout(title="USA COVID19 Numbers",
                  yaxis=dict(title="# Count", 
                              zeroline=False),
                  xaxis=dict(title="Date",
                              ),
                  margin=dict(l=20, r=20, t=75, b=20),
                  paper_bgcolor="whitesmoke",
                  autosize=True)                         
```
```
fig = go.Figure(data=data, layout=layout)
fig.show()
```
![Covid19LineGraph](/assets/images/Covid19USALineGraph/PLG3.png) <br>
(Image of the graph.)
Using an AWS Lambda Function, RDS Database, FalconIO, and Ploty Chart Studio, I created a live graph that updates daily.  [Link]({{'https://portfolioprojects.herokuapp.com/covid19us'}})

#### Summary
Just because its a 'line graph' does not mean its not useful and  or engaging.  A static graph may not be the best route 
to go but adding a little bit of data that the user can engage with can change everything.  Plotly is a big library and has 
plenty more complex beautiful charts and graphs but it also can present some of the more basic visualiation really well too.

Any suggestions or feedback is greatly appreciated, I am still learning and am always open to suggestions and comments.

Using an AWS Lambda Function, RDS Database, FalconIO, and Ploty Chart Studio, I created a live graph that updates daily.

Live[Link]({{'https://portfolioprojects.herokuapp.com/covid19us'}})

GitHub file 
[Link]({{'https://github.com/CVanchieri/DSPortfolio/blob/master/posts/PlotlyCOVID19LineGraphPost/PlotlyCovid19LineGraph.ipynb'}})




---
[[<< Back]](https://cvanchieri.github.io/DSPortfolio/Tile1_Projects.html)

