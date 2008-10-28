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

from dbapi import Database, Show, Filesystem
from imdbtvbackend import imdbtvbackend
import os
import sys
import copy

class Backends :
    """
    Common methods for backends.
    """
    def __init__ ( self ) :
        pass
    
    def getBackends ( self ) :
        """
        Return registered backends.
        """
        backends = [ ]
        for file in os.listdir( sys.path[0] ) :
            print file
            if "backend.py" in file :
                if file != "backendapi.py" and ".pyc" not in file:
                    backends.append( file.split( '.', 1)[0] )
        return backends

class Backend :
    """
    Common methods to interface with the backends.
    """
    def __init__( self ) :
        
        self.currentDB = Database()
        self.currentDB.loadDB()
        
        self.updateDB = Database()
    
    def addNewShow ( self, Show ) :
    
        return self.currentDB.addShow( Show )
    
    def updateDatabase ( self ) :
        
        self.fillUpdateDB()
        
        self.mergeDB.write()
    
    def fillUpdateDB( self ) :
        
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
                show = self.updateDB.getShow( Show.name )
                for Season in Show.seasons :
                    show.addSeason( Season )
        
        self.incrementalUpdate()
        
    def incrementalUpdate( self ) :
        """
        Updates Database incrementally, not overwriting unless allowed.
        """
        self.mergeDB = Database()
        
        for Show in self.updateDB.database :
#            print 'Show: ' + Show.name + str(Show)
#            Show.printShow()
            show = self.currentDB.getShow( Show.name )
#            print 'show: ' + show.name + str(show)
#            show.printShow()
            if show == None :
                self.mergeDB.addShow( Show )
            
            result = self.compareDetails( show , Show )
#            print '-' + str(result)
            
            if result == None :
                self.mergeDB.addShow( Show )
            else :
                show = result
                self.mergeDB.addShow( show )
    
    def compareDetails( self, currentShow, newShow ) :
        """
        Compares two Seasons.
        """
        for Season in newShow.seasons :
#            print '   Season: ' + Season.name + str(Season)
            season = currentShow.getSeason( Season.name )
#            if season != None :
#                print '   season: ' + season.name + str(season)
            if season == None :
                currentShow.addSeason( Season )
                continue
            result = self.compareSeasons( season, Season )
#            print '      -' + str(result)
            if result == None :
                currentShow.addSeason( Season )
            else :
                season = result
        
        return newShow
        
        
    def compareSeasons( self, currentSeason, newSeason) :
        
        for Episode in newSeason.episodes :
#            print '      Episode: ' + Episode.name + str(Episode)
            episode = currentSeason.getEpisode( Episode.name )
#            if episode != None :
#                print '      episode :' + episode.name + str(episode)
            if episode == None :
                currentSeason.addEpisode( Episode )
                continue
            result = self.compareEpisodes( episode, Episode )
#            print '          episode result :' + str(result)
            if result == None :
                currentSeason.addEpisode( Episode )
            else :
                episode = result
        
        return newSeason
        
    def compareEpisodes ( self, currentEpisode, newEpisode ) :
        
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
            return None
        
    def solveEpisodeConflicts ( self, firstEpisode, secondEpisode ) :
        """
        Choose the right episode to keep.
        """
        #FIXME: Needs to be overloaded and ask the user, instead of just returning the most recent episode information.
        print '          conflict: ' + str(firstEpisode) + ':' + firstEpisode.title + ' vs. ' + str(secondEpisode) + ':' + secondEpisode.title
        return secondEpisode
        
if __name__ == '__main__':
    testSession = Backend()
    #testSession.addNewShow( Show() )
    testSession.updateDatabase()
    
