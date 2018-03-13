#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 10:41:59 2018

@author: markditsworth
"""

# Fix similarity Algorithm

import zen
import numpy as np
#import matplotlib.pyplot as plt

def similarity_matrix(A,tol,max_iter):
    # Algorithmic Issue Here
    print 'starting similarity matrix...'
    min_iter = 50
    alpha = 3e-1
    sigma = np.zeros(A.shape)
    diff = 1
    iter_num = 0
    max_iter_flag=0
    loop = 1
    while loop:
        sigma_new =  np.add(np.multiply(alpha,np.matmul(A,np.matmul(sigma,A))),np.identity(A.shape[0]))
        #print sigma_new
        diff = np.mean(np.abs(np.subtract(sigma,sigma_new)))
        sigma = sigma_new
        iter_num += 1
        if iter_num > min_iter:
            if diff < tol:
                loop = 0
            elif iter_num > max_iter:
                loop = 0
    if iter_num >= max_iter:
        max_iter_flag=1
       
    return sigma,max_iter_flag

def global_stats(S):
    # Compute global stats
    mean = np.mean(S)
    std = np.std(S)
    
    return mean, std

def indiv_stats(S,nodes_of_interest_,mean, std):
    sim = S[nodes_of_interest_[0],nodes_of_interest_[1]]
    #print mean,sim,std
    #mean_diff = (mean-sim)/std
    
    return sim

def analyze(G,filename,tol,max_iter):
    bots_ = []
    for nidx in G.nodes_():
        try:
            BOT = G.node_data_(nidx)['zenData']
        except KeyError:
            BOT = ''
        if BOT == 'bot':
            bots_.append(nidx)
    print 'bots found'
    A = G.matrix()
    #print A.dtype
    print 'Adjacency Matrix Created'
    S,flag = similarity_matrix(A,tol,max_iter)
    if flag:
        with open('./Logs/Similarity_Log.txt','ab') as fObj:
            fObj.write('Similarity Calculation Stopped at maximum iteration limit.\n')
            
    S = np.subtract(S,np.identity(S.shape[0]))
    #print S
    print 'similarity matrix created'
    
    mean,std = global_stats(S)
    print 'global stats found'
    for bot1_ in bots_:
        bot1 = G.node_object(bot1_)
        for bot2_ in bots_:
            bot2 = G.node_object(bot2_)
            mean_ref= indiv_stats(S,[bot1_,bot2_],mean,std)
            report = '%s,%s,%.2f\n'%(bot1,bot2,mean_ref)
            with open(filename,'ab') as fObj:
                fObj.write(report)
    
    h,bins=np.histogram(S.flatten(),bins=100)
    h = h.reshape((len(h),1))
    #print h.shape
    bins = bins[1:].reshape((len(bins)-1,1))
    #print bins.shape
    
    X = np.concatenate((bins,h),axis=1)
    np.savetxt('./Stats/Similarity_Histogram.csv',X,delimiter=',')
    
    '''
    X = np.loadtxt('Similarity_Histogram.csv',delimiter=',')
    bins = X[:,0].flatten()
    height = X[:,1].flatten()
    
    plt.bar(bins,height,width=-0.01,align='edge',log=True)
    plt.show()'''
    
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
    print 'Args parsed'
    fname = './Stats/Bot_Similarities.txt'
    
    G = zen.io.gml.read(network_file,weight_fxn=lambda x:x['weight'])
    print 'network loaded'
    analyze(G,fname,tol,max_iter)

if __name__ == '__main__':
    from sys import argv
    main(argv)