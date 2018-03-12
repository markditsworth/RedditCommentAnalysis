#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  6 07:50:51 2018

@author: markditsworth
"""

import zen
import traceback
import pandas as pd

#networkfile = 'RedditNetwork_Nov_2017.gml'
#botfile = 'Nov2017_BotList.txt'

def clustering(G,output_file):
    try:
        c = zen.algorithms.clustering.__lcc_undirected(G)
        accts = G.nodes()
        S = pd.Series(data=c,index=accts)
        S.sort_values(ascending=False,inplace=True)
        S.to_csv(output_file)
        end_mes = 'Successfully written to: %s\n'%output_file
        print 'Clustering Info Saved...'
    except:
        end_mes = traceback.format_exc()
        print 'Error Occured: See Log.'
        
    return end_mes

def main(argv):
    p = 0
    network_file = ''
    bot_file = ''
    
    while argv:
        if argv[0] == '-p':
            p = float(argv[1])
            
        elif argv[0] == '-N':
            network_file = argv[1]
            
        elif argv[0] == '-B':
            bot_file = argv[1]
            
        argv = argv[1:]
    
    if network_file == '':
        print 'Error: Network File Required! Use flag -N'
    else:
        file_error_flag = 0
        try:
            #G = zen.io.gml.read(networkfile,weight_fxn= lambda x:x['weight'])
            G = zen.generating.erdos_renyi(20,0.1)
        except IOError:
            print 'Error: Invalid Network File Name.\n'
            file_error_flag = 1
        
        # Remove p percentage of bots (should be incremental or random?) [incremental right now]
        if p>0:
            try:
                with open(bot_file,'rb') as fObj:
                    bots = fObj.readlines()
                
                n = int(len(bots)*p)
                bots = bots[0:n]
                
                for bot in bots:
                    bot = bot.strip().split('/')[-1]
                    G.rm_node(bot)
            except IOError:
                print 'Error: Invalid Bot File Name.\n'
                file_error_flag = 1
                
        if not file_error_flag:  
            suff = '_'.join(str(p).split('.'))          # Suffix denotes bot removal percentage
            log = './Logs/Clustering_Log_'+suff+'.txt'  # Create Log File Name
            # Clustering
            result = clustering(G,'./Stats/clustering_'+suff+'.csv')
            with open(log,'wb') as fObj:
                fObj.write(result)
        
if __name__ == '__main__':
    from sys import argv
    main(argv)