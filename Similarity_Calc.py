#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 10:41:59 2018

@author: markditsworth
"""

# NEED TO TEST ON SMALL NETWORK!!!!!!!!!!!!!!!!!!!!!


import zen
import numpy as np

def similarity_matrix(A,tol,max_iter):
    alpha = 1
    sigma = np.zeros(A.shape)
    diff = 1
    iter_num = 0
    while diff < tol:
        if iter_num > max_iter:
            break
        else:
           sigma_new =  np.add(np.multiply(alpha,np.matmul(A,np.matmul(sigma,A))),np.identity(A.shape[0]))
           
           diff = np.mean(np.abs(np.subtract(sigma,sigma_new)))
           sigma = sigma_new
           iter_num += 1
           
    return sigma

def global_stats(S):
    # Compute global stats
    lower_quartile = np.percentile(S,25)
    median = np.percentile(S,50)
    upper_quartile = np.percentile(S,75)
    top_ten_percent = np.percentile(S,90)
    mean = np.mean(S)
    std = np.std(S)
    
    return mean, std, lower_quartile, median, upper_quartile, top_ten_percent

def indiv_stats(S,nodes_of_interest_,mean, std, lower_quartile, median, upper_quartile, top_ten_percent):
    sim = S[nodes_of_interest_[0],nodes_of_interest_[1]]
    
    mean_diff = (mean-sim)/std
        
    if sim >= top_ten_percent:
        pos_text = 'Upper 10'
    elif sim >= upper_quartile:
        pos_text = 'Upper Qrt'
    elif sim >= median:
        pos_text = 'Upper Half'
    elif sim >= lower_quartile:
        pos_text = 'Lower half'
    else:
        pos_text = 'Lower Qrt'
    
    return mean_diff,pos_text

def analyze(G,filename,tol,max_iter):
    bots_ = []
    for nidx in G.nodes_():
        if G.node_data_(nidx) == 'bot':
            bots_.append(nidx)
    
    A = G.matrix()
    S = similarity_matrix(A,tol,max_iter)
    mean,std,lq,median,up,top_ten = global_stats(S)
    
    for bot1_ in bots_:
        bot1 = G.node_object(bot1_)
        for bot2_ in bots_:
            bot2 = G.node_object(bot2_)
            mean_ref, pos = indiv_stats(S,[bot1_,bot2_],mean,std,lq,median,up,top_ten)
            report = '%20s   %20s   %.2f (%10s)\n'%(bot1,bot2,mean_ref,pos)
            with open(filename,'ab') as fObj:
                fObj.write(report)

    print 'Done.'

def main(argv):
    max_iter=1000
    tol=0.01
    while argv:
        if argv[0] == '-N':
            network_file = argv[1]
        elif argv[0] == '-t':
            tol = float(argv[1])
        elif argv[0] == '-i':
            max_iter = int(argv[1])
        argv = argv[1:]
    
    fname = './Stats/Bot_Similarities.txt'
    
    G = zen.io.gml.read(network_file,weight_fxn=lambda x:x['weight'])
    
    analyze(G,fname,tol,max_iter)

if __name__ == '__main__':
    from sys import argv
    main(argv)