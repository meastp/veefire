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

# CREATE FILE NAMES FOR TESTING
#TODO: Create checks if directories exist.
import os
import shutil

def createTempFiles():
    rootDir = testFileDirectory
    testDirs = testSubDirectories
    testFiles = testFileNames
    
    if os.path.exists(rootDir) :
        removeTempFiles()
    os.mkdir(rootDir)
    
    absDirs = [os.path.join(rootDir,name) for name in testDirs]
    for directory in absDirs:
        os.mkdir(directory)
    # replaces os.system in python 2.6 : p = Popen("command" + "arg", shell=True)
    # sts = os.waitpid(p.pid, 0)
    while( len(absDirs) > 0 ):
        currentDir = absDirs.pop()
        for files in testFiles[-1] :
            os.system('touch ' + '"' + os.path.join( currentDir, files ) + '"')
    return

def removeTempFiles():
    rootDir = testFileDirectory
    
    shutil.rmtree(rootDir)
    return

def getRootDir():
    return testFileDirectory

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
