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
df = pd.read_pickle('../Stats/NetworkStatsDF.pkl')
df.drop(index='Node_For_Comments_On_Submission:',inplace=True)

botlist = np.loadtxt('../Nov2017_BotList_update.txt',dtype=str)
botlist = [bot.split('/')[-1] for bot in botlist]
dfBot = df.loc[botlist,:]

#%% Plotting
plt.figure(figsize=(12,8))
plt.scatter(df['Out Degree'].values,df['Eigenvector'].values,s=1,c='k', label='All Accounts')
plt.scatter(dfBot['Out Degree'].values,dfBot['Eigenvector'].values,s=30,marker='+',c='r',label='Bot Accounts')
plt.xlabel('Out Degree Centrality')
plt.ylabel('Eigenvector Centrality')
plt.legend(loc='upper right')
plt.show()

#%% Sampling
#interesting_accts = df[(df['Clustering']<0.0018) & (df['In Degree']>250)].index.values
#interesting_accts = df[df['Clustering']>0.03].index.values
#interesting_accts = df[(df['Clustering']<0.0018) & (df['Out Degree']>250)].index.values

drop_accts = df[df['Clustering']>=0.0018].index.values
selected_accts = df[df['Clustering']<0.0018].index.values

# For getting interesting_accts that are NOT in botlist
#interesting_accts1 = np.setdiff1d(interesting_accts,botlist,assume_unique=True)
# For getting interesting_accts that ARE in botlist
#interesting_accts1 = np.intersect1d(interesting_accts,botlist)

#drop_list = np.setdiff1d(df.index.values,selected_accts,assume_unique=True)

#print len(interesting_accts)
#print len(interesting_accts1)
print len(selected_accts)
for acct in drop_accts:
    with open('Droplist_for_sample.txt','ab') as fObj:
        #fObj.write('www.reddit.com/u/'+acct+'\n')
        fObj.write(acct+'\n')


print 'Done.'