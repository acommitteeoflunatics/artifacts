#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2012-2013 Jerry W Jackson, All rights reserved.
# All rights reserved.
#
# This software is licensed under the BSD license.

""" 'kouch-mailer' is a collection of useful classes for manipulating
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

class CouchListener(server, auth, db):
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
		'param' {default value}
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
	global exts, chgs
	if len(argv) > 4:
		# call exts
		exts['server'] = argv[1]
		exts['auth'] = argv[2]
		exts['db'] = argv[3]
		exts['cmd'] = argv[4]
		exts['args'] = argv[5:]
		print "Starting Externals Listener..."
	elif len(argv) == 4:
		# call chgs
		chgs['server'] = argv[1]
		chgs['auth'] = argv[2]
		chgs['db'] = argv[3]
		chgs['params'] = argv[4:]
		print "Starting Changes Listener..."
	else:
		# improper number of parameters
		sys.stderr.write("Usage: 'kouch-mailer <server url> <auth> <db> \
		<external command> <options to command as string>' or 'kouch-mailer \
		<server url> <auth> <db> <parameters to changes listener>'")
		return 1

if __name__ == '__main__':
	''' If script is called directly, parse through the arguments and build a connection 
	    string. Once we're finished fire off the 'main()' function. '''
	description='''Versatile CouchDB Feed Consumer'''
	usage="%(prog)s [server] [database] [username] [password] {chgs,exts} {,ext_cmd} args"
	parser = argparse.ArgumentParser(usage=usage, description=description, 
		epilog=''' If you haven't noticed, username and password are positional; 
			and ext_cmd is only to be used with the exts feed. ''')
	group = parser.add_mutually_exclusive_group(required=False)
	group.add_argument('-v', '--verbose', action="store_true")
	group.add_argument('-q', '--quiet', action="store_true")
	# we add the server and database items
	parser.add_argument('server', action='store', nargs=1, default='http://localhost:5984',
		help='server url to connect to your couch (default: %(default)s')
	parser.add_argument('database', action='store', nargs=1, default='mailspool', 
		help='database to load from (default: %(default)s)')
	# we make an auth group and add the username and password to it
	group = parser.add_argument_group('auth')
	group.add_argument('username', action="store", nargs=1, 
		help='Which user to authorize?')
	group.add_argument('password', action="store", nargs=1, 
		help='What is the password for this user?')
	# we make a feed for the feed choices
	subparsers = parser.add_subparsers(help='''Choose whether to use the _changes or the 
		_external feed. Will be kept in results.type. ''')
	# create the parser for choosing the feed to work on
	parser_feed = subparsers.add_parser('feed')
	parser_feed.add_argument('type', choices=['chgs', 'exts'], nargs='?', 
		help='Choose a feed to work with.')
	parser_args = subparsers.add_parser('args')
	parser_args.add_argument('args', nargs=argparse.REMAINDER, 
		help="Operation(s) to be performed on the chosen feed.")
	print parser_feed
	print parser_args
	if ( parser_feed.type == 'exts' ):
          print 'We are using the _externals feed.'
          parser_args.add_argument('ext_cmd', action='store', nargs=1, 
          	help="Command to be run when a feed changes.")
          parser_args.add_argument('params', action='store', nargs=1, 
          	help="Options to be used with external command.")
        elif ( parser_feed.type == 'chgs' ):
          print 'We are using the _changes feed.'
        results = parser.parse_args()
    # fire off main() with the results of our parsing
    sys.exit(main(results))
	
