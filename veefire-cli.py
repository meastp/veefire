#!/usr/bin/env python

#    Copyright 2008 Mats Taraldsvik <hallgeir.lien@gmail.com>

#    This file is part of veefire.

#    veefire is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    veefire is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with Foobar.  If not, see <http://www.gnu.org/licenses/>.

import getopt, sys, os
from api.dbapi import Show, Episode, Season, Database
from api.renameapi import Rename, Folder, FileName as AbstractFileName
from backends.imdbtv import Backend

class NewFileName(AbstractFileName):
	def setCorrectShow( self, Shows ) :
		return Shows[0]

class NewFolder(Folder) :
	def loadFiles( self ) :
		self.database = Database( self.dbDir , self.shows )
		self.database.loadDB()
		self.fileNames = []
		for afile in os.listdir( self.path ) :
			if os.path.isfile( os.path.join( self.path, afile) ) :
				aFileName = NewFileName( afile, self.database )
				self.fileNames.append( aFileName )

#def rename(rn):


def usage():
	print "Usage: veefire [options]..."
	print "Options:"
	print "-h, --help\t\t\tShow help."
	print "-v, --version\t\t\tShow version."
	print "-t, --target\t\tTarget directory for renaming. Default is current directory."
	print "-f, --filesystem <fs-name>\tUse the rules for the assigned filesystem for renaming."
	print "-l, --showlist\t\t\tPrint all episodes of all shows in database."
	print "-D, --DB-path <db-path>\t\tUse this path as the database path. Default: \"database\"."
	print ""
	print "Example: "
	print "veefire -f ext3 -t /home/santa/series/battlestar-galactica"

def version():
	print "veefire v. 1.0"
	print "This is free software; see the source for copying conditions. There is NO warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.\n"

def addFolders(rn, folder, recursive, dbdir):
	#TODO: Add recursive-support
	f = NewFolder(folder, dbdir)
	rn.addFolder(f)


def main():
	#TODO: Missing stuff that should be handled by command line:
	#fsdir - directory of the filetypes.xml file
	#recursive

	try:
		# Let's get those o'holy command line arguments.
		opts, args = getopt.getopt(sys.argv[1:], "hvf:ltD:", ["help", "version", "filesystem=", "showlist", "target=","DB-path"])
	except getopt.GetoptError, err:
		print str(err)
		usage()
		sys.exit(2)
	
	directory = "./"
	filesystem = "ext3" # Filesystem to consider when renaming
	printlist = False   # Set to true for those who seek a listing of all shows
	dbpath = "database" # Path to the great repository of show information
	ftdir = "/home/hallgeir/Programming/Python/veefire/filetypes.xml"		# Directory of the filetypes.xml file
	recursive = False	# Set to true if we want to dig recursively

	for o, a in opts:
		if o in ("-v", "--version"):
			version()
			sys.exit()
		elif o in ("-h", "--help"):
			usage()
			sys.exit()
		elif o in ("-f", "--filesystem"):
			filesystem = a
		elif o in ("-t", "--target"):
			directory = a
		elif o in ("-D", "--DB-path"):
			dbpath = a
		elif o in ("-l", "--showlist"):
			printlist = True
		else:
			assert False, "Invalid option."

	print "Database path: " + dbpath
	DB = Database(dbpath)
	DB.loadDB()

	if printlist:
		DB.printDb()
	else:
		# Program hasn't exited yet... what can that mean? Maybe it's time to start renaming those episode babies!
		print "Using filesystem: " + filesystem
		print "Target directory is: " + directory
		print "Path to filetypes.xml: " + ftdir
		rn = Rename(dbpath, ftdir)
		
		addFolders(rn, directory, False, dbpath)
		
		#ms = rn.getMatchingShows()
		#for Folder in ms:
		#	print Folder.path
		#	for FileName in Folder.fileNames:
		#		print FileName.CorrectShow.name
		#		print [ season.name for season in FileName.CorrectShow.seasons ]
		
		pv = rn.generatePreviews()
		for Folder in pv:
			for item in Folder:
				print item

if __name__ == "__main__":
	main()
