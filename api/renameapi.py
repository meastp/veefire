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

'''
.. moduleauthor:: Mats Taraldsvik <mats.taraldsvik@gmail.com>

Contains classes for renaming files, using :mod:`backends`.

'''

from dbapi import Database, Show, Season, Episode, Alias
import xml.etree.ElementTree as ET
import os
import re
import copy

class Error(Exception): pass

#        fileSystem3 = Filesystems(self.Tools.filetypesXML).getFilesystem( Filesystem( 'ntfs' ) )

class Rename :
    """
    Rename files. Contains Folders.
    """
    def __init__(self, dbDir, filesystemDir) :
        '''
        :param dbDir: Path to database directory
        :type dbDir: string or None
        :param filesystemDir: Path to filetypes.xml
        :type filesystemDir: string
        :param fileSystem: Filesystem to use
        :type fileSystem: string
        '''
        self.folders = [ ]
        
        self.filesystemDir = filesystemDir
        self.dbDir = dbDir
        
    def addFolder(self, InputFolder) :
        """
        Add a Folder.
        
        :param InputFolder: Folder to add
        :type InputFolder: :class:`api.renameapi.Folder`
        :returns: On success, returns Folder.
        :rtype: :class:`api.renameapi.Folder` or None
        """
        
        if self.getFolder( InputFolder ) != None :
            return None
        
        else :
            InputFolder.dbDir = self.dbDir
            InputFolder.loadFiles()
            self.folders.append( InputFolder )
            return InputFolder
        
    def addFoldersRecursively(self, RootFolder) :
        """
        Add a Folder.
        
        :param InputFolder: Root folder.
        :type InputFolder: :class:`api.renameapi.Folder`
        :returns: On success, returns root Folder.
        :rtype: :class:`api.renameapi.Folder` or None
        """
        #FIXME: If folder is added as a single directory. It cannot be added recursively afterwards.
        if self.getFolder( RootFolder ) != None :
            return None
        
        for root, dirs, files in os.walk(RootFolder.path, topdown=True):
            for directory in dirs :
                self.addFolder(Folder(os.path.join( root, directory )))
        
        return RootFolder
        
    def getFolder ( self, InputFolder ) :
        """
        Return a Folder.
        
        :param InputFolder: Folder to add. Path needs to match
        :type InputFolder: :class:`api.renameapi.Folder`
        :returns: On success, returns Folder.
        :rtype: :class:`api.renameapi.Folder` or None
        """
        for Folder in self.folders :
            if InputFolder.path == Folder.path :
                return True
        return None
        
    def removeFolder ( self, InputFolder ) :
        """
        Remove a Folder.
        
        :param InputFolder: Folder to remove
        :type InputFolder: :class:`api.renameapi.Folder`
        :returns: On success, returns Folder.
        :rtype: :class:`api.renameapi.Folder` or None
        """
        Folder = self.getFolder( InputFolder )
        if Folder == None :
            return None
        else :
            for index, item in enumerate(self.folders[:]) :
                if item.path == InputFolder.path :
                    return self.folders.pop(index)
        
    def getMatchingShows(self) :
        """
        Get Possible show matches for every FileName in Folder.
        
        :returns: list of Folder objects
        :rtype: list
        """
        for Folder in self.folders :
            Folder.getMatchingShows()
        return self.folders
        
    def generatePreviews(self, fileSystem=None) :
        """
        Generate previews for every Folder->FileName.
        
        :returns: previews (oldname, newname) for every file in every folder
        :rtype: list
        """
        
        tfolders = []
        for Folder in self.folders :
            tfolders.append(Folder.generatePreviews(self.filesystemDir, fileSystem))
        return tfolders

class Folder :
    """
    A Folder. Contains FileNames.
    """
    def __init__ (self, path, dbDir=None, shows=None) :
        """
        :param path: folder path to search in
        :type path: string
        :param dbDir: Path to database directory
        :type dbDir: string or None
        :param shows: limit shows to search through by passing a list of Show objects
        :type shows: list or none
        """
        self.dbDir = dbDir
        self.shows = shows
        self.path = path
        
    def __cmp__(self, other):
        """
        :param other: object to compare with
        :type other: :class:`api.renameapi.Folder` or None
        """
        if other == None :
            return False
        
        if self.dbDir != other.dbDir or self.path != other.path :
            return False
        
        if self.shows == None and other.shows == None :
            return True
        
        for i in xrange(0, len(self.shows)) :
            if self.shows[i].fileName != other.shows[i].fileName :
                return False
        
        return True
        
    def loadFiles( self ) :
        ## Load Databse (optionally with limits.)
        self.database = Database( self.dbDir , self.shows )
        self.database.loadDB()
        
        ## Add FileNames to folder.
        self.fileNames = []
        for afile in os.listdir( self.path ) :
            if os.path.isfile( os.path.join( self.path, afile) ) :
                aFileName = FileName( afile, self.database )
                
                self.fileNames.append( aFileName )
    
    def getMatchingShows(self) :
        """
        Get Possible show matches for every FileName.
        
        :returns: list of FileName objects
        :rtype: list
        """
        for FileName in self.fileNames :
            FileName.getMatchingShows()
        return self.fileNames
        
    def generatePreviews(self, filesystemDir, fileSystem) :
        """
        Generate previews for every FileName.
        
        :param filesystemDir: Path to filetypes.xml
        :type filesystemDir: string
        :param fileSystem: Filesystem to use
        :type fileSystem: string
        :returns: list of tuples (oldname, newname) for every FileName
        :rtype: list
        """
        previews = []
        for FileName in self.fileNames :
            previews.append(FileName.generatePreview(filesystemDir, fileSystem))
        return previews

class FileName :
    """
    A File.
    """
    def __init__(self, fileName, Database, invalidphrases=None) :
        """
        :param fileName: raw file name
        :type fileName: string
        :param Database: Database object
        :type Database: :class:`api.dbapi.Database`
        :param invalidphrase: phrases to remove from file name
        :type invalidphrase: string
        """
        #TODO: (optional) Remove invalidphrases from fileName (from invalidphrases)
        self.fileName = fileName
        self.database = Database
        
        ## Regexes
        #FIXME: Integrate with getpattern() so you don't have to add a new pattern two places.
        
        self.pattern1 = r'[sS](?:[0]+)?([1-9]+)[eE](?:[0]+)?([1-9]+)'
        self.seepattern1 = re.compile( self.pattern1 )
        
        self.pattern2 = r'(?:[0]+)?([1-9]+)[xX](?:[0]+)?([1-9]+)'
        self.seepattern2 = re.compile( self.pattern2 )
        
        self.generatedFileName = None
        
        ##Determine the file's regex pattern.
        self.regexPattern = self.getPattern()
        
        ##Styles
        #TODO: Support multiple Styles.
        
        
    def getMatchingShows(self) :
        """
        Get Possible show matches for this file name.
        
        :returns: list of Show objects
        :rtype: list
        """
        if self.regexPattern == None:
            return None
        
        ##Get Alias / show name for this file.
        rawShowName = re.match( r'([^0-9]+)(?=' + self.regexPattern + r').*' , self.fileName ).groups()[0].strip(' .-')
        
        if rawShowName == None :
            return None
        
        ## Search through Shows and try to match Aliases
        ## PossibleShowMatches could have multiple Show matches.
        PossibleShowMatches = []
        for Show in self.database.database :
            for Alias in Show.alias :
                if rawShowName.lower() == Alias.name :
                    
                    PossibleShowMatches.append( copy.deepcopy( Show ) )
        
        #FIXME: Use a function to resolve the conflicts here. Needs to be abstract and overridden.
        if len( PossibleShowMatches ) == 0 :
            self.CorrectShow = None
            return
        
        if len( PossibleShowMatches ) == 1 :
            self.CorrectShow = PossibleShowMatches[0]
            return self.CorrectShow
        
        self.CorrectShow = self.setCorrectShow( PossibleShowMatches )
        
        return self.CorrectShow
        
    def setCorrectShow(self, Shows ) :
        """
        Choose correct show for this file name.
        
        .. warning::
            This function is abstract. It raises an exception.
        
        :param Shows: list of possible matches (Show objects) for this file name
        :type Shows: list
        :returns: the correct, chosen Show object for this file name
        :rtype: :class:`api.dbapi.Show`
        """
        
        raise NotImplemented
        
    def generatePreview(self, filesystemDir, fileSystem) :
        """
        Return current file name and new file name in a tuple.
        
        :param filesystemDir: Path to filetypes.xml
        :type filesystemDir: string
        :param fileSystem: Filesystem to use
        :type fileSystem: string
        :returns: tuple (oldname, newname)
        :rtype: tuple
        """
        
        CorrectShow = self.getMatchingShows()
        NewShow = self.getShowDetails( filesystemDir, CorrectShow )
        
        ## Episode does not exist.
        if NewShow == None:
            return self.fileName , None
            
        self.generatedFileName = self.generateFileName(NewShow, filesystemDir, fileSystem)
        #FIXME: Proper way to use different styles.
        
        return self.fileName, self.generatedFileName
    
    def getShowDetails (self, filesystemDir, MatchingShow) :
        """
        Retrieves Show details.
        
        :param filesystemDir: Path to filetypes.xml
        :type filesystemDir: string
        :param Show: Show object to add file name details to.
        :type Show: :class:`api.dbapi.Show`
        """
        
        if MatchingShow == None :
            return None
        
        #FIXME: Show should not be a list (but resolved after self.getMatchingShows() ).
        
        seasonNumber = self.getSeason()
        episodeNumber = self.getEpisode()
        
        NewSeason = MatchingShow.getSeason( Season( seasonNumber ) )
        NewEpisode = NewSeason.getEpisode( Episode( episodeNumber , 'title', 'airdate' ))
        NewSeason.episodes = [ ]
        
        ## Episode does not exist.
        if NewEpisode == None :
            return None
        
        #FIXME: Proper regex function to get file suffix.
        self.fileSuffix = self.fileName[-4:]
        
        NewShow = Show( MatchingShow.name, MatchingShow.duration, MatchingShow.backend, MatchingShow.url )
        NewShow.addEpisode( NewEpisode, NewSeason )
        
        return NewShow
        
    def generateFileName( self, Show, fileSystemDir, fileSystem, Style=None ) :
        """
        Generate and return a file name.
        
        :param Show: Show object to get file name details from.
        :type Show: :class:`api.dbapi.Show`
        :param fileSystemDir: Path to filetypes.xml
        :type fileSystemDir: string
        :param fileSystem: Filesystem to use
        :type fileSystem: string
        :param Style: Style to use for the new file name
        :type Style: string or None
        """
        
        fs = Filesystems(fileSystemDir).getFilesystem( Filesystem(fileSystem) )
        
        showName = Show.name
        if len(Show.seasons[0].episodes) != 1 or len(Show.seasons) != 1 :
            print 'error: more than one episode or season in show object.'
            return -1
        seasonNumber = fs.validateString(Show.seasons[0].name)
        episodeNumber = fs.validateString(Show.seasons[0].episodes[0].name)
        episodeTitle = fs.validateString(Show.seasons[0].episodes[0].title)
        episodeArc = fs.validateString(Show.seasons[0].episodes[0].arc)
        episodeAirDate = fs.validateString(Show.seasons[0].episodes[0].airdate)
        
        #FIXME: Proper way to use different styles.
        
        ## Temporary default style.
        Style1 = showName + ' - S' + str('%02d' % int(seasonNumber)) + 'E' + str('%02d' % int(episodeNumber)) + ' - ' + episodeTitle + self.fileSuffix
        
        return Style1
        
    def getPattern(self) :
        """
        Return regex pattern.
        
        :returns: correct regex pattern for this file name
        :rtype: regex string or None
        """
        if self.seepattern1.search( self.fileName ) != None :
            return self.pattern1
        elif self.seepattern2.search( self.fileName ) != None :
            return self.pattern2
        else :
            return None
        
    def getEpisode(self) :
        """
        Return episode number.
        
        :returns: correct episode number for this file name
        :rtype: string or None
        """
        ## Generate regex from the pattern.
        exec ( 'result = re.compile(r"' + self.regexPattern + '").search("' + self.fileName + '")' )
        exec ( 'searchResults = re.compile(r"' + self.regexPattern + '").search("' + self.fileName + '").groups()[1]'  )
        
        if result != None :
            return searchResults
        else :
            return None
        
    def getSeason(self):
        """
        Return season number.
        
        :returns: correct season number for this file name
        :rtype: string or None
        """
        ## Generate regex from the pattern.
        exec ( 'result = re.compile(r"' + self.regexPattern + '").search("' + self.fileName + '")' )
        exec ( 'searchResults = re.compile(r"' + self.regexPattern + '").search("' + self.fileName + '").groups()[0]'  )
        
        if result != None :
            return searchResults
        else :
            return None

class Filesystems :
    """
    Filesystems. Methods for Filesystem.
    """
    def __init__ ( self, filesystemsDir=None ) :
        """
        :param filesystemDir: Path to filetypes.xml
        :type filesystemDir: string
        """
        
        self.filesystemsDir = filesystemsDir
        if filesystemsDir != None :
            self.filesystems = self.loadFilesystems()
        else :
            self.filesystems = []
        
    def loadFilesystems ( self ) :
        """
        Return current registered filesystems
        
        :returns: list of Filesystem objects from the filetypes.xml file.
        :rtype: list
        """
        filesystems = [ ]
        root = ET.parse( os.path.abspath(self.filesystemsDir )).getroot()
        
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
        if self.getFilesystem( InputFilesystem ) != None :
            return None
        else : 
            self.filesystems.append( InputFilesystem )
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
        Filesystem = self.getFilesystem( InputFilesystem )
        if Filesystem == None :
            return None
        else :
            self.filesystems.remove(Filesystem)
            return Filesystem

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
        Char = self.getChar( InvChar )
        if Char == None :
            return None
        else :
            self.chars.remove(Char)
            return Char
        
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
