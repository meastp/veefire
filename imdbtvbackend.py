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

from dbapi import Show, Episode, Season, Database
import BeautifulSoup
import re
import httplib
import StringIO
import gzip
import sys

class imdbtvbackend :
    '''
    Backend to fetch data from imdb.com's tv section ( imdbtv ).
    '''
    def __init__ ( self ) :
        pass
    
    def downloadShowList ( self, showslist ) :
        '''
        Download a Show's Episodes from imdbtv and return a dictionary with { Show : content, Show2 : content2 }.
        downloadShowList( [ Show, Show1, Show2 ] )
        '''
        conn = httplib.HTTPConnection("www.imdb.com")
        #totalbytes = 0
        gzippedfiles = [ ]
        showcontentdict = { }
        
        for Show in showslist :
            headers = {'User-Agent' : 'veefire/1.0', 'Accept-encoding' : 'gzip' }
            params = ''
            conn.request("GET", "/title/" + Show.url + "/episodes", params , headers)
            
            r1 = conn.getresponse()
            data1 = r1.read()
            #print r1.status, r1.reason, ' [ gzipped: ' + str(len(data1)) + ' bytes ]'
            #totalbytes += len(data1)
            gzippedfiles.append(data1)
            
            showcontentdict[Show] = gzip.GzipFile(fileobj=StringIO.StringIO(data1)).read()
        
        conn.close()
        
        return showcontentdict
        
    def getShowDetails ( self, showandcontentlist ) :
        '''
        Takes a dictionary with Show : content objects, and populates the Show element from content. Returns this dictionary.
        getShowDetails ( { Show : content , Show2 : content2 } )
        '''
        updateDB = Database()
        #TODO: Test for changes in code.
        for Show, content in showandcontentlist.items() :
            seasons = BeautifulSoup.SoupStrainer('div', { "class" : re.compile("season-filter-all filter-season-[0-9]+") })
            
            all = [ tag for tag in BeautifulSoup.BeautifulSoup( content, parseOnlyThese=seasons)]
            
            for i in xrange( 0, len(all)) :
                ## Remove rubbish from the content.
                [ tag.extract() for tag in all[i].findAll('hr') ]
                [ tag.parent.extract() for tag in all[i].findAll('a', { "name" : re.compile("season-[0-9]+")} )]
            
            regexp = imdbtvregexes()
            
            for x in all :
                for item in x.findAll('div', { "class" : re.compile("filter-all filter-year-[0-9]+")} ) :
                    ## Extract info in every episode/item, and add to one tuple
                    merge = regexp.extractEpSeTitle( str(item.find('h3')) ) + regexp.extractAirDate( str( item.find('strong') ) )
                    if ( len(merge) == 4 ) : ## If merge is proper
                        Show.addEpisode( Episode( merge[1], merge[2], merge[3] ), merge[0] )
            updateDB.addShow( Show )
        
        ## showandcontentlist is mutable, so not neccessary to return it.
        return updateDB

class imdbtvregexes :
    '''
    Regular expressions for imdbtvbackend.
    '''
    def __init__ ( self ) :
        '''
        Initialize regexes.
        '''
        self.airdate = re.compile(r'<strong>([12]?[0-9] [a-zA-Z]+ [0-9]+)</strong>')
        self.septi = re.compile(r'<h3>Season ([12]?[0-9]), Episode ([1-9]?[0-9]): <a href="/title/[a-z0-9]+/">([^<]+)</a></h3>')
        self.removetags = re.compile(r'<[^>]*>([^<]*)<[^>]*>')
        self.invalidtitle = re.compile(r'(Episode #[1-9]+.[1-9]([0-9]+)?)')
        
    def removeTags( self, html ) :
        '''
        Remove sorrounding html/xml tags from a string.
        removeTags( string )
        '''
        #FIXME: WILL FAIL ON NESTED TAGS.
        return self.removetags.match( html ).groups()[0]
        
    def extractAirDate( self, html ) :
        '''
        Extract the Air Date from an episode string.
        extractAirDate( string )
        '''
        try :
            return self.airdate.match ( html ).groups()
        except :
            return 'None',
        
    def extractEpSeTitle ( self, html ) :
        '''
        Extract the Episode and Season number from an episode string.
        extractEpSeTitle ( string )
        '''
        try :
            return self.septi.match( html ).groups()
        except :
            return 'None',

if __name__ == '__main__':
    
    Showlist = [ Show( "Black Books", "30", "ext3" , "imdbtvbackend", "tt0262150" ) ,
                 Show( "The IT Crowd", "30", "ext3" , "imdbtvbackend", "tt0487831" ) ,
                 Show( "Life on Mars", "60", "ext3" , "imdbtvbackend", "tt0478942" ) ,
                 Show( "Chuck", "60", "ext3" , "imdbtvbackend", "tt0934814" ) ,
                 Show( "M*A*S*H", "60", "ext3" , "imdbtvbackend", "tt0068098" ),
                 Show( "My Name Is Earl", "30", "ext3" , "imdbtvbackend", "tt0460091" ) ]
    
    backend = imdbtvbackend()
    
    dictionary = backend.downloadShowList( Showlist )
    DB = backend.getShowDetails( dictionary )
    
    DB.printDb()
