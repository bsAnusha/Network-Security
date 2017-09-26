#!/usr/bin/env python

import time
import socket
import sys
import subprocess
import shlex

blocked=["ls","chmod","logname","mv","uname","pwd"]

def getInput():
	motd = raw_input('MOTD: ')
	host = raw_input('IP Address: ')
	while True:
		try:
			port = int(raw_input('Port: '))
		except TypeError:
			print 'Error: Invalid port number.'
			continue
		else:
			if (port < 1) or (port > 65535):
				print 'Error: Invalid port number.'
				continue
			else:
				return (host, port, motd)

def writeLog(client, data=''):
	separator = '='*50
	fopen = open('./honey.mmh', 'a')
	fopen.write('Time: %s\nIP: %s\nPort: %d\nData: %s\n%s\n\n'%(time.ctime(), client[0], client[1], data, separator))
	fopen.close()

def main(host, port, motd):
	print 'Starting honeypot!'
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((host, port))
	s.listen(100)
	while True:
		(insock, address) = s.accept()
		print 'Connection from: %s:%d' % (address[0], address[1])
		out="Connection established\n"
		block = 5
		num_exec = 0
		while(num_exec<block):
			try:
				data = insock.recv(100)
				if shlex.split(data)[0] in blocked:
					num_exec = num_exec+1
					name=shlex.split(data)[0]+".txt"
					with open (name, "r") as myfile:
    						lines=myfile.read()
					lines=lines+"\n"
					out = lines
					insock.send(out)
				else:			
					out=subprocess.check_output(shlex.split(data))
					insock.send(out)
							
			except socket.error, e:
				writeLog(address)
			else:
				writeLog(address, data)
		insock.close()
        
if __name__=='__main__':
	try:
		stuff = getInput()
		main(stuff[0], stuff[1], stuff[2])
	except KeyboardInterrupt:
		print 'Bye!'
		exit(0)
	except BaseException, e:
		print 'Error: %s' % (e)
		exit(1)
