#!/usr/bin/python

"""This script is an external python mailer making use of the _changes
feed and kept alive by couchdb as an [OS daemon]. After parsing the
object received from the feed, an email is crafted from the doc and
sent using any available smtp relay agent (it first tries using smtp via
ssmtp and falls back gracefully to python's smtplib module. We are using
a pre-provisioned gmail address of mailerbot@gmail.com to relay all msgs
in the database with a 'state' of 'unsent'. """

from couchdb import Server, Session
from mailer import Message
from mailer import Mailer
from mailer import make_header
from time import datetime, localtime, strftime
import json as json
import smtplib
import subprocess
import sys

def feedConsumer():
	""" 'feedConsumer()' will connect and continuously listen to the
	changes feed for any docs with a 'state' value of 'unsent'. Finding
	one; it will parse the data into email headers and body, send the
	email, and update the doc's 'state' value to either 'sent' or
	'error'. If the latter, it will also add a errormsg field with
	the contents of the message for debugging purposes. """
	global auth, data, sender, recipients, toaddr, ccs, bccs, fromaddr, toaddrs, headers, msgformat
	# TODO:FIXME
	""" change to couchdb:couchdb user:group combination"""
	auth = Session()
	auth.name = ''
	auth.password = ''

	s1 = Server('http://localhost:5984/', session=auth)
	db1 = s1['mailspool']
	ch = db1.changes(feed='continuous',heartbeat='1000',include_docs=True,filter='spooler/unsent')

	for line in ch:
		""" reset all vars to preclude any pollution between lines """
		data = ''
		sender = {}
		recipients = {}
		fromaddr = ''
		toaddrs = []
		toaddr = []
		ccs = []
		bccs = []
		headers = ''
		msgformat = ''
		""" now grab the document object included in the feed """
		data = line['doc']
		""" assign some vars to populate the actual email fields """
		sender = data['sender']
		recipients = data['recipients']
		msgformat = data['msgformat']
		message = data['message']
		subject = data['subject']
		""" begin parsing """
		parseChange()
		sendEmail(toaddr, ccs, bccs, message, subject)
		updateState(data)

def parseChange():
	""" 'parseChange()' is called by 'feedConsumer()' for parsing the
	lines from the incoming _changes object so that a properly formatted
	email message may be generated from the information. """
	global sender, recipients
	""" parse through the individual sender and receiver objects """
	parseSender(sender)
	parseReceivers(recipients)

def parseSender(sender):
	""" 'parseSender()' is called by 'feedConsumer()' to grab the individual
	sender(s) listed in the doc. """
	global fromaddr
	temp = ''
	for k,v in sender.items():
		temp = '"' + k + '" <' + v + '>'
		fromaddr = [temp]

def parseReceivers(data):
	""" 'parseReceivers()' is called by 'feedConsumer()' to grab the
	individual reciepients listed in the doc. """
	# TODO:FIXME craft a fix for multiple email addresses for all
	global toaddr, toaddrs, ccs, bccs
	for item in data:
		if item == 'to':
			for item in data['to']:
				to = '"'+ item + '" <' + data['to'][item] + '>'
				if not toaddr:
					toaddr = [to]
				else:
					toaddr = toaddr + [to]
		if item == 'cc':
			for item in data['cc']:
				cc = '"'+ item + '" <' + data['cc'][item] + '>'
				if not ccs:
					ccs = [cc]
				else:
					ccs = ccs + [cc]
		if item == 'bcc':
			for item in data['bcc']:
				bcc = '"'+ item + '" <' + data['bcc'][item] + '>'
				if not ccs:
					bccs = [bcc]
				else:
					bccs = bccs + [bcc]
	
	toaddrs = toaddrs + [to]
	toaddrs = toaddrs + ccs
	toaddrs = toaddrs + bccs
	flatten(toaddrs)
	
def flatten(input):
    ret = []
    if not isinstance(input, (list, tuple)):
        return [input]
    for i in input:
        if isinstance(i, (list, tuple)):
            ret.extend(flatten(i))
        else:
            ret.append(i)
    return ret
    
def sendEmail(toaddr, ccs, bccs, body, subject):
	""" 'sendEmail()' is called by 'feedConsumer()' when it is ready to
	send the e-mail to the specified recipient using SMTP; in case of
	failure to send, fallback gracefully to using the existing
	mailerbot@gmail.com account."""
	mailer = Mailer('smtp.gmail.com', port=587, use_tls=True, usr="mailerbot@gmail.com", pwd="mailerbot")
	msg = Message(From="email.account@gmail.com", To=toaddr, CC=ccs, BCC=bccs, Body=body)
	msg.Subject = subject
	mailer.send(msg)

def updateState(doc):
	""" 'updateState()' is called by 'feedConsumer()' when it has
	completed sending the e-mail. It will thenadjust the value of the
	doc's 'state' field to 'sent' and save the document. """
	global auth, data
	now = datetime.datetime.now()
	s2 = Server('http://localhost:5984/', session=auth)
	db2 = s2['mailspool']
	doc['state'] = 'sent'
	doc['date']['sent'] = strftime("%a, %d %b %Y %H:%M:%S %Z", localtime())
	try:
		db2.save(doc)
	except Exception as e:
		doc['errormsg'] = e


if __name__=="__main__":
	""" If script is called directly [this is the default usage], fire
	off the 'feedConsumer()' function to begin listening to the changes
	feed and make use of any changes received. """
	feedConsumer()
