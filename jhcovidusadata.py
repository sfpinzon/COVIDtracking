# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 16:49:39 2020

@author: Admin
"""


import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats.mstats import gmean
import xlrd
import datetime as dt
import matplotlib.dates as mdates
import numpy as np
os.chdir('C:\\Users\\Vaq Workstation\\Dropbox (VGI)\\!sfp\\COVID')
data=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
data3=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv')
deathdataUS=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv')
deathdataGlobal=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
#data3=pd.read_csv('https://covidtracking.com/api/v1/states/daily.csv') #US State Data Import
#data4=pd.read_excel(r'C:\Users\roth1\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Covid_Project\Anaconda3 (64-bit)\Texas_COVID-19_Case_Count_Data_by_County.xlsx') #Texas County Data
#data3=pd.read_csv('https://dshs.texas.gov/coronavirus/additionaldata.aspx')#Texas County Data
df=pd.DataFrame(data) #set as dataframe
df3=pd.DataFrame(data3)#set (US_States) as dataframe
#df4=pd.DataFrame(data4)#set (Texas_County Data) as dataframe
#df3[(df3['date'] > '20200712') & (df3['date'] < '20200712')]
#df.dropna(inplace = True)
#df3.dropna(inplace = True)
#df4.dropna(inplace = True)
df=df.rename(columns={'Country/Region': 'Country', 'Province/State' : 'State'}) #Rename columns
df = df.drop(['Lat','Long'], axis=1)#drop latitude longitudetes
#df3 = df3.drop(['positive','negative','pending','hospitalizedCurrently','hospitalizedCumulative','onVentilatorCurrently','onVentilatorCumulative','lastUpdateEt','dateModified','checkTimeEt','dateChecked','totalTestsViral','positiveTestsViral','negativeTestsViral','positiveCasesViral','deathConfirmed','deathProbable','fips','positiveIncrease','negativeIncrease','total','totalTestResultsIncrease','posNeg','deathIncrease','hospitalizedIncrease','hash','commercialScore','negativeRegularScore','negativeScore','positiveScore','score','grade'],axis=1)
#df= df.set_index('Country')
df=df.sort_values(by=['Country']) #sort by country
#df3=df.sort_values(by=['date'])
cols= df.columns.values #get column names
df.loc['Global']=df.sum() #create grand total 
df.loc['Global', 'Country']='Global' #fill in Country column for total
dates = cols[2:] #get dates
#df3.iloc[:,0] = pd.to_datetime(df3.iloc[:,0], format= '%Y%m%d')

#Subsetting data for cleaning
nosubs= df[pd.isnull(df['State'])] #Separate data with no states/provinces
subs=df[~pd.isnull(df['State'])]# Separate data with states/provinces
subsnosum=subs[subs.Country==subs.State] #Take country mainland numbers only, exclude territories
subs = subs.drop(subsnosum.index) #Remove mainlaind country data from subs
nosubs = nosubs.append(subsnosum) #Append subsnosum to nosubs
del[subsnosum]
#DEALING WITH CRUISE DATA
#cruisea = subs[subs['Country'].str.contains("ruise")] #Separate cruise cases 
#cruiseb = subs[subs['State'].str.contains("Princess")] #Separate cruise cases
#cruises = cruisea.append(cruiseb) #merge cruises
#del [cruisea,cruiseb] #remove redundant data
#subs = subs.drop(cruises.index) #remove cruises data from subs 
#cruises.loc[22, 'State'] = 'Diamond Princess' #Clean extra words in name
#cruisesum= cruises.groupby(by='State').sum().reset_index() #Aggregate cruise numbers
#cruisesum=cruisesum.rename(columns={'State': 'Country'}) #Rename column for matching other subsets

#prelimsum = df.groupby(['Country']).sum()
#subssum=subs[subs.Country!=subs.State] #separate countries with reporting sub-units


#DEALING WITH TERRITORIES
noterritorycountries=['Australia', 'Canada', 'China', 'US'] #Countries without territories list
territories= subs[~subs.Country.isin(noterritorycountries)] #Separate countries with territories
subs = subs.drop(territories.index) #drop territories from subs subset
territorysum = territories.groupby(by='Country').sum().reset_index() #Sum numbers for territories
territorysum['Country'] = territorysum['Country'].astype(str) + ' Territories' #relabel country column
subsum = subs.groupby(by='Country').sum().reset_index() #sum subs subset
# DEALING WITH LOWER 48
#ustable = subs[subs['Country']=='US'] #Subset for US data only
#not48= ['Guam', 'Puerto Rico', 'Virgin Islands', 'Diamond Princess', 'Grand Princess', 'Alaska', 'Hawaii', 'Honolulu County, HI'] #List to exclude AK, HI and territories
#lower48 = ustable[~ustable.State.isin(not48)] # Subset for lower 48 data 
#ussums = lower48.groupby(by='Country').sum().reset_index()
#ussums['Country'] = ussums['Country'].astype(str) + ' Lower 48'

#####APPENDING FINAL DATA FRAME################
nosubs= nosubs.drop('State', axis=1) #Drop State variable for later appending sums to nosubs
#nosubs.drop( nosubs[ nosubs['Country'] == 'US' ].index , inplace=True)
#df2 = nosubs.append(cruisesum) #add aggregated data to nosubs dataframe
df2 = nosubs.append(territorysum) #add territory sums
df2 = df2.append(subsum) #add sums for countries w/o territories
#df2 = df2.append(ussums) #add lower 48 sums

custom_dict = {'US' : 0, 'Belgium' : 1, 'Canada' : 3, 'France' : 4, 'Germany' : 5,
                      'Italy' : 6, 'Japan' :7, 'Korea, South': 8, 'Netherlands' :9, 'Norway' : 10,
                      'Portugal' : 11, 'Spain' : 12, 'Sweden' : 13, 'Switzerland' : 14,
                      'United Kingdom' : 15,'Egypt' : 16, 'South Africa' : 17, 'China' : 18,
                      'India' : 19, 'Indonesia' : 20, 'Iran' : 21, 'Philippines' : 22,
                      'Saudi Arabia' : 23, 'Singapore' : 24, 'Thailand' : 25, 'Poland' : 26, 
                      'Russia' : 27, 'Turkey' : 28, 'Brazil' : 29, 'Chile' : 30, 'Colombia' : 31, 
                      'Mexico' : 32, 'Peru' : 33}

interest_countries = ['US', 'Belgium', 'Canada', 'France', 'Germany','Italy', 'Japan',
                      'Korea, South', 'Netherlands', 'Norway','Portugal' , 'Spain' , 
                      'Sweden' , 'Switzerland' ,'United Kingdom' ,'Egypt' , 'South Africa', 
                      'China' , 'India' , 'Indonesia' , 'Iran' , 'Philippines',
                      'Saudi Arabia' , 'Singapore' , 'Thailand' , 'Poland' , 
                      'Russia', 'Turkey' , 'Brazil' , 'Chile' , 'Colombia' , 
                      'Mexico' , 'Peru' ]

int_states2 = ['Alabama', 'Arizona', 'California', 'Colorado','Connecticut','Florida', 'Georgia', 'Louisiana','Massachusetts', 'Nevada', 'New Mexico', 'New York', 'Oklahoma', 'Washington', 'South Carolina']

a = df2[df2.Country.isin(interest_countries)]
a = a.sort_values(by=['Country'])
b = df2[~df2.Country.isin(interest_countries)]
df2 = a.append(b)
poplm = pd.read_excel('pop land data.xlsx')
dem=pd.merge(poplm, df2, how='left', on= 'Country')
dem['Population'] = dem['Population (thousands)']*1000
dem = dem.drop('Population (thousands)', axis=1)

#######
df3 = df3.drop(['UID','iso2','iso3','code3','FIPS','Lat','Long_','Combined_Key'], axis=1)
df3 = df3.rename(columns={'Country_Region':'Country'})
State = df3.groupby(by='Province_State').sum().reset_index()
State.insert(0,'Admin2',"")
State.insert(2,'Country','US')
df2.insert(0,'Admin2',"")
df2.insert(1,'Province_State',"")
df4 = df2[df2.Country == 'US']
df4 = df4.append(State[State.Province_State == 'Texas'])
df4 = df4.append(df3[df3.Admin2 == 'Bexar'])
df4 = df4.append(State[State.Province_State.isin(int_states2)])
df4 = df4.append(df2[df2.Country == 'China'])
df4 = df4.append(df2[df2.Country == 'Belgium'])
df4 = df4.append(df2[df2.Country == 'Canada'])
df4 = df4.append(df2[df2.Country == 'France'])
df4 = df4.append(df2[df2.Country == 'Germany'])
df4 = df4.append(df2[df2.Country == 'Italy'])
df4 = df4.append(df2[df2.Country == 'Japan'])
df4 = df4.append(df2[df2.Country == 'Korea, South'])
df4 = df4.append(df2[df2.Country == 'Netherlands'])
df4 = df4.append(df2[df2.Country == 'Norway'])
df4 = df4.append(df2[df2.Country == 'Portugal'])
df4 = df4.append(df2[df2.Country == 'Spain'])
df4 = df4.append(df2[df2.Country == 'Sweden'])
df4 = df4.append(df2[df2.Country == 'Switzerland'])
df4 = df4.append(df2[df2.Country == 'United Kingdom'])
df4 = df4.append(df2[df2.Country == 'Egypt'])
df4 = df4.append(df2[df2.Country == 'South Africa'])
df4 = df4.append(df2[df2.Country == 'India'])
df4 = df4.append(df2[df2.Country == 'Indonesia'])
df4 = df4.append(df2[df2.Country == 'Iran'])
df4 = df4.append(df2[df2.Country == 'Philippines'])
df4 = df4.append(df2[df2.Country == 'Saudi Arabia'])
df4 = df4.append(df2[df2.Country == 'Singapore'])
df4 = df4.append(df2[df2.Country == 'Thailand'])
df4 = df4.append(df2[df2.Country == 'Poland'])
df4 = df4.append(df2[df2.Country == 'Russia'])
df4 = df4.append(df2[df2.Country == 'Turkey'])
df4 = df4.append(df2[df2.Country == 'Brazil'])
df4 = df4.append(df2[df2.Country == 'Chile'])
df4 = df4.append(df2[df2.Country == 'Colombia'])
df4 = df4.append(df2[df2.Country == 'Mexico'])
df4 = df4.append(df2[df2.Country == 'Peru'])
df4 = df4.drop('Population', axis=1)
df4 = df4.reset_index(drop=True)

#######
 
def  coldiff(data,interval=1):
    cols= np.arange(6,len(df4.columns)-1,1)
    a=df4.iloc[:,5]-df4.iloc[:,4]
    for i in cols:
        d=df4.iloc[:,i]-df4.iloc[:,i-interval]
        a=a.concat()

import datetime
import xlsxwriter

writer = pd.ExcelWriter('new_covid_data_'+datetime.date.today().strftime("%Y%m%d")+'.xlsx', engine='xlsxwriter')    
df4.to_excel(writer, sheet_name='Cumulative_Cases')
workbook = writer.book
worksheet = writer.sheets['Cumulative_Cases']
writer.save()
