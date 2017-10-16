#!/usr/bin/env python
import hashlib, os
def proof_of_work(start, match):
	for nonce in range(1000000):
		hash_result = hashlib.sha256(str(start+str(nonce)).encode('utf-8')).hexdigest()
		if hash_result.startswith(match):
			print(nonce)
			return(nonce)
	print('failed')

def get_match(hello):
	actions = hashlib.sha256(str(hello).encode('utf-8')).hexdigest()[:5]
	print(actions)
	return actions

def check_match(start, nonce, match):
	actions = hashlib.sha256(str(start+str(nonce)).encode('utf-8')).hexdigest()
	if actions.startswith(match):
		print('true')
	else:
		print('false')

for a in range(100):
	actions = str(os.urandom(15)).encode('hex')
	match = get_match(actions)
	once = proof_of_work("then",match)
	print(once)
	check_match("then",once,match)
