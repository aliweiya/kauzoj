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

