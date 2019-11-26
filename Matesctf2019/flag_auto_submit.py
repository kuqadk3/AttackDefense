#!/usr/bin/env python2
# vim: set fileencoding=utf-8 :

import re
import requests

s = requests.Session()
s.get("https://final.matesctf.org/final-scoreboard")
csrf = s.cookies["csrf_cookie"]
payload = {'username':'Just ∫du It!','password':'m4AzLUUz6DgsSDKQ04xB','csrf_token':csrf}
print s.post("https://final.matesctf.org/final-scoreboard/api/sign-in", data=payload).content
challs = [9, 16, 14, 15, 13, 10]

while True:
    gr = re.search("MATESCTF{(.+)}", raw_input())
    
    if gr is None:
        continue

    flag = gr.group(0)
    payload = {'flag':flag,'id':0,'csrf_token':csrf}
    
    for i in challs:
        payload['id'] = i
        rsp = s.post("https://final.matesctf.org/final-scoreboard/api/challenge-submit", data=payload)
        print str(i) + " " + rsp.content
