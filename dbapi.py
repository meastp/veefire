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

import xml.etree.ElementTree as ET
import os
import sys

class Database :
    """
    A Database. Contains Shows.
    """
    def __init__ ( self, dbDir=None, shows=None ) :
        """
        Initialize an empty Database.
        """
        self.database = [ ]
        
        self.shows = shows
        
        if dbDir == None :
            self.dbDir = os.path.join( os.path.dirname( __file__ ) , 'database' )
        else :
            self.dbDir = dbDir
        
    def loadDB ( self ) :
        """
        Load shows from the 'database'.
        """
        #FIXME: Catch the right exeption. ( when database directory is empty )
        try :
            for afile in os.listdir( self.dbDir ) :
                ## We don't want to include temporary files.
                if afile[-1] == '~' :
                    continue
                
                ## Not very elegant? Omits Shows not in self.shows, if not None.
                if self.shows != None :
                    if self.shows.getShow( properties.attrib['name'] ) == None :
                        continue
                
                files = os.path.join( self.dbDir , afile )
                
                ## Root XML Tag
                root = ET.parse( files ).getroot()
                properties = root.find('showproperties')
                show = Show( properties.attrib['name'], properties.attrib['duration'], properties.attrib['filesystem'], properties.attrib['backend'], properties.attrib['url'] )
                
                ## Aliases
                for showname in root.find('fileproperties').findall('alias') :
                    show.addAlias( Alias( showname.attrib['value'] ) )
                
                ## Seasons and Episodes
                for season in root.findall('season') :
                    newSeason = Season( season.attrib['number'] )
                    for episode in season.findall('episode') :
                        newSeason.addEpisode( Episode( episode.attrib["number"], episode.attrib["title"], episode.attrib["airdate"] ,episode.attrib["arc"] ) )
                    show.addSeason( newSeason )
                
                self.database.append(show)
        except :
            self.database = [ ]

    def addShow ( self, Show ) :
        """
        Add a Show.
        """
        result = self.getShow( Show.name )
        if result == None : 
            self.database.append(Show)
            return Show
        else :
            return None
        
    def getShow ( self, name ) :
        """
        Return a Show.
        """
        for Show in self.database :
            if name == Show.name :
                return Show
        return None
        
    def removeShow ( self, name ) :
        """
        Remove a Show.
        """
        for Show in self.database :
            if name == Show.name :
                self.database.remove( Show )
                return Show
        return None
    
    def printDb ( self ) :
        """
        Show the Database's contents.
        """
        for show in self.database :
            print '####   ' + show.name + '   ####'
            for season in show.seasons :
                print '       Season: ' + season.name
                for episode in season.episodes :
                    print '               Episode: ' + episode.title
    
    def write( self, verbose = False ) :
        """
        Write the Database (XML) to the 'database' folder.
        <verbose> : (optional) print info to stdout
        """
        for Show in self.database :
            if verbose == True :
                print '-----  ',
                print Show
                print Show.name
            rootElement = ET.Element("tvshow")
            showPropertiesElement = ET.SubElement(rootElement, "showproperties" )
            showPropertiesElement.set("name", Show.name)
            showPropertiesElement.set("duration", Show.duration)
            showPropertiesElement.set("filesystem", Show.filesystem)
            showPropertiesElement.set("backend", Show.backend)
            showPropertiesElement.set("url", Show.url)
            if verbose == True :
                print showPropertiesElement.attrib
            filePropertiesElement = ET.SubElement(rootElement, "fileproperties" )
            for Alias in Show.alias :
                aliasElement = ET.Element( "alias" )
                aliasElement.set("value", Alias.name )
                filePropertiesElement.append( aliasElement )
            for Season in Show.seasons :
                if verbose == True :
                    print '---'
                    print Season.name
                    print Season
                    print Season.episodes
                seasonElement = ET.Element( "season" )
                seasonElement.set("number", Season.name )
                rootElement.append( seasonElement )
                for Episode in Season.episodes :
                    if verbose == True :
                        print '---'
                        print Episode.name
                        print Episode
                        print Episode.title
                    episodeElement = ET.Element( "episode" )
                    episodeElement.set("number", Episode.name )
                    episodeElement.set("title", Episode.title )
                    episodeElement.set("airdate", Episode.airdate )
                    episodeElement.set("arc", Episode.arc )
                    seasonElement.append( episodeElement )
            if verbose == True :
                print '-----'
                print ET.tostring( rootElement )
            tree = ET.ElementTree( rootElement )
            #FIXME: Get correct filesystem string instead of hardcoding filename?
            showName = Show.name.replace(" ", "")
            showName2 = showName.replace(".", "")
            showName3 = showName2.replace("*", "")
            showName4 = showName3.replace("'", "")
            showName5 = showName4.replace("/", "")
            tree.write(  os.path.join( self.dbDir , showName5.lower() + ".show") )

class Show :
    """
    A Show. Contains Seasons, Aliases and a Filesystem.
    """
    def __init__ ( self, name, duration, Filesystem, backend, url ) :
        self.name = name
        self.duration = duration
        self.filesystem = Filesystem
        self.backend = backend
        self.url = url
        self.alias = []
        self.seasons = []
    def addAlias ( self, Alias ) :
        """
        Add an alias.
        """
        self.alias.append( Alias )
        return Alias
        
    def getAlias ( self, Alias ) :
        """
        Return an Alias
        """
        Alias.name = Alias.name.lower()
        for AliasItem in self.alias :
            if AliasItem.name == Alias.name :
                return AliasItem
        return None
        
    def removeAlias ( self, Alias ) :
        """
        Remove an Alias
        """
        aliasItem = self.getAlias( Alias )
        if aliasItem != None :
            self.alias.remove( aliasItem )
            return Alias
        return None
        
    def addSeason ( self, Season ) :
        """
        Add a Season to the Show.
        """
        result = self.getSeason( Season.name )
        
        if result == None :
            self.seasons.append( Season )
            return self.getSeason( Season.name )
        else :
            return result
        
    def addEpisode ( self, Episode, SeasonNr ) :
        """
        Add an Episode to a Season.
        """
        result = self.addSeason( Season(SeasonNr) )
        return result.addEpisode( Episode )
        
    def getSeason ( self, seasonNr ) :
        """
        Return a Season.
        """
        for Season in self.seasons :
            if seasonNr == Season.name :
                return Season
        return None
        
    def removeSeason ( self, seasonName ) :
        """
        Remove a Season.
        """
        for Season in self.seasons :
            if episodeName == Season.name :
                self.seasons.remove(Season)
                return Season
        return None
    
    def clearEpisodes ( self ) :
        """
        Remove all Seasons and Episodes.
        """
        self.seasons = [ ]
        
    def printShow ( self ) :
        """
        Print contents.
        """
        for Season in self.seasons :
            print '       Season: ' + str(Season) + Season.name
            for Episode in Season.episodes :
                print '               ' + str(Episode) + Episode.title

class Season :
    """
    A Season. Contains Episodes.
    """
    def __init__ ( self, seasonName ) :
        self.name = seasonName
        self.episodes = []
        
    def addEpisode ( self, Episode ) :
        """
        Add an Episode.
        """
        if self.getEpisode(Episode.name) != None :
            return None
        else : 
            self.episodes.append( Episode )
            return Episode
        
    def getEpisode ( self, episodeName ) :
        """
        Return an Episode determined by episode number (string).
        """
        for Episode in self.episodes :
            if episodeName == Episode.name :
                return Episode
        return None
        
    def removeEpisode ( self, episodeName ) :
        """
        Remove an episode from the Season determined by episode number (string).
        """
        for Episode in self.episodes :
            if episodeName == Episode.name :
                self.episodes.remove(Episode)
                return Episode
        return None

class Episode :
    """
    An Episode.
    """
    def __init__ ( self, episodeName, episodeTitle, episodeAirDate, episodeArc="none" ) :
        self.name=episodeName
        self.title=episodeTitle
        self.airdate=episodeAirDate
        self.arc=episodeArc

class Alias :
    """
    An Alias.
    """
    def __init__ ( self, name ) :
        self.name = name

class Filesystems :
    """
    Filesystems. Methods for Filesystem.
    """
    def __init__ ( self ) :
        
        self.filesystems = self.loadFilesystems()
        
    def loadFilesystems ( self ) :
        """
        Return current registered filesystems
        """
        filesystems = [ ]
        root = ET.parse( os.path.join( os.path.dirname( __file__ ) , 'filetypes.xml' ) ).getroot()
        
        for filetype in root.findall('filetype') :
            system = Filesystem( filetype.attrib['name'] )
            for invchar in filetype.findall('invalid_char') :
                system.addChar( InvChar( invchar.attrib['name'], invchar.attrib['char'], invchar.attrib['replacement'] ) )
            filesystems.append( system )
        
        return filesystems
    
    def getFilesystem( self, name ) :
        """
        Return Filesystem.
        """
        for Filesystem in self.filesystems :
            if name == Filesystem.name :
                return Filesystem
        
        return None

class Filesystem :
    """
    A Filesystem. Contains InvChars.
    """
    def __init__ ( self, name ) :
        self.chars = [ ]
        self.name = name
        
    def addChar ( self, InvChar) :
        """
        Add an invalid character.
        """
        self.chars.append( InvChar )
        
    def validateString( self, String ) :
        """
        Return valid string.
        """
        if String == None :
            return None
        
        for InvChar in self.chars :
            exec('invalidChar = ' + 'u"\u' + InvChar.char + '"')
            invalidCharDecoded = invalidChar.encode( 'utf-8')
            if invalidCharDecoded in String :
                String = String.replace( invalidCharDecoded, InvChar.replacement )
        
        return String

class InvChar :
    """
    Invalid character.
    """
    def __init__ ( self, descr, char, replacement ) :
        self.description = descr
        self.char = char
        self.replacement = replacement
        
if __name__ == '__main__':
    #db = Database()
    #db.loadDB()
    #db.printDb()
#    fst = Filesystems()
#    ext = fst.getFilesystem( "ext3" )
#    print ext
    pass
