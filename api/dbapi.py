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

Contains classes for the show database and filesystems.

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
        
        self.dbDir = dbDir
        
    def loadDB ( self, shows=None ) :
        """
        Load shows from the 'database' directory.
        
        :param shows: list of valid Shows in this database
        :type shows: list or None
        """
        self.database = []
        
        if shows == None and self.shows == None :
            validShows = None
        elif shows == None and self.shows != None :
            validShows = self.shows
        else :
            validShows = shows
        
        #FIXME: Catch the right exeption. ( when database directory is empty )
        for afile in os.listdir( self.dbDir ) :
            ## We don't want to include temporary files.
            if afile[-1] == '~' :
                continue
            
            files = os.path.join( self.dbDir , afile )
            
            ## Root XML Tag
            root = ET.parse( files ).getroot()
            properties = root.find('showproperties')
            
            show = Show( properties.attrib['name'], properties.attrib['duration'], properties.attrib['backend'], properties.attrib['url'] )
            
            notInList = False
            ## Not very elegant? Omits Shows not in self.shows, if not None.
            if validShows != None :
                for S in validShows :
                    if S.name != show.name or S.duration != show.duration or S.backend != show.backend or S.url != show.url:
                        notInList = True
            
            if notInList == True:
                continue
            
            ## Aliases
            for showname in root.find('aliases').findall('alias') :
                show.addAlias( Alias( showname.attrib['value'] ) )
            
            ## Seasons and Episodes
            for season in root.findall('season') :
                newSeason = Season( season.attrib['number'] )
                for episode in season.findall('episode') :
                    newSeason.addEpisode( Episode( episode.attrib["number"], episode.attrib["title"], episode.attrib["airdate"] ,episode.attrib["arc"] ) )
                show.addSeason( newSeason )
            
            self.addShow(show)
    
    def updateShow( self, Show ) :
        """
        Updade a single show from the 'database' directory.
        
        :param shows: Show to update
        :type shows: :class:`api.dbapi.Show`
        """
        db = Database()
        db.loadDB( Show )
        
        UpdatedShow = db.getShow(Show)
        
        self.removeShow( Show )
        
        self.addShow(UpdatedShow)
        
        return UpdatedShow
        
    
    def addShow ( self, InputShow ) :
        """
        Add a Show.
        
        :param InputShow: Show to add.
        :type InputShow: :class:`api.dbapi.Show`
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
        Show = self.getShow( InputShow )
        if Show == None :
            return None
        else : 
            self.database.remove( Show )
            return Show
    
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
    
    def delete( self, Show ) :
        """
        Delete a show from disk.
        
        :param Show: The show to be deleted.
        :type Show: :class:`api.dbapi.Show`
        :returns: On success, returns Show. Else, returns None.
        :rtype: :class:`api.dbapi.Show`
        """
        #FIXME: Get correct filesystem string instead of hardcoding filename?
        showName = Show.name.replace(" ", "")
        showName2 = showName.replace(".", "")
        showName3 = showName2.replace("*", "")
        showName4 = showName3.replace("'", "")
        showName5 = showName4.replace("/", "")
        if os.path.isfile(os.path.join( self.dbDir, showName5.lower() + ".show")) :
            os.remove(os.path.join( self.dbDir, showName5.lower() + ".show") )
            return Show
        return None
        
    def write( self, verbose = False ) :
        """
        Write the Database (XML) to the 'database' folder.
        
        :param verbose: verbose mode. prints info to stdout
        :type verbose: True or False
        """
        if os.path.exists( self.dbDir ) != True :
            return None
        
        for Show in self.database :
            if verbose == True :
                print '-----  ',
                print Show
                print Show.name
            rootElement = ET.Element("tvshow")
            showPropertiesElement = ET.SubElement(rootElement,"showproperties")
            showPropertiesElement.set("name", Show.name)
            showPropertiesElement.set("duration", Show.duration)
            showPropertiesElement.set("backend", Show.backend)
            showPropertiesElement.set("url", Show.url)
            if verbose == True :
                print showPropertiesElement.attrib
            aliasesElement = ET.SubElement(rootElement,"aliases")
            for Alias in Show.alias :
                aliasElement = ET.Element("alias")
                aliasElement.set("value", Alias.name )
                aliasesElement.append( aliasElement )
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
        
        return self.database
        
class Show :
    """
    A Show. Contains Seasons, Aliases and a Filesystem.
    """
    def __init__ ( self, name, duration, backend, url ) :
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
            #print Alias
            #print Alias.name
            #print InputAlias
            #print InputAlias.name
            #print '.........'
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
        Alias = self.getAlias( InputAlias )
        if Alias == None :
            return None
        else : 
            self.alias.remove( Alias )
            return Alias
        
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
        Season = self.getSeason( InputSeason )
        if Season == None :
            return None
        else : 
            self.seasons.remove( Season )
            return Season
        
    
    def addEpisode ( self, InputEpisode, InputSeason ) :
        """
        Add an Episode to a Season.
        
        :param InputEpisode: Episode to add
        :type InputEpisode: :class:`api.dbapi.Episode`
        :param InputSeason: Season the Episode belongs in
        :type InputSeason: :class:`api.dbapi.Season`
        :returns: Returns Episode if Season exists, else returns Season
        :rtype: :class:`api.dbapi.Episode` or `api.dbapi.Season`
        """
        Season = self.getSeason( InputSeason )
        if Season != None :
            return Season.addEpisode( InputEpisode )
        else :
            Episode = InputSeason.addEpisode( InputEpisode )
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
        Episode = self.getEpisode( InputEpisode )
        if Episode == None :
            return None
        else : 
            self.episodes.remove( Episode )
            return Episode

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
