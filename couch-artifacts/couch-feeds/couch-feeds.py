#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2012-2013 Jerry W Jackson, All rights reserved.
# All rights reserved.
#
# This software is licensed under the BSD license.

""" 'couch-feeds' is a collection of useful classes for manipulating
	couchdb's new _changes and _externals features. """

from couchdb import Server, Session
from mailer import Message, Mailer, make_header
from time import localtime, strftime
import datetime
import json as json
import sys
import argparse

exts = {}
chgs = {}
filtername = ''
heartbeat = ''
include = ''

class CouchListener(server, auth, db, feed):
	""" CouchListener is intended to be subclassed (see both 
	ChangesListener and ExternalsListener below) and may be used to 
	instantiate many types of CouchDB connection. CouchListener can 
	take the following as parameters: [
		'-param-' {-default-value-}
		'server' {"http://127.0.0.1:5984/"},
		'auth' {auth.name="", auth.password=""},
		'db' {none}
	] """
	def __init__(self, server, db):
		self.data = []
		self.server = server
		self.auth = auth
		self.db = db
	""" Create a new listener """
	def create(listener, type):
		pass
	""" Destroy an existing listener """
	def destroy(listener, type):
		pass
	""" Listen to a feed """
	def listen(feed, type):
		pass
	""" Ignore the feed """
	def ignore(feed, type, duration):
		pass
	
class ChangesListener(CouchListener):
	""" the ChangesListener takes the following parameters: [
		'-param-' {-default-value-}
		'heartbeat' {1 sec},   # heartbeat is used to check connection
		'include_docs' {True}, # whether or not to include documents
		'feed' {continuous},   # which type of feed 
		'filter' {none}		# named filter from design doc
	]
	This subclass will accept any other parameters the CouchListener 
	class would accept. """
	global filtername
	global heartbeat
	global include
	def __init__(self, filtername='spooler/unsent', heartbeat='1000', include=True):
		self.data = []
		self.filtername = filtername
		self.heartbeat = heartbeat
		self.include_docs = include

class ExternalListener(CouchListener):
	""" the ExternalListener takes the external command and it's 
	desired arguments (in a single string) as it's only two required 
	parameters. This subclass will accept any other parameters the 
	CouchListener class would accept.  """
	def __init__(self, command, arguments):
		self.data = []
		self.cmd = ext_cmd
		self.args = params

class MailSpooler:
	""" docstring goes here """
	def __init__(self, ccl):
		self.data = []

class CouchDBConnector:
	""" docstring goes here """
	def __init__(self, auth, server, db):
		self.data = []

class CouchDocParser:
	""" docstring goes here """
	def __init__(self, doc):
		self.data = []

def main():
	# TODO: replace this obsolete code with something else
	# global exts, chgs
	# if len(argv) > 4:
	# 	# call exts
	# 	exts['server'] = argv[1]
	# 	exts['auth'] = argv[2]
	# 	exts['db'] = argv[3]
	# 	exts['cmd'] = argv[4]
	# 	exts['args'] = argv[5:]
	# 	print "Starting Externals Listener..."
	# elif len(argv) == 4:
	# 	# call chgs
	# 	chgs['server'] = argv[1]
	# 	chgs['auth'] = argv[2]
	# 	chgs['db'] = argv[3]
	# 	chgs['params'] = argv[4:]
	# 	print "Starting Changes Listener..."
	# else:
	# 	# improper number of parameters
	# 	sys.stderr.write("Usage: 'couch-feeds <server url> <auth> <db> \
	# 	<external command> <options to command as string>' or 'couch-feeds \
	# 	<server url> <auth> <db> <parameters to changes listener>'")
	# 	return 1

if __name__ == '__main__':

	''' If script is called directly, parse through the arguments and build a connection 
	    string. Once we're finished fire off the 'main()' function. '''
	# usage = "usage: %(prog)s FEED [-h] [-v] [-V] SERVER DATABASE USERNAME PASSWORD [EXTERNAL_CMD] [ARGS]"
	description = '''Versatile CouchDB Feed Consumer'''
	parser = argparse.ArgumentParser(prog='couch-feeds', description=description, \
		epilog=''' EXTERNAL_CMD is only to be used with the externs FEED item. ''')
	parser.add_argument('-v', '--verbose', action='count', help='increases verbosity and is also cumulative')
	parser.add_argument('-V', '--version', action='version', version='%(prog)s 0.2')
	# we make a feed for the feed choices
	parser.add_argument('feed', choices=('changes', 'externs'), action='store', help='which feed to listen to')
	# we add server url and database name
	parser.add_argument('server', action='store', default='http://localhost:5984', help='server url to connect to (default: %(default)s)')
	parser.add_argument('database', action='store', default='mailspool', help='database you want to load')
	# we add the username and password
	parser.add_argument('username', action='store', nargs='?', help='which user to authorize')
	parser.add_argument('password', action='store', nargs='?', help='what is the password for this user')
	# if we're using the 'externs' feed items, use the rest of the commandline as it's external command with additional options for same
	feed_check = parser.parse_known_args()
	if [feed_check][0][0].feed == 'externs':
		print 'boo!'
		parser.add_argument('external_cmd', action='store', nargs='?', help='what external program to run')
		parser.add_argument('args', nargs=argparse.REMAINDER, help="additional arguments for external_cmd")
	results = parser.parse_args()
	print results.feed
	print "--------------------"
	# fire off main() with the results of our parsing
	main(results)