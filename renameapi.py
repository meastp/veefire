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
        """
        Initialize.
        """
        self.folders = [ ]
        
    def addFolder(self, path, shows=None) :
        """
        Add folder contents.
        """
        self.folders.append( Folder(path, shows) )
        
    def getMatchingShows(self) :
        """
        Get Possible show matches for every FileName in Folder.
        """
        for Folder in self.folders :
            Folder.getMatchingShows()
        return self.folders
        
    def generatePreviews(self) :
        """
        Generate previews for every Folder->FileName.
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
        <path> : folder path to search in
        <shows> : (optional) limit shows to search through
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
        """
        for FileName in self.fileNames :
            #FIXME: Error check.
            FileName.getMatchingShows()
        return self.fileNames
        
    def generatePreviews(self) :
        """
        Generate previews for every FileName.
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
        Initialize filename, regexes and styles.
        """
        #TODO: Remove invalidphrases from fileName
        self.fileName = fileName
        self.database = Database
        
        ## Regexes
        #FIXME: Integrate with getpattern() so you don't have to modify two places.
        self.seepattern1 = re.compile( r'[sS][0]*([1-9]+)[eE][0]*([1-9]+)' )
        self.pattern1 = r'[sS][0]*([1-9]+)[eE][0]*([1-9]+)'
        self.seepattern2 = re.compile( r'[0]*([1-9]+)[xX][0]*([1-9]+)' )
        self.pattern2 = r'[0]*([1-9]+)[xX][0]*([1-9]+)'
        
        ##Styles
        #TODO: Support multiple Styles.
        
        
    def getMatchingShows (self) :
        
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
        self.PossibleShowMatches = []
        for Show in self.database.database :
            for Alias in Show.alias :
                if rawShowName.lower() == Alias.name :
                    self.PossibleShowMatches.append( copy.deepcopy( Show ) )
        
        #FIXME: Use a function to resolve here. Needs to be manual and overridden.
        if len( self.PossibleShowMatches ) == 0 :
            return None
        
        self.setCorrectShow( self.PossibleShowMatches[0] )
        
        return self.PossibleShowMatches
        
    def setCorrectShow(self, Show) :
        ## Temporary function.
        self.Show = Show
        return self.Show
        
    def generatePreview(self) :
        """
        Return current file name and new file name in a tuple.
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
        <Show> : The chosen show from getMatchingShows().
        """
        #FIXME: Show should not be a list.
        self.fileSystem = Filesystems().getFilesystem( Show.filesystem )
        
        self.showName = Show.name
        self.seasonNumber = self.getSeason()
        self.episodeNumber = self.getEpisode()
        
        Season = Show.getSeason( self.seasonNumber )
        Episode = Season.getEpisode( self.episodeNumber )
        
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
        """
        #FIXME: Proper way to use different styles.
        
        ## Temporary default style.
        Style1 = self.showName + ' - S' + str('%02d' % int(self.seasonNumber)) + 'E' + str('%02d' % int(self.episodeNumber)) + ' - ' + self.episodeTitle + self.fileSuffix
        
        return Style1
        
    def getPattern(self) :
        """
        Return regex pattern.
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
    me.addFolder( '/home/meastp/test')
    me.addFolder( '/home/meastp/test/backup' )
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
