#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 10:28:10 2018

@author: markditsworth
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#%% DataFrame creation
df = pd.read_pickle('../Stats/V2/NetworkStatsDF.pkl')
#df = pd.read_pickle('../Stats/config/Config_NetworkStatsDF.pkl')
df.drop(index='Node_For_Comments_On_Submission:',inplace=True)

botlist = np.loadtxt('../Nov2017_BotList_update.txt',dtype=str)
botlist = [bot.split('/')[-1] for bot in botlist]
dfBot = df.loc[botlist,:]

#%% Plotting
plt.figure(figsize=(12,8))
plt.scatter(df['In Degree'].values,df['Clustering'].values,s=1,c='k', label='All Accounts')
plt.scatter(dfBot['In Degree'].values,dfBot['Clustering'].values,s=30,marker='+',c='r',label='Bot Accounts')
plt.xlabel('In Degree Centrality')
plt.ylabel('Clustering Coefficient')
plt.legend(loc='upper right')
plt.show()

#%% Sampling
#interesting_accts = df[(df['Clustering']<0.0018) & (df['In Degree']>250)].index.values
#interesting_accts = df[df['Clustering']>0.03].index.values
interesting_accts = df[(df['Clustering']<0.0018) & (df['Out Degree']>250)].index.values

# For getting interesting_accts that are NOT in botlist
interesting_accts1 = np.setdiff1d(interesting_accts,botlist,assume_unique=True)
# For getting interesting_accts that ARE in botlist
#interesting_accts1 = np.intersect1d(interesting_accts,botlist)


print len(interesting_accts)
print len(interesting_accts1)

for acct in interesting_accts1:
    with open('Check_These_Clustering_Out.txt','ab') as fObj:
        fObj.write('www.reddit.com/u/'+acct+'\n')
        #fObj.write(acct+'\n')


print 'Done.'