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

exts = {}
chgs = {}
filtername = ''
heartbeat = ''
include = ''

class CouchListener:
	""" CouchListener is intended to be subclassed (see both 
	ChangesListener and ExternalsListener below) and may be used to 
	instantiate many types of CouchDB connection. CouchListener can 
	take the following as parameters: [
		'param' {default value}
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
	def create(listener, feedtype):
		pass
	""" Destroy an existing listener """
	def destroy(listener, feedtype):
		pass
	""" Listen to a feed """
	def listen(feed, feedtype):
		pass
	""" Ignore the feed """
	def ignore(feed, feedtype, duration):
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
		self.cmd = command
		self.args = arguments

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

def main(argv):
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
		<external command> <options to command as string>' or 'koWch \
		<server url> <auth> <db> <parameters to changes listener>'")
		return 1
	

if __name__=="__main__":
	""" If script is called directly, fire off the 'main()' function. """
	sys.exit(main(sys.argv))
