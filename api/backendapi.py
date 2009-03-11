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

Contains classes for interfacing with the backends.

'''

from dbapi import Database, Show, Season, Episode
from backends.imdbtv import Backend as imdbtvbackend
import os
import sys
import copy

class Backends :
    """
    Common methods for backends.
    """
    def __init__ ( self ) :
        pass
    
    def getBackends ( self, BackendDir ) :
        """
        Get registered backends.
        
        :param BackendDir: Directory the backends are located.
        :type BackendDir: string
        :returns: list of backends as string
        :rtype: list
        """
        backends = [ ]
        for file in os.listdir( BackendDir ) :
            if file != "backendapi.py" and file != "__init__.py" and file != "base.py" and "~" not in file and file.split( '.', 1)[0] not in backends and ".pyc" not in file:
                backends.append( file.split( '.', 1)[0] + "backend" )
        return backends

class BackendInterface :
    """
    Common methods to interface with the backends.
    """
    def __init__( self, dbDir=None, shows=None ) :
        '''
        :param dbDir: Path to database directory
        :type dbDir: string or None
        :param shows: list of valid Shows in this database
        :type shows: list or None
        '''
        self.dbDir = dbDir
        self.shows = shows
        
        self.currentDB = Database(self.dbDir, self.shows)
        self.currentDB.loadDB()
        
        self.updateDB = Database(self.dbDir)
    
    def addNewShow ( self, Show ) :
        """
        Add show to database.
        
        :param Show: a Show object to add to Database
        :type Show: :class:`api.dbapi.Show`
        :rtype: :class:`api.dbapi.Show` or None
        """
        return self.currentDB.addShow( Show )
    
    def updateDatabase ( self ) :
        """
        Update database.
        
        :rtype: None
        """
        newdb = self.fillUpdateDB()
        
        #self.mergeDB.printDb()
        
        newdb.write()
    
    def fillUpdateDB( self ) :
        """
        Copies the Shows from the database to a temporary database, for determining what shows to update.
        
        :rtype: None
        """
        self.updateDB = copy.deepcopy( self.currentDB )
        
        backends = dict()
        
        ## Group every Show into the backend used.
        for Show in self.updateDB.database :
            Show.clearEpisodes()
            if backends.has_key( Show.backend ) == False :
                backends[ Show.backend ] = [ copy.deepcopy(Show) ]
            else :
                backends[ Show.backend ].append( copy.deepcopy(Show) )
        
        
        for backend, Shows in backends.iteritems() :
            exec( 'backend = ' + backend + '()' )
            
            ## Download every Show in one backend before moving on to another backend.
            dictionary = backend.downloadShowList( Shows )
            DB = backend.getShowDetails( dictionary )
            
            ## Populate the updateDB
            for Show in DB.database :
                show = self.updateDB.getShow( Show )
                for Season in Show.seasons :
                    show.addSeason( Season )
        
        return self.incrementalUpdate()
        
    def incrementalUpdate( self ) :
        """
        Updates Database incrementally, not overwriting unless allowed.
        
        :rtype: None
        """
        self.mergeDB = Database(self.dbDir)
        
        for newShow in self.updateDB.database :
            
            currentShow = self.currentDB.getShow( newShow )
            
            if currentShow == None :
                self.mergeDB.addShow( newShow )
            
            else :
                self.mergeDB.addShow( self.compareDetails( currentShow , newShow ) )
                
        return self.mergeDB
    
    def compareDetails( self, currentShow, newShow ) :
        """
        Compares two Shows for differences.
        
        :param currentShow: Old show
        :type currentShow: :class:`api.dbapi.Show`
        :param newShow: New show
        :type newShow: :class:`api.dbapi.Show`
        :returns: Updated show.
        :rtype: :class:`api.dbapi.Show`
        """
        editedShow = Show( currentShow.name, currentShow.duration, currentShow.backend, currentShow.url )
        
        for newSeason in newShow.seasons :
            
            currentSeason = currentShow.getSeason( newSeason )
            
            if currentSeason == None :
                editedShow.addSeason( newSeason )
            
            else :
                editedShow.addSeason( self.compareSeasons( currentSeason, newSeason ) )
                
        return editedShow
        
    def compareSeasons( self, currentSeason, newSeason) :
        """
        Compares two Seasons for differences.
        
        :param currentSeason: Old season
        :type currentSeason: :class:`api.dbapi.Season`
        :param newSeason: New season
        :type newSeason: :class:`api.dbapi.Seson`
        :returns: Updated season.
        :rtype: :class:`api.dbapi.Season`
        """
        editedSeason = Season(currentSeason.name)
        
        for newEpisode in newSeason.episodes :
            
            currentEpisode = currentSeason.getEpisode( newEpisode )
            
            print '##S'
            print currentEpisode.title
            print currentEpisode
            print '##E'
            
            if currentEpisode == None :
                editedSeason.addEpisode( newEpisode )
                print '## ## None'
            else :
                ny = editedSeason.addEpisode( self.compareEpisodes( currentEpisode, newEpisode ) )
                print '  ###'
            print '     ' + ny.title
            print '     ' + str(ny)
            print '  ###'
            
        return editedSeason
        
    def compareEpisodes ( self, currentEpisode, newEpisode ) :
        """
        Compares two Episodes for differences.
        
        :param currentEpisode: Old episode
        :type currentEpisode: :class:`api.dbapi.Episode`
        :param newEpisode: New episode
        :type newEpisode: :class:`api.dbapi.Episode`
        :returns: Updated episode or None, if there are no differences.
        :rtype: :class:`api.dbapi.Season` or None
        """
        conflict = False
        
        if currentEpisode.title != newEpisode.title :
            conflict = True
        
        #FIXME: Airdates
        #if currentEpisode.airdate != newEpisode.airdate :
        #    conflict = True
        
        #FIXME: Arcs
        #if currentEpisode.arc != newEpisode.arc :
        #    conflict = True
        
        if conflict == True :
            return self.solveEpisodeConflicts( currentEpisode, newEpisode )
        else :
            return currentEpisode
        
    def solveEpisodeConflicts ( self, firstEpisode, secondEpisode ) :
        """
        Choose which episode details to keep.
        
        .. warning::
            This function is abstract. It raises an exception.
        
        :param firstEpisode: Old episode
        :type firstEpisode: :class:`api.dbapi.Episode`
        :param secondEpisode: New episode
        :type secondEpisode: :class:`api.dbapi.Episode`
        :rtype: :class:`api.dbapi.Episode`
        """
        
#        print '          conflict: ' + str(firstEpisode) + ':' + firstEpisode.title + ' vs. ' + str(secondEpisode) + ':' + secondEpisode.title
#        return secondEpisode
        
        raise NotImplementedError
        
