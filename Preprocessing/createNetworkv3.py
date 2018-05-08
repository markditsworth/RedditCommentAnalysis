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
##  WARNING: This program will require AT LEAST 30 GB of RAM. Do not run without appropriate
##           memory available.
################################################################################
'''

import time
import pandas as pd
import zen
import numpy as np
import traceback

#  JSON Dictorary Contents
#           {'author':username,'comment_len':comment_length,'comment_id':comment_id,
#            'parent_id':parent_id,'score':score,'controversiality':contro,
#            'pic_link_num':pic_num, 'reddit_link_num':reddit_num,'gen_link_num':link_num}

def handleNumeric(name):
    try:
        dummy = int(name)
        name = name + ':USER'
    except ValueError:
        pass
    finally:
        return name

def makeNetwork(dataset,sub_dataset,gml_dst,error_log):
    start = time.time()                         # Get initial time
    error_flag=0
    G = zen.DiGraph()                           # Initialize directed graph
    
    G.add_node('Node_For_Comments_On_Submission:')
    
    #bots = np.loadtxt(bot_list,dtype=str)       # create array of known bot accounts
    
    dfSub = pd.read_json(sub_dataset,lines=True)    # add submission id information
    submission_ids = dfSub['id'].values
    del dfSub
    
    df = pd.read_json(dataset,lines=True)       # create dataframe from the comment data set
    df.set_index('id',inplace=True)     # index by comment id for easy searching
    
    #stats = df.describe()                       # calculate average upper quartile comment length
    #reddit_scale = np.mean([stats['comment_len']['max'],stats['comment_len']['75%']])
    
    for commentID in df.index.values:           # for each comment
        username = df['author'][commentID]      # get the username
        username = handleNumeric(username)
        parentID = df['parent_id'][commentID]   # get the id of the parent comment
        try:
            parent = df['author'][parentID]     # get the usename of the parent commentor
            parent = handleNumeric(parent)
            if username != '[deleted]' and parent != '[deleted]':    #ignore deleted comments (unknown account)
                
                G.add_edge(username,parent)   # add edge
                # if username is a known bot, mark the node as such
                # add /u/ prefix to allow for botname matching
                #if '/u/'+username in bots:
                    #G.set_node_data(username,'bot')
        
        # If the edge already exists, add the new information score to the existing edge weight
        except zen.exceptions.ZenException:
            #w = G.weight(username,parent) + info_score
            #G.set_weight(username,parent,w)
            continue
            
        # If the parent ID is not in the dataset, check if parent is a submission    
        except KeyError:
            if parentID in submission_ids:
                try:
                    G.add_edge(username,'Node_For_Comments_On_Submission:')
                except zen.exceptions.ZenException:
                    #w = G.weight(username,'Node_For_Comments_On_Submission:') + info_score
                    #G.set_weight(username,'Node_For_Comments_On_Submission:',w)
                    continue
        
        # If an unanticipated error happens, log it
        except:
            err = traceback.format_exc()
            with open(error_log, 'ab') as fObj:
                fObj.write(err)
                fObj.write('\n')
                
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

def main(argv):
    comment_file = ''
    sub_file = ''
    gml_file = ''
    error_log = 'Network_Creation_Error_Log.txt'
    while argv:
        if argv[0] == '-N':
            gml_file = argv[1]
        elif argv[0] == '-C':
            comment_file = argv[1]
        elif argv[0] == '-S':
            sub_file = argv[1]
        elif argv[0] == '-e':
            error_log = argv[1]
        argv = argv[1:]
    
    if comment_file == '':
        print 'Error: Requires Comment File -C <filename>'
    elif sub_file == '':
        print 'Error: Requires Submission File -S <filename>'
    elif gml_file == '':
        print 'Error: Requires Output Network file -N <filename.gml>'
    else:
        makeNetwork(comment_file,sub_file,gml_file,error_log)
        print 'Done'

if __name__ == '__main__':
    from sys import argv
    main(argv)