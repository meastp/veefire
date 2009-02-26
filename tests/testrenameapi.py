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

import nose

from api.dbapi import Database, Show, Season, Episode, Filesystem, Filesystems
from api.renameapi import FileName
from testproperties import Tools

class testFileName :
    """
    Test FileName Class
    """
    def setUp(self) :
        self.Tools = Tools()
        self.Tools.createRootDir()
        self.Tools.createDatabaseFiles()
        self.Tools.createFilesystemXML()
        
        self.database = Database(self.Tools.databaseDir)
        self.database.loadDB()
        self.filename1 = FileName( 'black.books.s01e02.avi', self.database )
        self.filename2 = FileName( 'spaced.2x03.avi', self.database )
        self.filename3 = FileName( 'csi.s02E13.avi', self.database )
        
    def tearDown(self):
        self.Tools.removeTempFiles()
        
    def testGetPattern(self):
        assert self.filename1.getPattern() == self.filename1.pattern1
        assert self.filename2.getPattern() == self.filename2.pattern2
        assert self.filename3.getPattern() == self.filename3.pattern1
        
    def testGetSeason(self):
        assert self.filename1.getSeason() == '1'
        assert self.filename2.getSeason() == '2'
        assert self.filename3.getSeason() == '2'
        
    def testGetEpisode(self):
        assert self.filename1.getEpisode() == '2'
        assert self.filename2.getEpisode() == '3'
        assert self.filename3.getEpisode() == '13'
        
    def testGetMatchingShows(self):
        assert self.filename1.getMatchingShows().name == 'Black Books'
        assert self.filename2.getMatchingShows().name == 'Spaced'
        assert self.filename3.getMatchingShows().name == 'C.S.I'
        
    def testGeneratePreview(self):
        
        assert self.filename1.generatePreview(self.Tools.filetypesXML) == ( 'black.books.s01e02.avi', "Black Books - S01E02 - Manny's First Day.avi" )
        assert self.filename2.generatePreview(self.Tools.filetypesXML) == ('spaced.2x03.avi', 'Spaced - S02E03 - Mettle.avi')
        assert self.filename3.generatePreview(self.Tools.filetypesXML) == ('csi.s02E13.avi', 'C.S.I - S02E13 - Identity Crisis.avi')
        
    def testGetShowDetails(self):
        show1 = self.filename1.getMatchingShows()
        show2 = self.filename2.getMatchingShows()
        show3 = self.filename3.getMatchingShows()
        
        testShow1 = self.filename1.getShowDetails( self.Tools.filetypesXML, show1 )
        testShow2 = self.filename2.getShowDetails( self.Tools.filetypesXML, show2 )
        testShow3 = self.filename3.getShowDetails( self.Tools.filetypesXML, show3 )
        
        assert len(testShow1.seasons) == 1
        assert len(testShow2.seasons) == 1
        assert len(testShow3.seasons) == 1
        
        assert len(testShow1.seasons[0].episodes) == 1
        assert len(testShow2.seasons[0].episodes) == 1
        assert len(testShow3.seasons[0].episodes) == 1
        
#        show = testShow3
#        print 'show: ' + show.name + ' - ' + show.duration + ' - ' + show.filesystem.name + ' - ' + show.backend + ' - ' + show.url
#        for season in show.seasons :
#            print '  season: ' + season.name
#            for episode in season.episodes :
#                print '    episode: ' + episode.name + ' - ' + episode.title + ' - ' + episode.airdate + ' - ' + episode.arc
        
        fileSystem1 = Filesystems(self.Tools.filetypesXML).getFilesystem( Filesystem( 'ext3' ) )
        correctShow1 = Show( 'Black Books', '30', fileSystem1, 'imdbtvbackend', 'tt0262150' )
        correctShow1.addEpisode( Episode( '2', "Manny's First Day", '6 October 2000', 'none'), Season('1') )
        
        fileSystem2 = Filesystems(self.Tools.filetypesXML).getFilesystem( Filesystem( 'ext3' ) )
        correctShow2 = Show( 'Spaced', '60', fileSystem2, 'imdbtvbackend', 'tt0187664' )
        correctShow2.addEpisode( Episode( '3', 'Mettle', '9 March 2001', 'none'), Season('2') )
        
        fileSystem3 = Filesystems(self.Tools.filetypesXML).getFilesystem( Filesystem( 'ext3' ) )
        correctShow3 = Show( 'C.S.I', '60', fileSystem2, 'imdbtvbackend', 'tt0247082' )
        correctShow3.addEpisode( Episode( '13', 'Identity Crisis', '17 January 2002', 'none'), Season('2') )
        
        def compareShows(show, other) :
            if show.name != other.name or show.duration != other.duration or show.filesystem.name != other.filesystem.name or show.backend != other.backend or show.url != other.url :
                assert False
            elif show.seasons[0].name != other.seasons[0].name :
                assert False
            elif show.seasons[0].episodes[0].name != other.seasons[0].episodes[0].name or show.seasons[0].episodes[0].title != other.seasons[0].episodes[0].title or show.seasons[0].episodes[0].airdate != other.seasons[0].episodes[0].airdate or show.seasons[0].episodes[0].arc != other.seasons[0].episodes[0].arc :
                assert False
            else :
                return True
                
        assert compareShows( testShow1, correctShow1 )
        assert compareShows( testShow2, correctShow2 )
        assert compareShows( testShow3, correctShow3 )
        
    def testGenerateFileName(self):
        #FIXME: More than one Style, different file suffixes, arcs.
        # generateFileName(Style=None)
        
        fileSystem1 = Filesystems(self.Tools.filetypesXML).getFilesystem( Filesystem( 'ntfs' ) )
        correctShow1 = Show( 'Black Books', '30', fileSystem1, 'imdbtvbackend', 'tt0262150' )
        correctShow1.addEpisode( Episode( '2', "A test's test' & a test / # a test", '6 October 2000', 'none'), Season('1') )
        
        fileSystem2 = Filesystems(self.Tools.filetypesXML).getFilesystem( Filesystem( 'ext3' ) )
        correctShow2 = Show( 'Spaced', '60', fileSystem2, 'imdbtvbackend', 'tt0187664' )
        correctShow2.addEpisode( Episode( '3', "A test's test' & a test / # a test", '9 March 2001', 'none'), Season('2') )
        
        fileSystem3 = Filesystems(self.Tools.filetypesXML).getFilesystem( Filesystem( 'ntfs' ) )
        correctShow3 = Show( 'C.S.I', '60', fileSystem3, 'imdbtvbackend', 'tt0247082' )
        correctShow3.addEpisode( Episode( '13', "Identity Crisis / # 4587", '17 January 2002', 'none'), Season('2') )
        
        self.FN = FileName('', self.database)
        self.FN.fileSuffix = '.avi'
        
        fileName1 = self.FN.generateFileName( correctShow1, self.Tools.filetypesXML )
        fileName2 = self.FN.generateFileName( correctShow2, self.Tools.filetypesXML )
        fileName3 = self.FN.generateFileName( correctShow3, self.Tools.filetypesXML )
        
        assert fileName1 == "Black Books - S01E02 - A tests test and a test or No. a test.avi"
        assert fileName2 == "Spaced - S02E03 - A test's test' & a test or # a test.avi"
        assert fileName3 == "C.S.I - S02E13 - Identity Crisis or No. 4587.avi"
