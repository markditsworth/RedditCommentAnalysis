#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  6 07:50:51 2018

@author: markditsworth
"""
# Degree Distributions Combine or Separate? (May be different distributions for each)
# Percolation, randomize bots at each step, or incrementally remove? Remove by highest degree etc.

# maybe look at changing edges (configuration model) to see how shuffeling affects
# similarity between nodes?
# DO THIS!!!!! ^^^^^^

# multithreading (under 50 cores) multiscreen

# bot model to continue the participation
import zen
import traceback
import pandas as pd


def centrality(G,output_file):
    try:
        v = zen.algorithms.centrality.eigenvector_centrality_(G,max_iter=1000,weighted=False)
        print len(v)
        print len(G.nodes_())
        accts = G.nodes()
        print len(accts)
        S = pd.Series(data=v,index=accts)
        S.sort_values(ascending=False,inplace=True)
        S.to_csv(output_file)
        mes = 'Successfully written to: %s\n'%output_file
        print 'Centraliy Info Saved...'
    except:
        mes = traceback.format_exc()
        print 'Error Occured: See Log.'
    return mes

def main(argv):
    p = 0
    network_file = ''
    stat_file_name = ''
    while argv:
        if argv[0] == '--remove-bots':
            p = 1
            
        elif argv[0] == '-N':
            network_file = argv[1]
            
        elif argv[0] == '-w':
            stat_file_name = argv[1]
            
        argv = argv[1:]
    
    if network_file == '':
        print 'Error: Network File Required! Use flag -N'
    elif stat_file_name == '':
        print 'Error: Stat File Required! Use Flag -w'
    else:
        file_error_flag = 0
        try:
            G = zen.io.gml.read(network_file,weight_fxn= lambda x:x['weight'])
            #G = zen.generating.erdos_renyi(20,0.1)
        except IOError:
            print 'Error: Invalid Network File Name.\n'
            file_error_flag = 1
        
        # Remove bot accounts if desired
        if p:
            for node in G.nodes():
                if G.node_data(node)['zenData'] == 'bot':
                    G.rm_node(node)
            
            G.compact()
            
        if not file_error_flag:  
            suff = '_'.join(str(p).split('.'))          # Suffix denotes bot removal percentage
            log = './Logs/Centrality_Log_'+suff+'.txt'  # Create Log File Name
            # Centrality
            #with open(log,'ab') as fObj:
            #    fObj.write('Eigenvector Centrality\n')
            result = centrality(G,'./Stats/'+stat_file_name)
            with open(log,'wb') as fObj:
                fObj.write(result)
        
if __name__ == '__main__':
    from sys import argv
    main(argv)