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
#    along with Foobar.  If not, see <http://www.gnu.org/licenses/>.

import nose

from api.dbapi import Filesystem, Filesystems, InvChar
from api.dbapi import Show, Season, Episode
from api.dbapi import Alias

class testShow :
    """
    Test Show Class
    """
    def __init__(self) :
        self.show = Show( "Test Show", "60", Filesystem("FileSystem"), "dummybackend", "dummyurl" )
        
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
    def __init__(self) :
        self.season = Season("100")
        
    def testAddEpisode(self) :
        Episode1 = Episode( "2", "What A Title", "6 November, 2008" )
        Episode2 = Episode( "333", "For A TV Show", "18 November, 2008" )
        Episode3 = Episode( "4", "What A Title", "6 November, 2008")
        assert self.season.addEpisode( Episode1 ) == Episode1
        assert self.season.addEpisode( Episode1 ) == None
        assert self.season.addEpisode( Episode2 ) == Episode2
        assert self.season.addEpisode( Episode3 ) == Episode3
        
    def testGetEpisode(self) :
        Episode1 = Episode( "2", "What A Title", "6 November, 2008" )
        Episode2 = Episode( "333", "For A TV Show", "18 November, 2008" )
        Episode3 = Episode( "4", "What A Title", "6 November, 2008")
        self.season.addEpisode( Episode1 )
        self.season.addEpisode( Episode2 )
        assert self.season.getEpisode( Episode1 ) == Episode1
        assert self.season.getEpisode( Episode3 ) == None
        assert self.season.getEpisode( Episode( "2", "What A Title", "6 November, 2008" ) ) == Episode1
        
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

#class testFilesystems :
#    """
#    Test Filesystems Class.
#    """
#    def __init__( self ) :
#        self.fileystems = Filesystems() # Filesystem dir is None
#        
#    def testAddFilesystem( self ) :
#        Filesystem1 = Filesystem('FS1')
#        Filesystem2 = Filesystem('FS2')
#        Filesystem3 = Filesystem('FS1')
#        assert self.filesystems.addFilesystem( Filesystem1 ) == Filesystem1
#        assert self.filesystems.addFilesystem( Filesystem1 ) == None
#        assert self.filesystems.addFilesystem( Filesystem2 ) == Filesystem2
#        assert self.filesystems.addFilesystem( Filesystem3 ) == None

class testFilesystem :
    """
    Test Filesystem Class.
    """
    def __init__( self ) :
        self.filesystem = Filesystem( "FileSystem" )
        
    def testAddChar( self ) :
        InvalidCharacter1 = InvChar( "Description", "002B", "plus" )
        InvalidCharacter2 = InvChar( "NewDescription", "002B", "plus" )
        InvalidCharacter3 = InvChar( "Description", "002F", "or" )
        assert self.filesystem.addChar( InvalidCharacter1 ) == InvalidCharacter1
        assert self.filesystem.addChar( InvalidCharacter1 ) == None
        assert self.filesystem.addChar( InvalidCharacter2 ) == None
        assert self.filesystem.addChar( InvalidCharacter3 ) == InvalidCharacter3
        
    def testGetChar( self ) :
        assert self.filesystem.chars == []
        InvalidCharacter1 = InvChar( "Description", "002B", "plus" )
        InvalidCharacter2 = InvChar( "NewDescription", "0026", "and" )
        self.filesystem.addChar( InvalidCharacter1 )
        self.filesystem.addChar( InvalidCharacter2 )
        assert self.filesystem.getChar( InvalidCharacter1 ) == InvalidCharacter1
        assert self.filesystem.getChar( InvChar( "Description", "002B", "ERROR" )) == None
        assert self.filesystem.getChar( InvalidCharacter2 ) == InvalidCharacter2
        assert self.filesystem.getChar( InvChar( "Description", "0000", "and" )) == None
        
    def testRemoveChar( self ) :
        InvalidCharacter1 = InvChar( "Description", "002B", "plus" )
        InvalidCharacter2 = InvChar( "NewDescription", "0026", "and" )
        InvalidCharacter3 = InvChar( "Description", "002F", "or" )
        self.filesystem.addChar( InvalidCharacter1 )
        self.filesystem.addChar( InvalidCharacter2 )
        assert self.filesystem.removeChar( InvalidCharacter1 ) == InvalidCharacter1
        assert self.filesystem.removeChar( InvalidCharacter1 ) == None
        assert self.filesystem.removeChar( InvChar( "Description", "002F", "or" ) ) == None
        assert self.filesystem.removeChar( InvChar( "NewDescription", "0026", "and" ) ) == InvalidCharacter2
        
    def testValidateString( self ) :
        InvalidCharacter1 = InvChar( "Description", "002B", "plus" )
        InvalidCharacter2 = InvChar( "NewDescription", "0026", "and" )
        InvalidCharacter3 = InvChar( "Description", "002F", "or" )
        self.filesystem.addChar( InvalidCharacter1 )
        self.filesystem.addChar( InvalidCharacter2 )
        self.filesystem.addChar( InvalidCharacter3 )
        assert self.filesystem.validateString( "test+test" ) == "testplustest"
        assert self.filesystem.validateString( "+test/test&test" ) == "plustestortestandtest"
        
        
