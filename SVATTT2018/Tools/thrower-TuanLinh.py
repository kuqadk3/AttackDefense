#!/usr/bin/python

import threading
import os

exitFlag = False
spamPayloadMode = False #change this if you want usingg specific target (I know i have double g but my OCD is screaming, dont remove it!!!!)
spamTargetMode = False #change this if you want attack specific target

#add targets = api.fetchTargets()
payloads = os.listdir(os.getcwd() + '/payloads/') #get payloads list in /payloads/
if spamTargetMode == False:
	targets = [("http://google.com", 80), ("http://facebook.com", 80)] #change this handy if you want attack specific target
if spamPayloadMode == False:
	payloads = ['exploit_01.py', 'exploit_02.py'] #change this handy if you want to use specific payloads

class exploit(threading.Thread):
	def __init__(self, ip, port, payloads):
		threading.Thread.__init__(self)
		self.ip = ip
		self.port = port
		self.payloads = payloads

	"""Need more works, write logs in json and parse it to html for better views"""
	"""Status code : Success, Fail, Error"""

	"""Throw payloads and get flag"""
	def throw(self, ip, port, payloads):
		result = os.system("python " + os.getcwd() + "\\payloads\\" + payloads + " " + str(ip) + " " + str(port)) #run payload and pass ip, port as arguments and get result
		return result

	def run(self):
		try:
			for payload in payloads:
				result = self.throw(self.ip, self.port, payload) #try all payload in payloads list for a given target
		except Exception as e:
			print e
			print(payload + " " + ip + " failed")
			pass

for ip, port in targets:
	exploit(ip, port, payloads).start()
