#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 13:30:53 2018

@author: markditsworth
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
'''
df = pd.read_csv('../Stats/clustering_0.csv',delimiter=',',header=None)

bots = np.loadtxt('../Nov2017_BotList.txt',dtype=str)

coeffs = []

for bot in bots:
    bot = bot.split('/')[-1]
    #print bot
    try:
        coeffs.append(df[df[0]==bot][1].values[0])
    except IndexError:
        coeffs.append(np.NaN)

np.savetxt('bot_clustering_coefficients.csv',coeffs,fmt='%.9f')
print 'Done'''

ranks = np.loadtxt('bot_clustering_coefficients.csv',delimiter=',')
ranks = ranks[~np.isnan(ranks)]

# As percentile
#ranks = ranks / df.shape[0]

plt.hist(ranks,bins=200)
plt.xlabel('Clustering Coefficient')
plt.title('Bot Clustering Coefficients')
plt.show()
