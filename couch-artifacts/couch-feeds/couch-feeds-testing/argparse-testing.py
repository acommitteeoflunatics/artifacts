import argparse

if __name__ == '__main__':
	description='Versatile CouchDB Feed Consumer'
	usage="usage: %(prog)s [server] [username] [password] [database] [ [chgs] | [exts] ] [[ext_cmd] | ] params"
	parent_parser = argparse.ArgumentParser(usage=usage, description=description, add_help=False)
	parent_parser.add_argument('-s', '--server', action='store',nargs=1, help='server url to connect to your couch (default: %(default)s', default='http://localhost:5984')
	group = parent_parser.add_argument_group('authentication')
	group.add_argument('-u', '--username', action="store", nargs=1, help='user to authorize')
	group.add_argument('-p', '--password', action="store", nargs=1, help='password for user')
	parent_parser.add_argument('-d', '--database', action='store',nargs=1, default='mailspool', help='database to load from (default: %(default)s)')
	group = parent_parser.add_mutually_exclusive_group()
	group.add_argument("-v", "--verbose", action="store_true")
	group.add_argument("-q", "--quiet", action="store_true")
	parser = argparse.ArgumentParser(parents=[parent_parser])
	subparsers = parser.add_subparsers(help='sub-command help')
	parser_chgs = subparsers.add_parser('--changes-feed', parents=[parent_parser])
	parser_exts = subparsers.add_parser('--externals-feed', parents=[parent_parser])
	parser_exts.add_argument('-e', '--ext_cmd', action='store', nargs=1, help="command to be run on feed changes")
	parser_exts.add_argument('params', action='store', nargs=argparse.REMAINDER, help="options for external command")
	print '-----------------'
	results = parser.parse_args()
	print type(results)
	for each in results.each:
		print each
	end
