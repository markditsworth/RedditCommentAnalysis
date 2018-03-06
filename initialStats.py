#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  6 07:50:51 2018

@author: markditsworth
"""

import zen
import numpy as np

networkfile = 'RedditNetwork_Nov_2017.gml'
deg_dist_outfile = 'Degree_Distribution.csv'


def degree_dist(G,output_file):
    ddist = zen.degree.ddist(G,normalize=False)
    n = len(ddist)
    k = np.arange(n)
    
    ddist = ddist.reshape((n,1))
    k = k.reshape((n,1))
    
    deg_dist = np.concatenate((k,ddist),axis=1)
    
    np.savetxt(output_file,deg_dist,delimiter=',')
    print  'Degree Distribution Saved...'
    return

def cocitation(G,output_file):
    print 'Cocitation Saved...'
    return

def centrality(G,output_file):
    print 'Centraliy Info Saved...'
    return



if __name__ == '__main__':
    pass