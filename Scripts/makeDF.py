#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 09:12:35 2018

@author: markditsworth
"""

#import zen
#import numpy as np
import pandas as pd

print 'Importing Clustering Data...'
dfClust = pd.read_csv('../Stats/V2/clustering_coefficients_v2.csv',delimiter=',',names = ['Acct','Clustering'])
dfClust.set_index('Acct',inplace=True)
print '    done.'
print 'Importing Eigenvector Centrality Data...'
dfEig = pd.read_csv('../Stats/V2/eig_centrality_v2.csv',delimiter=',',names = ['Acct','Eigenvector'])
dfEig.set_index('Acct',inplace=True)
print '    done.'
print 'Importing In Degree Centrality Data...'
dfIn = pd.read_csv('../Stats/V2/in_degree_centrality_v2.csv',delimiter=',',names = ['Acct','In Degree'])
dfIn.set_index('Acct',inplace=True)
print '    done.'
print 'Importing Out Degree Centrality Data...'
dfOut = pd.read_csv('../Stats/V2/out_degree_centrality_v2.csv',delimiter=',',names = ['Acct','Out Degree'])
dfOut.set_index('Acct',inplace=True)
print '    done.'
print 'Importing Katz Rank Data...'
dfPage = pd.read_csv('../Stats/V2/katz_centrality_v2.csv',delimiter=',',names=['Acct','Katz'])
dfPage.set_index('Acct',inplace=True)
print '    done.'
print 'Joining DataFrames...'
df = pd.concat((dfClust,dfEig,dfIn,dfOut,dfPage),axis=1)
print 'Writing to pkl...'
df.to_pickle('NetworkStatsDF.pkl')
print 'Done.'
