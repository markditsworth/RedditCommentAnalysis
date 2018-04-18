#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 10:33:35 2018

@author: markditsworth
"""

import zen

def component(G,logFile,threshold):
    H = G.skeleton()
    
    print 'Finding Components...'
    components = zen.algorithms.components(H)
    
    idx = 1
    print 'Saving Components...'
    for comp in components:
        fname = 'component_%d.csv'%idx
        c = np.array(comp)
        np.savetxt(fname,c,fmt='%s')
        print 'Saved %s...'%fname
        idx += 1
    with open(logFile,'wb') as f:
        f.write('%d Components found.'%idx)
    
    small_components = []
    
    print 'Removing small components...'
    for comp in components:
        if len(comp) < threshold:
            small_components.append(comp)
        
    del components
    
    for comp in small_components:
        if node in comp:
            H.rm_node(node)
    
    print 'Finding Communities...'
    from zen.algorithms.community import louvain
    cset = louvain(H)
    
    with open(logFile,'ab') as f:
        f.write('\n%d Communities found.'%(cset.communities().__len__()))
    
    print 'Saving Community info...'
    
    for comm in cset.communities():
        with open('reddit_communities.csv','ab') as fObj:
            fObj.write(','.join(comm.nodes()))
            fObj.write('\n')
            
    print 'Done.'

def main(argv):
    networkFile = ''
    logFile = 'Community_Output.txt'
    threshold = 100
    while argv:
        if argv[0] == '-N':
            networkFile = argv[1]
        elif argv[0] == '-t':
            threshold = int(argv[1])
        argv = argv[1:]
    
    if networkFile == '':
        print 'Error: Requries Network GML File. Use -N <file>'
    else:
        print 'Reading Network...'
        G = zen.io.gml.read(networkFile)
        
        component(G,logFile,threshold)

if __name__ == '__main__':
    from sys import argv
    main(argv)
        
        
    
    
    
    
    
    
    
    

    