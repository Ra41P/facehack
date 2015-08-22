#facehack v2.0
#Automated Commenting/Liking python tool based on Graph v2.3
#Added easier functionality 
"""
Created on Sat Aug 22 10:26:00 2015

@author: ra41p
@stolen from: Vivek Aithal
"""
from urllib import urlencode
import requests
from datetime import datetime
import random

def genUTCTime(time_to_convert):
    #calculate utc timestamp
    epoch=datetime(1970,1,1)
    td = time_to_convert - epoch
    return int((td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 1e6)


def getAllPosts():
    #get wishes
    baseURL = 'https://graph.facebook.com/v2.3/me/feed'
    
    params = {'since': startTime,'until': endTime, 'access_token': access_token, 'limit':limit}
    url = '%s?%s' % (baseURL, urlencode(params))
    #print url
    req = requests.get(url)
    
    if req.status_code == 200:    
        rawData = req.json()['data']
        print 'The total number of posts from utm= '+str(startTime)+' to utm = '+str(endTime)+'%s is = '+str(len(rawData))+'\n'    
        return rawData
                
    else:
        print req.status_code
        print "Unable to connect. Check if session is still valid"
    
def processPosts(posts):
   
    for post in posts:
        message= post['message']
        createdTime=post['created_time']
        postID = post['id']
        friendFullName= post['from']['name']
        friendID = post['from']['id']
        record = [postID,friendFullName,friendID,createdTime]
        #print record

        try:
            friend = requests.get('https://graph.facebook.com/v2.3/'+friendID+'?access_token='+access_token).json()['first_name']
        except :
            friend = friendFullName

        message = random.choice(part1)+' '+friend+'! '+ random.choice(part2)

        #Add to log
        log.writelines(('|').join(record)+ '|' + message +'\n')
        print message
        
        #Reply to attach        
        payload = {'message': message}
        
        if(like):
            url = 'https://graph.facebook.com/%s/likes?access_token=%s' % (postID, access_token)
            #url = baseURL++'/likes?access_token='+access_token
            print url
            likeit = requests.post(url)
            if(likeit.status_code == 200):
                print 'liked\n'
            else:
                print str(likeit.json()) + '\nFailed at liking. Wtf did you do wrong\n'
        if(comment):
            url= 'https://graph.facebook.com/%s/comments?access_token=%s' % (postID, access_token)
            commentit = requests.post(url, data=payload)
            if(commentit.status_code ==200):
                print 'commented\n'
            else:
                print str(likeit.json()) + '\nFailed at commenting. Wtf did you do wrong\n'
##-------------------------------------------------------------------------------------#
#Configurations
#log file path
logFilePath = '/home/ra41p/Desktop/pythonCrap/facebook_reader/dump.csv' 

#Times to crawl/reply between
#Format is (%yyyy,%m,%d,%h,%m,%s)
startTime = datetime(2015,8,15,12,30,0)
endTime = datetime(2015,8,22,12,30,0)

#Token
#Generate from https://developers.facebook.com/tools/debug/
access_token = 'fill_me_up'

#set true to like posts on your wall
like = False;

#set true to comment
comment = False;

#limit on posts(?)
limit = '500'

#Response options
part1 = ['Hey,','Hello,','Thank you,','Yo,','Thanks a lot,']
part2= ["How're you doing? :)", "Much appreciated. What's up? :)", "How have you been? :)", "What are you up to? :)"]

##-------------------------------------------------------------------------------------#
#Don't touch these

log = open(logFilePath,'w')
startTime = genUTCTime(startTime)
endTime = genUTCTime(endTime)
posts = getAllPosts()
#print posts
processPosts(posts)
