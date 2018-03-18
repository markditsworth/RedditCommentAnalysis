#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 17 19:13:56 2018

@author: markditsworth
"""

# Changes node names in Zen GML file to ensure
# that no names have only integer names by 
# appending an underscore

def fix(src_file,dst_file):
    with open(src_file,'rb') as fObj:
        lines = fObj.readlines()
    
    for line in lines:
        if '\tname' in line:
            a = line.find('"')+1
            #print a
            b = line.find('"',a)
            #print b
            lineA = line[:a]
            lineB = line[a:b]
            lineC = line[b:]
            try:
                dummy = int(lineB)
                lineB = lineB + '_'
            except ValueError:
                pass
            line = lineA+lineB+lineC
        
        with open(dst_file,'ab') as fObj:
            fObj.write(line)
   
def main(argv):
    src_gml = ''
    dst_gml = ''
    while argv:
        if argv[0] == '-s':
            src_gml = argv[1]
            
        elif argv[0] == '-d':
            dst_gml = argv[1]
            
        argv = argv[1:]
    
    if src_gml == '':
        print 'Error: Must provide a source gml file (-s)'
        
    elif dst_gml == '':
        print 'Error: Must provide a destination gml file (-d)'
        
    else:
        fix(src_gml,dst_gml)
        print 'Done.'
if __name__ == '__main__':
    from sys import argv
    main(argv)