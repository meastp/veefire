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
        filesystemsXML = open(self.filetypesXML ,"w")
        filesystemsXML.writelines(testFiletypesContent)
        filesystemsXML.close()

# TEST CLASS

class testFiles:
    def setUp(self):
        createTempFiles()
        
    def tearDown(self):
        removeTempFiles()
        
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
