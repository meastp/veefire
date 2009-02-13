#!/usr/bin/env python

#    Copyright 2008 Mats Taraldsvik <mats.taraldsvik@gmail.com>

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
#    along with veefire.  If not, see <http://www.gnu.org/licenses/>.

# DIRECTORY FOR TEST FILES

testFileDirectory = '/tmp/veefire'
testSubDirectories = [ 'Black Books', 'CSI', 'Spaced']
testFileNames = [   [ 'blackbooks.s01e02.avi', 'bb.s03e05.avi'],
                    [ 'CSIS01E11.avi', 'CSI.5x12.avi' ],
                    [ 'Spaced.2x3.avi', 'Spaced.S02E03.avi']   ]

# CONTENTS FOR FILETYPES / FILESYSTEMS

testFiletypesDirectory = testFileDirectory
testFiletypesContent = r'''<?xml version="1.0" encoding="UTF-8"?>
<filetypes>
    <filetype name="ext3">
        <invalid_char name="SLASH, VIRGULE" char="002F" replacement="or" />
        <invalid_char name="QUOTATION MARK" char="0022" replacement="" />
    </filetype>
    <filetype name="ntfs">
        <invalid_char name="COMMERCIAL AT" char="0040" replacement="at" />
        <invalid_char name="POUND SIGN" char="00A3" replacement="GBP" />
        <invalid_char name="DOLLAR SIGN" char="0024" replacement="USD" />
        <invalid_char name="NUMBER SIGN" char="0023" replacement="No." />
        <invalid_char name="PERCENT SIGN" char="0025" replacement="PerCent" />
        <invalid_char name="QUESTION MARK" char="003F" replacement="Qo" />
        <invalid_char name="EXCLAMATION MARK" char="0021" replacement="" />
        <invalid_char name="PLUS SIGN" char="002B" replacement="plus" />
        <invalid_char name="ASTERISK" char="002A" replacement="" />
        <invalid_char name="REVERSE SOLIDUS" char="005C" replacement=" " />
        <invalid_char name="AMPERSAND" char="0026" replacement="and" />
        <invalid_char name="SLASH, VIRGULE" char="002F" replacement="or" />
        <invalid_char name="QUOTATION MARK" char="0022" replacement="" />
        <invalid_char name="COLON" char="003A" replacement="" />
        <invalid_char name="APOSTROPHE" char="0027" replacement="" />
    </filetype>
</filetypes>
'''

# CONTENTS FOR DATABASE

testDatabaseDirectory = os.path.join(testFileDirectory, 'database')
testDatabase = { testDatabaseBlackBooks : 'blackbooks.xml', testDatabaseSpaced : 'spaced.xml', testDatabaseCSI : 'csi.xml' }

testDatabaseBlackBooks = r'''<?xml version="1.0" encoding="UTF-8"?>
<tvshow>
  <showproperties backend="imdbtvbackend" duration="30" filesystem="ext3" name="Black Books" url="tt0262150"/>
  <fileproperties>
    <alias value="black.books"/>
    <alias value="bb"/>
  </fileproperties>
  <season number="1">
    <episode airdate="29 September 2000" arc="none" number="1" title="Cooking the Books"/>
    <episode airdate="6 October 2000" arc="none" number="2" title="Manny's First Day"/>
    <episode airdate="13 October 2000" arc="none" number="3" title="The Grapes of Wrath"/>
    <episode airdate="20 October 2000" arc="none" number="4" title="The Blackout"/>
    <episode airdate="27 October 2000" arc="none" number="5" title="The Big Lock-Out"/>
    <episode airdate="3 November 2000" arc="none" number="6" title="He's Leaving Home"/>
  </season>
  <season number="2">
    <episode airdate="1 March 2002" arc="none" number="1" title="The Entertainer"/>
    <episode airdate="8 March 2002" arc="none" number="2" title="Fever"/>
    <episode airdate="15 March 2002" arc="none" number="3" title="The Fixer"/>
    <episode airdate="22 March 2002" arc="none" number="4" title="Blood"/>
    <episode airdate="29 March 2002" arc="none" number="5" title="Hello Sun"/>
    <episode airdate="5 April 2002" arc="none" number="6" title="A Nice Change"/>
  </season>
  <season number="3">
    <episode airdate="11 March 2004" arc="none" number="1" title="Manny Come Home"/>
    <episode airdate="18 March 2004" arc="none" number="2" title="Elephants and Hens"/>
    <episode airdate="25 March 2004" arc="none" number="3" title="Moo-Ma and Moo-Pa"/>
    <episode airdate="1 April 2004" arc="none" number="4" title="A Little Flutter"/>
    <episode airdate="8 April 2004" arc="none" number="5" title="The Travel Writer"/>
    <episode airdate="15 April 2004" arc="none" number="6" title="Party"/>
  </season>
</tvshow>
'''

testDatabaseSpaced = r'''<?xml version="1.0" encoding="UTF-8"?>
<tvshow>
  <showproperties backend="imdbtvbackend" duration="60" filesystem="ext3" name="Spaced" url="tt0187664"/>
  <fileproperties/>
  <season number="1">
    <episode airdate="24 September 1999" arc="none" number="1" title="Beginnings"/>
    <episode airdate="1 October 1999" arc="none" number="2" title="Gatherings"/>
    <episode airdate="8 October 1999" arc="none" number="3" title="Art"/>
    <episode airdate="15 October 1999" arc="none" number="4" title="Battles"/>
    <episode airdate="22 October 1999" arc="none" number="5" title="Chaos"/>
    <episode airdate="29 October 1999" arc="none" number="6" title="Epiphanies"/>
    <episode airdate="5 November 1999" arc="none" number="7" title="Ends"/>
  </season>
  <season number="2">
    <episode airdate="23 February 2001" arc="none" number="1" title="Back"/>
    <episode airdate="2 March 2001" arc="none" number="2" title="Change"/>
    <episode airdate="9 March 2001" arc="none" number="3" title="Mettle"/>
    <episode airdate="23 March 2001" arc="none" number="4" title="Help"/>
    <episode airdate="None" arc="none" number="5" title="Gone"/>
    <episode airdate="6 April 2001" arc="none" number="6" title="Dissolution"/>
    <episode airdate="13 April 2001" arc="none" number="7" title="Leaves"/>
  </season>
</tvshow>'''

testDatabaseCSI = r'''<?xml version="1.0" encoding="UTF-8"?>
<tvshow>
  <showproperties backend="imdbtvbackend" duration="60" filesystem="ext3" name="C.S.I" url="tt0247082"/>
  <fileproperties>
    <alias value="csi"/>
  </fileproperties>
  <season number="1">
    <episode airdate="6 October 2000" arc="none" number="1" title="Pilot"/>
    <episode airdate="13 October 2000" arc="none" number="2" title="Cool Change"/>
    <episode airdate="20 October 2000" arc="none" number="3" title="Crate 'n' Burial"/>
    <episode airdate="27 October 2000" arc="none" number="4" title="Pledging Mr. Johnson"/>
    <episode airdate="3 November 2000" arc="none" number="5" title="Friends &amp;#38; Lovers"/>
    <episode airdate="10 November 2000" arc="none" number="6" title="Who Are You?"/>
    <episode airdate="17 November 2000" arc="none" number="7" title="Blood Drops"/>
    <episode airdate="24 November 2000" arc="none" number="8" title="Anonymous"/>
    <episode airdate="8 December 2000" arc="none" number="9" title="Unfriendly Skies"/>
    <episode airdate="22 December 2000" arc="none" number="10" title="Sex, Lies and Larvae"/>
    <episode airdate="12 January 2001" arc="none" number="11" title="I-15 Murders"/>
    <episode airdate="1 February 2001" arc="none" number="12" title="Fahrenheit 932"/>
    <episode airdate="8 February 2001" arc="none" number="13" title="Boom"/>
    <episode airdate="15 February 2001" arc="none" number="14" title="To Halve and to Hold"/>
    <episode airdate="22 February 2001" arc="none" number="15" title="Table Stakes"/>
    <episode airdate="1 March 2001" arc="none" number="16" title="Too Tough to Die"/>
    <episode airdate="8 March 2001" arc="none" number="17" title="Face Lift"/>
    <episode airdate="29 March 2001" arc="none" number="18" title="$35K O.B.O."/>
    <episode airdate="12 April 2001" arc="none" number="19" title="Gentle, Gentle"/>
    <episode airdate="19 April 2001" arc="none" number="20" title="Sounds of Silence"/>
    <episode airdate="26 April 2001" arc="none" number="21" title="Justice Is Served"/>
    <episode airdate="10 May 2001" arc="none" number="22" title="Evaluation Day"/>
    <episode airdate="17 May 2001" arc="none" number="23" title="The Strip Strangler"/>
  </season>
  <season number="2">
    <episode airdate="27 September 2001" arc="none" number="1" title="Burked"/>
    <episode airdate="4 October 2001" arc="none" number="2" title="Chaos Theory"/>
    <episode airdate="11 October 2001" arc="none" number="3" title="Overload"/>
    <episode airdate="18 October 2001" arc="none" number="4" title="Bully for You"/>
    <episode airdate="25 October 2001" arc="none" number="5" title="Scuba Doobie-Doo"/>
    <episode airdate="1 November 2001" arc="none" number="6" title="Alter Boys"/>
    <episode airdate="8 November 2001" arc="none" number="7" title="Caged"/>
    <episode airdate="15 November 2001" arc="none" number="8" title="Slaves of Las Vegas"/>
    <episode airdate="22 November 2001" arc="none" number="9" title="And Then There Were None"/>
    <episode airdate="6 December 2001" arc="none" number="10" title="Ellie"/>
    <episode airdate="13 December 2001" arc="none" number="11" title="Organ Grinder"/>
    <episode airdate="20 December 2001" arc="none" number="12" title="You've Got Male"/>
    <episode airdate="17 January 2002" arc="none" number="13" title="Identity Crisis"/>
    <episode airdate="None" arc="none" number="14" title="The Finger"/>
    <episode airdate="7 February 2002" arc="none" number="15" title="Burden of Proof"/>
    <episode airdate="28 February 2002" arc="none" number="16" title="Primum Non Nocere"/>
    <episode airdate="7 March 2002" arc="none" number="17" title="Felonious Monk"/>
    <episode airdate="28 March 2002" arc="none" number="18" title="Chasing the Bus"/>
    <episode airdate="4 April 2002" arc="none" number="19" title="Stalker"/>
    <episode airdate="25 April 2002" arc="none" number="20" title="Cats in the Cradle..."/>
    <episode airdate="2 May 2002" arc="none" number="21" title="Anatomy of a Lye"/>
    <episode airdate="9 May 2002" arc="none" number="22" title="Cross-Jurisdictions"/>
    <episode airdate="18 May 2002" arc="none" number="23" title="The Hunger Artist"/>
  </season>
</tvshow>
'''

# CREATE FILE NAMES FOR TESTING
#TODO: Create checks if directories exist.
import os
import shutil

class Tools :
    
    def __init__(self):
        self.rootDir = testFileDirectory
        self.testDirs = testSubDirectories
        self.testFiles = testFileNames
        
        self.filetypesXML = os.path.join(testFiletypesDirectory, 'filetypes.xml')
        
        self.databaseDir = testDatabaseDirectory
        
    
    def createRootDir(self):
        if os.path.exists(self.rootDir) :
            self.removeTempFiles()
        os.mkdir(self.rootDir)
    
    def createTempFiles(self):
        
        absDirs = [os.path.join(self.rootDir,name) for name in self.testDirs]
        for directory in absDirs:
            os.mkdir(directory)
        # replaces os.system in python 2.6 : p = Popen("command" + "arg", shell=True)
        # sts = os.waitpid(p.pid, 0)
        while( len(absDirs) > 0 ):
            currentDir = absDirs.pop()
            for files in self.testFiles[-1] :
                os.system('touch ' + '"' + os.path.join( currentDir, files ) + '"')
    
    def removeTempFiles(self):
        shutil.rmtree(self.rootDir)
    
    def createFilesystemXML(self):
        testfile = open(self.filetypesXML ,"w")
        testfile.writelines(testFiletypesContent)
        testfile.close()
    
    def createDatabaseFiles(self):
        for content, filename in testDatabase.items() :
            testfile = open(os.path.join( self.databaseDir, filename ),"w")
            testfile.writelines( content )
            testfile.close()

# TEST CLASS

class testFiles:
    def setUp(self):
        self.Tools = Tools()
        self.Tools.createRootDir()
        self.Tools.createTempFiles()
        
    def tearDown(self):
        self.Tools.removeTempFiles()
        
    def testTestFileDirectory(self):
        assert os.path.isdir( testFileDirectory ) == True
        
    def testTestFiles(self):
        absDirs = [os.path.join(testFileDirectory,name) for name in testSubDirectories]
        while( len(absDirs) > 0 ):
            currentDir = absDirs.pop()
            for files in testFileNames[-1] :
                print currentDir
                print files
                assert os.path.isfile( os.path.join(currentDir, files) ) == True
