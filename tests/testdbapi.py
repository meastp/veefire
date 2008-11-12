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
        self.season.addEpisode( Episode1 ) == Episode1
        self.season.addEpisode( Episode2 ) == Episode2
        assert self.season.getEpisode( Episode1 ) == Episode1
        assert self.season.getEpisode( Episode3 ) == None
        assert self.season.getEpisode( Episode( "2", "What A Title", "6 November, 2008" ) ) == Episode1
        
    def testRemoveEpisode(self) :
        Episode1 = Episode( "2", "What A Title", "6 November, 2008" )
        Episode2 = Episode( "333", "For A TV Show", "18 November, 2008" )
        Episode3 = Episode( "4", "What A Title", "6 November, 2008")
        self.season.addEpisode( Episode1 ) == Episode1
        self.season.addEpisode( Episode2 ) == Episode2
        assert self.season.removeEpisode( Episode1 ) == Episode1
        assert self.season.removeEpisode( Episode1 ) == None
        assert self.season.removeEpisode( Episode( "2", "What A Title", "6 November, 2008" ) ) == None
        assert self.season.removeEpisode( Episode2 ) == Episode2
        assert self.season.removeEpisode( Episode( "333", "For A TV Show", "18 November, 2008" ) ) == None

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
        self.filesystem.addChar( InvalidCharacter1 )
        self.filesystem.addChar( InvalidCharacter2 )
        assert self.filesystem.removeChar( InvalidCharacter1 ) == InvalidCharacter1
        assert self.filesystem.removeChar( InvalidCharacter1 ) == None
        assert self.filesystem.removeChar( InvChar( "NewDescription", "0000", "and")) == None
        assert self.filesystem.removeChar( InvChar( "NewDescription", "0026", "ERROR")) == None
        
    def testValidateString( self ) :
        InvalidCharacter1 = InvChar( "Description", "002B", "plus" )
        InvalidCharacter2 = InvChar( "NewDescription", "0026", "and" )
        InvalidCharacter3 = InvChar( "Description", "002F", "or" )
        self.filesystem.addChar( InvalidCharacter1 )
        self.filesystem.addChar( InvalidCharacter2 )
        self.filesystem.addChar( InvalidCharacter3 )
        assert self.filesystem.validateString( "test+test" ) == "testplustest"
        assert self.filesystem.validateString( "+test/test&test" ) == "plustestortestandtest"
        
        
