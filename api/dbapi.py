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

'''
.. moduleauthor:: Mats Taraldsvik <mats.taraldsvik@gmail.com>

Contains classes for the show database and filesystems.

**Example:**
    
    Load the current database files into Python objects, and print a nice formatted overview of it.
    

.. code-block:: python
    :linenos:
    
    db = Database()
    db.loadDB()
    db.printDb()


**Example:**
    
    Get Filesystem object by name.
    

.. code-block:: python
    :linenos:
    
    fs = Filesystems()
    Filesystem = fs.getFilesystem( "ext3" )
    print Filesystem
'''

import xml.etree.ElementTree as ET
import os
import sys

class Database :
    """
    Database contains all shows, and provides methods for manipulating them.
    """
    def __init__ ( self, dbDir=None, shows=None ) :
        '''
        :param dbDir: Path to database directory
        :type dbDir: string or None
        :param shows: list of valid Shows in this database
        :type shows: list or None
        '''
        self.database = [ ]
        
        self.shows = shows
        
        if dbDir == None :
            self.dbDir = os.path.join( os.path.dirname( __file__ ) , 'database' )
        else :
            self.dbDir = dbDir
        
    def loadDB ( self ) :
        """
        Load shows from the 'database' directory.
        """
        #FIXME: Catch the right exeption. ( when database directory is empty )
        try :
            for afile in os.listdir( self.dbDir ) :
                ## We don't want to include temporary files.
                if afile[-1] == '~' :
                    continue
                
                show = Show( properties.attrib['name'], properties.attrib['duration'], properties.attrib['filesystem'], properties.attrib['backend'], properties.attrib['url'] )
                ## Not very elegant? Omits Shows not in self.shows, if not None.
                if self.shows != None :
                    if self.shows.getShow( show ) == None :
                        continue
                
                files = os.path.join( self.dbDir , afile )
                
                ## Root XML Tag
                root = ET.parse( files ).getroot()
                properties = root.find('showproperties')
                
                ## Aliases
                for showname in root.find('fileproperties').findall('alias') :
                    show.addAlias( Alias( showname.attrib['value'] ) )
                
                ## Seasons and Episodes
                for season in root.findall('season') :
                    newSeason = Season( season.attrib['number'] )
                    for episode in season.findall('episode') :
                        newSeason.addEpisode( Episode( episode.attrib["number"], episode.attrib["title"], episode.attrib["airdate"] ,episode.attrib["arc"] ) )
                    show.addSeason( newSeason )
                
                self.addShow(show)
        except :
            self.database = [ ]

    def addShow ( self, InputShow ) :
        """
        Add a Show.
        
        :param InputShow: Show to add.
        :type InputShow: api.dbapi.Show
        :returns: On success, returns Show.
        :rtype: :class:`api.dbapi.Show` or None
        """
        if self.getShow( InputShow ) != None :
            return None
        else : 
            self.database.append( InputShow )
            return InputShow
        
    def getShow ( self, InputShow ) :
        """
        Return a Show.
        
        :param InputShow: Show to get. The name needs to be equal.
        :type InputShow: :class:`api.dbapi.Show`
        :returns: On success, returns Show.
        :rtype: :class:`api.dbapi.Show` or None
        """
        for Show in self.database :
            if InputShow.name == Show.name :
                return Show
        return None
        
    def removeShow ( self, InputShow ) :
        """
        Remove a Show.
        
        :param InputShow: Show to remove
        :type InputShow: :class:`api.dbapi.Show`
        :returns: On success, returns Show.
        :rtype: :class:`api.dbapi.Show` or None
        """
        if self.getShow( InputShow ) == None :
            return None
        else : 
            self.database.remove( InputShow )
            return InputShow
    
    def printDb ( self ) :
        """
        Print the Database's contents.
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
        
        :param verbose: verbose mode. prints info to stdout
        :type verbose: True or False
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
        '''
        :param name: Show name
        :type name: string
        :param duration: Duration of this show
        :type duration: string
        :param Filesystem: Filesystem for this show
        :type Filesystem: :class:`api.dbapi.Filesystem`
        :param backend: The backend this show uses. Must be valid.
        :type backend: string
        :param url: relative url for this show
        :type url: string
        '''
        self.name = name
        self.duration = duration
        self.filesystem = Filesystem
        self.backend = backend
        self.url = url
        self.alias = []
        self.seasons = []
    def addAlias ( self, InputAlias ) :
        """
        Add an alias.
        
        :param InputAlias: Alias to add
        :type InputAlias: :class:`api.dbapi.Alias`
        :returns: On success, returns Alias.
        :rtype: :class:`api.dbapi.Alias` or None
        """
        if self.getAlias( InputAlias ) != None :
            return None
        else : 
            self.alias.append( InputAlias )
            return InputAlias
        
    def getAlias ( self, InputAlias ) :
        """
        Return an Alias.
        
        :param InputAlias: Alias to return. Name needs to be equal
        :type InputAlias: :class:`api.dbapi.Alias`
        :returns: On success, returns Alias.
        :rtype: :class:`api.dbapi.Alias` or None
        """
        ## Aliases are lowercase.
        InputAlias.name = InputAlias.name.lower()
        for Alias in self.alias :
            if Alias.name == InputAlias.name :
                return Alias
        return None
        
    def removeAlias ( self, InputAlias ) :
        """
        Remove an Alias
        
        :param InputAlias: Alias to remove
        :type InputAlias: :class:`api.dbapi.Alias`
        :returns: On success, returns Alias.
        :rtype: :class:`api.dbapi.Alias` or None
        """
        if self.getAlias( InputAlias ) == None :
            return None
        else : 
            self.alias.remove( InputAlias )
            return InputAlias
        
    def addSeason ( self, InputSeason ) :
        """
        Add a Season to the Show.
        
        :param InputSeason: Season to add
        :type InputSeason: :class:`api.dbapi.Season`
        :returns: On success, returns Season.
        :rtype: :class:`api.dbapi.Season` or None
        """
        if self.getSeason( InputSeason ) != None :
            return None
        else : 
            self.seasons.append( InputSeason )
            return InputSeason
        
    def getSeason ( self, InputSeason ) :
        """
        Return a Season.
        
        :param InputSeason: Season to return. Name needs to be equal.
        :type InputSeason: :class:`api.dbapi.Season`
        :returns: On success, returns Season.
        :rtype: :class:`api.dbapi.Season` or None
        """
        for Season in self.seasons :
            if InputSeason.name == Season.name :
                return Season
        return None
        
    def removeSeason ( self, InputSeason ) :
        """
        Remove a Season.
        
        :param InputSeason: Season to remove
        :type InputSeason: :class:`api.dbapi.Season`
        :returns: On success, returns Season.
        :rtype: :class:`api.dbapi.Season` or None
        """
        if self.getSeason( InputSeason ) == None :
            return None
        else : 
            self.seasons.remove( InputSeason )
            return InputSeason
    
    def addEpisode ( self, InputEpisode, InputSeason ) :
        """
        Add an Episode to a Season.
        
        :param InputEpisode: Episode to add
        :type InputEpisode: :class:`api.dbapi.Episode`
        :param InputSeason: Season the Episode belongs in
        :type InputSeason: :class:`api.dbapi.Season`
        :returns: On success, returns Episode.
        :rtype: :class:`api.dbapi.Episode` or None
        """
        Season = self.getSeason( InputSeason )
        if Season != None :
            return Season.addEpisode( InputEpisode )
        else :
            InputSeason.addEpisode( InputEpisode )
            return self.addSeason( InputSeason )
    
    def clearEpisodes ( self ) :
        """
        Remove all Seasons and Episodes.
        """
        self.seasons = [ ]
        
    def printShow ( self ) :
        """
        Print contents of Show.
        """
        for Season in self.seasons :
            print '       Season: ' + str(Season) + Season.name
            for Episode in Season.episodes :
                print '               ' + str(Episode) + Episode.title

class Season :
    """
    A Season. Contains Episodes.
    """
    def __init__ ( self, SeasonName ) :
        """
        :param SeasonName: Season number
        :type SeasonName: string
        """
        self.name = SeasonName
        self.episodes = []
        
    def addEpisode ( self, InputEpisode ) :
        """
        Add an Episode.
        
        :param InputEpisode: Episode to add
        :type InputEpisode: :class:`api.dbapi.Episode`
        :returns: On success, returns Episode.
        :rtype: :class:`api.dbapi.Episode` or None
        """
        if self.getEpisode( InputEpisode ) != None :
            return None
        else : 
            self.episodes.append( InputEpisode )
            return InputEpisode
        
    def getEpisode ( self, InputEpisode ) :
        """
        Return an Episode.
        
        :param InputEpisode: Episode to return. Name needs to be equal
        :type InputEpisode: :class:`api.dbapi.Episode`
        :returns: On success, returns Episode.
        :rtype: :class:`api.dbapi.Episode` or None
        """
        for Episode in self.episodes :
            if InputEpisode.name == Episode.name :
                return Episode
        return None
        
    def removeEpisode ( self, InputEpisode ) :
        """
        Remove an Episode.
        
        :param InputEpisode: Episode to remove
        :type InputEpisode: :class:`api.dbapi.Episode`
        :returns: On success, returns Episode.
        :rtype: :class:`api.dbapi.Episode` or None
        """
        if self.getEpisode( InputEpisode ) == None :
            return None
        else : 
            self.episodes.remove( InputEpisode )
            return InputEpisode

class Episode :
    """
    An Episode.
    """
    def __init__ ( self, episodeName, episodeTitle, episodeAirDate, episodeArc="none" ) :
        """
        :param episodeName: Name of episode
        :type episodeName: string
        :param episodeTitle: Title of episode
        :type episodeName: string
        :param episodeAirDate: When this episode was aired
        :type episodeAirDate: string
        :param episodeArc: If this is part of an arc.
        :type episodeArc: string or "none"
        """
        self.name=episodeName
        self.title=episodeTitle
        self.airdate=episodeAirDate
        self.arc=episodeArc

class Alias :
    """
    An Alias.
    """
    def __init__ ( self, name ) :
        """
        :param name: Alternative file name for this show. e.g bb for black books or mash for M*A*S*H
        :type name: string
        """
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
        
        :returns: list of Filesystem objects from the filesystems.xml file.
        :rtype: list
        """
        filesystems = [ ]
        root = ET.parse( os.path.join( os.path.dirname( __file__ ) , 'filetypes.xml' ) ).getroot()
        
        for filetype in root.findall('filetype') :
            system = Filesystem( filetype.attrib['name'] )
            for invchar in filetype.findall('invalid_char') :
                system.addChar( InvChar( invchar.attrib['name'], invchar.attrib['char'], invchar.attrib['replacement'] ) )
            filesystems.append( system )
        
        return filesystems
    
    def addFilesystem ( self, InputFilesystem) :
        """
        Add a Filesystem.
        
        :param InputFilesystem: Filesystem to add
        :type InputFilesystem: :class:`api.dbapi.Filesystem`
        :returns: On success, returns Filesystem.
        :rtype: :class:`api.dbapi.Filesystem` or None
        """
        if self.getChar( InputFilesystem ) != None :
            return None
        else : 
            self.chars.append( InputFilesystem )
            return InputFilesystem
    
    def getFilesystem( self, InputFilesystem ) :
        """
        Return a Filesystem.
        
        :param InputFilesystem: Filesystem to return. Name needs to be equal
        :type InputFilesystem: :class:`api.dbapi.Filesystem`
        :returns: On success, returns Filesystem.
        :rtype: :class:`api.dbapi.Filesystem` or None
        """
        for Filesystem in self.filesystems :
            if InputFilesystem.name == Filesystem.name :
                return Filesystem
        return None
    
    def removeFilesystem ( self, InputFilesystem) :
        """
        Remove a Filesystem.
        
        :param InputFilesystem: Filesystem to remove
        :type InputFilesystem: :class:`api.dbapi.Filesystem`
        :returns: On success, returns Filesystem.
        :rtype: :class:`api.dbapi.Filesystem` or None
        """
        if self.getChar( InputFilesystem ) == None :
            return None
        else : 
            self.chars.remove( InputFilesystem )
            return InputFilesystem

class Filesystem :
    """
    A Filesystem. Contains InvChars.
    """
    def __init__ ( self, name ) :
        """
        :param name: Name of filesystem
        :type name: string
        """
        self.chars = [ ]
        self.name = name
        
    def addChar ( self, InvChar) :
        """
        Add an invalid character.
        
        :param InvChar: Invalid character to add
        :type InvChar: :class:`api.dbapi.InvChar`
        :returns: On success, returns Invalid character.
        :rtype: :class:`api.dbapi.InvChar` or None
        """
        if self.getChar( InvChar ) != None :
            return None
        else : 
            self.chars.append( InvChar )
            return InvChar
        
    def getChar ( self, InvChar ) :
        """
        Return an invalid character.
        
        :param InvChar: Invalid character to return. char and replacement needs to be equal
        :type InvChar: :class:`api.dbapi.InvChar`
        :returns: On success, returns Invalid character.
        :rtype: :class:`api.dbapi.InvChar` or None
        """
        for Char in self.chars :
            if InvChar.char == Char.char and InvChar.replacement == Char.replacement :
                return Char
        return None
        
    def removeChar ( self, InvChar) :
        """
        Remove an invalid character.
        
        :param InvChar: Invalid character to remove
        :type InvChar: :class:`api.dbapi.InvChar`
        :returns: On success, returns Invalid character.
        :rtype: :class:`api.dbapi.InvChar` or None
        """
        if self.getChar( InvChar ) == None :
            return None
        else : 
            self.chars.remove( InvChar )
            return InvChar
        
    def validateString( self, String ) :
        """
        Return valid string.
        
        :param String: The string to validate against this filesystem
        :type String: string
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
        """
        :param descr: Name of this invalid character
        :type descr: string
        :param char: The unicode of this character, as four integers, e.g 0023
        :param char: string
        :param replacement: the text or character replacing the invalid character (char)
        """
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