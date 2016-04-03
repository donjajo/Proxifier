#!/usr/bin/env python
from getpass import getuser
from urlparse import urlsplit
import sys
import os
import shutil
from glob import glob
from datetime import datetime
from packages.Packages import *

class Proxifier( Wget, KDE, GTK, SSH, APT, Bash ):

	def __init__( self, host = '127.0.0.1', port = 3128, verbose = True ):
		if getuser() != 'root':
			raise UserWarning( 'Must be run as root' )

		self.verbose = verbose
		self.port = int( port )
		self.port = 3128 if not port else port 
		self.host = host
		self.http = str( host ) + ':' + str( self.port ) if not str( host ).endswith( '/' ) else str( host[ :-1 ] ) + ':' + str( self.port )
		super( self.__class__, self ).__init__()

	def date( self ):
		return datetime.now().strftime( '%a %b %d %H:%M:%S ' )

	def Set( self ):
		super( self.__class__, self ).Set()

	def Unset( self ):
		super( self.__class__, self ).Unset()

	def backup_config( self, config ):
		if os.path.isfile( config ):
			path, file = os.path.split( config )
			file = file + '.bak' if file else file 
			backup = os.path.join( path, file )

			if not os.path.isfile( backup ):
				if self.verbose:
					print( '%s Creating backup of %s to %s' % ( self.date(), config, backup ) )
				shutil.copyfile( config, backup )
			return True;
		else:
			return False 

	def dependancy_check( self ):
		Pass = True 
		for package in [ 'python-configobj', 'python-storm' ]:
			if not self.package_installed( package ):
				print( '%s package not installed\n' % package )
				Pass = False 
		if not Pass:
			sys.exit( 1 )

	def package_installed( self, package_name ):
		try:
			import apt
			cache = apt.Cache()
			return cache[ package_name ].is_installed
		except ImportError:
			raise ImportError( 'Install python-apt to use this package' )
		except KeyError:
			return False

	def desktops( self ):
		if os.path.isdir( '/usr/share/xsessions' ):
			desktops = glob( '/usr/share/xsessions/*.desktop' )
			desktops = [ os.path.split( desktop )[ 1 ].replace( '.desktop', '' ) for desktop in desktops ]
			return desktops 
		else:
			return list()

	def get_sudoer( self ):
		if 'SUDO_USER' in os.environ:
			return os.environ[ 'SUDO_USER' ]
		else:
			return getuser()

if __name__ == '__main__':
	from argparse import ArgumentParser
	parser = ArgumentParser( description = 'Proxify - One Time Linux Proxifer' )
	parser.add_argument( '-H', dest = 'http', help = 'Proxy Host', default = '', metavar = 'host' )
	parser.add_argument( '-p', dest = 'port', help = 'Proxy Port', default = 3128, metavar = 'port' )
	args = parser.parse_args()

	if not args.http:
		i = str( raw_input( 'Remove Proxy? (Y/N): ' ) ).upper()
		if i == 'Y':
			print( 'Removing proxy' )
			Proxifier().Unset();
		else:
			host = raw_input( 'Host (127.0.0.1): ' )
			port = raw_input( 'Port (3128): ' )

			host = host if host else '127.0.0.1'
			port = int( port ) if port else 3128
			print( 'Setting proxy to http://{0}:{1}'.format( host, port ) )
			Proxifier( host = host, port = port ).Set()
	else:
		Proxifier( host = args.http, port = args.port ).Set()

