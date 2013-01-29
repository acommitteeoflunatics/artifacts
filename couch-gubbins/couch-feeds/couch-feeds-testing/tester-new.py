import argparse
from argparse import RawTextHelpFormatter
import sys

if __name__ == '__main__':

	''' If script is called directly, parse through the arguments and build a connection 
	    string. Once we're finished fire off the 'main()' function. '''
	description = '''Versatile CouchDB Feed Consumer'''
	parser = argparse.ArgumentParser(prog='kouch-mailer v0.2', description=description, \
		epilog=''' EXTERNAL_CMD is only to be used with the externs FEED item. ''')
	parser.add_argument('-v', '--verbose', action='count', \
		help='increases verbosity and is also cumulative')
	parser.add_argument('-V', '--version', action='version', version='%(prog)s 0.2')
	# we make a feed for the feed choices
	parser.add_argument('feed', choices=('changes', 'externs'), action='store', \
		help='available feeds: [changes | externs]', metavar='FEED')
	# we add server url and database name
	parser.add_argument('server', action='store', default='http://localhost:5984', \
		metavar='SERVER', help='server url to connect to (default: %(default)s)')
	parser.add_argument('database', action='store', default='mailspool', 
		metavar='DATABASE', help='database you want to load')
	# we add the username and password
	parser.add_argument('username', action='store', help='which user to authorize', metavar='USERNAME')
	parser.add_argument('password', action='store', help='the password for this user', metavar='PASSWORD')
	# if we're using the 'externs' feed items, use the rest of the commandline as it's options
	parser.add_argument('external_cmd', action='store', nargs='?', \
		metavar='EXTERNAL_CMD', help='what external program to run')
	parser.add_argument('args', nargs=argparse.REMAINDER, \
		metavar='ARGS', help="additional arguments to EXTERNAL_CMD")
	# print help if no arguments given
	if len(sys.argv)==1:
		parser.print_help()
	sys.exit(1)

	results = parser.parse_args()
	print results.feed
	print "--------------------"
	# fire off main() with the results of our parsing
	#main(results)
