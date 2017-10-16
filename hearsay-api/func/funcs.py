import frontmatter, base64, sys, webbrowser, hashlib
from itertools import cycle
from newsapi import articles, sources

from pprint import pformat
def gethash(dictionary):
    h = hashlib.sha256(pformat(dictionary).encode('utf-8')).hexdigest()
    return h




ScrapePreventionChildProtection = "sgdhu0zJqMNwJMptmKK7,D2tD8NvxzqaOYTTsMyLF,GxE9O06PhZ76l26h3jWk,tbgpTwdRRrjPVatmRst0,Tjg05gCHSyVzwbdrDswZ,RYbgX8HE2RdJlucai4je,G68x6cY2lZlQmU1ndOEV,9gOCaOEkmcvwLFfgVLHb,PPJkVEbvB1WWx9YTUgIb,qTZGIfrqIv8FLSunL93A"
#https://gist.github.com/packetchef/ee66f1892d4f92d5f39b
# somehow this and https://github.com/kauzoj/kauzoj.github.io/blob/master/assets/js/XORCipher.js
# don't get along with base64 or the xor at that position..
def decrypt(text,key=ScrapePreventionChildProtection):
    text = base64.decodestring(text)
    xored = ''.join(chr(ord(x) ^ ord(y)) for (x,y) in zip(text, cycle(key)))
    return xored
def encrypt(text,key=ScrapePreventionChildProtection):
    xored = ''.join(chr(ord(x) ^ ord(y)) for (x,y) in zip(text, cycle(key)))
    return base64.encodestring(xored).strip()
def getkey():
    with open('secret.key','r') as kf:
        return kf.read().strip()
def getsources(key):
    return sources.Sources(API_KEY=key).get(language="en")['sources']
def getarticles(source,key):
    try:
        result = articles.Articles(API_KEY=key).get(source=source)['articles']
    except: result = []
    return result
def opentab(url):
    webbrowser.open(url)
def new(filename,author):
    post = {'author':author,'content':''}
    return post
def load(filename):
    post = frontmatter.load(filename)
    #post.content, post['enc']
    return post
def dump(content,filename):
    with open(filename,'w+') as file:
        frontmatter.dump(content, file)
def args():
    """get the filename from arguments"""
    return sys.argv[1]
# Copyright Ferry Boender, released under the MIT license.
def deepupdate(target, src):
    """Deep update target dict with src
    For each k,v in src: if k doesn't exist in target, it is deep copied from
    src to target. Otherwise, if v is a list, target[k] is extended with
    src[k]. If v is a set, target[k] is updated with v, If v is a dict,
    recursively deep-update it.

    Examples:
    >>> t = {'name': 'Ferry', 'hobbies': ['programming', 'sci-fi']}
    >>> deepupdate(t, {'hobbies': ['gaming']})
    >>> print t
    {'name': 'Ferry', 'hobbies': ['programming', 'sci-fi', 'gaming']}
    """
    for k, v in src.items():
        if type(v) == list:
            if not k in target:
                target[k] = copy.deepcopy(v)
            else:
                target[k].extend(v)
        elif type(v) == dict:
            if not k in target:
                target[k] = copy.deepcopy(v)
            else:
                deepupdate(target[k], v)
        elif type(v) == set:
            if not k in target:
                target[k] = v.copy()
            else:
                target[k].update(v.copy())
        else:
            target[k] = copy.copy(v)
    return target
