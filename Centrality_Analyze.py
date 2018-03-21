#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 13:30:53 2018

@author: markditsworth
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('../Stats/centrality_0.csv',delimiter=',',header=None)
'''
bots = np.loadtxt('../Nov2017_BotList.txt',dtype=str)

ranks = []

for bot in bots:
    bot = bot.split('/')[-1]
    #print bot
    try:
        ranks.append(df.index[df[0]==bot].tolist()[0] + 1)
    except IndexError:
        ranks.append(np.NaN)

np.savetxt('bot_eigenvalue_centrality_rankings.csv',ranks,fmt='%.1f')
'''
ranks = np.loadtxt('bot_eigenvalue_centrality_rankings.csv',delimiter=',')
ranks = ranks[~np.isnan(ranks)]
# As percentile
#ranks = ranks / df.shape[0]

plt.hist(ranks,bins=200)
plt.xlabel('Eigenvalue Centrality Ranking')
plt.title('Bot Centrality Rankings')
plt.show()    
print 'Done'