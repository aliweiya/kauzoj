#!/usr/bin/env python3
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
doc
"""
from __future__ import absolute_import
from __future__ import unicode_literals

from dateutil import parser
import datetime
from shutil import copyfile
import json


def getsources(key):
    return sources.Sources(API_KEY=key).get(language="en")['sources']
def getarticles(source,key):
    try:
        result = articles.Articles(API_KEY=key).get(source=source)['articles']
    except: result = []
    return result


key = getkey()

dates = {}

for source in getsources(key):
    a = 0
    for article in getarticles(source['id'],key):
        article['source'] = source['name']
        article['hash'] = gethash(article)
        year = 2017; month = 1; day = 1
        try:
            dt = parser.parse(article['publishedAt'])
            year = dt.year
            month = dt.month
            day = dt.day
        except: pass
        if year not in dates: dates[year] = {}
        if month not in dates[year]: dates[year][month] = {}
        if day not in dates[year][month]: dates[year][month][day] = []
        dates[year][month][day].append(article)
        a = a + 1
    print("{}:{}".format(source['id'],a))

# for year in sorted(list(dates.keys())):
#     for month in sorted(list(dates[year].keys())):
#         for day in sorted(list(dates[year][month].keys())):
#             print('### {}/{}/{} ###'.format(year,month,day))
#             for article in dates[year][month][day]:
#                 print(article)

with open('db/articledb.json','w+') as dbjson:
    try:
        exdb = json.loads(dbjson.read())
        dates = deepupdate(exdb, dates)
    except:
        pass
    dbjson.write(json.dumps(dates,indent=4, sort_keys=True))

dst = "db/article-db-{}.json".format(datetime.now().strftime("%Y-%m-%d-at-%H-%M"))
copyfile('db/articledb.json', dst)



file = args()
post = load(file)
content_1 = decrypt(post['source'])
content_2 = post.content
# edit a combination or choice of the two, resulting in a final document...
post['source'] = encrypt(final)
post.content = final
print(post)
dump(post,file)
file = args()
post = load(file)
post['source'] = encrypt(post.content)
post['encrypted'] = True
post.content = "> this post has been encrypted.\n"
print(post)
dump(post,file)
# try:
print("Begin News Loop.")
key = getkey()
while True:
    print('1. Evaluate Source Articles:')
    # try:
    for source in getsources(key):
        print(source['id'])
        for article in getarticles(source['id'],key):
            # add code to store if we've seen the article before
            choice = raw_input("{}: {}\n{}\n{} Useful? (opens tab) (Y/n)".format(source['name'],article['title'],article['description'],article['url']))
            if choice == "y" or choice == "Y":
                opentab(article['url'])
    # except: pass
    print('2. Add Sources:')
    # try:
    while True:
        addsources(input)
    # except: pass
    print('3. Add Searches:')
    # try:
    while True:
        addsearch(input)
    # except: pass
file = args()

post = load(file)

true_content = decrypt(post['source'])

print(true_content)

file = args()
post = load(file)
post.content = decrypt(post['source'])
post['encrypted'] = False
print(post)
dump(post,file)


#!/usr/bin/env python3
import twitter, toml, json, os, sys
with open("twitter.toml","r") as twoml:
    creds = toml.loads(twoml.read())
api = twitter.Api(consumer_key=creds['consumer']['key'],
                  consumer_secret=creds['consumer']['secret'],
                  access_token_key=creds['access']['token'],
                  access_token_secret=creds['access']['token_secret'],
                  sleep_on_rate_limit=True)

print(api.rate_limit.resources)
# get current user object?
#api.PostUpdate('Test twitter api again...')
sys.exit(1)
print('getting friends')
users = api.GetFriends()
print(users[0].__dict__)
print('initializing maps')
if not os.path.isfile("twitter-todo.json"):
    accts = list(api.GetFollowers())
    print(len(accts))
    for a in accts:
        seedaccts[a.id] = a
    with open('twitter-todo.json','w+') as td:
        json.dump(seedaccts,td)
    #mentions = api.GetMentions()
else:
    with open('twitter-todo.json','r') as td:
        seedaccts = json.load(td)
if os.path.isfile("twitter-mapped.json"):
    with open('twitter-mapped.json','r') as tm:
        mappedaccts = json.load(tm)
else:
    mappedaccts = {}
todoaccts = {}
print('for-loop, maps')
## removing done accounts from seed accounts
for acct in mappedaccts.keys():
    if acct in seedaccts.keys():
        del seedaccts[acct]
## removing mapped from seeds
for acct in seedaccts.keys():
    if acct not in mappedaccts.keys():
        todoaccts.append(seedaccts[acct])
print('finished for loop, maps')
worldTrends = api.GetTrendsCurrent()

print(worldTrends.__dict__)
for trend in worldTrends:
    print(trend)
print('finished trends')
## search accounts
def getuserinfo(user):
    name = user.name
    screen_name = user.screen_name
    bio = user.bio
    friends = api.GetFriendIDs(user_id=user.id)
    followers = api.GetFollowerIDsPaged(user_id=user.id)

    favorites = api.GetFavorites(user_id=user.id)

    trends = api.GetTrendsWoeid(user.location)

    lists = api.GetListsPaged(user_id=user.id)
    memberships = api.GetMemberships(user_id=user.id)
    subscriptions = api.GetSubscriptions(user_id=user.id)
    listmembers = api.GetListMembers(list_id=list.id)
    listmembers = api.GetListMembersPaged(list_id=list.id)

    statuses = api.GetUserTimeline(user_id=user.id)


def getstatusinfo(status):
    retweeters = GetRetweeters(status.id)

def getsearch(term):
    results = api.GetSearch(term=term)

def getusersearch(term):
    results = api.GetUsersSearch(term=term)


getuserinfo()

for user in users:
    if user not in mappedaccts.keys():
        info = getuserinfo(user)
        mappedaccts[u.handle] = info
    else:
        print('already mapped user')
print('hello')




"""

Could use celery tasks...

def undone_user(user):
    if user not in redis.list['crunchedusers']:
        if user not in redis.list['crunchingusers']:
            crunchuser.apply_async(user)

@celery.task()
def crunchuser(user):
    redis.list['crunchingusers'].add(user)
    bio = user.bio
    followers = user.followers
    following = user.following
    location = user.location
    exampletweets = user.feed

    for follower in followers:
        undone_user(follower)
    for follow in following:
        undone_user(follow)
    for term in bio.split(" "):
        undone_term(term)
    for tweet in exampletweets:
        undone_tweet(tweet)
    redis.list['crunchedusers'].add(user)

for user in UserTodos
