#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
@author: markditsworth
"""

import os
import json

file_name = 'RC_2017-11.txt'
small_file_name = 'Reduced_Comments.txt'
path = '/Volumes/My Passport for Mac/Grad/Networks and Systems'
os.chdir(path)

# Generator to create iterable structure of objects in dataset
def iterateJSONObjects(filename,n):
    line = '\n'
    f = open(filename,'rb')
    for x in range(n):
        line = f.readline()
        yield line.strip()
    f.close()

# send dictionary to file as json string
def sendToFile(dic, filename):
    s = json.dumps(dic)
    s = s + '\n'
    f = open(filename,'ab')
    f.write(s)
    f.close()

def parse(filename):
    for item in iterateJSONObjects(filename):
        try:
            comment_info = json.loads(item)
            # make file of subset
            sendToFile(comment_info,small_file_name)
            
        except ValueError:
            if item == '':
                print 'End.'
            else:
                print 'Something went wrong...'
    
if __name__ == '__main__':
    parse(file_name)
