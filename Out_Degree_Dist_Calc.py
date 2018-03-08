#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  6 07:50:51 2018

@author: markditsworth
"""

import zen
import numpy as np
import traceback

def out_degree_dist(G,output_file):
    try:
        ddist = zen.degree.ddist(G,normalize=False,direction='out_dir')
        n = len(ddist)
        k = np.arange(n)
        
        ddist = ddist.reshape((n,1))
        k = k.reshape((n,1))
        
        deg_dist = np.concatenate((k,ddist),axis=1)
        
        np.savetxt(output_file,deg_dist,delimiter=',',fmt='%d')
        end_mes = 'Successfully written to: %s\n'%output_file
        print  'Out-Degree Distribution Saved...'
        
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
            G = zen.io.gml.read(network_file,weight_fxn= lambda x:x['weight'])
            #G = zen.generating.erdos_renyi(20,0.1,directed=True)
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
            log = './Logs/Out_Degree_Dist_Log_'+suff+'.txt'  # Create Log File Name
            # Out Degree
            result = out_degree_dist(G,'./Stats/out_degree_dist_'+suff+'.csv')
            with open(log,'wb') as fObj:
                fObj.write(result)
        
if __name__ == '__main__':
    from sys import argv
    main(argv)