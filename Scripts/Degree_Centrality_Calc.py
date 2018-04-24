#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 18:03:16 2018

@author: markditsworth
"""

import zen
import traceback

def deg_cent(G,fname):
    try:
        for node in G.nodes():
            deg = G.degree(node)
            with open(fname,'ab') as fObj:
                fObj.write('%s,%d\n'%(node,deg))
        mes = 'Successfully Writen to %s'%fname
    except:
        mes = traceback.format_exc()
    
    return mes

def out_deg_cent(G,fname):
    try:
        for node in G.nodes():
            deg = G.out_degree(node)
            with open(fname,'ab') as fObj:
                fObj.write('%s,%d\n'%(node,deg))
        mes = 'Successfully Writen to %s'%fname
    except:
        mes = traceback.format_exc()
    
    return mes

def in_deg_cent(G,fname):
    try:
        for node in G.nodes():
            deg = G.in_degree(node)
            with open(fname,'ab') as fObj:
                fObj.write('%s,%d\n'%(node,deg))
        mes = 'Successfully Writen to %s'%fname
    except:
        mes = traceback.format_exc()
    
    return mes

def weighted_deg_cent(G,fname):
    try:
        for node in G.nodes():
            w = 0
            for neighbor in G.neighbors():
                try:
                    w += G.weight(node,neighbor)
                except zen.exceptions.ZenException:
                    w += G.weight(neighbor,node)
            
            with open(fname,'ab') as fObj:
                fObj.write('%s,%.3f\n'%(node,w))
        mes = 'Successfully written to %s'%fname
    
    except:
        mes = traceback.format_exc()
    
    return mes

def log(mes):
    with open('./Logs/Degree_Centrality_Log.txt','wb') as fObj:
        fObj.write(mes)

def main(argv):
    fname = ''
    NetworkFile = ''
    weighted=False
    direction = 'both'
    help_flag = 0
    
    # process arguments
    while argv:
        if argv[0] == '-h':
            help_flag == 1
        elif argv[0] == '-N':
            NetworkFile = argv[1]
        elif argv[0] == '-w':
            fname = argv[1]
        elif argv[0] == '--weighted':
            weighted = True
        elif argv[0] == '-d':
            direction = argv[1].lower()
        
        argv = argv[1:]
    
    # handle input errors
    if help_flag:
        print '   -h      help'
        print '   -N <filename.gml>        required for network input'
        print '   -w <filename.csv>        required for stat output'
        print '   --weighted               uses weights in calculation'
        print '   -d in/out/both(default)  specifies directionality'
        print ''
        print 'Logs in ./Logs/Degree_Centrality_Log.txt'
        print ''
    if NetworkFile == '':
        print 'Error: Requires an gml file. Use -N <file>'
    elif fname == '':
        print 'Error: Requires a filename for the stats. Use -w <file>'
    elif direction not in ['both','in','out']:
        print 'Error: Direction is either "in","out", or "both"(default)'
    else:
        G = zen.io.gml.read(NetworkFile,weight_fxn=lambda x:x['weight'])
        if not weighted:
            if direction == 'both':
                status = deg_cent(G,fname)
            elif direction == 'in':
                status = in_deg_cent(G,fname)
            else:
                status = out_deg_cent(G,fname)
        else:
            status = weighted_deg_cent(G,fname)
            
        log(status)
        print 'Done.'

if __name__ == '__main__':
    from sys import argv
    main(argv)
                
        


    
    
