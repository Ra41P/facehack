#This will thank people who have wished.
#There are 5 pre-name thank segments and 4 post wish, so 20 variations. 
#Also, this creates a csv file for all records

import requests
import random
import json
lob = open('e:/Projects/facehack/record6.csv','w')


baseURL = 'https://graph.facebook.com/v2.3/'

authToken = #Your token for v2.3 goes here

wishesPart1 = ['Hey,','Hello,','Thank you,','Yo,','Thanks a lot,']

wishesPart2= ["How're you doing? :)", "Much appreciated. What's up? :)", "How have you been? :)", "What are you up to? :)"]

limit = '500'

#Get all posts
#UTC of start post_time
startTime ='1437395340' #replace this with the post time you want to begin with
#UTC of end post_time
endTime ='1437418074' #replace this with the post time you want to end with

wishes = requests.get(baseURL+'me/feed?access_token='+authToken+'&since='+startTime+'&until='+endTime+'&limit='+limit)

readableWishes = json.loads(wishes.text)
posts = readableWishes['data']
print 'data is in'
print 'The total number of posts from utm= '+startTime+' to utm = '+endTime+'%s is = '+str(len(posts))
print '\n\n'



for post in posts:
    message= post['message']
    createdTime=post['created_time']
    postID = post['id']
    friendFullName= post['from']['name']
    friendID = post['from']['id']
    record = [postID,friendFullName,friendID,createdTime]
    print record
    try:
        friend = json.loads((requests.get(baseURL+friendID+'?access_token='+authToken)).text)['first_name']
    except :
        friend = friendFullName
    thanks = random.choice(wishesPart1)+' '+friend+'! '+ random.choice(wishesPart2)
    lob.writelines(('|').join(record)+'\n')
    print thanks
    print '\n'
    payload = {'access_token':authToken, 'message': thanks}
    likeit = requests.post(baseURL+postID+'/likes?access_token='+authToken)
    commentit = requests.post(baseURL+postID+'/comments',data=payload)

print 'Thanked everyone. Finally can strike it off the good manners bucket list' 
lob.close()