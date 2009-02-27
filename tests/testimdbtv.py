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
from backends.imdbtv import Regexes, Backend
from testproperties import Tools

class testBackend :
    """
    Test Backend Class
    """
    def setUp(self) :
        self.Tools = Tools()
        self.Tools.createRootDir()
        self.Tools.createBackendFiles()
        self.Tools.createDatabaseFiles()
        
        self.backend = Backend()
        
        validShows1 = [ Show(  "Spaced", "60", Filesystem( 'FS1' ), "imdbtvbackend", "tt0187664" ) ]
        self.database1 = Database(self.Tools.databaseDir, validShows1)
        self.database1.loadDB()
        
        validShows2 = [ Show(  "Black Books", "30", Filesystem( 'FS1' ), "imdbtvbackend", "tt0262150" ) ]
        self.database2 = Database(self.Tools.databaseDir, validShows2)
        self.database2.loadDB()
        
    def tearDown(self):
        self.Tools.removeTempFiles()
        
    def testDownloadShowList(self):
        
        content = self.backend.downloadShowList(self.database1.database)
        assert [ show.name for show in content.keys() ] == ['Spaced']
        
        content = self.backend.downloadShowList(self.database2.database)
        assert [ show.name for show in content.keys() ] == ['Black Books']
        
    def testGetShowDetails(self):
        
        updateDB1 = self.backend.getShowDetails( self.backend.downloadShowList(self.database1.database))
        assert [ (show.name, season.name, episode.name, episode.title ) for show in updateDB1.database for season in show.seasons for episode in season.episodes ] == [('Spaced', '1', '1', 'Beginnings'), ('Spaced', '1', '2', 'Gatherings'), ('Spaced', '1', '3', 'Art'), ('Spaced', '1', '4', 'Battles'), ('Spaced', '1', '5', 'Chaos'), ('Spaced', '1', '6', 'Epiphanies'), ('Spaced', '1', '7', 'Ends'), ('Spaced', '2', '1', 'Back'), ('Spaced', '2', '2', 'Change'), ('Spaced', '2', '3', 'Mettle'), ('Spaced', '2', '4', 'Help'), ('Spaced', '2', '5', 'Gone'), ('Spaced', '2', '6', 'Dissolution'), ('Spaced', '2', '7', 'Leaves')]
        
        updateDB2 = self.backend.getShowDetails( self.backend.downloadShowList(self.database2.database))
        assert [ (show.name, season.name, episode.name, episode.title ) for show in updateDB2.database for season in show.seasons for episode in season.episodes ] == [('Black Books', '1', '1', 'Cooking the Books'), ('Black Books', '1', '2', "Manny's First Day"), ('Black Books', '1', '3', 'The Grapes of Wrath'), ('Black Books', '1', '4', 'The Blackout'), ('Black Books', '1', '5', 'The Big Lock-Out'), ('Black Books', '1', '6', "He's Leaving Home"), ('Black Books', '2', '1', 'The Entertainer'), ('Black Books', '2', '2', 'Fever'), ('Black Books', '2', '3', 'The Fixer'), ('Black Books', '2', '4', 'Blood'), ('Black Books', '2', '5', 'Hello Sun'), ('Black Books', '2', '6', 'A Nice Change'), ('Black Books', '3', '1', 'Manny Come Home'), ('Black Books', '3', '2', 'Elephants and Hens'), ('Black Books', '3', '3', 'Moo-Ma and Moo-Pa'), ('Black Books', '3', '4', 'A Little Flutter'), ('Black Books', '3', '5', 'The Travel Writer'), ('Black Books', '3', '6', 'Party')]
        
class testRegexes :
    """
    Test Regexes Class
    """
    def setUp(self) :
        self.Tools = Tools()
        self.Tools.createRootDir()
        self.Tools.createBackendFiles()
        
        self.regex = Regexes()
        
    def tearDown(self):
        self.Tools.removeTempFiles()
        
    def testRemoveTags(self):
        
        assert self.regex.removeTags( '<h1>Text</h1>' ) == 'Text'
        #assert self.regex.removeTags( '<h1><h1>Text</h1></h1>' ) == 'Text'
        #assert self.regex.removeTags( '<h1>Text</h1></h1>' ) == 'Text'
        
    def testExtractAirDate(self):
        
        self.regex.extractAirDate( '<strong>6 November 2008</strong>' ) == ('6 November 2008',)
        
    def testExtractEpSeTitle(self):
        
        assert self.regex.extractEpSeTitle( '<h3>Season 00051, Episode 010: <a href="/title/t0987tsa/">Title</a></h3>' ) == ('51', '10', 'Title')
        assert self.regex.extractEpSeTitle( '<h3>Season 9, Episode 201: <a href="/title/t/">T80932sdf/[]}}]</a></h3>' ) == ('9', '201', 'T80932sdf/[]}}]')
        assert self.regex.extractEpSeTitle( '<h3>Season 12, Episode 00: <a href="/title/098sdft8/">) s{ }350dfklj</a></h3>' ) == ('12', '0', ') s{ }350dfklj')
        assert self.regex.extractEpSeTitle( '<h3>Season 001000050, Episode 010: <a href="/title/098sdft8/"></a></h3>' ) == ('1000050', '10', None)
        

