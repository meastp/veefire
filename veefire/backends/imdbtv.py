#!/usr/bin/env python
# -*- coding: latin-1 -*-

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

Contains the backend class for imdbtv's tv section

'''

import nose

from base import BaseBackend
from veefire.api.dbapi import Show, Episode, Season, Database
import tests.testproperties
import BeautifulSoup
import re
import httplib
import StringIO
import gzip
import sys
    
class Backend ( BaseBackend ) :
    '''
    Backend to fetch data from imdb.com's tv section ( imdbtv ). Uses BeautifulSoup library for parsing html.
    '''
        
    def updateShows( self, Shows ) :
        '''
        Update Shows through a Backend.
        
        :param Shows: Shows to update
        :type Shows: list of api.dbapi.Show objects
        :returns: Database of Show objects
        :rtype: :class:`api.dbapi.Database`
        '''
        
        dictionary = self.downloadShowList( Shows )
        ShowDatabase = self.getShowDetails( dictionary )
        
        return ShowDatabase
        
    def downloadShowList ( self, Shows ) :
        '''
        Download a list of Show object's episodes.
        
        :param Shows: Shows to feth data for
        :type Shows: list of api.dbapi.Show objects
        :returns: dictionary { value( Show ) : key ( raw html from web page ) }
        :rtype: dict
        '''
        conn = httplib.HTTPConnection("www.imdb.com")
        #totalbytes = 0
        gzippedfiles = [ ]
        Showdict = { }
        
        for Show in Shows :
            headers = {'User-Agent' : 'veefire/1.0', 'Accept-encoding' : 'gzip' }
            params = ''
            conn.request("GET", "/title/" + Show.url + "/episodes", params , headers)
            
            r1 = conn.getresponse()
            data1 = r1.read()
            
            seasons_select_form_id = BeautifulSoup.SoupStrainer('select', { "id" : "bySeason" })
            seasons_select_form = BeautifulSoup.BeautifulSoup( gzip.GzipFile(fileobj=StringIO.StringIO(data1)).read(), parseOnlyThese=seasons_select_form_id).findAll('option')
            
            seasonsraw = [seasonnumber["value"] for seasonnumber in seasons_select_form] 
            
            seasons = dict()
            
            for season in seasonsraw :
                conn.request("GET", "/title/" + Show.url + "/episodes?season="+season, params , headers)
                r = conn.getresponse()
                d = r.read()
                filter = BeautifulSoup.SoupStrainer('div', { "class" : "info" })
                
                if season not in seasons :
                    seasons[season] = list()
                
                seasons[season].extend([ { "season" : season, "episode" : episode } for episode in BeautifulSoup.BeautifulSoup( gzip.GzipFile(fileobj=StringIO.StringIO(d)).read(), parseOnlyThese=filter) ])
                
                
                
            #print seasons
            
            #print r1.status, r1.reason, ' [ gzipped: ' + str(len(data1)) + ' bytes ]'
            #totalbytes += len(data1)
            #gzippedfiles.append(data1)
            
            Showdict[Show] = seasons
        
        conn.close()
        
        return Showdict
        
    def getShowDetails ( self, showandseasonsdict ) :
        '''
        Download a list of Show object's episodes.
        
        :param showandcontentlist: dictionary { Show : content( raw html from web page ) }
        :type showandcontentlist: :mod:`dict`
        :returns: Database with api.dbapi.Show objects
        :rtype: :class:`api.dbapi.Database`
        '''
        updateDB = Database()
        #TODO: Test for changes in code.
        for Show, seasons in showandseasonsdict.items() :
            
            for season, episodes in seasons.items() :
                
                for episode in episodes :
                    
                    assert season == episode["season"]
                    
                    #print episode["episode"]
                    
                    episodenr = episode["episode"].findAll('meta', { "itemprop" : "episodeNumber" })[0]["content"]
                    #print episodenr
                    
                    episodename = episode["episode"].findAll('a', { "itemprop" : "name" })[0]["title"]
                    #print episodename
                    
                    episodeairdate = episode["episode"].findAll('div', { "class" : "airdate" })[0].string.strip()
                    #print episodeairdate
                    
                    Show.addEpisode( Episode( episodenr, episodename, episodeairdate ), Season( season ) )
            
            updateDB.addShow( Show )
                
#            seasons = BeautifulSoup.SoupStrainer('div', { "class" : re.compile("season-filter-all filter-season-[0-9]+") })
#            
#            all = [ tag for tag in BeautifulSoup.BeautifulSoup( content, parseOnlyThese=seasons)]
#            
#            for i in xrange( 0, len(all)) :
#                ## Remove rubbish from the content.
#                [ tag.extract() for tag in all[i].findAll('hr') ]
#                [ tag.parent.extract() for tag in all[i].findAll('a', { "name" : re.compile("season-[0-9]+")} )]
#            
#            regexp = Regexes()
#            
#            for x in all :
#                for item in x.findAll('div', { "class" : re.compile("filter-all filter-year-[0-9]+")} ) :
#                    ## Extract info in every episode/item, and add to one tuple
#                    merge = regexp.extractEpSeTitle( str(item.find('h3')) ) + regexp.extractAirDate( str( item.find('strong') ) )
#                    if ( len(merge) == 4 ) : ## If merge is proper
#                        Show.addEpisode( Episode( merge[1], regexp.removeEntities(merge[2]), merge[3] ), Season( merge[0] ) )
#            updateDB.addShow( Show )
        
        return updateDB

class Regexes :
    '''
    Regular expressions for :class:`backends.imdbtv.Backend`.
    '''
    def __init__ ( self ) :
        self.airdate = re.compile(r'<strong>([12]?[0-9] [a-zA-Z]+ [0-9]+)</strong>')
        self.septi = re.compile(r'<h3>Season (?:[0]+)?([12]?[0-9]+), Episode (?:[0]+)?([12]?[0-9]+): <a href="/title/[a-z0-9]+/">([^<]+)?</a></h3>')
        self.removetags = re.compile(r'<[^>]*>([^<]*)<[^>]*>')
        self.invalidtitle = re.compile(r'(Episode #[1-9]+.[1-9]([0-9]+)?)') #FIXME: Not Used?
        
        self.htmlentities = re.compile(r'(&#x\d+;)')
        
    def removeEntities( self, string ) :
        """
        Removes XML entities from a string.
        
        :type string: string
        :rtype: string
        """
        ct = CleanupTools()
        result = self.htmlentities.sub(ct.removeEntities, string )
        if result == None :
            return string
        return result
        
    def removeTags( self, string ) :
        '''
        Remove sorrounding html/xml tags from a string.
        
        :type string: string
        :rtype: string
        '''
        #FIXME: WILL FAIL ON NESTED TAGS.
        return self.removetags.match( string ).groups()[0]
        
    def extractAirDate( self, string ) :
        '''
        Extract the air date from an Episode string.
        
        :type string: string
        :rtype: string
        '''
        try :
            return self.airdate.match ( string ).groups()
        except :
            return 'None',
        
    def extractEpSeTitle ( self, string ) :
        '''
        Extract the episode and season number and title from an Episode string.
        
        :type string: string
        :rtype: string
        '''
        try :
            return self.septi.match( string ).groups()
        except :
            return 'None',

    
class CleanupTools :
    def __init__(self) :
        #FIXME: Need more entities...
        self.htmlEntities = { "&#x22;" : '"',
                              "&#x27;" : "'",
                              "&#x26;" : "&",
                              "&#x3C;" : "<",
                              "&#187;" : "»",
                              "&#171;" : "«",
                              "&#x23;" : "#",
                              "&#x2b;" : "+",
                              "&#x3E;" : ">"   }
    def removeEntities(self, string) :
        return self.htmlEntities[string.group(1)]
        
class testBackend() :
    '''
    Unit test for :class:`backends.imdbtv.Backend`.
    '''
    def setUp(self) :
        self.backend = Backend()
        
        self.tools = tests.testproperties.Tools()
        self.tools.createRootDir()
        self.tools.createDatabaseFiles()
        
        validShows1 = [ Show(  "Spaced", "60", "imdbtvbackend", "tt0187664" ) ]
        self.database1 = Database(self.tools.databaseDir, validShows1)
        self.database1.loadDB()
        
        validShows2 = [ Show(  "Black Books", "30", "imdbtvbackend", "tt0262150" ) ]
        self.database2 = Database(self.tools.databaseDir, validShows2)
        self.database2.loadDB()
    
    def tearDown(self):
        self.tools.removeTempFiles()
        
    def testDownloadShowList(self):
        
        content = self.backend.downloadShowList(self.database1.database)
        self.database1.database[0].clearEpisodes()
        
        assert [ show.name for show in content.keys() ] == ['Spaced']
        
        content = self.backend.downloadShowList(self.database2.database)
        self.database2.database[0].clearEpisodes()
        
        assert [ show.name for show in content.keys() ] == ['Black Books']
        
    def testGetShowDetails(self):
        
        #self.database1.database[0].clearEpisodes()
        
        updateDB1 = self.backend.getShowDetails( self.backend.downloadShowList(self.database1.database))
        
        assert [ (show.name, season.name, episode.name, episode.title ) for show in updateDB1.database for season in show.seasons for episode in season.episodes ] == [('Spaced', '1', '1', 'Beginnings'), ('Spaced', '1', '2', 'Gatherings'), ('Spaced', '1', '3', 'Art'), ('Spaced', '1', '4', 'Battles'), ('Spaced', '1', '5', 'Chaos'), ('Spaced', '1', '6', 'Epiphanies'), ('Spaced', '1', '7', 'Ends'), ('Spaced', '2', '1', 'Back'), ('Spaced', '2', '2', 'Change'), ('Spaced', '2', '3', 'Mettle'), ('Spaced', '2', '4', 'Help'), ('Spaced', '2', '5', 'Gone'), ('Spaced', '2', '6', 'Dissolution'), ('Spaced', '2', '7', 'Testkonflikt')]
        
        self.database1.database[0].clearEpisodes()
        
        updateDB1 = self.backend.getShowDetails( self.backend.downloadShowList(self.database1.database))
        
        assert [ (show.name, season.name, episode.name, episode.title ) for show in updateDB1.database for season in show.seasons for episode in season.episodes ] ==  [('Spaced', u'1', u'1', u'Beginnings'), ('Spaced', u'1', u'2', u'Gatherings'), ('Spaced', u'1', u'3', u'Art'), ('Spaced', u'1', u'4', u'Battles'), ('Spaced', u'1', u'5', u'Chaos'), ('Spaced', u'1', u'6', u'Epiphanies'), ('Spaced', u'1', u'7', u'Ends'), ('Spaced', u'2', u'1', u'Back'), ('Spaced', u'2', u'2', u'Change'), ('Spaced', u'2', u'3', u'Mettle'), ('Spaced', u'2', u'4', u'Help'), ('Spaced', u'2', u'5', u'Gone'), ('Spaced', u'2', u'6', u'Dissolution'), ('Spaced', u'2', u'7', u'Leaves')]
        
        #self.database2.database[0].clearEpisodes()
        
        updateDB2 = self.backend.getShowDetails( self.backend.downloadShowList(self.database2.database))
        assert [ (show.name, season.name, episode.name, episode.title ) for show in updateDB2.database for season in show.seasons for episode in season.episodes ] == [('Black Books', '1', '1', 'Cooking the Books'), ('Black Books', '1', '2', "Manny's First Day"), ('Black Books', '1', '3', 'The Grapes of Wrath'), ('Black Books', '1', '4', 'The Blackout'), ('Black Books', '1', '5', 'The Big Lock-Out'), ('Black Books', '1', '6', "He's Leaving Home"), ('Black Books', '2', '1', 'The Entertainer'), ('Black Books', '2', '2', 'Fever'), ('Black Books', '2', '3', 'The Fixer'), ('Black Books', '2', '4', 'Blood'), ('Black Books', '2', '5', 'Hello Sun'), ('Black Books', '2', '6', 'A Nice Change'), ('Black Books', '3', '1', 'Manny Come Home'), ('Black Books', '3', '2', 'Elephants and Hens'), ('Black Books', '3', '3', 'Moo-Ma and Moo-Pa'), ('Black Books', '3', '4', 'A Little Flutter'), ('Black Books', '3', '5', 'The Travel Writer'), ('Black Books', '3', '6', 'Party')]
        
        self.database2.database[0].clearEpisodes()
        
        updateDB2 = self.backend.getShowDetails( self.backend.downloadShowList(self.database2.database))
        
        assert [ (show.name, season.name, episode.name, episode.title ) for show in updateDB2.database for season in show.seasons for episode in season.episodes ] == [('Black Books', u'1', u'1', u'Cooking the Books'), ('Black Books', u'1', u'2', u"Manny's First Day"), ('Black Books', u'1', u'3', u'Grapes of Wrath'), ('Black Books', u'1', u'4', u'The Blackout'), ('Black Books', u'1', u'5', u'The Big Lock-Out'), ('Black Books', u'1', u'6', u"He's Leaving Home"), ('Black Books', u'2', u'1', u'The Entertainer'), ('Black Books', u'2', u'2', u'Fever'), ('Black Books', u'2', u'3', u'The Fixer'), ('Black Books', u'2', u'4', u'Blood'), ('Black Books', u'2', u'5', u'Hello Sun'), ('Black Books', u'2', u'6', u'A Nice Change'), ('Black Books', u'3', u'1', u'Manny Come Home'), ('Black Books', u'3', u'2', u'Elephants and Hens'), ('Black Books', u'3', u'3', u'Moo-Ma and Moo-Pa'), ('Black Books', u'3', u'4', u'A Little Flutter'), ('Black Books', u'3', u'5', u'Travel Writer'), ('Black Books', u'3', u'6', u'Party')]
