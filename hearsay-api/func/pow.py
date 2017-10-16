#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
example of proof of work algorithm - need to redo nonce-difficulty
"""


import hashlib
import time
max_nonce = 2 ** 32  # 4 billion


def proof_of_work(header, difficulty_bits_in):
    target = 2 ** (256 - difficulty_bits_in)
    for nonce in xrange(max_nonce):
        hash_result = hashlib.sha256(str(header) + str(nonce)).hexdigest()
        if long(hash_result, 16) < target:
            print "Success with nonce %d" % nonce
            print "Hash is %s" % hash_result
            return (hash_result, nonce)
    # pylint: disable=undefined-loop-variable
    print "Failed after %d (max_nonce) tries" % nonce
    return nonce
    # pylint: enable=undefined-loop-variable
if __name__ == '__main__':

    resnonce = 0
    reshash_result = ''
    for difficulty_bits in xrange(32):
        difficulty = 2 ** difficulty_bits
        print ""
        print "Difficulty: %ld (%d bits)" % (difficulty, difficulty_bits)
        print "Starting search..."
        start_time = time.time()
        new_block = 'test block with transactions' + reshash_result

        (reshash_result, resnonce) = proof_of_work(new_block, difficulty_bits)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print "Elapsed time: %.4f seconds" % elapsed_time
        if elapsed_time > 0:
            hash_power = float(long(resnonce) / elapsed_time)
            print "Hashing power: %ld hashes per second" % hash_power
