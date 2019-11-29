import threading 
from pwn import *
import random
import time
context(arch= 'i386', os = 'linux')

def randomString():
	randString = ""
	for i in range(0, random.randint(1, 60)):
		randString += chr(random.randint(1, 255))
	return "SVATTT2019{" + randString + "}"

def sendFakeStuff(ip, port):
    #r = remote(ip, port)
    for i in range(0, random.randint(5, 100)):
        r = remote(ip, port)
        r.send(randomString())
        time.sleep(random.random())
	r.close()
    print "Successfully generated fake traffic to " + str(ip) + " on " + str(port) 

  
if __name__ == "__main__":
    ports = ["1234", "2345"]
    # creating thread
    for port in ports:
        threading.Thread(target=sendFakeStuff, args=("45.77.170.130", port)).start()
        # t2 = threading.Thread(target=sendFakeStuff, args=("45.77.170.130", port)) 

        # # starting thread 1 
        # t1.start() 
        # # starting thread 2 
        # t2.start() 
  
  
    # both threads completely executed 
    print("Done!") 

