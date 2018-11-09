#!/usr/bin/python

import threading
from exploit_01 import *

exitFlag = 0

class exploit(threading.Thread):
	def __init__(self, ip, port):
		threading.Thread.__init__(self)
		self.ip = ip
		self.port = port

	def logging(ip, port):
		f = open('failed.txt', 'a')
		f.write(str(ip) + ' ' + str(port) + '\n')
		f.close()

	def run(self):
		try:
			run_exploit(ip, port) # name your function as run_exploit
		except:
			print(ip + " failed")
			logging(ip, port) # logging ip, port to failed.txt
		# exploit code here
		pass

targets = ["xxx.xxx.xxx.xxx", 80] #change this
for ip, port in targets:
	exploit(ip, port).start()
