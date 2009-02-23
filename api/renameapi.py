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

from dbapi import Database, Show, Season, Episode, Alias, Filesystems, Filesystem, InvChar
import xml.etree.ElementTree as ET
import os
import re
import copy

class Error(Exception): pass

class Rename :
    """
    Rename files. Contains Folders.
    """
    def __init__(self, dbDir, filesystemDir) :
        '''
        :param dbDir: Path to database directory
        :type dbDir: string or None
        :param filesystemDir: Path to filesystems.xml
        :type filesystemDir: string
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
                return Folder
        return None
        
    def removeFolder ( self, InputFolder ) :
        """
        Remove a Folder.
        
        :param InputFolder: Folder to remove
        :type InputFolder: :class:`api.renameapi.Folder`
        :returns: On success, returns Folder.
        :rtype: :class:`api.renameapi.Folder` or None
        """
        if self.getFolder( InputFolder ) == None :
            return None
        else : 
            self.folders.remove( InputFolder )
            return InputFolder
        
    def getMatchingShows(self) :
        """
        Get Possible show matches for every FileName in Folder.
        
        :returns: list of Folder objects
        :rtype: list
        """
        for Folder in self.folders :
            Folder.getMatchingShows()
        return self.folders
        
    def generatePreviews(self) :
        """
        Generate previews for every Folder->FileName.
        
        :returns: previews (oldname, newname) for every file in every folder
        :rtype: list
        """
        tfolders = []
        for Folder in self.folders :
            tfolders.append(Folder.generatePreviews(self.filesystemDir))
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
        
    def generatePreviews(self, filesystemDir) :
        """
        Generate previews for every FileName.
        
        :param filesystemDir: Path to filesystems.xml
        :type filesystemDir: string
        :returns: list of tuples (oldname, newname) for every FileName
        :rtype: list
        """
        previews = []
        for FileName in self.fileNames :
            previews.append(FileName.generatePreview(filesystemDir))
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
        self.seepattern1 = re.compile( r'[sS][0]*([1-9]+)[eE][0]*([1-9]+)' )
        self.pattern1 = r'[sS][0]*([1-9]+)[eE][0]*([1-9]+)'
        self.seepattern2 = re.compile( r'[0]*([1-9]+)[xX][0]*([1-9]+)' )
        self.pattern2 = r'[0]*([1-9]+)[xX][0]*([1-9]+)'
        
        self.generatedFileName = None
        
        ##Determine the file's regex pattern.
        self.regexPattern = self.getPattern()
        
        ##Styles
        #TODO: Support multiple Styles.
        
        
    def getMatchingShows (self) :
        """
        Get Possible show matches for this file name.
        
        :returns: list of Show objects
        :rtype: list
        """
        if self.regexPattern == None:
            return None
        
        ##Get Alias / show name for this file.
        rawShowName = re.match( r'([^0-9]+)(?=' + self.regexPattern + r').*' , self.fileName ).groups()[0].strip('.')
        
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
        
    def generatePreview(self, filesystemDir) :
        """
        Return current file name and new file name in a tuple.
        
        :param filesystemDir: Path to filesystems.xml
        :type filesystemDir: string
        :returns: tuple (oldname, newname)
        :rtype: tuple
        """
        ## Episode does not exist.
        if self.getShowDetails( filesystemDir, self.CorrectShow ) == None :
            return self.fileName , None
            
        self.generatedFileName = self.generateFileName(filesystemDir)
        
        return self.fileName, self.generatedFileName
    
    def getShowDetails (self, filesystemDir, MatchingShow) :
        """
        Retrieves Show details.
        
        :param filesystemDir: Path to filesystems.xml
        :type filesystemDir: string
        :param Show: Show object to add file name details to.
        :type Show: :class:`api.dbapi.Show`
        """
        
        if MatchingShow == None :
            return None
        
        #FIXME: Show should not be a list (but resolved after self.getMatchingShows() ).
        fileSystem = Filesystems(filesystemDir).getFilesystem( Filesystem( MatchingShow.filesystem ) )
        
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
        
        NewShow = Show( MatchingShow.name, MatchingShow.duration, fileSystem, MatchingShow.backend, MatchingShow.url )
        NewShow.addEpisode( NewEpisode, NewSeason )
        
        return NewShow
        
    def generateFileName( self, Show, fileSystemDir, Style=None ) :
        """
        Generate and return a file name.
        
        :param Show: Show object to get file name details from.
        :type Show: :class:`api.dbapi.Show`
        :param filesystemDir: Path to filesystems.xml
        :type filesystemDir: string
        :param Style: Style to use for the new file name
        :type Style: string or None
        """
        
        fs = Filesystems(fileSystemDir).getFilesystem( Filesystem( Show.filesystem.name ) )
        
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
    
if __name__ == '__main__':
    
    me = Rename()
    me.addFolder( Folder('/home/meastp/test'))
    me.addFolder( Folder('/home/meastp/test/backup'))
    ms = me.getMatchingShows()
    for Folder in ms :
        print Folder.path
        for FileName in Folder.fileNames :
            print '  ' + str(FileName.PossibleShowMatches) + '  ' + str( FileName.PossibleShowMatches[0].name )
    pv = me.generatePreviews()
    for Folder in pv :
        for item in Folder :
            print item
#        for FileName in Folder.fileNames :
#            print '  ' + FileName.generatedFileName
