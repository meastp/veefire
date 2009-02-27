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

Contains the backend class for imdbtv's tv section

'''

from base import BaseBackend
from api.dbapi import Show, Episode, Season, Database
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
            #print r1.status, r1.reason, ' [ gzipped: ' + str(len(data1)) + ' bytes ]'
            #totalbytes += len(data1)
            gzippedfiles.append(data1)
            
            Showdict[Show] = gzip.GzipFile(fileobj=StringIO.StringIO(data1)).read()
        
        conn.close()
        
        return Showdict
        
    def getShowDetails ( self, showandcontentdict ) :
        '''
        Download a list of Show object's episodes.
        
        :param showandcontentlist: dictionary { Show : content( raw html from web page ) }
        :type showandcontentlist: :mod:`dict`
        :returns: Database with api.dbapi.Show objects
        :rtype: :class:`api.dbapi.Database`
        '''
        updateDB = Database()
        #TODO: Test for changes in code.
        for Show, content in showandcontentdict.items() :
            seasons = BeautifulSoup.SoupStrainer('div', { "class" : re.compile("season-filter-all filter-season-[0-9]+") })
            
            all = [ tag for tag in BeautifulSoup.BeautifulSoup( content, parseOnlyThese=seasons)]
            
            for i in xrange( 0, len(all)) :
                ## Remove rubbish from the content.
                [ tag.extract() for tag in all[i].findAll('hr') ]
                [ tag.parent.extract() for tag in all[i].findAll('a', { "name" : re.compile("season-[0-9]+")} )]
            
            regexp = Regexes()
            
            for x in all :
                for item in x.findAll('div', { "class" : re.compile("filter-all filter-year-[0-9]+")} ) :
                    ## Extract info in every episode/item, and add to one tuple
                    merge = regexp.extractEpSeTitle( str(item.find('h3')) ) + regexp.extractAirDate( str( item.find('strong') ) )
                    if ( len(merge) == 4 ) : ## If merge is proper
                        Show.addEpisode( Episode( merge[1], merge[2], merge[3] ), Season( merge[0] ) )
            updateDB.addShow( Show )
        
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

if __name__ == '__main__':
    
    Showlist = [ Show( "Black Books", "30", "ext3" , "imdbtvbackend", "tt0262150" ) ]#,
#                 Show( "The IT Crowd", "30", "ext3" , "imdbtvbackend", "tt0487831" ) ,
#                 Show( "Life on Mars", "60", "ext3" , "imdbtvbackend", "tt0478942" ) ,
#                 Show( "Chuck", "60", "ext3" , "imdbtvbackend", "tt0934814" ) ,
#                 Show( "M*A*S*H", "60", "ext3" , "imdbtvbackend", "tt0068098" ),
#                 Show( "My Name Is Earl", "30", "ext3" , "imdbtvbackend", "tt0460091" ) ]
    
    backend = Backend()
    
    DB = backend.updateShows( Showlist )
    
    DB.printDb()
