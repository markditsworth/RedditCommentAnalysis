#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 10:13:41 2018

@author: markditsworth
"""

import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

def power(x,a,c):
    y = np.power(x,-1*a) + c
    return y

def inverse(x,a):
    y = np.divide(a,x)
    return y

df = pd.read_pickle('../Stats/config/Config_NetworkStatsDF.pkl')
df.drop(index='Node_For_Comments_On_Submission:',inplace=True)
df = df[df['Clustering'] > 0]
df = df[df['Out Degree'] < 2500]
y = df['Clustering'].values
x = df['Out Degree'].values

#popt,_ = curve_fit(power,x,y)
popt,_ = curve_fit(inverse,x,y)
x_ = np.arange(2000)
y_ = inverse(x_,popt[0])

# Uncomment to show trendline on real-data instead of the configuration model
#df = pd.read_pickle('../Stats/V2/NetworkStatsDF.pkl')
#df.drop(index='Node_For_Comments_On_Submission:',inplace=True)
botlist = np.loadtxt('../Nov2017_BotList_update.txt',dtype=str)
botlist = [bot.split('/')[-1] for bot in botlist]
dfBot = df.loc[botlist,:]

plt.figure(figsize=(12,8))
plt.scatter(df['Out Degree'].values,df['Clustering'].values,s=1,c='k',label='All Accounts')
plt.scatter(dfBot['Out Degree'].values,dfBot['Clustering'].values,s=30,marker='+',c='r',label='Bot Accounts')
plt.plot(x_,y_,color='g',label='Config Model Trend',linewidth=3)
plt.xlabel('Out Degree Centrality')
plt.ylabel('Clustering Coefficient')
plt.legend(loc='upper right')
plt.show()