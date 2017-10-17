Cache for articles obtained via newsapi (also part of the Queue system for deciding (round robin) which reporter gets autoqueued.

- hash (article url, description, title)
- linked list (double?)


- recently used
	- age of article (LFU + aging, redit, LFRU)
- frequently used (number of times accessed)
	- views (just clicks)
	- votes (yes/no)
	- drafts
- locked (in use)

- never seen before
- written about before


possibly write in upscaledb or just stick to sqlite (not complicated / requiring speed)

https://github.com/cruppstahl/upscaledb/blob/master/python/samples/db1.py


---
save cache to yml, load yml to cache

# Kauzoj Edit Scripts

Simple scripts to edit & view kauzoj, if you don't trust our JS providers.

* print.py -> print article
* edit.py -> open, decrypt, modify, encrypt, save
* lock.py -> encrypt a file with the xor key (prevent searching)
* unlock.py -> decrypt a file (for editing with your own things)

Searchengine


inverted index:
  URI - keywords in the URI

if word in index.keys()

return filename for (all of the ones that match)
return [filename for filename in index[word].keys()]

for word in string.split()

result += query()

return list(set(set))

33.66 kb (truncate)
