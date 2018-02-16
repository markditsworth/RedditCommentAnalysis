#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 09:59:48 2018

@author: markditsworth
"""


# Scrapes /r/BotBustLog to compile a list of known bot accountus during a secified duration of time

import urllib2

def genUniqueNumbers(n):
    ''' returns list of n unique numbers to be used in the User-Agent String'''
    import random
    count = 0
    m = int(n*1.5)
    strings = [0]*m
    while count < m:
        strings[count] = random.randint(1,99999999)
        count += 1
    
    s = list(set(strings))
    try:
        s = s[0:n]
        return s
    
    except IndexError:
        print 'Error: Not enough unique random values were generated'


def fetchHTML(url, UserAgentString):
    ''' gets html data from url, using the given User-Agent String '''
    req = urllib2.Request(url,headers={'User-Agent':UserAgentString})
    resp = urllib2.urlopen(req)
    return resp.read()


def findBotAccts(url,log_file,time_frame,durations):
    ''' Inputs:
        url:        [str] url of subreddit
        log_file:   [str] text file to save bot account usernames to
        time_frame: [str] time frame to parse by: (minutes,hour,day,month,year)
        durations:  [list of strings] how many "time_frames" to include
        '''
    from bs4 import BeautifulSoup as BS
    time_frame_s = time_frame + 's'
    random_number = genUniqueNumbers(500)
    idx = 0
    bot_count = 0
    loop = True
    while loop:
        print url
        usr_agent_str = "Mozilla/5.0 (X11; U; Linux i686) Gecko/%d Firefox/2.0.0.11"%(random_number[idx])
        idx += 1
        if idx == len(random_number):
            idx = 0
        
        html = fetchHTML(url,usr_agent_str)
        # get iterable of posts on page
        soup = BS(html,'html.parser')
        d = soup.find_all('div')
        botnames = []
        for D in d:
            e=D.find_all('div')
            for E in e:
                f = E.find_all('div')
                for F in f:
                    if F.get('class') == [u'top-matter']:
                        g = F.find_all('p')
                        info_for_botname = g[0]
                        info_for_timing = g[1]
                        time_info = info_for_timing.get_text()
                        timeFrame = time_info.split(' ')[2]
                        duration = time_info.split(' ')[1]
                        if timeFrame == time_frame or timeFrame == time_frame_s:
                            if duration in durations:
                                botname = info_for_botname.get_text().split(' ')[0][3:]
                                if botname[0] == '/':
                                    if botname not in botnames:
                                        botnames.append(botname)
                                        #print 'Writing Bot Name...'
                                        fObj = open(log_file, 'ab')
                                        fObj.write(botname+'\n')
                                        fObj.close()
                                        bot_count += 1
                            elif duration == str(int(durations[-1])+1):
                                loop = False
        
        # update url from the 'next' button
        links = soup.find_all('a')
        for link in links:
            if link.get('rel') == [u'nofollow',u'next']:
                url = link.get('href')
    return bot_count



def main():
    import time
    search_url = 'https://www.reddit.com/r/BotBustLog/new/'
    log_file = 'BotList.txt'
    print 'Running...'
    start = time.time()
    bot_count = findBotAccts(search_url,log_file,'day',['1','2','3','4','5'])
    print 'Done.'
    print '{:,} bot accounuts saved.'.format(bot_count)
    duration = time.time()-start
    duration_hour = duration/3600
    duration_min = (duration_hour - int(duration_hour))*60
    duration_sec = (duration_min - int(duration_min))*60
    print 'Processing time: %d hours %d minutes %.2f seconds'%(duration_hour,duration_min,duration_sec)

if __name__ == '__main__':
    main()
        
    
     