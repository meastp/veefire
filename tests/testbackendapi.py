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

from api.dbapi import Database, Season, Show, Episode, Filesystem
from api.backendapi import Backends, BackendInterface
from testproperties import Tools

class testBackends :
    """
    Test Backends Class
    """
    def setUp(self) :
        self.Tools = Tools()
        self.Tools.createRootDir()
        self.Tools.createBackendFiles()
        
        self.backend1 = Backends()
        
    def tearDown(self):
        self.Tools.removeTempFiles()
        
    def testGetBackends(self):
        
        assert self.backend1.getBackends(self.Tools.BackendDirectory) == ['imdbtvbackend']
        

class testBackendInterface :
    """
    Test BackendInterface Class
    """
    def setUp(self) :
        self.Tools = Tools()
        self.Tools.createRootDir()
        self.Tools.createBackendFiles()
        
        self.Tools.createDatabaseFiles()
        
        self.BaIf1 = BackendInterface(self.Tools.databaseDir)
        
    def tearDown(self):
        self.Tools.removeTempFiles()
        
    def testAddNewShow(self):
        
        Show1 = Show( "Test Show One", "60", Filesystem("FS1"), "dummybackend", "dummyurlone" )
        Show2 = Show( "Test Show Two", "60", Filesystem("FS2"), "dummybackend", "dummyurltwo" )
        Show3 = Show( "Test Show Three", "60", Filesystem("FS3"), "dummybackend", "dummyurlthree" )
        
        assert self.BaIf1.addNewShow( Show1 ) == Show1
        assert self.BaIf1.addNewShow( Show1 ) == None
        assert self.BaIf1.addNewShow( Show2 ) == Show2
        assert self.BaIf1.addNewShow( Show( "Test Show Two", "60", Filesystem("FS2"), "dummybackend", "dummyurltwo" )) == None
        assert self.BaIf1.addNewShow( Show3 ) == Show3
        
    def testUpdateDatabase(self):
        
        #Depends on Database.writeDB()
        
        assert False
        
    def testFillUpdateDB(self):
        
        #Depends on Backends, databases, update.
        
        assert False
        
    def testCompareDetails(self):
        
        Episode1 = Episode( "2", "What A Title", "6 November, 2008" )
        Episode2 = Episode( "333", "For A TV Show", "18 November, 2008" )
        Episode3 = Episode( "4", "What A Title", "6 November, 2008")
        Episode4 = Episode( "2", "What A Title", "6 November, 2008" )
        Episode5 = Episode( "333", "For A TV Show", "18 November, 2008" )
        Episode6 = Episode( "4", "What A Title", "6 November, 2008")
        
        Season1 = Season('1')
        Season2 = Season('2')
        
        Season1.addEpisode( Episode1 )
        Season1.addEpisode( Episode2 )
        Season1.addEpisode( Episode3 )
        Season2.addEpisode( Episode4 )
        Season2.addEpisode( Episode5 )
        Season2.addEpisode( Episode6 )
        
        Season3 = Season1
        Season4 = Season2
        
        Show1 = Show( "Test Show One", "60", Filesystem("FS1"), "dummybackend", "dummyurlone" )
        Show2 = Show( "Test Show Two", "60", Filesystem("FS2"), "dummybackend", "dummyurltwo" )
        
        Show3 = Show2
        
        Show1.addSeason(Season1)
        Show1.addSeason(Season2)
        Show2.addSeason(Season3)
        Show2.addSeason(Season4)
        
        assert self.BaIf1.compareDetails( Show1, Show2 ) == Show3
        assert self.BaIf1.compareDetails( Show1, Show2 ) == Show3
        
    def testCompareSeasons(self):
        
        Episode1 = Episode( "2", "What A Title", "6 November, 2008" )
        Episode2 = Episode( "333", "For A TV Show", "18 November, 2008" )
        Episode3 = Episode( "4", "What A Title", "6 November, 2008")
        Episode4 = Episode( "2", "What A Title", "6 November, 2008" )
        Episode5 = Episode( "333", "For A TV Show", "18 November, 2008" )
        Episode6 = Episode( "4", "What A Title", "6 November, 2008")
        
        Season1 = Season('1')
        Season2 = Season('2')
        
        Season1.addEpisode( Episode1 )
        Season1.addEpisode( Episode2 )
        Season1.addEpisode( Episode3 )
        Season2.addEpisode( Episode4 )
        Season2.addEpisode( Episode5 )
        Season2.addEpisode( Episode6 )
        
        Season3 = Season2
        
        assert self.BaIf1.compareSeasons( Season1, Season2 ) == Season3
        assert self.BaIf1.compareSeasons( Season1, Season2 ) == Season3
        
    def testCompareEpisodes(self):
        
        Episode1 = Episode( "2", "What A Title", "6 November, 2008" )
        Episode2 = Episode( "2", "For A TV Show", "6 November, 2008" ) # Gives NotImplemented Error, which is correct behaviour.
        Episode3 = Episode( "2", "What A Title", "6 November, 2008")
        
        assert self.BaIf1.compareEpisodes(Episode1, Episode1 ) == None
        assert self.BaIf1.compareEpisodes(Episode1, Episode3 ) == None
