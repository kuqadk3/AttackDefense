#!/usr/bin/env python3
import time
import requests
import re, os, sys
import threading, subprocess

"""
This is an exploit thrower for RuCTFe. The following is an outline representing an abstract view of it's functionality.
The thower will be given the exploit path as an arugment. It will then be sent to each target within individual threads.

1. We query the shim API (GET /get_targets) for all targets
2. Exploit path will be passed as an arguement
3. We'll exploit each target within it's own thread
4. For each exploit, we'll recieve the output (i.e. flag)
5. We'll submit each flag to the shim's API (POST /submit-flag)
"""

# Default flask location
HOST = "http://127.0.0.1:5000"

class Thrower(threading.Thread):
    def __init__(self, target, xpl_path):
        threading.Thread.__init__(self)
        self.trgt = target
        self.payload = xpl_path

    def run(self):
        p = os.popen("%s %s" % (self.payload,self.trgt))
        submit_flag(p.read())

def get_targets():
    """ This function will make GET request to our flask web API at /get-targets
    returns: list of targets"""
    return requests.get(HOST+'/get_targets')

def throw(xpl_path):
    """ This function will send each target an exploit for it's respective exploit
    and submit the flag to the shim's API"""
    trgts = get_targets()
    for trgt in trgts:
        t = Thrower(trgt, xpl_path)
        t.start()

def submit_flag(flags):
    """ This function will make POST requests to our flask web API at /submit-flags """
    requests.post(HOST+'/submit-flag', data={'flag':flags})
    return

def main(xpl_path):
    # Check is xpl_path starts with './' or '/'; if not default to './' (relative path)
    if not re.match('^./',xpl_path) and not re.match('^/',xpl_path) :
        xpl_path = './' + xpl_path
    throw(xpl_path)

if __name__=="__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("Usage: thrower.py <xpl-file-path>")
        sys.exit(2)

