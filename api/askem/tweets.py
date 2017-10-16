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
