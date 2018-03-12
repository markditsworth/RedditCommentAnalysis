#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 10:42:54 2018

@author: markditsworth
"""

# Shuffles network using the configuration model

import zen
import numpy as np

def configuration(G):
    # get stub numbers for each node
    in_deg, out_deg = degree_array(G)
    H = G.copy()
    
    # clear all edges
    for edge in H.edges():
        H.rm_edge(edge[0],edge[1])
    
    # get array of node indices, repeated k times, where k is the in/out degree of the node
    src = [idx for idx,deg in enumerate(out_deg) for x in range(int(deg))]
    dst = [idx for idx,deg in enumerate(in_deg) for x in range(int(deg))]
    
    # randomize source nodes to allow for randomized pairing
    np.random.shuffle(src)
    
    # connect nodes
    for i in range(len(src)):
        if H.has_edge_(src[i],dst[i]):
            eidx = H.edge_idx_(src[i],dst[i])
            H.set_weight_(eidx, H.weight_(eidx)+1)
        else:
            H.add_edge_(src[i],dst[i])
    
    return H

def degree_array(G):
    in_degree = np.zeros(G.num_nodes)
    out_degree = np.zeros(G.num_nodes)
    
    for nidx in G.nodes_():
        in_degree[nidx] = G.in_degree_(nidx)
        out_degree[nidx] = G.out_degree_(nidx)
    
    return in_degree, out_degree

def main(argv):
    while argv:
        if argv[0] == '-N':
            network_file = argv[1]
            
        elif argv[0] == '-C':
            config_mdl_file = argv[1]
            
        argv = argv[1:]
    try:
        G = zen.io.gml.read(network_file,weight_fxn= lambda x:x['weight'])
        conf_mdl = configuration(G)
        zen.io.gml.write(conf_mdl,config_mdl_file)
        with open('./Logs/Config_Model_Log.txt','wb') as fObj:
            fObj.write('Successfully written to %s.'%config_mdl_file)
    except:
        import traceback
        err = traceback.format_exc()
        with open('./Logs/Config_Model_Log.txt','wb') as fObj:
            fObj.write(err)
        
if __name__ == '__main__':
    from sys import argv
    main(argv)