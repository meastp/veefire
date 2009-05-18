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
import copy
import os

from veefire.api.dbapi import Database, Season, Show, Episode
from veefire.api.backendapi import Backends, BackendInterface
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
        
        class NewBackendInterface(BackendInterface):
            def solveEpisodeConflicts(self, firstEpisode, secondEpisode):
                return firstEpisode
        
        self.BaIf1 = NewBackendInterface(self.Tools.databaseDir)
        
        
        
    def tearDown(self):
        self.Tools.removeTempFiles()
        
    def testAddNewShow(self):
        
        Show1 = Show( "Test Show One", "60", "dummybackend", "dummyurlone" )
        Show2 = Show( "Test Show Two", "60", "dummybackend", "dummyurltwo" )
        Show3 = Show( "Test Show Three", "60", "dummybackend", "dummyurlthree" )
        
        assert self.BaIf1.addNewShow( Show1 ) == Show1
        assert self.BaIf1.addNewShow( Show1 ) == None
        assert self.BaIf1.addNewShow( Show2 ) == Show2
        assert self.BaIf1.addNewShow( Show( "Test Show Two", "60", "dummybackend", "dummyurltwo" )) == None
        assert self.BaIf1.addNewShow( Show3 ) == Show3
        
    def testUpdateDatabase(self):
        
        assert os.path.exists(self.Tools.databaseDir) == True
        
        DB2 = [ ]
        for filename in self.Tools.databaseFiles.values() :
            testfile = open(os.path.join( self.Tools.databaseDir, filename ),"r")
            content = testfile.read()
            testfile.close()
            DB2.append( ( content , filename ) )
        
        assert DB2 == [('<?xml version="1.0" encoding="UTF-8"?>\n<tvshow>\n  <showproperties backend="imdbtvbackend" duration="60" name="Spaced" url="tt0187664"/>\n  <aliases>\n    <alias value="spaced"/>\n  </aliases>\n  <season number="1">\n    <episode airdate="24 September 1999" arc="none" number="1" title="Beginnings"/>\n    <episode airdate="1 October 1999" arc="none" number="2" title="Gatherings"/>\n    <episode airdate="8 October 1999" arc="none" number="3" title="Art"/>\n    <episode airdate="15 October 1999" arc="none" number="4" title="Battles"/>\n    <episode airdate="22 October 1999" arc="none" number="5" title="Chaos"/>\n    <episode airdate="29 October 1999" arc="none" number="6" title="Epiphanies"/>\n    <episode airdate="5 November 1999" arc="none" number="7" title="Ends"/>\n  </season>\n  <season number="2">\n    <episode airdate="23 February 2001" arc="none" number="1" title="Back"/>\n    <episode airdate="2 March 2001" arc="none" number="2" title="Change"/>\n    <episode airdate="9 March 2001" arc="none" number="3" title="Mettle"/>\n    <episode airdate="23 March 2001" arc="none" number="4" title="Help"/>\n    <episode airdate="None" arc="none" number="5" title="Gone"/>\n    <episode airdate="6 April 2001" arc="none" number="6" title="Dissolution"/>\n    <episode airdate="13 April 2001" arc="none" number="7" title="Testkonflikt"/>\n  </season>\n</tvshow>', 'spaced.show'), ('<?xml version="1.0" encoding="UTF-8"?>\n<tvshow>\n  <showproperties backend="imdbtvbackend" duration="30" name="Black Books" url="tt0262150"/>\n  <aliases>\n    <alias value="blackbooks"/>\n    <alias value="black books"/>\n    <alias value="black.books"/>\n    <alias value="bb"/>\n  </aliases>\n  <season number="1">\n    <episode airdate="29 September 2000" arc="none" number="1" title="Cooking the Books"/>\n    <episode airdate="6 October 2000" arc="none" number="2" title="Manny\'s First Day"/>\n    <episode airdate="13 October 2000" arc="none" number="3" title="The Grapes of Wrath"/>\n    <episode airdate="20 October 2000" arc="none" number="4" title="The Blackout"/>\n    <episode airdate="27 October 2000" arc="none" number="5" title="The Big Lock-Out"/>\n    <episode airdate="3 November 2000" arc="none" number="6" title="He\'s Leaving Home"/>\n  </season>\n  <season number="2">\n    <episode airdate="1 March 2002" arc="none" number="1" title="The Entertainer"/>\n    <episode airdate="8 March 2002" arc="none" number="2" title="Fever"/>\n    <episode airdate="15 March 2002" arc="none" number="3" title="The Fixer"/>\n    <episode airdate="22 March 2002" arc="none" number="4" title="Blood"/>\n    <episode airdate="29 March 2002" arc="none" number="5" title="Hello Sun"/>\n    <episode airdate="5 April 2002" arc="none" number="6" title="A Nice Change"/>\n  </season>\n  <season number="3">\n    <episode airdate="11 March 2004" arc="none" number="1" title="Manny Come Home"/>\n    <episode airdate="18 March 2004" arc="none" number="2" title="Elephants and Hens"/>\n    <episode airdate="25 March 2004" arc="none" number="3" title="Moo-Ma and Moo-Pa"/>\n    <episode airdate="1 April 2004" arc="none" number="4" title="A Little Flutter"/>\n    <episode airdate="8 April 2004" arc="none" number="5" title="The Travel Writer"/>\n    <episode airdate="15 April 2004" arc="none" number="6" title="Party"/>\n  </season>\n</tvshow>\n', 'blackbooks.show'), ('<?xml version="1.0" encoding="UTF-8"?>\n<tvshow>\n  <showproperties backend="imdbtvbackend" duration="60" name="C.S.I" url="tt0247082"/>\n  <aliases>\n    <alias value="csi"/>\n  </aliases>\n  <season number="1">\n    <episode airdate="6 October 2000" arc="none" number="1" title="Pilot"/>\n    <episode airdate="13 October 2000" arc="none" number="2" title="Cool Change"/>\n    <episode airdate="20 October 2000" arc="none" number="3" title="Crate \'n\' Burial"/>\n    <episode airdate="27 October 2000" arc="none" number="4" title="Pledging Mr. Johnson"/>\n    <episode airdate="3 November 2000" arc="none" number="5" title="Friends &amp; Lovers"/>\n    <episode airdate="10 November 2000" arc="none" number="6" title="Who Are You?"/>\n    <episode airdate="17 November 2000" arc="none" number="7" title="Blood Drops"/>\n    <episode airdate="24 November 2000" arc="none" number="8" title="Anonymous"/>\n    <episode airdate="8 December 2000" arc="none" number="9" title="Unfriendly Skies"/>\n    <episode airdate="22 December 2000" arc="none" number="10" title="Sex, Lies and Larvae"/>\n    <episode airdate="12 January 2001" arc="none" number="11" title="I-15 Murders"/>\n    <episode airdate="1 February 2001" arc="none" number="12" title="Fahrenheit 932"/>\n    <episode airdate="8 February 2001" arc="none" number="13" title="Boom"/>\n    <episode airdate="15 February 2001" arc="none" number="14" title="To Halve and to Hold"/>\n    <episode airdate="22 February 2001" arc="none" number="15" title="Table Stakes"/>\n    <episode airdate="1 March 2001" arc="none" number="16" title="Too Tough to Die"/>\n    <episode airdate="8 March 2001" arc="none" number="17" title="Face Lift"/>\n    <episode airdate="29 March 2001" arc="none" number="18" title="$35K O.B.O."/>\n    <episode airdate="12 April 2001" arc="none" number="19" title="Gentle, Gentle"/>\n    <episode airdate="19 April 2001" arc="none" number="20" title="Sounds of Silence"/>\n    <episode airdate="26 April 2001" arc="none" number="21" title="Justice Is Served"/>\n    <episode airdate="10 May 2001" arc="none" number="22" title="Evaluation Day"/>\n    <episode airdate="17 May 2001" arc="none" number="23" title="The Strip Strangler"/>\n  </season>\n  <season number="2">\n    <episode airdate="27 September 2001" arc="none" number="1" title="Burked"/>\n    <episode airdate="4 October 2001" arc="none" number="2" title="Chaos Theory"/>\n    <episode airdate="11 October 2001" arc="none" number="3" title="Overload"/>\n    <episode airdate="18 October 2001" arc="none" number="4" title="Bully for You"/>\n    <episode airdate="25 October 2001" arc="none" number="5" title="Scuba Doobie-Doo"/>\n    <episode airdate="1 November 2001" arc="none" number="6" title="Alter Boys"/>\n    <episode airdate="8 November 2001" arc="none" number="7" title="Caged"/>\n    <episode airdate="15 November 2001" arc="none" number="8" title="Slaves of Las Vegas"/>\n    <episode airdate="22 November 2001" arc="none" number="9" title="And Then There Were None"/>\n    <episode airdate="6 December 2001" arc="none" number="10" title="Ellie"/>\n    <episode airdate="13 December 2001" arc="none" number="11" title="Organ Grinder"/>\n    <episode airdate="20 December 2001" arc="none" number="12" title="You\'ve Got Male"/>\n    <episode airdate="17 January 2002" arc="none" number="13" title="Identity Crisis"/>\n    <episode airdate="None" arc="none" number="14" title="The Finger"/>\n    <episode airdate="7 February 2002" arc="none" number="15" title="Burden of Proof"/>\n    <episode airdate="28 February 2002" arc="none" number="16" title="Primum Non Nocere"/>\n    <episode airdate="7 March 2002" arc="none" number="17" title="Felonious Monk"/>\n    <episode airdate="28 March 2002" arc="none" number="18" title="Chasing the Bus"/>\n    <episode airdate="4 April 2002" arc="none" number="19" title="Stalker"/>\n    <episode airdate="25 April 2002" arc="none" number="20" title="Cats in the Cradle..."/>\n    <episode airdate="2 May 2002" arc="none" number="21" title="Anatomy of a Lye"/>\n    <episode airdate="9 May 2002" arc="none" number="22" title="Cross-Jurisdictions"/>\n    <episode airdate="18 May 2002" arc="none" number="23" title="The Hunger Artist"/>\n  </season>\n</tvshow>\n', 'csi.show')]
        
        show1 = self.BaIf1.currentDB.getShow( Show('Spaced', '30', 'imdbtvbackend', 'tt000000') )
        show1.removeSeason( Season('1') )
        self.BaIf1.currentDB.removeShow( Show('C.S.I', '60', 'imdbtvbackend', 'tt000000') )
        
        self.BaIf1.updateDatabase()
        
        DB3 = [ ]
        for filename in self.Tools.databaseFiles.values() :
            testfile = open(os.path.join( self.Tools.databaseDir, filename ),"r")
            content = testfile.read()
            testfile.close()
            DB3.append( ( content , filename ) )
            
        assert DB3 == [('<tvshow><showproperties backend="imdbtvbackend" duration="60" name="Spaced" url="tt0187664" /><aliases /><season number="1"><episode airdate="24 September 1999" arc="none" number="1" title="Beginnings" /><episode airdate="1 October 1999" arc="none" number="2" title="Gatherings" /><episode airdate="8 October 1999" arc="none" number="3" title="Art" /><episode airdate="15 October 1999" arc="none" number="4" title="Battles" /><episode airdate="22 October 1999" arc="none" number="5" title="Chaos" /><episode airdate="29 October 1999" arc="none" number="6" title="Epiphanies" /><episode airdate="5 November 1999" arc="none" number="7" title="Ends" /></season><season number="2"><episode airdate="23 February 2001" arc="none" number="1" title="Back" /><episode airdate="2 March 2001" arc="none" number="2" title="Change" /><episode airdate="9 March 2001" arc="none" number="3" title="Mettle" /><episode airdate="23 March 2001" arc="none" number="4" title="Help" /><episode airdate="None" arc="none" number="5" title="Gone" /><episode airdate="6 April 2001" arc="none" number="6" title="Dissolution" /><episode airdate="13 April 2001" arc="none" number="7" title="Testkonflikt" /></season></tvshow>', 'spaced.show'), ('<tvshow><showproperties backend="imdbtvbackend" duration="30" name="Black Books" url="tt0262150" /><aliases /><season number="1"><episode airdate="29 September 2000" arc="none" number="1" title="Cooking the Books" /><episode airdate="6 October 2000" arc="none" number="2" title="Manny&apos;s First Day" /><episode airdate="13 October 2000" arc="none" number="3" title="The Grapes of Wrath" /><episode airdate="20 October 2000" arc="none" number="4" title="The Blackout" /><episode airdate="27 October 2000" arc="none" number="5" title="The Big Lock-Out" /><episode airdate="3 November 2000" arc="none" number="6" title="He&apos;s Leaving Home" /></season><season number="2"><episode airdate="1 March 2002" arc="none" number="1" title="The Entertainer" /><episode airdate="8 March 2002" arc="none" number="2" title="Fever" /><episode airdate="15 March 2002" arc="none" number="3" title="The Fixer" /><episode airdate="22 March 2002" arc="none" number="4" title="Blood" /><episode airdate="29 March 2002" arc="none" number="5" title="Hello Sun" /><episode airdate="5 April 2002" arc="none" number="6" title="A Nice Change" /></season><season number="3"><episode airdate="11 March 2004" arc="none" number="1" title="Manny Come Home" /><episode airdate="18 March 2004" arc="none" number="2" title="Elephants and Hens" /><episode airdate="25 March 2004" arc="none" number="3" title="Moo-Ma and Moo-Pa" /><episode airdate="1 April 2004" arc="none" number="4" title="A Little Flutter" /><episode airdate="8 April 2004" arc="none" number="5" title="The Travel Writer" /><episode airdate="15 April 2004" arc="none" number="6" title="Party" /></season></tvshow>', 'blackbooks.show'), ('<?xml version="1.0" encoding="UTF-8"?>\n<tvshow>\n  <showproperties backend="imdbtvbackend" duration="60" name="C.S.I" url="tt0247082"/>\n  <aliases>\n    <alias value="csi"/>\n  </aliases>\n  <season number="1">\n    <episode airdate="6 October 2000" arc="none" number="1" title="Pilot"/>\n    <episode airdate="13 October 2000" arc="none" number="2" title="Cool Change"/>\n    <episode airdate="20 October 2000" arc="none" number="3" title="Crate \'n\' Burial"/>\n    <episode airdate="27 October 2000" arc="none" number="4" title="Pledging Mr. Johnson"/>\n    <episode airdate="3 November 2000" arc="none" number="5" title="Friends &amp; Lovers"/>\n    <episode airdate="10 November 2000" arc="none" number="6" title="Who Are You?"/>\n    <episode airdate="17 November 2000" arc="none" number="7" title="Blood Drops"/>\n    <episode airdate="24 November 2000" arc="none" number="8" title="Anonymous"/>\n    <episode airdate="8 December 2000" arc="none" number="9" title="Unfriendly Skies"/>\n    <episode airdate="22 December 2000" arc="none" number="10" title="Sex, Lies and Larvae"/>\n    <episode airdate="12 January 2001" arc="none" number="11" title="I-15 Murders"/>\n    <episode airdate="1 February 2001" arc="none" number="12" title="Fahrenheit 932"/>\n    <episode airdate="8 February 2001" arc="none" number="13" title="Boom"/>\n    <episode airdate="15 February 2001" arc="none" number="14" title="To Halve and to Hold"/>\n    <episode airdate="22 February 2001" arc="none" number="15" title="Table Stakes"/>\n    <episode airdate="1 March 2001" arc="none" number="16" title="Too Tough to Die"/>\n    <episode airdate="8 March 2001" arc="none" number="17" title="Face Lift"/>\n    <episode airdate="29 March 2001" arc="none" number="18" title="$35K O.B.O."/>\n    <episode airdate="12 April 2001" arc="none" number="19" title="Gentle, Gentle"/>\n    <episode airdate="19 April 2001" arc="none" number="20" title="Sounds of Silence"/>\n    <episode airdate="26 April 2001" arc="none" number="21" title="Justice Is Served"/>\n    <episode airdate="10 May 2001" arc="none" number="22" title="Evaluation Day"/>\n    <episode airdate="17 May 2001" arc="none" number="23" title="The Strip Strangler"/>\n  </season>\n  <season number="2">\n    <episode airdate="27 September 2001" arc="none" number="1" title="Burked"/>\n    <episode airdate="4 October 2001" arc="none" number="2" title="Chaos Theory"/>\n    <episode airdate="11 October 2001" arc="none" number="3" title="Overload"/>\n    <episode airdate="18 October 2001" arc="none" number="4" title="Bully for You"/>\n    <episode airdate="25 October 2001" arc="none" number="5" title="Scuba Doobie-Doo"/>\n    <episode airdate="1 November 2001" arc="none" number="6" title="Alter Boys"/>\n    <episode airdate="8 November 2001" arc="none" number="7" title="Caged"/>\n    <episode airdate="15 November 2001" arc="none" number="8" title="Slaves of Las Vegas"/>\n    <episode airdate="22 November 2001" arc="none" number="9" title="And Then There Were None"/>\n    <episode airdate="6 December 2001" arc="none" number="10" title="Ellie"/>\n    <episode airdate="13 December 2001" arc="none" number="11" title="Organ Grinder"/>\n    <episode airdate="20 December 2001" arc="none" number="12" title="You\'ve Got Male"/>\n    <episode airdate="17 January 2002" arc="none" number="13" title="Identity Crisis"/>\n    <episode airdate="None" arc="none" number="14" title="The Finger"/>\n    <episode airdate="7 February 2002" arc="none" number="15" title="Burden of Proof"/>\n    <episode airdate="28 February 2002" arc="none" number="16" title="Primum Non Nocere"/>\n    <episode airdate="7 March 2002" arc="none" number="17" title="Felonious Monk"/>\n    <episode airdate="28 March 2002" arc="none" number="18" title="Chasing the Bus"/>\n    <episode airdate="4 April 2002" arc="none" number="19" title="Stalker"/>\n    <episode airdate="25 April 2002" arc="none" number="20" title="Cats in the Cradle..."/>\n    <episode airdate="2 May 2002" arc="none" number="21" title="Anatomy of a Lye"/>\n    <episode airdate="9 May 2002" arc="none" number="22" title="Cross-Jurisdictions"/>\n    <episode airdate="18 May 2002" arc="none" number="23" title="The Hunger Artist"/>\n  </season>\n</tvshow>\n', 'csi.show')]
        
    def testFillUpdateDB(self):
        
        assert os.path.exists(self.Tools.databaseDir) == True
        
        assert [ ( show.name, season.name, episode.name, episode.title ) for show in self.BaIf1.currentDB.database for season in show.seasons for episode in season.episodes ] == [('C.S.I', '1', '1', 'Pilot'), ('C.S.I', '1', '2', 'Cool Change'), ('C.S.I', '1', '3', "Crate 'n' Burial"), ('C.S.I', '1', '4', 'Pledging Mr. Johnson'), ('C.S.I', '1', '5', 'Friends & Lovers'), ('C.S.I', '1', '6', 'Who Are You?'), ('C.S.I', '1', '7', 'Blood Drops'), ('C.S.I', '1', '8', 'Anonymous'), ('C.S.I', '1', '9', 'Unfriendly Skies'), ('C.S.I', '1', '10', 'Sex, Lies and Larvae'), ('C.S.I', '1', '11', 'I-15 Murders'), ('C.S.I', '1', '12', 'Fahrenheit 932'), ('C.S.I', '1', '13', 'Boom'), ('C.S.I', '1', '14', 'To Halve and to Hold'), ('C.S.I', '1', '15', 'Table Stakes'), ('C.S.I', '1', '16', 'Too Tough to Die'), ('C.S.I', '1', '17', 'Face Lift'), ('C.S.I', '1', '18', '$35K O.B.O.'), ('C.S.I', '1', '19', 'Gentle, Gentle'), ('C.S.I', '1', '20', 'Sounds of Silence'), ('C.S.I', '1', '21', 'Justice Is Served'), ('C.S.I', '1', '22', 'Evaluation Day'), ('C.S.I', '1', '23', 'The Strip Strangler'), ('C.S.I', '2', '1', 'Burked'), ('C.S.I', '2', '2', 'Chaos Theory'), ('C.S.I', '2', '3', 'Overload'), ('C.S.I', '2', '4', 'Bully for You'), ('C.S.I', '2', '5', 'Scuba Doobie-Doo'), ('C.S.I', '2', '6', 'Alter Boys'), ('C.S.I', '2', '7', 'Caged'), ('C.S.I', '2', '8', 'Slaves of Las Vegas'), ('C.S.I', '2', '9', 'And Then There Were None'), ('C.S.I', '2', '10', 'Ellie'), ('C.S.I', '2', '11', 'Organ Grinder'), ('C.S.I', '2', '12', "You've Got Male"), ('C.S.I', '2', '13', 'Identity Crisis'), ('C.S.I', '2', '14', 'The Finger'), ('C.S.I', '2', '15', 'Burden of Proof'), ('C.S.I', '2', '16', 'Primum Non Nocere'), ('C.S.I', '2', '17', 'Felonious Monk'), ('C.S.I', '2', '18', 'Chasing the Bus'), ('C.S.I', '2', '19', 'Stalker'), ('C.S.I', '2', '20', 'Cats in the Cradle...'), ('C.S.I', '2', '21', 'Anatomy of a Lye'), ('C.S.I', '2', '22', 'Cross-Jurisdictions'), ('C.S.I', '2', '23', 'The Hunger Artist'), ('Spaced', '1', '1', 'Beginnings'), ('Spaced', '1', '2', 'Gatherings'), ('Spaced', '1', '3', 'Art'), ('Spaced', '1', '4', 'Battles'), ('Spaced', '1', '5', 'Chaos'), ('Spaced', '1', '6', 'Epiphanies'), ('Spaced', '1', '7', 'Ends'), ('Spaced', '2', '1', 'Back'), ('Spaced', '2', '2', 'Change'), ('Spaced', '2', '3', 'Mettle'), ('Spaced', '2', '4', 'Help'), ('Spaced', '2', '5', 'Gone'), ('Spaced', '2', '6', 'Dissolution'), ('Spaced', '2', '7', 'Testkonflikt'), ('Black Books', '1', '1', 'Cooking the Books'), ('Black Books', '1', '2', "Manny's First Day"), ('Black Books', '1', '3', 'The Grapes of Wrath'), ('Black Books', '1', '4', 'The Blackout'), ('Black Books', '1', '5', 'The Big Lock-Out'), ('Black Books', '1', '6', "He's Leaving Home"), ('Black Books', '2', '1', 'The Entertainer'), ('Black Books', '2', '2', 'Fever'), ('Black Books', '2', '3', 'The Fixer'), ('Black Books', '2', '4', 'Blood'), ('Black Books', '2', '5', 'Hello Sun'), ('Black Books', '2', '6', 'A Nice Change'), ('Black Books', '3', '1', 'Manny Come Home'), ('Black Books', '3', '2', 'Elephants and Hens'), ('Black Books', '3', '3', 'Moo-Ma and Moo-Pa'), ('Black Books', '3', '4', 'A Little Flutter'), ('Black Books', '3', '5', 'The Travel Writer'), ('Black Books', '3', '6', 'Party')]
        
        show1 = self.BaIf1.currentDB.getShow( Show('Spaced', '30', 'imdbtvbackend', 'tt000000') )
        show1.removeSeason( Season('1') )
        
        assert [ ( show.name, season.name, episode.name, episode.title ) for show in self.BaIf1.currentDB.database for season in show.seasons for episode in season.episodes ] == [('C.S.I', '1', '1', 'Pilot'), ('C.S.I', '1', '2', 'Cool Change'), ('C.S.I', '1', '3', "Crate 'n' Burial"), ('C.S.I', '1', '4', 'Pledging Mr. Johnson'), ('C.S.I', '1', '5', 'Friends & Lovers'), ('C.S.I', '1', '6', 'Who Are You?'), ('C.S.I', '1', '7', 'Blood Drops'), ('C.S.I', '1', '8', 'Anonymous'), ('C.S.I', '1', '9', 'Unfriendly Skies'), ('C.S.I', '1', '10', 'Sex, Lies and Larvae'), ('C.S.I', '1', '11', 'I-15 Murders'), ('C.S.I', '1', '12', 'Fahrenheit 932'), ('C.S.I', '1', '13', 'Boom'), ('C.S.I', '1', '14', 'To Halve and to Hold'), ('C.S.I', '1', '15', 'Table Stakes'), ('C.S.I', '1', '16', 'Too Tough to Die'), ('C.S.I', '1', '17', 'Face Lift'), ('C.S.I', '1', '18', '$35K O.B.O.'), ('C.S.I', '1', '19', 'Gentle, Gentle'), ('C.S.I', '1', '20', 'Sounds of Silence'), ('C.S.I', '1', '21', 'Justice Is Served'), ('C.S.I', '1', '22', 'Evaluation Day'), ('C.S.I', '1', '23', 'The Strip Strangler'), ('C.S.I', '2', '1', 'Burked'), ('C.S.I', '2', '2', 'Chaos Theory'), ('C.S.I', '2', '3', 'Overload'), ('C.S.I', '2', '4', 'Bully for You'), ('C.S.I', '2', '5', 'Scuba Doobie-Doo'), ('C.S.I', '2', '6', 'Alter Boys'), ('C.S.I', '2', '7', 'Caged'), ('C.S.I', '2', '8', 'Slaves of Las Vegas'), ('C.S.I', '2', '9', 'And Then There Were None'), ('C.S.I', '2', '10', 'Ellie'), ('C.S.I', '2', '11', 'Organ Grinder'), ('C.S.I', '2', '12', "You've Got Male"), ('C.S.I', '2', '13', 'Identity Crisis'), ('C.S.I', '2', '14', 'The Finger'), ('C.S.I', '2', '15', 'Burden of Proof'), ('C.S.I', '2', '16', 'Primum Non Nocere'), ('C.S.I', '2', '17', 'Felonious Monk'), ('C.S.I', '2', '18', 'Chasing the Bus'), ('C.S.I', '2', '19', 'Stalker'), ('C.S.I', '2', '20', 'Cats in the Cradle...'), ('C.S.I', '2', '21', 'Anatomy of a Lye'), ('C.S.I', '2', '22', 'Cross-Jurisdictions'), ('C.S.I', '2', '23', 'The Hunger Artist'), ('Spaced', '2', '1', 'Back'), ('Spaced', '2', '2', 'Change'), ('Spaced', '2', '3', 'Mettle'), ('Spaced', '2', '4', 'Help'), ('Spaced', '2', '5', 'Gone'), ('Spaced', '2', '6', 'Dissolution'), ('Spaced', '2', '7', 'Testkonflikt'), ('Black Books', '1', '1', 'Cooking the Books'), ('Black Books', '1', '2', "Manny's First Day"), ('Black Books', '1', '3', 'The Grapes of Wrath'), ('Black Books', '1', '4', 'The Blackout'), ('Black Books', '1', '5', 'The Big Lock-Out'), ('Black Books', '1', '6', "He's Leaving Home"), ('Black Books', '2', '1', 'The Entertainer'), ('Black Books', '2', '2', 'Fever'), ('Black Books', '2', '3', 'The Fixer'), ('Black Books', '2', '4', 'Blood'), ('Black Books', '2', '5', 'Hello Sun'), ('Black Books', '2', '6', 'A Nice Change'), ('Black Books', '3', '1', 'Manny Come Home'), ('Black Books', '3', '2', 'Elephants and Hens'), ('Black Books', '3', '3', 'Moo-Ma and Moo-Pa'), ('Black Books', '3', '4', 'A Little Flutter'), ('Black Books', '3', '5', 'The Travel Writer'), ('Black Books', '3', '6', 'Party')]

        
        self.BaIf1.currentDB.removeShow( Show('C.S.I', '60', 'imdbtvbackend', 'tt000000') )
        
        self.BaIf1.fillUpdateDB()
        
        assert [ ( show.name, season.name, episode.name, episode.title ) for show in self.BaIf1.mergeDB.database for season in show.seasons for episode in season.episodes ] == [('Spaced', '1', '1', 'Beginnings'), ('Spaced', '1', '2', 'Gatherings'), ('Spaced', '1', '3', 'Art'), ('Spaced', '1', '4', 'Battles'), ('Spaced', '1', '5', 'Chaos'), ('Spaced', '1', '6', 'Epiphanies'), ('Spaced', '1', '7', 'Ends'), ('Spaced', '2', '1', 'Back'), ('Spaced', '2', '2', 'Change'), ('Spaced', '2', '3', 'Mettle'), ('Spaced', '2', '4', 'Help'), ('Spaced', '2', '5', 'Gone'), ('Spaced', '2', '6', 'Dissolution'), ('Spaced', '2', '7', 'Testkonflikt'), ('Black Books', '1', '1', 'Cooking the Books'), ('Black Books', '1', '2', "Manny's First Day"), ('Black Books', '1', '3', 'The Grapes of Wrath'), ('Black Books', '1', '4', 'The Blackout'), ('Black Books', '1', '5', 'The Big Lock-Out'), ('Black Books', '1', '6', "He's Leaving Home"), ('Black Books', '2', '1', 'The Entertainer'), ('Black Books', '2', '2', 'Fever'), ('Black Books', '2', '3', 'The Fixer'), ('Black Books', '2', '4', 'Blood'), ('Black Books', '2', '5', 'Hello Sun'), ('Black Books', '2', '6', 'A Nice Change'), ('Black Books', '3', '1', 'Manny Come Home'), ('Black Books', '3', '2', 'Elephants and Hens'), ('Black Books', '3', '3', 'Moo-Ma and Moo-Pa'), ('Black Books', '3', '4', 'A Little Flutter'), ('Black Books', '3', '5', 'The Travel Writer'), ('Black Books', '3', '6', 'Party')]

        
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
        
        Show1 = Show( "Test Show One", "60", "dummybackend", "dummyurlone" )
        Show2 = Show( "Test Show Two", "60", "dummybackend", "dummyurltwo" )
        
        Show3 = Show1
        
        Show1.addSeason(Season1)
        Show1.addSeason(Season2)
        Show2.addSeason(Season3)
        Show2.addSeason(Season4)
        
        s = self.BaIf1.compareDetails( Show1, Show2 )
        assert (s.name, s.duration, s.backend, s.url ) == ( "Test Show One", "60", "dummybackend", "dummyurlone" )
        s = self.BaIf1.compareDetails( Show1, Show2 )
        assert (s.name, s.duration, s.backend, s.url ) == ( "Test Show One", "60", "dummybackend", "dummyurlone" )
        
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
        
        assert self.BaIf1.compareSeasons( Season1, Season2 ).name == "1"
        assert self.BaIf1.compareSeasons( Season1, Season2 ).name == "1"
        
    def testCompareEpisodes(self):
        
        Episode1 = Episode( "2", "What A Title", "6 November, 2008" )
        Episode2 = Episode( "2", "For A TV Show", "6 November, 2008" ) # Gives NotImplemented Error, which is correct behaviour.
        Episode3 = Episode( "2", "What A Title", "6 November, 2008")
        
        e = self.BaIf1.compareEpisodes(Episode1, Episode1 )
        ( e.name, e.title, e.airdate )==( "2", "What A Title", "6 November, 2008" )
        #e = self.BaIf1.compareEpisodes(Episode1, Episode3 ) 
        #( e.name, e.title, e.airdate )==( "2", "What A Title", "6 November, 2008" )
