#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 19:58:06 2018

@author: markditsworth
"""
# Question: Is it a good or bad idea to combine multiple information types into an edge's weight?

import os
import json
import time
import re


# Generator to create iterable structure of objects in dataset
def iterateJSONObjects(filename):
    line = '\n'
    with open(filename,'rb') as f:
        #for x in range(10000):
        while line != '':
            line = f.readline()
            yield line.strip()

# send dictionary to file as json string
def sendToFile(dic, filename):
    s = json.dumps(dic)
    s = s + '\n'
    #with open(filename,'ab') as fObj:
    fObj = open(filename,'ab')
    fObj.write(s)
    fObj.close()

# check if string is a URL
def isLink(string):
    http = string.find('http')+1
    https = string.find('https')+1
    
    if http != 0 or https != 0:
        return True
    else:
        return False 

# check for image (url ends in .png, .jpg, .jpeg, .gif or contains imgur.com)
def isImage(link):
    filetypes = ['.jpg','.png','.jpeg','.gif']
    image = False
    for ftype in filetypes:
        if link.find(ftype) != -1:
            image = True
    if not image:
        idx = link.find('.com')
        if link[idx-5:idx] == 'imgur':
            image = True
    return image

# check for reddit
def isInternal(link):
    reddit = False
    idx = link.find('.com')
    if link[idx-6:idx] == 'reddit':
        reddit = True
    return reddit

def scoreForLinks(string):
    reddit_links = 0
    image_links = 0
    other_links = 0
    penalty = 0
    for x in re.finditer(r'\[(.*?)\]\((.*?)\)',string):  # find '[___](________)' pattern
        link = x.group(2)
        hyperlink = x.group(1)
        if isLink(link):
            if isImage(link):
                image_links += 1
            elif isInternal(link):
                reddit_links += 1
            else:
                other_links += 1
            penalty = penalty + len(hyperlink.split(' '))
    return [reddit_links,image_links,other_links,penalty]

def parse(filename_src,filename_dst):
    start = time.time()
    comment_count = 0
    for item in iterateJSONObjects(filename_src):
        try:
            comment_count = comment_count+1
            comment_info = json.loads(item)
            comment = comment_info['body']
            comment_length = len(comment.split(' '))
            
            reddit_num,pic_num,link_num,penalty = scoreForLinks(comment)
            
            comment_length = comment_length - penalty # neglect words in hyperlink
            
            username = comment_info['author']
            
            comment_id = comment_info['id']
            
            parent_id = comment_info['parent_id'].split('_')[1]
            
            score = comment_info['score']
            
            contro = comment_info['controversiality']
            
            # create new dictionary of relevant data
            d = {'author':username,'comment_len':comment_length,'comment_id':comment_id,
                 'parent_id':parent_id,'score':score,'controversiality':contro,
                 'pic_link_num':pic_num, 'reddit_link_num':reddit_num,'gen_link_num':link_num}
            
            sendToFile(d,filename_dst)
            '''
            if comment_id == 'dp61rmh':
                print comment
                print 'parent id: %s'%parent_id
            elif comment_id == 'dp6276x':
                print comment
                print 'parent ID: %s'%parent_id
                '''
        except ValueError:
            if item == '':
                print 'End.'
            else:
                print 'Something went wrong...'
        
        except KeyError:
            print 'Key Error'
            sendToFile(comment_info,'ErrorLog.txt')
            
    
    duration = time.time()-start
    duration_hour = duration/3600
    duration_min = (duration_hour - int(duration_hour))*60
    duration_sec = (duration_min - int(duration_min))*60
    num = "{:,}".format(comment_count)
    print '%s comments analyzed.'%num
    print 'Processing time: %d hours %d minutes %.2f seconds'%(duration_hour,duration_min,duration_sec)
    os.system('say "Program Finished"')

if __name__ == '__main__':
    file_name = 'RC_2017-11.txt'
    file_name_dst = 'RC_parsed_Nov_2017.txt'
    path = '/Volumes/My Passport for Mac/Grad/Networks and Systems'
    os.chdir(path)
    parse(file_name, file_name_dst)