#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 19:58:06 2018

@author: markditsworth
"""

'''
Creates a directed graph from Reddit Comments.
Nodes: Accounts
Node Data: 'bot' if account is a known bot account
            empty if not
Edges: directed from an account A to account B, where A has replied to a comment by B
Edeg Weight: ammount of information sent from one account to another via replying
             (accounts for hyperlinks)
             
################################################################################  
##  WARNING: This program will require AT LEAST 40 GB of RAM. Do not run without appropriate
##           memory available.
################################################################################
'''

import os
import time
import pandas as pd
import zen
import numpy as np
import sys

#  JSON Dictorary Contents
#           {'author':username,'comment_len':comment_length,'comment_id':comment_id,
#            'parent_id':parent_id,'score':score,'controversiality':contro,
#            'pic_link_num':pic_num, 'reddit_link_num':reddit_num,'gen_link_num':link_num}

def makeNetwork(dataset,bot_list,gml_dst,error_log):
    start = time.time()                         # Get initial time
    error_flag=0
    G = zen.DiGraph()                           # Initialize directed graph
    
    bots = np.loadtxt(bot_list,dtype=str)       # create array of known bot accounts
    
    df = pd.read_json(dataset,lines=True)       # create dataframe from the comment data set
    df.set_index('comment_id',inplace=True)     # index by comment id for easy searching
    
    stats = df.describe()                       # calculate average upper quartile comment length
    reddit_scale = np.mean([stats['comment_len']['max'],stats['comment_len']['75%']])
    
    for commentID in df.index.values:           # for each comment
        username = df['author'][commentID]      # get the username
        parentID = df['parent_id'][commentID]   # get the id of the parent comment
        try:
            parent = df['author'][parentID]     # get the usename of the parent commentor
            if username != '[deleted]' and parent != '[deleted]':    #ignore deleted comments (unknown account)
                # Calculate the information score
                info_score = df['comment_len'][commentID]
                info_score += df['gen_link_num'][commentID]*1100
                info_score += df['reddit_link_num'][commentID]*reddit_scale
                info_score += df['pic_link_num'][commentID]*500
                
                G.add_edge(username,parent,weight=info_score)   # add edge
                # if username is a known bot, mark the node as such
                # add /u/ prefix to allow for botname matching
                if '/u/'+username in bots:
                    G.set_node_data(username,'bot')
        
        # If the edge already exists, add the new information score to the existing edge weight
        except zen.exceptions.ZenException:
            w = G.weight(username,parent) + info_score
            G.set_weight(username,parent,w)
            
        # If the parent ID is not in the dataset, don't add an edge    
        except KeyError:
            pass
        
        # If an unanticipated error happens, log it
        except:
            error_flag = 1
            error_msg = sys.exc_info()
            TYPE = error_msg[0]
            VALUE = error_msg[1]
            TB = error_msg[2]
            error_str = '\n' + TYPE + '\n' + VALUE + '\n' + TB + '\n'
            with open(error_log, 'ab') as fObj:
                fObj.write(error_str)
    # Write GML file
    zen.io.gml.write(G,gml_dst)
    
    duration = time.time()-start
    duration_hour = duration/3600
    duration_min = (duration_hour - int(duration_hour))*60
    duration_sec = (duration_min - int(duration_min))*60
    N = "{:,}".format(G.num_nodes)
    E = "{:,}".format(G.num_edges)
    with open('Output.txt','wb') as fObj:
        fObj.write('%s nodes, %s edges.\n'%(N,E))
        fObj.write('Processing time: %d hours %d minutes %.2f seconds'%(duration_hour,duration_min,duration_sec))
    
    if error_flag:
        with open('Output.txt','ab') as fObj:
            fObj.write('\n\nERRORS ENCOUNTERED')

if __name__ == '__main__':
    botList_filename = 'Nov2017_BotList.txt'
    dataset_filename = '/localdisk/RC_parsed_Nov_2017.txt'
    gml_file = 'RedditNetwork_Nov_2017.gml'
    error_log = 'Error_Log.txt'
    #path = '/Volumes/My Passport for Mac/Grad/Networks and Systems'
    #os.chdir(path)
    makeNetwork(dataset_filename,botList_filename,gml_file,error_log)