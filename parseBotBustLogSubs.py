#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 19:58:06 2018

@author: markditsworth
"""
# Gets bot names from /r/BotBustLog submission history

import os
import json
import time


# Generator to create iterable structure of objects in dataset
def iterateJSONObjects(filename):
    line = '\n'
    with open(filename,'rb') as f:
        #for x in range(100000):
        while line != '':
            line = f.readline()
            yield line.strip()

# send dictionary to file as json string
def sendToFile(dic, filename):
    s = json.dumps(dic)
    s = s + '\n'
    with open(filename,'ab') as fObj:
        fObj.write(s)


def parse(filename_src,filename_dst):
    start = time.time()
    bot_count = 0
    unique_Names = []
    for item in iterateJSONObjects(filename_src):
        try:
            sub_info = json.loads(item)
            try:
                if sub_info['subreddit'] == 'BotBustLog':
                    botname = sub_info['title'].split(' ')[0]
                    if botname[0] == '/':
                        if botname not in unique_Names:
                            bot_count = bot_count+1
                            unique_Names.append(botname)
                            with open(filename_dst, 'ab') as fObj:
                                fObj.write(botname)
                                fObj.write('\n')
            except KeyError:
                pass
            
        except ValueError:
            if item == '':
                print 'End.'
            else:
                print 'Something went wrong...'
    
    duration = time.time()-start
    duration_hour = duration/3600
    duration_min = (duration_hour - int(duration_hour))*60
    duration_sec = (duration_min - int(duration_min))*60
    num = "{:,}".format(bot_count)
    print '%s bots found.'%num
    print 'Processing time: %d hours %d minutes %.2f seconds'%(duration_hour,duration_min,duration_sec)
    os.system('say "Program Finished"')

if __name__ == '__main__':
    file_name = 'RS_2017-11.txt'
    file_name_dst = 'Nov2017_BotList.txt'
    path = '/Volumes/My Passport for Mac/Grad/Networks and Systems'
    os.chdir(path)
    parse(file_name, file_name_dst)
