#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 20:01:29 2018

@author: markditsworth
"""

import pandas as pd
import numpy as np
import datetime

def getBotAccts(acctFile):
    with open(acctFile,'rb') as fObj:
        acct_list = fObj.readlines()
    
    acctList = np.empty(len(acct_list),dtype=str)
    
    for idx,acct in enumerate(acct_list):
        acctList[idx] = acct.strip()
    
    return acctList

def botComments(dataset,acctFile):
    print 'Getting Bot Names...'
    acctList = getBotAccts(acctFile)
    
    print 'Reading dataset...'
    df = pd.read_json(dataset,lines=True)       # create dataframe from the comment data set
    
    df = df[df['author'].isin(acctList)]
    
    for author in acctList:
        print 'Analyzing %s\'s activity...'%author
        df1 = df[df['author'] == author]
        fname = author + '_activity.txt'
        count = 0
        for idx in df1.index.values:
            count += 1
            time = datetime.datetime.fromtimestamp(int(df1.loc[idx,'created_utc'])).strftime('%Y-%m-%d %H:%M:%S')
            with open(fname,'ab') as fObj:
                fObj.write(time+'\n')
        with open(fname,'ab') as fObj:
            fObj.write('%d comments total.'%(str(count)))
    print 'done.'

def main(argv):
    botnameFile = ''
    dataFile = ''
    
    while argv:
        if argv[0] == '-s':
            dataFile = argv[1]
        elif argv[0] == '-b':
            botnameFile = argv[1]
        argv = argv[1:]
    
    if botnameFile == '':
        print 'Error. Bot Account List Required. Use -b <file>'
    elif dataFile == '':
        print 'Error. Dataset file required. Use -s <file>'
    else:
        botComments(dataFile,botnameFile)
    
if __name__ == '__main__':
    from sys import argv
    main(argv)
    