#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 09:28:02 2018

@author: markditsworth
"""

import zen
import numpy as np
import pandas as pd

def katz(G,tol,max_iter,alpha,beta):
    iteration = 0
    centrality = np.zeros(G.num_nodes)
    while iteration < max_iter:
        iteration += 1          # increment iteration count
        centrality_old = centrality.copy()
        
        for node in G.nodes_():
            Ax = 0
            for neighbor in G.in_neighbors_(node):
                #weight = G.weight_(G.edge_idx_(neighbor,node))
                #Ax += np.multiply(centrality[neighbor],weight)
                
                Ax += centrality[neighbor]      #exclude weight due to overflow in multiplication
                
            centrality[node] = np.multiply(alpha,Ax)+beta
        
        if np.sum(np.abs(np.subtract(centrality,centrality_old))) < tol:
            return centrality
    
    return 'Failed to converge in %d iterations.'%max_iter

def writeStat(cent,G,filename):
    node_names = G.nodes()
    v = pd.Series(data=cent,index=node_names)
    v.to_csv(filename)

def main(argv):
    networkFile = ''
    outFile = ''
    tolerance = 0.01
    alpha = 0.85
    beta = 1.0
    maxi=500
    while argv:
        if argv[0] == '-N':
            networkFile = argv[1]
        elif argv[0] == '-w':
            outFile = argv[1]
        elif argv[0] == '--tolerance':
            tolerance = float(argv[1])
        elif argv[0] == '--alpha':
            alpha = float(argv[1])
        elif argv[0] == '--max-iter':
            maxi = int(argv[1])
        elif argv[0] == '--beta':
            beta = float(argv[1])
        argv = argv[1:]
    
    if networkFile == '':
        print 'Error! Network file required. Use -N <filename.gml>'
    elif outFile == '':
        print 'Error! Out file required. Use -w <filename.csv>'
    else:
        print 'Reading Network File...'
        G = zen.io.gml.read(networkFile,weight_fxn=lambda x:x['weight'])
        print 'Network Created.'
        print 'Calculating Katz centrality...'
        centrality = katz(G,tolerance,maxi,alpha,beta)
        
        if type(centrality) == str:
            with open('Logs/Katz_Centrality_Log.txt','wb') as fObj:
                fObj.write(centrality)
            print centrality
        else:
            print 'Katz centrality calculated'
            print 'Writing to file...'
            writeStat(centrality,G,outFile)
            with open('Logs/Katz_Centrality_Log.txt','wb') as fObj:
                fObj.write('Katz Centrality successfully calculated and written.')
            print 'Done.'
        
if __name__ == '__main__':
    from sys import argv
    main(argv)
    
