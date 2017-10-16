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
