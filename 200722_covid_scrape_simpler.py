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
rgcases=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
ruscases=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv')
rusdeaths=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv')
rgdeaths=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')

#Rename columns
dfgcases=rgcases.rename(columns={'Country/Region': 'Country', 'Province/State' : 'State'})
dfuscases=ruscases.rename(columns={'Country_Region': 'Country', 'Province_State' : 'State'})
dfgdeaths=rgdeaths.rename(columns={'Country/Region': 'Country', 'Province/State' : 'State'})
dfusdeaths=rusdeaths.rename(columns={'Country_Region': 'Country', 'Province_State' : 'State'}) 

#drop latitude longitudes
dfgcases = dfgcases.drop(['Lat','Long'], axis=1)
dfuscases = dfuscases.drop(['UID','iso2','iso3','code3','FIPS','Lat','Long_','Combined_Key'], axis=1)
dfusdeaths = dfusdeaths.drop(['UID','iso2','iso3','code3','FIPS','Lat','Long_','Combined_Key'], axis=1)
dfgdeaths = dfgdeaths.drop(['Lat','Long'], axis=1)


#create grand total 
dfgcases.loc['Global']=dfgcases.sum() 
dfgdeaths.loc['Global']=dfgdeaths.sum() 


#fill in Country column for total
dfgcases.loc['Global', 'Country']='Global' 
dfgdeaths.loc['Global', 'Country']='Global' 

#Create Country totals
dfgcases=dfgcases.groupby(by='Country').sum().reset_index()
dfgdeaths=dfgdeaths.groupby(by='Country').sum().reset_index()


interest_countries = ['US', 'Belgium', 'Canada', 'France', 'Germany','Italy', 'Japan',
                      'Korea, South', 'Netherlands', 'Norway','Portugal' , 'Spain' , 
                      'Sweden' , 'Switzerland' ,'United Kingdom' ,'Egypt' , 'South Africa', 
                      'China' , 'India' , 'Indonesia' , 'Iran' , 'Philippines',
                      'Saudi Arabia' , 'Singapore' , 'Thailand' , 'Poland' , 
                      'Russia', 'Turkey' , 'Brazil' , 'Chile' , 'Colombia' , 
                      'Mexico' , 'Peru' ]

int_states2 = ['Alabama', 'Arizona', 'California', 'Colorado','Connecticut','Florida', 'Georgia', 'Louisiana','Massachusetts', 'Nevada', 'New Mexico', 'New York', 'Oklahoma', 'Washington', 'South Carolina']



#Create state level data
statecases = dfuscases.groupby(by='State').sum().reset_index()
statedeaths = dfusdeaths.groupby(by='State').sum().reset_index()
statecases.insert(0,'Admin2',"")
statedeaths.insert(0,'Admin2',"")
statecases.insert(2,'Country','US')
statedeaths.insert(2,'Country','US')
dfgcases.insert(0,'Admin2',"")
dfgdeaths.insert(0,'Admin2',"")
dfgcases.insert(1,'State',"")
dfgdeaths.insert(1,'State',"")

#Global Cases in Wilbur Order
gcasesxl = dfgcases[dfgcases.Country == 'US']
gcasesxl = gcasesxl.append(statecases[statecases.State == 'Texas'])
gcasesxl = gcasesxl.append(dfuscases[dfuscases.Admin2 == 'Bexar'])
gcasesxl = gcasesxl.append(dfuscases[dfuscases.Admin2 == 'Harris'])
gcasesxl = gcasesxl.append(dfuscases[dfuscases.Admin2 == 'Dallas'])
gcasesxl = gcasesxl.append(dfuscases[dfuscases.Admin2 == 'Tarrant'])
gcasesxl = gcasesxl.append(dfuscases[dfuscases.Admin2 == 'Travis'])
gcasesxl = gcasesxl.append(dfuscases[dfuscases.Admin2 == 'Collin'])
gcasesxl = gcasesxl.append(dfuscases[dfuscases.Admin2 == 'Hidalgo'])
gcasesxl = gcasesxl.append(dfuscases[dfuscases.Admin2 == 'El Paso'])
gcasesxl = gcasesxl.append(statecases[statecases.State.isin(int_states2)])
gcasesxl = gcasesxl.append(dfgcases[dfgcases.Country == 'China'])
gcasesxl = gcasesxl.append(dfgcases[dfgcases.Country == 'Belgium'])
gcasesxl = gcasesxl.append(dfgcases[dfgcases.Country == 'Canada'])
gcasesxl = gcasesxl.append(dfgcases[dfgcases.Country == 'France'])
gcasesxl = gcasesxl.append(dfgcases[dfgcases.Country == 'Germany'])
gcasesxl = gcasesxl.append(dfgcases[dfgcases.Country == 'Italy'])
gcasesxl = gcasesxl.append(dfgcases[dfgcases.Country == 'Japan'])
gcasesxl = gcasesxl.append(dfgcases[dfgcases.Country == 'Korea, South'])
gcasesxl = gcasesxl.append(dfgcases[dfgcases.Country == 'Netherlands'])
gcasesxl = gcasesxl.append(dfgcases[dfgcases.Country == 'Norway'])
gcasesxl = gcasesxl.append(dfgcases[dfgcases.Country == 'Portugal'])
gcasesxl = gcasesxl.append(dfgcases[dfgcases.Country == 'Spain'])
gcasesxl = gcasesxl.append(dfgcases[dfgcases.Country == 'Sweden'])
gcasesxl = gcasesxl.append(dfgcases[dfgcases.Country == 'Switzerland'])
gcasesxl = gcasesxl.append(dfgcases[dfgcases.Country == 'United Kingdom'])
gcasesxl = gcasesxl.append(dfgcases[dfgcases.Country == 'Egypt'])
gcasesxl = gcasesxl.append(dfgcases[dfgcases.Country == 'South Africa'])
gcasesxl = gcasesxl.append(dfgcases[dfgcases.Country == 'India'])
gcasesxl = gcasesxl.append(dfgcases[dfgcases.Country == 'Indonesia'])
gcasesxl = gcasesxl.append(dfgcases[dfgcases.Country == 'Iran'])
gcasesxl = gcasesxl.append(dfgcases[dfgcases.Country == 'Philippines'])
gcasesxl = gcasesxl.append(dfgcases[dfgcases.Country == 'Saudi Arabia'])
gcasesxl = gcasesxl.append(dfgcases[dfgcases.Country == 'Singapore'])
gcasesxl = gcasesxl.append(dfgcases[dfgcases.Country == 'Thailand'])
gcasesxl = gcasesxl.append(dfgcases[dfgcases.Country == 'Poland'])
gcasesxl = gcasesxl.append(dfgcases[dfgcases.Country == 'Russia'])
gcasesxl = gcasesxl.append(dfgcases[dfgcases.Country == 'Turkey'])
gcasesxl = gcasesxl.append(dfgcases[dfgcases.Country == 'Brazil'])
gcasesxl = gcasesxl.append(dfgcases[dfgcases.Country == 'Chile'])
gcasesxl = gcasesxl.append(dfgcases[dfgcases.Country == 'Colombia'])
gcasesxl = gcasesxl.append(dfgcases[dfgcases.Country == 'Mexico'])
gcasesxl = gcasesxl.append(dfgcases[dfgcases.Country == 'Peru'])
gcasesxl = gcasesxl.reset_index(drop=True)


########Global Deaths in Wilbur Order
gdeathsxl = dfgdeaths[dfgdeaths.Country == 'US']
gdeathsxl = gdeathsxl.append(statedeaths[statedeaths.State == 'Texas'])
gdeathsxl = gdeathsxl.append(dfusdeaths[dfusdeaths.Admin2 == 'Bexar'])
gdeathsxl = gdeathsxl.append(dfusdeaths[dfusdeaths.Admin2 == 'Harris'])
gdeathsxl = gdeathsxl.append(dfusdeaths[dfusdeaths.Admin2 == 'Dallas'])
gdeathsxl = gdeathsxl.append(dfusdeaths[dfusdeaths.Admin2 == 'Tarrant'])
gdeathsxl = gdeathsxl.append(dfusdeaths[dfusdeaths.Admin2 == 'Travis'])
gdeathsxl = gdeathsxl.append(dfusdeaths[dfusdeaths.Admin2 == 'Collin'])
gdeathsxl = gdeathsxl.append(dfusdeaths[dfusdeaths.Admin2 == 'Hidalgo'])
gdeathsxl = gdeathsxl.append(dfusdeaths[dfusdeaths.Admin2 == 'El Paso'])
gdeathsxl = gdeathsxl.append(statedeaths[statedeaths.State.isin(int_states2)])
gdeathsxl = gdeathsxl.append(dfgdeaths[dfgdeaths.Country == 'China'])
gdeathsxl = gdeathsxl.append(dfgdeaths[dfgdeaths.Country == 'Belgium'])
gdeathsxl = gdeathsxl.append(dfgdeaths[dfgdeaths.Country == 'Canada'])
gdeathsxl = gdeathsxl.append(dfgdeaths[dfgdeaths.Country == 'France'])
gdeathsxl = gdeathsxl.append(dfgdeaths[dfgdeaths.Country == 'Germany'])
gdeathsxl = gdeathsxl.append(dfgdeaths[dfgdeaths.Country == 'Italy'])
gdeathsxl = gdeathsxl.append(dfgdeaths[dfgdeaths.Country == 'Japan'])
gdeathsxl = gdeathsxl.append(dfgdeaths[dfgdeaths.Country == 'Korea, South'])
gdeathsxl = gdeathsxl.append(dfgdeaths[dfgdeaths.Country == 'Netherlands'])
gdeathsxl = gdeathsxl.append(dfgdeaths[dfgdeaths.Country == 'Norway'])
gdeathsxl = gdeathsxl.append(dfgdeaths[dfgdeaths.Country == 'Portugal'])
gdeathsxl = gdeathsxl.append(dfgdeaths[dfgdeaths.Country == 'Spain'])
gdeathsxl = gdeathsxl.append(dfgdeaths[dfgdeaths.Country == 'Sweden'])
gdeathsxl = gdeathsxl.append(dfgdeaths[dfgdeaths.Country == 'Switzerland'])
gdeathsxl = gdeathsxl.append(dfgdeaths[dfgdeaths.Country == 'United Kingdom'])
gdeathsxl = gdeathsxl.append(dfgdeaths[dfgdeaths.Country == 'Egypt'])
gdeathsxl = gdeathsxl.append(dfgdeaths[dfgdeaths.Country == 'South Africa'])
gdeathsxl = gdeathsxl.append(dfgdeaths[dfgdeaths.Country == 'India'])
gdeathsxl = gdeathsxl.append(dfgdeaths[dfgdeaths.Country == 'Indonesia'])
gdeathsxl = gdeathsxl.append(dfgdeaths[dfgdeaths.Country == 'Iran'])
gdeathsxl = gdeathsxl.append(dfgdeaths[dfgdeaths.Country == 'Philippines'])
gdeathsxl = gdeathsxl.append(dfgdeaths[dfgdeaths.Country == 'Saudi Arabia'])
gdeathsxl = gdeathsxl.append(dfgdeaths[dfgdeaths.Country == 'Singapore'])
gdeathsxl = gdeathsxl.append(dfgdeaths[dfgdeaths.Country == 'Thailand'])
gdeathsxl = gdeathsxl.append(dfgdeaths[dfgdeaths.Country == 'Poland'])
gdeathsxl = gdeathsxl.append(dfgdeaths[dfgdeaths.Country == 'Russia'])
gdeathsxl = gdeathsxl.append(dfgdeaths[dfgdeaths.Country == 'Turkey'])
gdeathsxl = gdeathsxl.append(dfgdeaths[dfgdeaths.Country == 'Brazil'])
gdeathsxl = gdeathsxl.append(dfgdeaths[dfgdeaths.Country == 'Chile'])
gdeathsxl = gdeathsxl.append(dfgdeaths[dfgdeaths.Country == 'Colombia'])
gdeathsxl = gdeathsxl.append(dfgdeaths[dfgdeaths.Country == 'Mexico'])
gdeathsxl = gdeathsxl.append(dfgdeaths[dfgdeaths.Country == 'Peru'])
gdeathsxl = gdeathsxl.drop('Population', axis=1)
gdeathsxl = gdeathsxl.reset_index(drop=True)



import xlsxwriter

writer = pd.ExcelWriter('new_covid_data_.xlsx', engine='xlsxwriter')    
gcasesxl.to_excel(writer, sheet_name='Cumulative_Cases')
workbook = writer.book
worksheet = writer.sheets['Cumulative_Cases']
gdeathsxl.to_excel(writer, sheet_name='Cumulative_Deaths')
workbook = writer.book
worksheet = writer.sheets['Cumulative_Deaths']

writer.save()
