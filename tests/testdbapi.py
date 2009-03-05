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
import os

from api.dbapi import Database, Show, Season, Episode
from api.dbapi import Alias
from testproperties import Tools

class testDatabase :
    """
    Test Database Class
    """
    def setUp(self) :
        self.Tools = Tools()
        self.Tools.createRootDir()
        self.Tools.createDatabaseFiles()
        
        self.database = Database(self.Tools.databaseDir)
        
    def tearDown(self):
        self.Tools.removeTempFiles()
        
    def testLoadDB(self) :
        
        assert self.database.database == [ ]
        
        self.database.loadDB()
        
        assert [ ( show.name, season.name, episode.name, episode.title ) for show in self.database.database for season in show.seasons for episode in season.episodes ] == [('C.S.I', '1', '1', 'Pilot'), ('C.S.I', '1', '2', 'Cool Change'), ('C.S.I', '1', '3', "Crate 'n' Burial"), ('C.S.I', '1', '4', 'Pledging Mr. Johnson'), ('C.S.I', '1', '5', 'Friends &#38; Lovers'), ('C.S.I', '1', '6', 'Who Are You?'), ('C.S.I', '1', '7', 'Blood Drops'), ('C.S.I', '1', '8', 'Anonymous'), ('C.S.I', '1', '9', 'Unfriendly Skies'), ('C.S.I', '1', '10', 'Sex, Lies and Larvae'), ('C.S.I', '1', '11', 'I-15 Murders'), ('C.S.I', '1', '12', 'Fahrenheit 932'), ('C.S.I', '1', '13', 'Boom'), ('C.S.I', '1', '14', 'To Halve and to Hold'), ('C.S.I', '1', '15', 'Table Stakes'), ('C.S.I', '1', '16', 'Too Tough to Die'), ('C.S.I', '1', '17', 'Face Lift'), ('C.S.I', '1', '18', '$35K O.B.O.'), ('C.S.I', '1', '19', 'Gentle, Gentle'), ('C.S.I', '1', '20', 'Sounds of Silence'), ('C.S.I', '1', '21', 'Justice Is Served'), ('C.S.I', '1', '22', 'Evaluation Day'), ('C.S.I', '1', '23', 'The Strip Strangler'), ('C.S.I', '2', '1', 'Burked'), ('C.S.I', '2', '2', 'Chaos Theory'), ('C.S.I', '2', '3', 'Overload'), ('C.S.I', '2', '4', 'Bully for You'), ('C.S.I', '2', '5', 'Scuba Doobie-Doo'), ('C.S.I', '2', '6', 'Alter Boys'), ('C.S.I', '2', '7', 'Caged'), ('C.S.I', '2', '8', 'Slaves of Las Vegas'), ('C.S.I', '2', '9', 'And Then There Were None'), ('C.S.I', '2', '10', 'Ellie'), ('C.S.I', '2', '11', 'Organ Grinder'), ('C.S.I', '2', '12', "You've Got Male"), ('C.S.I', '2', '13', 'Identity Crisis'), ('C.S.I', '2', '14', 'The Finger'), ('C.S.I', '2', '15', 'Burden of Proof'), ('C.S.I', '2', '16', 'Primum Non Nocere'), ('C.S.I', '2', '17', 'Felonious Monk'), ('C.S.I', '2', '18', 'Chasing the Bus'), ('C.S.I', '2', '19', 'Stalker'), ('C.S.I', '2', '20', 'Cats in the Cradle...'), ('C.S.I', '2', '21', 'Anatomy of a Lye'), ('C.S.I', '2', '22', 'Cross-Jurisdictions'), ('C.S.I', '2', '23', 'The Hunger Artist'), ('Spaced', '1', '1', 'Beginnings'), ('Spaced', '1', '2', 'Gatherings'), ('Spaced', '1', '3', 'Art'), ('Spaced', '1', '4', 'Battles'), ('Spaced', '1', '5', 'Chaos'), ('Spaced', '1', '6', 'Epiphanies'), ('Spaced', '1', '7', 'Ends'), ('Spaced', '2', '1', 'Back'), ('Spaced', '2', '2', 'Change'), ('Spaced', '2', '3', 'Mettle'), ('Spaced', '2', '4', 'Help'), ('Spaced', '2', '5', 'Gone'), ('Spaced', '2', '6', 'Dissolution'), ('Spaced', '2', '7', 'Leaves'), ('Black Books', '1', '1', 'Cooking the Books'), ('Black Books', '1', '2', "Manny's First Day"), ('Black Books', '1', '3', 'The Grapes of Wrath'), ('Black Books', '1', '4', 'The Blackout'), ('Black Books', '1', '5', 'The Big Lock-Out'), ('Black Books', '1', '6', "He's Leaving Home"), ('Black Books', '2', '1', 'The Entertainer'), ('Black Books', '2', '2', 'Fever'), ('Black Books', '2', '3', 'The Fixer'), ('Black Books', '2', '4', 'Blood'), ('Black Books', '2', '5', 'Hello Sun'), ('Black Books', '2', '6', 'A Nice Change'), ('Black Books', '3', '1', 'Manny Come Home'), ('Black Books', '3', '2', 'Elephants and Hens'), ('Black Books', '3', '3', 'Moo-Ma and Moo-Pa'), ('Black Books', '3', '4', 'A Little Flutter'), ('Black Books', '3', '5', 'The Travel Writer'), ('Black Books', '3', '6', 'Party')]
        
        os.remove( os.path.join( self.Tools.databaseDir , 'csi.show' ))
        
        self.database.loadDB()
        
        assert [ ( show.name, season.name, episode.name, episode.title ) for show in self.database.database for season in show.seasons for episode in season.episodes ] == [('Spaced', '1', '1', 'Beginnings'), ('Spaced', '1', '2', 'Gatherings'), ('Spaced', '1', '3', 'Art'), ('Spaced', '1', '4', 'Battles'), ('Spaced', '1', '5', 'Chaos'), ('Spaced', '1', '6', 'Epiphanies'), ('Spaced', '1', '7', 'Ends'), ('Spaced', '2', '1', 'Back'), ('Spaced', '2', '2', 'Change'), ('Spaced', '2', '3', 'Mettle'), ('Spaced', '2', '4', 'Help'), ('Spaced', '2', '5', 'Gone'), ('Spaced', '2', '6', 'Dissolution'), ('Spaced', '2', '7', 'Leaves'), ('Black Books', '1', '1', 'Cooking the Books'), ('Black Books', '1', '2', "Manny's First Day"), ('Black Books', '1', '3', 'The Grapes of Wrath'), ('Black Books', '1', '4', 'The Blackout'), ('Black Books', '1', '5', 'The Big Lock-Out'), ('Black Books', '1', '6', "He's Leaving Home"), ('Black Books', '2', '1', 'The Entertainer'), ('Black Books', '2', '2', 'Fever'), ('Black Books', '2', '3', 'The Fixer'), ('Black Books', '2', '4', 'Blood'), ('Black Books', '2', '5', 'Hello Sun'), ('Black Books', '2', '6', 'A Nice Change'), ('Black Books', '3', '1', 'Manny Come Home'), ('Black Books', '3', '2', 'Elephants and Hens'), ('Black Books', '3', '3', 'Moo-Ma and Moo-Pa'), ('Black Books', '3', '4', 'A Little Flutter'), ('Black Books', '3', '5', 'The Travel Writer'), ('Black Books', '3', '6', 'Party')]
        
        
    def testAddShow(self) :
        Show1 = Show( "Test Show One", "60", "dummybackend", "dummyurlone" )
        Show2 = Show( "Test Show Two", "60", "dummybackend", "dummyurltwo" )
        Show3 = Show( "Test Show Three", "60", "dummybackend", "dummyurlthree" )
        assert self.database.addShow( Show1 ) == Show1
        assert self.database.addShow( Show1 ) == None
        assert self.database.addShow( Show2 ) == Show2
        assert self.database.addShow( Show( "Test Show Two", "60", "dummybackend", "dummyurltwo" )) == None
        assert self.database.addShow( Show3 ) == Show3
        
    def testGetShow(self) :
        Show1 = Show( "Test Show One", "60", "dummybackend", "dummyurlone" )
        Show2 = Show( "Test Show Two", "60", "dummybackend", "dummyurltwo" )
        Show3 = Show( "Test Show Three", "60", "dummybackend", "dummyurlthree" )
        self.database.addShow( Show1 )
        self.database.addShow( Show2 )
        assert self.database.getShow( Show1 ) == Show1
        assert self.database.getShow( Show3 ) == None
        assert self.database.getShow( Show( "Test Show Two", "60", "dummybackend", "dummyurltwo" ) ) == Show2
        assert self.database.getShow( Show( "Test Show Three", "60", "dummybackend", "dummyurlthree" ) ) == None
        
    def testRemoveShow(self) :
        Show1 = Show( "Test Show One", "60", "dummybackend", "dummyurlone" )
        Show2 = Show( "Test Show Two", "60", "dummybackend", "dummyurltwo" )
        Show3 = Show( "Test Show Three", "60", "dummybackend", "dummyurlthree" )
        self.database.addShow( Show1 )
        self.database.addShow( Show2 )
        assert self.database.removeShow( Show1 ) == Show1
        assert self.database.removeShow( Show1 ) == None
        assert self.database.removeShow( Show( "Test Show Three", "60", "dummybackend", "dummyurlthree" ) ) == None
        assert self.database.removeShow( Show( "Test Show Two", "60", "dummybackend", "dummyurltwo" ) ) == Show2
        
    def testWrite(self) :
        assert  self.database.write() == []
        
        self.database.loadDB()
        
        assert [ ( show.name, season.name, episode.name, episode.title ) for show in self.database.write() for season in show.seasons for episode in season.episodes ] == [('C.S.I', '1', '1', 'Pilot'), ('C.S.I', '1', '2', 'Cool Change'), ('C.S.I', '1', '3', "Crate 'n' Burial"), ('C.S.I', '1', '4', 'Pledging Mr. Johnson'), ('C.S.I', '1', '5', 'Friends &#38; Lovers'), ('C.S.I', '1', '6', 'Who Are You?'), ('C.S.I', '1', '7', 'Blood Drops'), ('C.S.I', '1', '8', 'Anonymous'), ('C.S.I', '1', '9', 'Unfriendly Skies'), ('C.S.I', '1', '10', 'Sex, Lies and Larvae'), ('C.S.I', '1', '11', 'I-15 Murders'), ('C.S.I', '1', '12', 'Fahrenheit 932'), ('C.S.I', '1', '13', 'Boom'), ('C.S.I', '1', '14', 'To Halve and to Hold'), ('C.S.I', '1', '15', 'Table Stakes'), ('C.S.I', '1', '16', 'Too Tough to Die'), ('C.S.I', '1', '17', 'Face Lift'), ('C.S.I', '1', '18', '$35K O.B.O.'), ('C.S.I', '1', '19', 'Gentle, Gentle'), ('C.S.I', '1', '20', 'Sounds of Silence'), ('C.S.I', '1', '21', 'Justice Is Served'), ('C.S.I', '1', '22', 'Evaluation Day'), ('C.S.I', '1', '23', 'The Strip Strangler'), ('C.S.I', '2', '1', 'Burked'), ('C.S.I', '2', '2', 'Chaos Theory'), ('C.S.I', '2', '3', 'Overload'), ('C.S.I', '2', '4', 'Bully for You'), ('C.S.I', '2', '5', 'Scuba Doobie-Doo'), ('C.S.I', '2', '6', 'Alter Boys'), ('C.S.I', '2', '7', 'Caged'), ('C.S.I', '2', '8', 'Slaves of Las Vegas'), ('C.S.I', '2', '9', 'And Then There Were None'), ('C.S.I', '2', '10', 'Ellie'), ('C.S.I', '2', '11', 'Organ Grinder'), ('C.S.I', '2', '12', "You've Got Male"), ('C.S.I', '2', '13', 'Identity Crisis'), ('C.S.I', '2', '14', 'The Finger'), ('C.S.I', '2', '15', 'Burden of Proof'), ('C.S.I', '2', '16', 'Primum Non Nocere'), ('C.S.I', '2', '17', 'Felonious Monk'), ('C.S.I', '2', '18', 'Chasing the Bus'), ('C.S.I', '2', '19', 'Stalker'), ('C.S.I', '2', '20', 'Cats in the Cradle...'), ('C.S.I', '2', '21', 'Anatomy of a Lye'), ('C.S.I', '2', '22', 'Cross-Jurisdictions'), ('C.S.I', '2', '23', 'The Hunger Artist'), ('Spaced', '1', '1', 'Beginnings'), ('Spaced', '1', '2', 'Gatherings'), ('Spaced', '1', '3', 'Art'), ('Spaced', '1', '4', 'Battles'), ('Spaced', '1', '5', 'Chaos'), ('Spaced', '1', '6', 'Epiphanies'), ('Spaced', '1', '7', 'Ends'), ('Spaced', '2', '1', 'Back'), ('Spaced', '2', '2', 'Change'), ('Spaced', '2', '3', 'Mettle'), ('Spaced', '2', '4', 'Help'), ('Spaced', '2', '5', 'Gone'), ('Spaced', '2', '6', 'Dissolution'), ('Spaced', '2', '7', 'Leaves'), ('Black Books', '1', '1', 'Cooking the Books'), ('Black Books', '1', '2', "Manny's First Day"), ('Black Books', '1', '3', 'The Grapes of Wrath'), ('Black Books', '1', '4', 'The Blackout'), ('Black Books', '1', '5', 'The Big Lock-Out'), ('Black Books', '1', '6', "He's Leaving Home"), ('Black Books', '2', '1', 'The Entertainer'), ('Black Books', '2', '2', 'Fever'), ('Black Books', '2', '3', 'The Fixer'), ('Black Books', '2', '4', 'Blood'), ('Black Books', '2', '5', 'Hello Sun'), ('Black Books', '2', '6', 'A Nice Change'), ('Black Books', '3', '1', 'Manny Come Home'), ('Black Books', '3', '2', 'Elephants and Hens'), ('Black Books', '3', '3', 'Moo-Ma and Moo-Pa'), ('Black Books', '3', '4', 'A Little Flutter'), ('Black Books', '3', '5', 'The Travel Writer'), ('Black Books', '3', '6', 'Party')]
        
        
        assert os.path.exists(self.Tools.databaseDir) == True
        
        DB2 = [ ]
        for filename in self.Tools.databaseFiles.values() :
            testfile = open(os.path.join( self.Tools.databaseDir, filename ),"r")
            content = testfile.read()
            testfile.close()
            DB2.append( ( content , filename ) )
        
        assert DB2 == [('<tvshow><showproperties backend="imdbtvbackend" duration="60" name="Spaced" url="tt0187664" /><aliases><alias value="spaced" /></aliases><season number="1"><episode airdate="24 September 1999" arc="none" number="1" title="Beginnings" /><episode airdate="1 October 1999" arc="none" number="2" title="Gatherings" /><episode airdate="8 October 1999" arc="none" number="3" title="Art" /><episode airdate="15 October 1999" arc="none" number="4" title="Battles" /><episode airdate="22 October 1999" arc="none" number="5" title="Chaos" /><episode airdate="29 October 1999" arc="none" number="6" title="Epiphanies" /><episode airdate="5 November 1999" arc="none" number="7" title="Ends" /></season><season number="2"><episode airdate="23 February 2001" arc="none" number="1" title="Back" /><episode airdate="2 March 2001" arc="none" number="2" title="Change" /><episode airdate="9 March 2001" arc="none" number="3" title="Mettle" /><episode airdate="23 March 2001" arc="none" number="4" title="Help" /><episode airdate="None" arc="none" number="5" title="Gone" /><episode airdate="6 April 2001" arc="none" number="6" title="Dissolution" /><episode airdate="13 April 2001" arc="none" number="7" title="Leaves" /></season></tvshow>', 'spaced.show'), ('<tvshow><showproperties backend="imdbtvbackend" duration="30" name="Black Books" url="tt0262150" /><aliases><alias value="blackbooks" /><alias value="black books" /><alias value="black.books" /><alias value="bb" /></aliases><season number="1"><episode airdate="29 September 2000" arc="none" number="1" title="Cooking the Books" /><episode airdate="6 October 2000" arc="none" number="2" title="Manny&apos;s First Day" /><episode airdate="13 October 2000" arc="none" number="3" title="The Grapes of Wrath" /><episode airdate="20 October 2000" arc="none" number="4" title="The Blackout" /><episode airdate="27 October 2000" arc="none" number="5" title="The Big Lock-Out" /><episode airdate="3 November 2000" arc="none" number="6" title="He&apos;s Leaving Home" /></season><season number="2"><episode airdate="1 March 2002" arc="none" number="1" title="The Entertainer" /><episode airdate="8 March 2002" arc="none" number="2" title="Fever" /><episode airdate="15 March 2002" arc="none" number="3" title="The Fixer" /><episode airdate="22 March 2002" arc="none" number="4" title="Blood" /><episode airdate="29 March 2002" arc="none" number="5" title="Hello Sun" /><episode airdate="5 April 2002" arc="none" number="6" title="A Nice Change" /></season><season number="3"><episode airdate="11 March 2004" arc="none" number="1" title="Manny Come Home" /><episode airdate="18 March 2004" arc="none" number="2" title="Elephants and Hens" /><episode airdate="25 March 2004" arc="none" number="3" title="Moo-Ma and Moo-Pa" /><episode airdate="1 April 2004" arc="none" number="4" title="A Little Flutter" /><episode airdate="8 April 2004" arc="none" number="5" title="The Travel Writer" /><episode airdate="15 April 2004" arc="none" number="6" title="Party" /></season></tvshow>', 'blackbooks.show'), ('<tvshow><showproperties backend="imdbtvbackend" duration="60" name="C.S.I" url="tt0247082" /><aliases><alias value="csi" /></aliases><season number="1"><episode airdate="6 October 2000" arc="none" number="1" title="Pilot" /><episode airdate="13 October 2000" arc="none" number="2" title="Cool Change" /><episode airdate="20 October 2000" arc="none" number="3" title="Crate &apos;n&apos; Burial" /><episode airdate="27 October 2000" arc="none" number="4" title="Pledging Mr. Johnson" /><episode airdate="3 November 2000" arc="none" number="5" title="Friends &amp;#38; Lovers" /><episode airdate="10 November 2000" arc="none" number="6" title="Who Are You?" /><episode airdate="17 November 2000" arc="none" number="7" title="Blood Drops" /><episode airdate="24 November 2000" arc="none" number="8" title="Anonymous" /><episode airdate="8 December 2000" arc="none" number="9" title="Unfriendly Skies" /><episode airdate="22 December 2000" arc="none" number="10" title="Sex, Lies and Larvae" /><episode airdate="12 January 2001" arc="none" number="11" title="I-15 Murders" /><episode airdate="1 February 2001" arc="none" number="12" title="Fahrenheit 932" /><episode airdate="8 February 2001" arc="none" number="13" title="Boom" /><episode airdate="15 February 2001" arc="none" number="14" title="To Halve and to Hold" /><episode airdate="22 February 2001" arc="none" number="15" title="Table Stakes" /><episode airdate="1 March 2001" arc="none" number="16" title="Too Tough to Die" /><episode airdate="8 March 2001" arc="none" number="17" title="Face Lift" /><episode airdate="29 March 2001" arc="none" number="18" title="$35K O.B.O." /><episode airdate="12 April 2001" arc="none" number="19" title="Gentle, Gentle" /><episode airdate="19 April 2001" arc="none" number="20" title="Sounds of Silence" /><episode airdate="26 April 2001" arc="none" number="21" title="Justice Is Served" /><episode airdate="10 May 2001" arc="none" number="22" title="Evaluation Day" /><episode airdate="17 May 2001" arc="none" number="23" title="The Strip Strangler" /></season><season number="2"><episode airdate="27 September 2001" arc="none" number="1" title="Burked" /><episode airdate="4 October 2001" arc="none" number="2" title="Chaos Theory" /><episode airdate="11 October 2001" arc="none" number="3" title="Overload" /><episode airdate="18 October 2001" arc="none" number="4" title="Bully for You" /><episode airdate="25 October 2001" arc="none" number="5" title="Scuba Doobie-Doo" /><episode airdate="1 November 2001" arc="none" number="6" title="Alter Boys" /><episode airdate="8 November 2001" arc="none" number="7" title="Caged" /><episode airdate="15 November 2001" arc="none" number="8" title="Slaves of Las Vegas" /><episode airdate="22 November 2001" arc="none" number="9" title="And Then There Were None" /><episode airdate="6 December 2001" arc="none" number="10" title="Ellie" /><episode airdate="13 December 2001" arc="none" number="11" title="Organ Grinder" /><episode airdate="20 December 2001" arc="none" number="12" title="You&apos;ve Got Male" /><episode airdate="17 January 2002" arc="none" number="13" title="Identity Crisis" /><episode airdate="None" arc="none" number="14" title="The Finger" /><episode airdate="7 February 2002" arc="none" number="15" title="Burden of Proof" /><episode airdate="28 February 2002" arc="none" number="16" title="Primum Non Nocere" /><episode airdate="7 March 2002" arc="none" number="17" title="Felonious Monk" /><episode airdate="28 March 2002" arc="none" number="18" title="Chasing the Bus" /><episode airdate="4 April 2002" arc="none" number="19" title="Stalker" /><episode airdate="25 April 2002" arc="none" number="20" title="Cats in the Cradle..." /><episode airdate="2 May 2002" arc="none" number="21" title="Anatomy of a Lye" /><episode airdate="9 May 2002" arc="none" number="22" title="Cross-Jurisdictions" /><episode airdate="18 May 2002" arc="none" number="23" title="The Hunger Artist" /></season></tvshow>', 'csi.show')]
        
        show1 = self.database.getShow( Show('Spaced', '30', 'imdbtvbackend', 'tt000000') )
        show1.addEpisode( Episode( '8', 'New Test Episode', '8 January 2009', 'none' ) , Season('2') )
        
        assert [ ( show.name, season.name, episode.name, episode.title ) for show in self.database.write() for season in show.seasons for episode in season.episodes ] == [('C.S.I', '1', '1', 'Pilot'), ('C.S.I', '1', '2', 'Cool Change'), ('C.S.I', '1', '3', "Crate 'n' Burial"), ('C.S.I', '1', '4', 'Pledging Mr. Johnson'), ('C.S.I', '1', '5', 'Friends &#38; Lovers'), ('C.S.I', '1', '6', 'Who Are You?'), ('C.S.I', '1', '7', 'Blood Drops'), ('C.S.I', '1', '8', 'Anonymous'), ('C.S.I', '1', '9', 'Unfriendly Skies'), ('C.S.I', '1', '10', 'Sex, Lies and Larvae'), ('C.S.I', '1', '11', 'I-15 Murders'), ('C.S.I', '1', '12', 'Fahrenheit 932'), ('C.S.I', '1', '13', 'Boom'), ('C.S.I', '1', '14', 'To Halve and to Hold'), ('C.S.I', '1', '15', 'Table Stakes'), ('C.S.I', '1', '16', 'Too Tough to Die'), ('C.S.I', '1', '17', 'Face Lift'), ('C.S.I', '1', '18', '$35K O.B.O.'), ('C.S.I', '1', '19', 'Gentle, Gentle'), ('C.S.I', '1', '20', 'Sounds of Silence'), ('C.S.I', '1', '21', 'Justice Is Served'), ('C.S.I', '1', '22', 'Evaluation Day'), ('C.S.I', '1', '23', 'The Strip Strangler'), ('C.S.I', '2', '1', 'Burked'), ('C.S.I', '2', '2', 'Chaos Theory'), ('C.S.I', '2', '3', 'Overload'), ('C.S.I', '2', '4', 'Bully for You'), ('C.S.I', '2', '5', 'Scuba Doobie-Doo'), ('C.S.I', '2', '6', 'Alter Boys'), ('C.S.I', '2', '7', 'Caged'), ('C.S.I', '2', '8', 'Slaves of Las Vegas'), ('C.S.I', '2', '9', 'And Then There Were None'), ('C.S.I', '2', '10', 'Ellie'), ('C.S.I', '2', '11', 'Organ Grinder'), ('C.S.I', '2', '12', "You've Got Male"), ('C.S.I', '2', '13', 'Identity Crisis'), ('C.S.I', '2', '14', 'The Finger'), ('C.S.I', '2', '15', 'Burden of Proof'), ('C.S.I', '2', '16', 'Primum Non Nocere'), ('C.S.I', '2', '17', 'Felonious Monk'), ('C.S.I', '2', '18', 'Chasing the Bus'), ('C.S.I', '2', '19', 'Stalker'), ('C.S.I', '2', '20', 'Cats in the Cradle...'), ('C.S.I', '2', '21', 'Anatomy of a Lye'), ('C.S.I', '2', '22', 'Cross-Jurisdictions'), ('C.S.I', '2', '23', 'The Hunger Artist'), ('Spaced', '1', '1', 'Beginnings'), ('Spaced', '1', '2', 'Gatherings'), ('Spaced', '1', '3', 'Art'), ('Spaced', '1', '4', 'Battles'), ('Spaced', '1', '5', 'Chaos'), ('Spaced', '1', '6', 'Epiphanies'), ('Spaced', '1', '7', 'Ends'), ('Spaced', '2', '1', 'Back'), ('Spaced', '2', '2', 'Change'), ('Spaced', '2', '3', 'Mettle'), ('Spaced', '2', '4', 'Help'), ('Spaced', '2', '5', 'Gone'), ('Spaced', '2', '6', 'Dissolution'), ('Spaced', '2', '7', 'Leaves'), ('Spaced', '2', '8', 'New Test Episode'), ('Black Books', '1', '1', 'Cooking the Books'), ('Black Books', '1', '2', "Manny's First Day"), ('Black Books', '1', '3', 'The Grapes of Wrath'), ('Black Books', '1', '4', 'The Blackout'), ('Black Books', '1', '5', 'The Big Lock-Out'), ('Black Books', '1', '6', "He's Leaving Home"), ('Black Books', '2', '1', 'The Entertainer'), ('Black Books', '2', '2', 'Fever'), ('Black Books', '2', '3', 'The Fixer'), ('Black Books', '2', '4', 'Blood'), ('Black Books', '2', '5', 'Hello Sun'), ('Black Books', '2', '6', 'A Nice Change'), ('Black Books', '3', '1', 'Manny Come Home'), ('Black Books', '3', '2', 'Elephants and Hens'), ('Black Books', '3', '3', 'Moo-Ma and Moo-Pa'), ('Black Books', '3', '4', 'A Little Flutter'), ('Black Books', '3', '5', 'The Travel Writer'), ('Black Books', '3', '6', 'Party')]
        
        DB3 = [ ]
        for filename in self.Tools.databaseFiles.values() :
            testfile = open(os.path.join( self.Tools.databaseDir, filename ),"r")
            content = testfile.read()
            testfile.close()
            DB3.append( ( content , filename ) )
        
        assert DB3 == [('<tvshow><showproperties backend="imdbtvbackend" duration="60" name="Spaced" url="tt0187664" /><aliases><alias value="spaced" /></aliases><season number="1"><episode airdate="24 September 1999" arc="none" number="1" title="Beginnings" /><episode airdate="1 October 1999" arc="none" number="2" title="Gatherings" /><episode airdate="8 October 1999" arc="none" number="3" title="Art" /><episode airdate="15 October 1999" arc="none" number="4" title="Battles" /><episode airdate="22 October 1999" arc="none" number="5" title="Chaos" /><episode airdate="29 October 1999" arc="none" number="6" title="Epiphanies" /><episode airdate="5 November 1999" arc="none" number="7" title="Ends" /></season><season number="2"><episode airdate="23 February 2001" arc="none" number="1" title="Back" /><episode airdate="2 March 2001" arc="none" number="2" title="Change" /><episode airdate="9 March 2001" arc="none" number="3" title="Mettle" /><episode airdate="23 March 2001" arc="none" number="4" title="Help" /><episode airdate="None" arc="none" number="5" title="Gone" /><episode airdate="6 April 2001" arc="none" number="6" title="Dissolution" /><episode airdate="13 April 2001" arc="none" number="7" title="Leaves" /><episode airdate="8 January 2009" arc="none" number="8" title="New Test Episode" /></season></tvshow>', 'spaced.show'), ('<tvshow><showproperties backend="imdbtvbackend" duration="30" name="Black Books" url="tt0262150" /><aliases><alias value="blackbooks" /><alias value="black books" /><alias value="black.books" /><alias value="bb" /></aliases><season number="1"><episode airdate="29 September 2000" arc="none" number="1" title="Cooking the Books" /><episode airdate="6 October 2000" arc="none" number="2" title="Manny&apos;s First Day" /><episode airdate="13 October 2000" arc="none" number="3" title="The Grapes of Wrath" /><episode airdate="20 October 2000" arc="none" number="4" title="The Blackout" /><episode airdate="27 October 2000" arc="none" number="5" title="The Big Lock-Out" /><episode airdate="3 November 2000" arc="none" number="6" title="He&apos;s Leaving Home" /></season><season number="2"><episode airdate="1 March 2002" arc="none" number="1" title="The Entertainer" /><episode airdate="8 March 2002" arc="none" number="2" title="Fever" /><episode airdate="15 March 2002" arc="none" number="3" title="The Fixer" /><episode airdate="22 March 2002" arc="none" number="4" title="Blood" /><episode airdate="29 March 2002" arc="none" number="5" title="Hello Sun" /><episode airdate="5 April 2002" arc="none" number="6" title="A Nice Change" /></season><season number="3"><episode airdate="11 March 2004" arc="none" number="1" title="Manny Come Home" /><episode airdate="18 March 2004" arc="none" number="2" title="Elephants and Hens" /><episode airdate="25 March 2004" arc="none" number="3" title="Moo-Ma and Moo-Pa" /><episode airdate="1 April 2004" arc="none" number="4" title="A Little Flutter" /><episode airdate="8 April 2004" arc="none" number="5" title="The Travel Writer" /><episode airdate="15 April 2004" arc="none" number="6" title="Party" /></season></tvshow>', 'blackbooks.show'), ('<tvshow><showproperties backend="imdbtvbackend" duration="60" name="C.S.I" url="tt0247082" /><aliases><alias value="csi" /></aliases><season number="1"><episode airdate="6 October 2000" arc="none" number="1" title="Pilot" /><episode airdate="13 October 2000" arc="none" number="2" title="Cool Change" /><episode airdate="20 October 2000" arc="none" number="3" title="Crate &apos;n&apos; Burial" /><episode airdate="27 October 2000" arc="none" number="4" title="Pledging Mr. Johnson" /><episode airdate="3 November 2000" arc="none" number="5" title="Friends &amp;#38; Lovers" /><episode airdate="10 November 2000" arc="none" number="6" title="Who Are You?" /><episode airdate="17 November 2000" arc="none" number="7" title="Blood Drops" /><episode airdate="24 November 2000" arc="none" number="8" title="Anonymous" /><episode airdate="8 December 2000" arc="none" number="9" title="Unfriendly Skies" /><episode airdate="22 December 2000" arc="none" number="10" title="Sex, Lies and Larvae" /><episode airdate="12 January 2001" arc="none" number="11" title="I-15 Murders" /><episode airdate="1 February 2001" arc="none" number="12" title="Fahrenheit 932" /><episode airdate="8 February 2001" arc="none" number="13" title="Boom" /><episode airdate="15 February 2001" arc="none" number="14" title="To Halve and to Hold" /><episode airdate="22 February 2001" arc="none" number="15" title="Table Stakes" /><episode airdate="1 March 2001" arc="none" number="16" title="Too Tough to Die" /><episode airdate="8 March 2001" arc="none" number="17" title="Face Lift" /><episode airdate="29 March 2001" arc="none" number="18" title="$35K O.B.O." /><episode airdate="12 April 2001" arc="none" number="19" title="Gentle, Gentle" /><episode airdate="19 April 2001" arc="none" number="20" title="Sounds of Silence" /><episode airdate="26 April 2001" arc="none" number="21" title="Justice Is Served" /><episode airdate="10 May 2001" arc="none" number="22" title="Evaluation Day" /><episode airdate="17 May 2001" arc="none" number="23" title="The Strip Strangler" /></season><season number="2"><episode airdate="27 September 2001" arc="none" number="1" title="Burked" /><episode airdate="4 October 2001" arc="none" number="2" title="Chaos Theory" /><episode airdate="11 October 2001" arc="none" number="3" title="Overload" /><episode airdate="18 October 2001" arc="none" number="4" title="Bully for You" /><episode airdate="25 October 2001" arc="none" number="5" title="Scuba Doobie-Doo" /><episode airdate="1 November 2001" arc="none" number="6" title="Alter Boys" /><episode airdate="8 November 2001" arc="none" number="7" title="Caged" /><episode airdate="15 November 2001" arc="none" number="8" title="Slaves of Las Vegas" /><episode airdate="22 November 2001" arc="none" number="9" title="And Then There Were None" /><episode airdate="6 December 2001" arc="none" number="10" title="Ellie" /><episode airdate="13 December 2001" arc="none" number="11" title="Organ Grinder" /><episode airdate="20 December 2001" arc="none" number="12" title="You&apos;ve Got Male" /><episode airdate="17 January 2002" arc="none" number="13" title="Identity Crisis" /><episode airdate="None" arc="none" number="14" title="The Finger" /><episode airdate="7 February 2002" arc="none" number="15" title="Burden of Proof" /><episode airdate="28 February 2002" arc="none" number="16" title="Primum Non Nocere" /><episode airdate="7 March 2002" arc="none" number="17" title="Felonious Monk" /><episode airdate="28 March 2002" arc="none" number="18" title="Chasing the Bus" /><episode airdate="4 April 2002" arc="none" number="19" title="Stalker" /><episode airdate="25 April 2002" arc="none" number="20" title="Cats in the Cradle..." /><episode airdate="2 May 2002" arc="none" number="21" title="Anatomy of a Lye" /><episode airdate="9 May 2002" arc="none" number="22" title="Cross-Jurisdictions" /><episode airdate="18 May 2002" arc="none" number="23" title="The Hunger Artist" /></season></tvshow>', 'csi.show')]
        
        show1 = self.database.getShow( Show('Spaced', '30', 'imdbtvbackend', 'tt000000') )
        show1.removeSeason( Season('1') )
        
        assert [ ( show.name, season.name, episode.name, episode.title ) for show in self.database.write() for season in show.seasons for episode in season.episodes ] == [('C.S.I', '1', '1', 'Pilot'), ('C.S.I', '1', '2', 'Cool Change'), ('C.S.I', '1', '3', "Crate 'n' Burial"), ('C.S.I', '1', '4', 'Pledging Mr. Johnson'), ('C.S.I', '1', '5', 'Friends &#38; Lovers'), ('C.S.I', '1', '6', 'Who Are You?'), ('C.S.I', '1', '7', 'Blood Drops'), ('C.S.I', '1', '8', 'Anonymous'), ('C.S.I', '1', '9', 'Unfriendly Skies'), ('C.S.I', '1', '10', 'Sex, Lies and Larvae'), ('C.S.I', '1', '11', 'I-15 Murders'), ('C.S.I', '1', '12', 'Fahrenheit 932'), ('C.S.I', '1', '13', 'Boom'), ('C.S.I', '1', '14', 'To Halve and to Hold'), ('C.S.I', '1', '15', 'Table Stakes'), ('C.S.I', '1', '16', 'Too Tough to Die'), ('C.S.I', '1', '17', 'Face Lift'), ('C.S.I', '1', '18', '$35K O.B.O.'), ('C.S.I', '1', '19', 'Gentle, Gentle'), ('C.S.I', '1', '20', 'Sounds of Silence'), ('C.S.I', '1', '21', 'Justice Is Served'), ('C.S.I', '1', '22', 'Evaluation Day'), ('C.S.I', '1', '23', 'The Strip Strangler'), ('C.S.I', '2', '1', 'Burked'), ('C.S.I', '2', '2', 'Chaos Theory'), ('C.S.I', '2', '3', 'Overload'), ('C.S.I', '2', '4', 'Bully for You'), ('C.S.I', '2', '5', 'Scuba Doobie-Doo'), ('C.S.I', '2', '6', 'Alter Boys'), ('C.S.I', '2', '7', 'Caged'), ('C.S.I', '2', '8', 'Slaves of Las Vegas'), ('C.S.I', '2', '9', 'And Then There Were None'), ('C.S.I', '2', '10', 'Ellie'), ('C.S.I', '2', '11', 'Organ Grinder'), ('C.S.I', '2', '12', "You've Got Male"), ('C.S.I', '2', '13', 'Identity Crisis'), ('C.S.I', '2', '14', 'The Finger'), ('C.S.I', '2', '15', 'Burden of Proof'), ('C.S.I', '2', '16', 'Primum Non Nocere'), ('C.S.I', '2', '17', 'Felonious Monk'), ('C.S.I', '2', '18', 'Chasing the Bus'), ('C.S.I', '2', '19', 'Stalker'), ('C.S.I', '2', '20', 'Cats in the Cradle...'), ('C.S.I', '2', '21', 'Anatomy of a Lye'), ('C.S.I', '2', '22', 'Cross-Jurisdictions'), ('C.S.I', '2', '23', 'The Hunger Artist'), ('Spaced', '2', '1', 'Back'), ('Spaced', '2', '2', 'Change'), ('Spaced', '2', '3', 'Mettle'), ('Spaced', '2', '4', 'Help'), ('Spaced', '2', '5', 'Gone'), ('Spaced', '2', '6', 'Dissolution'), ('Spaced', '2', '7', 'Leaves'), ('Spaced', '2', '8', 'New Test Episode'), ('Black Books', '1', '1', 'Cooking the Books'), ('Black Books', '1', '2', "Manny's First Day"), ('Black Books', '1', '3', 'The Grapes of Wrath'), ('Black Books', '1', '4', 'The Blackout'), ('Black Books', '1', '5', 'The Big Lock-Out'), ('Black Books', '1', '6', "He's Leaving Home"), ('Black Books', '2', '1', 'The Entertainer'), ('Black Books', '2', '2', 'Fever'), ('Black Books', '2', '3', 'The Fixer'), ('Black Books', '2', '4', 'Blood'), ('Black Books', '2', '5', 'Hello Sun'), ('Black Books', '2', '6', 'A Nice Change'), ('Black Books', '3', '1', 'Manny Come Home'), ('Black Books', '3', '2', 'Elephants and Hens'), ('Black Books', '3', '3', 'Moo-Ma and Moo-Pa'), ('Black Books', '3', '4', 'A Little Flutter'), ('Black Books', '3', '5', 'The Travel Writer'), ('Black Books', '3', '6', 'Party')]
        
        DB3 = [ ]
        for filename in self.Tools.databaseFiles.values() :
            testfile = open(os.path.join( self.Tools.databaseDir, filename ),"r")
            content = testfile.read()
            testfile.close()
            DB3.append( ( content , filename ) )
        
        assert DB3 == [('<tvshow><showproperties backend="imdbtvbackend" duration="60" name="Spaced" url="tt0187664" /><aliases><alias value="spaced" /></aliases><season number="2"><episode airdate="23 February 2001" arc="none" number="1" title="Back" /><episode airdate="2 March 2001" arc="none" number="2" title="Change" /><episode airdate="9 March 2001" arc="none" number="3" title="Mettle" /><episode airdate="23 March 2001" arc="none" number="4" title="Help" /><episode airdate="None" arc="none" number="5" title="Gone" /><episode airdate="6 April 2001" arc="none" number="6" title="Dissolution" /><episode airdate="13 April 2001" arc="none" number="7" title="Leaves" /><episode airdate="8 January 2009" arc="none" number="8" title="New Test Episode" /></season></tvshow>', 'spaced.show'), ('<tvshow><showproperties backend="imdbtvbackend" duration="30" name="Black Books" url="tt0262150" /><aliases><alias value="blackbooks" /><alias value="black books" /><alias value="black.books" /><alias value="bb" /></aliases><season number="1"><episode airdate="29 September 2000" arc="none" number="1" title="Cooking the Books" /><episode airdate="6 October 2000" arc="none" number="2" title="Manny&apos;s First Day" /><episode airdate="13 October 2000" arc="none" number="3" title="The Grapes of Wrath" /><episode airdate="20 October 2000" arc="none" number="4" title="The Blackout" /><episode airdate="27 October 2000" arc="none" number="5" title="The Big Lock-Out" /><episode airdate="3 November 2000" arc="none" number="6" title="He&apos;s Leaving Home" /></season><season number="2"><episode airdate="1 March 2002" arc="none" number="1" title="The Entertainer" /><episode airdate="8 March 2002" arc="none" number="2" title="Fever" /><episode airdate="15 March 2002" arc="none" number="3" title="The Fixer" /><episode airdate="22 March 2002" arc="none" number="4" title="Blood" /><episode airdate="29 March 2002" arc="none" number="5" title="Hello Sun" /><episode airdate="5 April 2002" arc="none" number="6" title="A Nice Change" /></season><season number="3"><episode airdate="11 March 2004" arc="none" number="1" title="Manny Come Home" /><episode airdate="18 March 2004" arc="none" number="2" title="Elephants and Hens" /><episode airdate="25 March 2004" arc="none" number="3" title="Moo-Ma and Moo-Pa" /><episode airdate="1 April 2004" arc="none" number="4" title="A Little Flutter" /><episode airdate="8 April 2004" arc="none" number="5" title="The Travel Writer" /><episode airdate="15 April 2004" arc="none" number="6" title="Party" /></season></tvshow>', 'blackbooks.show'), ('<tvshow><showproperties backend="imdbtvbackend" duration="60" name="C.S.I" url="tt0247082" /><aliases><alias value="csi" /></aliases><season number="1"><episode airdate="6 October 2000" arc="none" number="1" title="Pilot" /><episode airdate="13 October 2000" arc="none" number="2" title="Cool Change" /><episode airdate="20 October 2000" arc="none" number="3" title="Crate &apos;n&apos; Burial" /><episode airdate="27 October 2000" arc="none" number="4" title="Pledging Mr. Johnson" /><episode airdate="3 November 2000" arc="none" number="5" title="Friends &amp;#38; Lovers" /><episode airdate="10 November 2000" arc="none" number="6" title="Who Are You?" /><episode airdate="17 November 2000" arc="none" number="7" title="Blood Drops" /><episode airdate="24 November 2000" arc="none" number="8" title="Anonymous" /><episode airdate="8 December 2000" arc="none" number="9" title="Unfriendly Skies" /><episode airdate="22 December 2000" arc="none" number="10" title="Sex, Lies and Larvae" /><episode airdate="12 January 2001" arc="none" number="11" title="I-15 Murders" /><episode airdate="1 February 2001" arc="none" number="12" title="Fahrenheit 932" /><episode airdate="8 February 2001" arc="none" number="13" title="Boom" /><episode airdate="15 February 2001" arc="none" number="14" title="To Halve and to Hold" /><episode airdate="22 February 2001" arc="none" number="15" title="Table Stakes" /><episode airdate="1 March 2001" arc="none" number="16" title="Too Tough to Die" /><episode airdate="8 March 2001" arc="none" number="17" title="Face Lift" /><episode airdate="29 March 2001" arc="none" number="18" title="$35K O.B.O." /><episode airdate="12 April 2001" arc="none" number="19" title="Gentle, Gentle" /><episode airdate="19 April 2001" arc="none" number="20" title="Sounds of Silence" /><episode airdate="26 April 2001" arc="none" number="21" title="Justice Is Served" /><episode airdate="10 May 2001" arc="none" number="22" title="Evaluation Day" /><episode airdate="17 May 2001" arc="none" number="23" title="The Strip Strangler" /></season><season number="2"><episode airdate="27 September 2001" arc="none" number="1" title="Burked" /><episode airdate="4 October 2001" arc="none" number="2" title="Chaos Theory" /><episode airdate="11 October 2001" arc="none" number="3" title="Overload" /><episode airdate="18 October 2001" arc="none" number="4" title="Bully for You" /><episode airdate="25 October 2001" arc="none" number="5" title="Scuba Doobie-Doo" /><episode airdate="1 November 2001" arc="none" number="6" title="Alter Boys" /><episode airdate="8 November 2001" arc="none" number="7" title="Caged" /><episode airdate="15 November 2001" arc="none" number="8" title="Slaves of Las Vegas" /><episode airdate="22 November 2001" arc="none" number="9" title="And Then There Were None" /><episode airdate="6 December 2001" arc="none" number="10" title="Ellie" /><episode airdate="13 December 2001" arc="none" number="11" title="Organ Grinder" /><episode airdate="20 December 2001" arc="none" number="12" title="You&apos;ve Got Male" /><episode airdate="17 January 2002" arc="none" number="13" title="Identity Crisis" /><episode airdate="None" arc="none" number="14" title="The Finger" /><episode airdate="7 February 2002" arc="none" number="15" title="Burden of Proof" /><episode airdate="28 February 2002" arc="none" number="16" title="Primum Non Nocere" /><episode airdate="7 March 2002" arc="none" number="17" title="Felonious Monk" /><episode airdate="28 March 2002" arc="none" number="18" title="Chasing the Bus" /><episode airdate="4 April 2002" arc="none" number="19" title="Stalker" /><episode airdate="25 April 2002" arc="none" number="20" title="Cats in the Cradle..." /><episode airdate="2 May 2002" arc="none" number="21" title="Anatomy of a Lye" /><episode airdate="9 May 2002" arc="none" number="22" title="Cross-Jurisdictions" /><episode airdate="18 May 2002" arc="none" number="23" title="The Hunger Artist" /></season></tvshow>', 'csi.show')]
        
class testShow :
    """
    Test Show Class
    """
    def setUp(self) :
        self.show = Show( "Test Show", "60", "dummybackend", "dummyurl" )
        
    def testAddAlias(self) :
        Alias1 = Alias("firstalias")
        Alias2 = Alias("secondalias")
        Alias3 = Alias("thirdalias")
        assert self.show.addAlias( Alias1 ) == Alias1
        assert self.show.addAlias( Alias1 ) == None
        assert self.show.addAlias( Alias2 ) == Alias2
        assert self.show.addAlias( Alias("secondalias")) == None
        assert self.show.addAlias( Alias3 ) == Alias3
        
    def testGetAlias(self) :
        Alias1 = Alias("firstalias")
        Alias2 = Alias("secondalias")
        Alias3 = Alias("thirdalias")
        self.show.addAlias( Alias1 )
        self.show.addAlias( Alias2 )
        assert self.show.getAlias( Alias1 ) == Alias1
        assert self.show.getAlias( Alias3 ) == None
        assert self.show.getAlias( Alias("secondalias") ) == Alias2
        assert self.show.getAlias( Alias("thirdalias") ) == None
        
    def testRemoveAlias(self) :
        Alias1 = Alias("firstalias")
        Alias2 = Alias("secondalias")
        Alias3 = Alias("thirdalias")
        self.show.addAlias( Alias1 )
        self.show.addAlias( Alias2 )
        assert self.show.removeAlias( Alias1 ) == Alias1
        assert self.show.removeAlias( Alias1 ) == None
        assert self.show.removeAlias( Alias("thirdalias") ) == None
        assert self.show.removeAlias( Alias("secondalias") ) == Alias2
        
    def testAddSeason(self) :
        Season1 = Season("1")
        Season2 = Season("2")
        Season3 = Season("3")
        assert self.show.addSeason( Season1 ) == Season1
        assert self.show.addSeason( Season1 ) == None
        assert self.show.addSeason( Season2 ) == Season2
        assert self.show.addSeason( Season("2") ) == None
        assert self.show.addSeason( Season3 ) == Season3
        
    def testGetSeason(self) :
        Season1 = Season("1")
        Season2 = Season("2")
        Season3 = Season("3")
        self.show.addSeason( Season1 )
        self.show.addSeason( Season2 )
        assert self.show.getSeason( Season1 ) == Season1
        assert self.show.getSeason( Season3 ) == None
        assert self.show.getSeason( Season("2") ) == Season2
        assert self.show.getSeason( Season("3") ) == None
        
    def testRemoveSeason(self) :
        Season1 = Season("1")
        Season2 = Season("2")
        Season3 = Season("3")
        self.show.addSeason( Season1 )
        self.show.addSeason( Season2 )
        assert self.show.removeSeason( Season1 ) == Season1
        assert self.show.removeSeason( Season1 ) == None
        assert self.show.removeSeason( Season("3") ) == None
        assert self.show.removeSeason( Season("2") ) == Season2
        
    def testAddEpisode(self) :
        Episode1 = Episode( "2", "What A Title", "6 November, 2008" )
        Episode2 = Episode( "333", "For A TV Show", "18 November, 2008" )
        Episode3 = Episode( "4", "What A Title", "6 November, 2008")
        Season1 = Season("1")
        Season2 = Season("2")
        self.show.addSeason( Season1 )
        assert self.show.addEpisode( Episode1, Season1 ) == Episode1
        assert self.show.addEpisode( Episode2, Season("1") ) == Episode2
        assert self.show.addEpisode( Episode1, Season("1") ) == None
        assert self.show.addEpisode( Episode1, Season2 ) == Season2
        assert self.show.addEpisode( Episode2, Season("2") ) == Episode2
        assert self.show.addEpisode( Episode2, Season2 ) == None
        assert self.show.addEpisode( Episode3, Season2 ) == Episode3

class testSeason :
    """
    Test Season Class
    """
    def setUp(self) :
        self.season = Season("100")
        
    def testAddEpisode(self) :
        Episode1 = Episode( "2", "What A Title", "6 November, 2008" )
        Episode2 = Episode( "333", "For A TV Show", "18 November, 2008" )
        Episode3 = Episode( "4", "What A Title", "6 November, 2008")
        assert self.season.addEpisode( Episode1 ) == Episode1
        assert self.season.addEpisode( Episode1 ) == None
        assert self.season.addEpisode( Episode2 ) == Episode2
        assert self.season.addEpisode( Episode( "333", "For A TV Show", "18 November, 2008" ) ) == None
        assert self.season.addEpisode( Episode3 ) == Episode3
        
    def testGetEpisode(self) :
        Episode1 = Episode( "2", "What A Title", "6 November, 2008" )
        Episode2 = Episode( "333", "For A TV Show", "18 November, 2008" )
        Episode3 = Episode( "4", "What A Title", "6 November, 2008")
        self.season.addEpisode( Episode1 )
        self.season.addEpisode( Episode2 )
        assert self.season.getEpisode( Episode1 ) == Episode1
        assert self.season.getEpisode( Episode3 ) == None
        assert self.season.getEpisode( Episode( "333", "For A TV Show", "18 November, 2008" ) ) == Episode2
        assert self.season.getEpisode( Episode( "4", "What A Title", "6 November, 2008") ) == None
        
    def testRemoveEpisode(self) :
        Episode1 = Episode( "2", "What A Title", "6 November, 2008" )
        Episode2 = Episode( "333", "For A TV Show", "18 November, 2008" )
        Episode3 = Episode( "4", "What A Title", "6 November, 2008")
        self.season.addEpisode( Episode1 )
        self.season.addEpisode( Episode2 )
        assert self.season.removeEpisode( Episode1 ) == Episode1
        assert self.season.removeEpisode( Episode1 ) == None
        assert self.season.removeEpisode( Episode( "4", "What A Title", "6 November, 2008" ) ) == None
        assert self.season.removeEpisode( Episode( "333", "For A TV Show", "18 November, 2008" ) ) == Episode2
