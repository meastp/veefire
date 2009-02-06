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

testFileDirectory = '/home/meastp'
testSubDirectories = [ 'Black Books', 'CSI', 'Spaced']
testFileNames = [   [ 'blackbooks.s01e02.avi', 'bb.s03e05.avi'],
                    [ 'CSIS01E11.avi', 'CSI.5x12.avi' ],
                    [ 'Spaced.2x3.avi', 'Spaced.S02E03.avi']   ]

# CREATE FILE NAMES FOR TESTING

import os

def createTempFiles(rootDir, testDirs, testFiles):
    os.mkdir(rootDir)
    absDirs = [os.path.join(rootDir,name) for name in testDirs]
    os.makedirs(absDirs)
    # replaces os.system in python 2.6 : p = Popen("command" + "arg", shell=True)
    # sts = os.waitpid(p.pid, 0)
    while( len(absDirs) > 0 ):
        currentDir = absDirs.pop()
        for files in testFiles[-1]
            os.system('touch ' + '""' + os.path.join( currentDir, files ) + '""')
    return

# TEST CLASS

class testFiles:
    def __init__():
        createTempFiles(testFileDirectory, testSubDirectories, testFileNames)
    def getRootDir():
        return testFileDirectory
        
    def testTestFileDirectory():
        assert os.path.isdir( testFileDirectory ) == True
        
    def testTestFiles():
        absDirs = [rootDir+name for name in testDirs]
        while( len(absDirs) > 0 ):
        currentDir = absDirs.pop()
        for files in testFiles[-1]
            assert os.path.isfile( os.path.join(currentDir, files) ) == True
    #TODO: Create a cleanup-function to delete the files after.
