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
import argparse_parent_with_group

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
import argparse

description='Versatile CouchDB Feed Consumer'
usage='%(prog)s <server> <username> <password> <database> [ chgs | exts ] [ <ext_cmd> <params> | <params> ]'

parent_parser = argparse.ArgumentParser(add_help=False)
parent_parser.add_argument('server', action='store',nargs=1, 
	help='server url to connect to your couch (default: %(default)s', 
	default='http://localhost:5984')
group = parent_parser.add_argument_group('authentication')
group.add_argument('username', action="store", nargs=1, help='user to authorize')
group.add_argument('password', action="store", nargs=1, help='password for user')
parent_parser.add_argument('database', action='store',nargs=1, default='mailspool',
	help='database to load from (default: %(default)s)')

group = parent_parser.add_mutually_exclusive_group()
group.add_argument("-v", "--verbose", action="store_true")
group.add_argument("-q", "--quiet", action="store_true")

parser = argparse.ArgumentParser(parents=[parent_parser])
subparsers = parser.add_subparsers(help='sub-command help')

parser_chgs = subparsers.add_parser('feed', parents=[parent_parser],
	help="selects the _changes feed")

parser_exts = subparsers.add_parser('feedt', parents=[parent_parser],
	help="selects the _externals feed")
parser_exts.add-argument( 'ext_cmd', action='store', nargs=1, 
	help="command to be run on feed changes")
parser_exts.add-argument( 'params', action='store', nargs=argparse.REMAINDER,
	help="options for external command")

args = parser.parse_args('http://localhost:5984', 'schade', 'testing', 'db_test', 'chgs')
print args
	
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
	

if __name__=="__main__":
	""" If script is called directly, fire off the 'main()' function. """
	sys.exit(main(sys.argv))
