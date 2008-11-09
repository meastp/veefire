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

Contains classes for renaming files, using :mod:`backends`.

**Example:**
    
    Generate previews for every file name
    
    .. warning::
        Remember that FileName.setCorrectShow() needs to be overloaded.
    

.. code-block:: python
    :linenos:
    
    me = Rename()
    me.addFolder( Folder('a/test/folder/path/with/files'))
    me.addFolder( Folder('a/test/folder/path/with/files/subfolder'))
    ms = me.getMatchingShows()
    for Folder in ms :
        print Folder.path
        for FileName in Folder.fileNames :
            print '  ' + str(FileName.PossibleShowMatches) + '  ' + str( FileName.PossibleShowMatches[0].name )
    pv = me.generatePreviews()
    for Folder in pv :
        for item in Folder :
            print item
        for FileName in Folder.fileNames :
            print '  ' + FileName.generatedFileName
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
    def __init__(self) :
        self.folders = [ ]
        
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
            tfolders.append(Folder.generatePreviews())
        return tfolders

class Folder :
    """
    A Folder. Contains FileNames.
    """
    def __init__ (self, path, shows=None) :
        """
        Initialize folder.
        :param path: folder path to search in
        :type path: string
        :param shows: limit shows to search through by passing a list of Show objects
        :type shows: list or none
        """
        self.path = path
        
        ## Load Databse (optionally with limits.)
        self.database = Database( shows )
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
        
    def generatePreviews(self) :
        """
        Generate previews for every FileName.
        
        :returns: list of tuples (oldname, newname) for every FileName
        :rtype: list
        """
        previews = []
        for FileName in self.fileNames :
            previews.append(FileName.generatePreview())
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
        
        ##Styles
        #TODO: Support multiple Styles.
        
        
    def getMatchingShows (self) :
        """
        Get Possible show matches for this file name.
        
        :returns: list of Show objects
        :rtype: list
        """
        ##Determine the file's regex pattern.
        self.regexPattern = self.getPattern()
        
        if self.regexPattern == None:
            return None
        
        ##Get Alias / show name for this file.
        rawShowName = re.match( r'([^0-9]+)(?=' + self.regexPattern + r').*' , self.fileName ).groups()[0].strip('.')
        
        if rawShowName == None :
            return None
        
        print rawShowName
        
        ## Search through Shows and try to match Aliases
        ## PossibleShowMatches could have multiple Show matches.
        PossibleShowMatches = []
        for Show in self.database.database :
            for Alias in Show.alias :
                if rawShowName.lower() == Alias.name :
                    PossibleShowMatches.append( copy.deepcopy( Show ) )
        
        #FIXME: Use a function to resolve the conflicts here. Needs to be abstract and overridden.
        if len( PossibleShowMatches ) == 0 :
            return None
        
        CorrectShow = self.setCorrectShow( PossibleShowMatches )
        
        return CorrectShow
        
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
        
    def generatePreview(self) :
        """
        Return current file name and new file name in a tuple.
        
        :returns: tuple (oldname, newname)
        :rtype: tuple
        """
        ## Episode does not exist.
        if self.getShowDetails( self.Show ) == None :
            return self.fileName , None
            
        self.replaceInvalidCharacters()
        self.generatedFileName = self.generateFileName()
        
        return self.fileName, self.generatedFileName
    
    def getShowDetails (self, Show) :
        """
        Retrieves Show details.
        
        :param Show: Show object to add file name details to.
        :type Show: :class:`api.dbapi.Show`
        """
        #FIXME: Show should not be a list (but resolved after self.getMatchingShows() ).
        self.fileSystem = Filesystems().getFilesystem( Filesystem( Show.filesystem ) )
        
        self.showName = Show.name
        self.seasonNumber = self.getSeason()
        self.episodeNumber = self.getEpisode()
        
        Season = Show.getSeason( Season( self.seasonNumber ) )
        Episode = Season.getEpisode( Episode( self.episodeNumber , 'title', 'airdate' ))
        
        ## Episode does not exist.
        if Episode == None :
            return None
        
        self.episodeTitle = Episode.title
        self.episodeAirDate = Episode.airdate
        self.episodeArc = Episode.arc
        
        #FIXME: Proper regex function to get file suffix.
        self.fileSuffix = self.fileName[-4:]
        
        return Show
        
    def replaceInvalidCharacters ( self ) :
        """
        Replace invalid characters.
        """
        self.showName = self.fileSystem.validateString( self.showName )
        self.episodeTitle = self.fileSystem.validateString( self.episodeTitle )
        self.episodeAirDate = self.fileSystem.validateString( self.episodeAirDate )
        self.episodeArc = self.fileSystem.validateString( self.episodeArc )
        self.fileSuffix = self.fileSystem.validateString( self.fileSuffix )
        
    def generateFileName( self, Style=None ) :
        """
        Generate and return a file name.
        
        :param Style: Style to use for the new file name
        :type Style: string or None
        """
        #FIXME: Proper way to use different styles.
        
        ## Temporary default style.
        Style1 = self.showName + ' - S' + str('%02d' % int(self.seasonNumber)) + 'E' + str('%02d' % int(self.episodeNumber)) + ' - ' + self.episodeTitle + self.fileSuffix
        
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
        
    def getSeason(self) :
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
