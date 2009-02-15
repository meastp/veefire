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

import nose

from api.dbapi import Database, Show, Filesystem
from api.renameapi import FileName
from testproperties import Tools

class testFileName :
    """
    Test FileName Class
    """
    def setUp(self) :
        self.Tools = Tools()
        self.Tools.createRootDir()
        self.Tools.createDatabaseFiles()
        
        self.database = Database(self.Tools.databaseDir)
        self.database.loadDB()
        self.filename1 = FileName( 'black.books.s01e02.avi', self.database )
        self.filename2 = FileName( 'spaced.2x03.avi', self.database )
        self.filename3 = FileName( 'csi.s02E13.avi', self.database )
        
    def tearDown(self):
        self.Tools.removeTempFiles()
        
    def testGetPattern(self):
        assert self.filename1.getPattern() == self.filename1.pattern1
        assert self.filename2.getPattern() == self.filename2.pattern2
        assert self.filename3.getPattern() == self.filename3.pattern1
        
    def testGetSeason(self):
        assert self.filename1.getSeason() == '1'
        assert self.filename2.getSeason() == '2'
        assert self.filename3.getSeason() == '2'
        
    def testGetEpisode(self):
        assert self.filename1.getEpisode() == '2'
        assert self.filename2.getEpisode() == '3'
        assert self.filename3.getEpisode() == '13'
        
    def testGetMatchingShows(self):
        assert self.filename1.getMatchingShows().name == 'Black Books'
        assert self.filename2.getMatchingShows().name == 'Spaced'
        assert self.filename3.getMatchingShows().name == 'C.S.I'
        
#    def testGenerateFileName(self):
#        # generateFileName(Style=None)
#        assert False
