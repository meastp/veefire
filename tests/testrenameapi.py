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
import os

from veefire.api.dbapi import Database, Show, Season, Episode, Alias
from veefire.api.renameapi import FileName, Folder, Rename, Filesystem, Filesystems, InvChar
from testproperties import Tools

class testRename :
    """
    Test Rename Class
    """
    def setUp(self) :
        self.Tools = Tools()
        self.Tools.createRootDir()
        self.Tools.createTempFiles()
        self.Tools.createDatabaseFiles()
        self.Tools.createFilesystemXML()
        
        self.database = Database(self.Tools.databaseDir)
        self.database.loadDB()
        
        self.folder1 = Folder(os.path.join(self.Tools.rootDir, self.Tools.testDirs[0]), self.Tools.databaseDir)
        self.folder2 = Folder(os.path.join(self.Tools.rootDir, self.Tools.testDirs[1]), self.Tools.databaseDir)
        self.folder3 = Folder(os.path.join(self.Tools.rootDir, self.Tools.testDirs[2]), self.Tools.databaseDir)
        
    def tearDown(self):
        self.Tools.removeTempFiles()
        
    def testAddFolder(self) :
        rename = Rename( self.Tools.databaseDir, self.Tools.filetypesXML )
        
        assert rename.addFolder( self.folder1 ) == self.folder1
        assert rename.addFolder( self.folder1 ) == None
        assert rename.addFolder( self.folder1 ) == self.folder1
        assert rename.addFolder( Folder(os.path.join(self.Tools.rootDir, self.Tools.testDirs[1]), self.Tools.databaseDir) ) == None
        assert rename.addFolder( self.folder3 ) == self.folder3
        
    def testAddFoldersRecursively(self) :
        rename = Rename( self.Tools.databaseDir, self.Tools.filetypesXML )
        
        rename.addFolder( self.folder1 )
        
        assert rename.addFoldersRecursively( Folder(self.Tools.rootDir) ) == Folder(self.Tools.rootDir)
        
        assert [ folder.path for folder in rename.folders ] == ['/tmp/veefire/Black Books', '/tmp/veefire', '/tmp/veefire/Spaced', '/tmp/veefire/CSI', '/tmp/veefire/database']
        
        rename.addFolder( self.folder1 )
        rename.addFolder( self.folder1 )
        rename.addFolder( Folder('/tmp/veefire/Spaced' ))
        rename.addFolder( Folder('/tmp/veefire/Spaced' ))
        rename.addFolder( Folder('/tmp/veefire/Spaced' ))
        
        assert rename.removeFolder(Folder('/tmp/veefire')).path == '/tmp/veefire'
        
        assert [ folder.path for folder in rename.folders ] == ['/tmp/veefire/Black Books', '/tmp/veefire/Spaced', '/tmp/veefire/CSI', '/tmp/veefire/database']
        
        assert rename.removeFolder(Folder('/tmp/veefire/Spaced')).path == '/tmp/veefire/Spaced'
        
        assert rename.removeFolder(Folder('/tmp/veefire/Spaced')) == None
        
        assert [ folder.path for folder in rename.folders ] == ['/tmp/veefire/Black Books', '/tmp/veefire/CSI', '/tmp/veefire/database']
        
    def testGetFolder(self) :
        rename = Rename( self.Tools.databaseDir, self.Tools.filetypesXML )
        
        rename.addFolder( self.folder1 )
        rename.addFolder( self.folder1 )
        assert rename.getFolder( self.folder1 ) == True
        assert rename.getFolder( self.folder3 ) == None
        assert rename.getFolder( Folder(os.path.join(self.Tools.rootDir, self.Tools.testDirs[1]), self.Tools.databaseDir) ) == None
        assert rename.getFolder( Folder(os.path.join(self.Tools.rootDir, self.Tools.testDirs[2]), self.Tools.databaseDir) ) == None
        
    def testRemoveFolder(self) :
        rename = Rename( self.Tools.databaseDir, self.Tools.filetypesXML )
        
        rename.addFolder( self.folder1 )
        rename.addFolder( self.folder1 )
        assert rename.removeFolder( self.folder1 ) == self.folder1
        assert rename.removeFolder( self.folder1 ) == None
        assert rename.removeFolder( Folder(os.path.join(self.Tools.rootDir, self.Tools.testDirs[2]), self.Tools.databaseDir) ) == None
        assert rename.removeFolder( Folder(os.path.join(self.Tools.rootDir, self.Tools.testDirs[1]), self.Tools.databaseDir) ) == self.folder1
        
    def testGetMatchingShows(self):
        self.folder1.loadFiles()
        self.folder2.loadFiles()
        self.folder3.loadFiles()
        
        rename1 = Rename( self.Tools.databaseDir, self.Tools.filetypesXML )
        rename2 = Rename( self.Tools.databaseDir, self.Tools.filetypesXML )
        rename3 = Rename( self.Tools.databaseDir, self.Tools.filetypesXML )
        
        rename1.addFolder(self.folder1)
        rename1.addFolder(self.folder2)
        rename2.addFolder(self.folder1)
        rename2.addFolder(self.folder3)
        rename3.addFolder(self.folder3)
        
        assert [ fn.CorrectShow.name for fo in rename1.getMatchingShows() for fn in fo.getMatchingShows()] == ['Black Books', 'Black Books', 'C.S.I', 'C.S.I']
        assert [ fn.CorrectShow.name for fo in rename2.getMatchingShows() for fn in fo.getMatchingShows()] == ['Black Books', 'Black Books', 'Spaced', 'Spaced']
        assert [ fn.CorrectShow.name for fo in rename3.getMatchingShows() for fn in fo.getMatchingShows()] == ['Spaced', 'Spaced']
        
    def testGeneratePreviews(self):
        
        self.folder1.loadFiles()
        self.folder2.loadFiles()
        self.folder3.loadFiles()
        
        rename1 = Rename( self.Tools.databaseDir, self.Tools.filetypesXML )
        rename2 = Rename( self.Tools.databaseDir, self.Tools.filetypesXML )
        rename3 = Rename( self.Tools.databaseDir, self.Tools.filetypesXML )
        
        rename1.addFolder(self.folder1)
        rename1.addFolder(self.folder2)
        rename2.addFolder(self.folder1)
        rename2.addFolder(self.folder3)
        rename3.addFolder(self.folder3)
        
        rename1.getMatchingShows()
        rename2.getMatchingShows()
        rename3.getMatchingShows()
        
        assert [ fo for fo in rename1.generatePreviews('ext3') ] == [[('bb.s03e05.avi', 'Black Books - S03E05 - The Travel Writer.avi'), ('blackbooks.s01e02.avi', "Black Books - S01E02 - Manny's First Day.avi")], [('csiS01E11.avi', 'C.S.I - S01E11 - I-15 Murders.avi'), ('CSI.2x12.avi', "C.S.I - S02E12 - You've Got Male.avi")]]
        assert [ fo for fo in rename2.generatePreviews('ntfs', '%show[%season](%title)') ] ==  [[('bb.s03e05.avi', 'Black Books[03](The Travel Writer).avi'), ('blackbooks.s01e02.avi', 'Black Books[01](Mannys First Day).avi')], [('Spaced.S02E03.avi', 'Spaced[02](Mettle).avi'), ('Spaced.2x4.avi', 'Spaced[02](Help).avi')]]
        assert [ fo for fo in rename3.generatePreviews('ext3', '%show - %seasonx%episode - %title') ] ==  [[('Spaced.S02E03.avi', 'Spaced - 02x03 - Mettle.avi'), ('Spaced.2x4.avi', 'Spaced - 02x04 - Help.avi')]]
        
    def testRename(self):
        
        self.folder1.loadFiles()
        
        rename1 = Rename( self.Tools.databaseDir, self.Tools.filetypesXML )
        
        rename1.addFolder(self.folder1)
        rename1.addFolder(self.folder2)
        
        rename1.getMatchingShows()
        
        rename1.generatePreviews('ext3')
        
        assert os.listdir(self.folder1.path) == ['bb.s03e05.avi', 'blackbooks.s01e02.avi']
        rename1.rename()
        assert os.listdir(self.folder1.path) == ["Black Books - S01E02 - Manny's First Day.avi", 'Black Books - S03E05 - The Travel Writer.avi']
        
    def testRevert(self):
        
        self.folder1.loadFiles()
        
        rename1 = Rename( self.Tools.databaseDir, self.Tools.filetypesXML )
        
        rename1.addFolder(self.folder1)
        rename1.addFolder(self.folder2)
        
        rename1.getMatchingShows()
        
        rename1.generatePreviews('ext3')
        
        assert os.listdir(self.folder1.path) == ['bb.s03e05.avi', 'blackbooks.s01e02.avi']
        rename1.rename()
        assert os.listdir(self.folder1.path) == ["Black Books - S01E02 - Manny's First Day.avi", 'Black Books - S03E05 - The Travel Writer.avi']
        rename1.revert()
        assert os.listdir(self.folder1.path) == ['bb.s03e05.avi', 'blackbooks.s01e02.avi']
        
class testFolder :
    """
    Test Folder Class
    """
    def setUp(self) :
        self.Tools = Tools()
        self.Tools.createRootDir()
        self.Tools.createTempFiles()
        self.Tools.createDatabaseFiles()
        self.Tools.createFilesystemXML()
        
        self.database = Database(self.Tools.databaseDir)
        self.database.loadDB()
        
        self.folder1 = Folder(os.path.join(self.Tools.rootDir, self.Tools.testDirs[0]), self.Tools.databaseDir)
        self.folder2 = Folder(os.path.join(self.Tools.rootDir, self.Tools.testDirs[1]), self.Tools.databaseDir)
        self.folder3 = Folder(os.path.join(self.Tools.rootDir, self.Tools.testDirs[2]), self.Tools.databaseDir)
        
    def tearDown(self):
        self.Tools.removeTempFiles()
        
    def testLoadFiles(self):
        self.folder1.loadFiles()
        self.folder2.loadFiles()
        self.folder3.loadFiles()
        
        assert [ fn.fileName for fn in self.folder1.fileNames ] == ['bb.s03e05.avi', 'blackbooks.s01e02.avi']
        assert [ fn.fileName for fn in self.folder2.fileNames ] == ['csiS01E11.avi', 'CSI.2x12.avi']
        assert [ fn.fileName for fn in self.folder3.fileNames ] == ['Spaced.S02E03.avi', 'Spaced.2x4.avi']
        
    def testGetMatchingShows(self):
        self.folder1.loadFiles()
        self.folder2.loadFiles()
        self.folder3.loadFiles()
        
        assert [ fn.CorrectShow.name for fn in self.folder1.getMatchingShows() ] == ['Black Books', 'Black Books']
        assert [ fn.CorrectShow.name for fn in self.folder2.getMatchingShows() ] == ['C.S.I', 'C.S.I']
        assert [ fn.CorrectShow.name for fn in self.folder3.getMatchingShows() ] == ['Spaced', 'Spaced']
        
    def testGeneratePreviews(self):
        
        self.folder1.loadFiles()
        self.folder2.loadFiles()
        self.folder3.loadFiles()
        
        self.folder1.getMatchingShows()
        self.folder2.getMatchingShows()
        self.folder3.getMatchingShows()
        
        assert [ fn for fn in self.folder1.generatePreviews(self.Tools.filetypesXML, 'ext3', '%show - S0%sesonE0%episode - %title') ] == [('bb.s03e05.avi', 'Black Books - S0%sesonE005 - The Travel Writer.avi'), ('blackbooks.s01e02.avi', "Black Books - S0%sesonE002 - Manny's First Day.avi")]
        assert [ fn for fn in self.folder2.generatePreviews(self.Tools.filetypesXML, 'ntfs', '%show - S0%sesonE0%episode - %title') ] == [('csiS01E11.avi', 'C.S.I - S0%sesonE011 - I-15 Murders.avi'), ('CSI.2x12.avi', 'C.S.I - S0%sesonE012 - Youve Got Male.avi')]
        assert [ fn for fn in self.folder3.generatePreviews(self.Tools.filetypesXML, 'ext3', '%show - S0%sesonE0%episode - %title') ] == [('Spaced.S02E03.avi', 'Spaced - S0%sesonE003 - Mettle.avi'), ('Spaced.2x4.avi', 'Spaced - S0%sesonE004 - Help.avi')]
        
    def testRename(self):
        
        self.folder1.loadFiles()
        self.folder1.getMatchingShows()
        self.folder1.generatePreviews(self.Tools.filetypesXML, 'ext3', '%show - S0%sesonE0%episode - %title')
        
        assert os.listdir(self.folder1.path) == ['bb.s03e05.avi', 'blackbooks.s01e02.avi']
        self.folder1.rename()
        assert os.listdir(self.folder1.path) == ["Black Books - S0%sesonE002 - Manny's First Day.avi", 'Black Books - S0%sesonE005 - The Travel Writer.avi']
        
    def testRevert(self):
        
        self.folder1.loadFiles()
        self.folder1.getMatchingShows()
        self.folder1.generatePreviews(self.Tools.filetypesXML, 'ext3', '%show - S0%sesonE0%episode - %title')
        
        assert os.listdir(self.folder1.path) == ['bb.s03e05.avi', 'blackbooks.s01e02.avi']
        self.folder1.rename()
        assert os.listdir(self.folder1.path) == ["Black Books - S0%sesonE002 - Manny's First Day.avi", 'Black Books - S0%sesonE005 - The Travel Writer.avi']
        self.folder1.revert()
        assert os.listdir(self.folder1.path) == ['bb.s03e05.avi', 'blackbooks.s01e02.avi']
        
class testFileName :
    """
    Test FileName Class
    """
    def setUp(self) :
        self.Tools = Tools()
        self.Tools.createRootDir()
        self.Tools.createTempFiles()
        self.Tools.createDatabaseFiles()
        self.Tools.createFilesystemXML()
        
        self.database = Database(self.Tools.databaseDir)
        self.database.loadDB()
        
        smallville = Show('Smallville', '60', 'dummy', 'dummy')
        smallville.addAlias(Alias('smallville'))
        smallville.addEpisode( Episode('10', 'Bizarro', 'dummy'), Season('7') )
        self.database.addShow( smallville )
        
        self.files = [ 'blackbooks.s01e02.avi', 'spaced.2x03.avi', 'csi.s02E13.avi', 'black books - 03x02 - Six of One.avi', 'Smallville.S07E10.HDTV.XviD-XOR.avi' ]
        self.filenames = [ FileName( files, self.database ) for files in self.files ]
        
    def tearDown(self):
        self.Tools.removeTempFiles()
        
    def testGetPattern(self):
        
        dummydb = Database()
        dummyFN = FileName( 'dummy', dummydb )
        
        assert [ fn.getPattern() for fn in self.filenames ] == \
        [ dummyFN.pattern1, dummyFN.pattern2, dummyFN.pattern1, dummyFN.pattern2, dummyFN.pattern1 ]
        
    def testGetSeason(self):
        
        assert [ fn.getSeason() for fn in self.filenames ] == \
        [ '1', '2', '2', '3', '7' ]
        
    def testGetEpisode(self):
        
        assert [ fn.getEpisode() for fn in self.filenames ] == \
        [ '2', '3', '13', '2', '10' ]
        
    def testGetMatchingShows(self):
        
        assert [ fn.getMatchingShows().name for fn in self.filenames ] == \
        [ 'Black Books', 'Spaced', 'C.S.I', 'Black Books', 'Smallville' ]
        
    def testGeneratePreview(self):
        
        result = []
        for fn in self.filenames :
            fn.getMatchingShows()
            result.append( fn.generatePreview(self.Tools.filetypesXML, 'ext3', '%show - %seasonx%episode - %title ( %arc - %airdate )' ) )
        assert result == [
                    ('blackbooks.s01e02.avi', "Black Books - 01x02 - Manny's First Day ( none - 6 October 2000 ).avi"), 
                    ('spaced.2x03.avi', 'Spaced - 02x03 - Mettle ( none - 9 March 2001 ).avi'), 
                    ('csi.s02E13.avi', 'C.S.I - 02x13 - Identity Crisis ( none - 17 January 2002 ).avi'), 
                    ('black books - 03x02 - Six of One.avi', 'Black Books - 03x02 - Elephants and Hens ( none - 18 March 2004 ).avi'), 
                    ('Smallville.S07E10.HDTV.XviD-XOR.avi', 'Smallville - 07x10 - Bizarro ( none - dummy ).avi')]
        
        result = []
        for fn in self.filenames :
            fn.getMatchingShows()
            result.append( fn.generatePreview(self.Tools.filetypesXML, 'ntfs', '%show - %seasonE%episode - %title ( %arc - %airdate )' ) )
        assert result == [('blackbooks.s01e02.avi', 'Black Books - 01E02 - Mannys First Day ( none - 6 October 2000 ).avi'), 
                            ('spaced.2x03.avi', 'Spaced - 02E03 - Mettle ( none - 9 March 2001 ).avi'), 
                            ('csi.s02E13.avi', 'C.S.I - 02E13 - Identity Crisis ( none - 17 January 2002 ).avi'), 
                            ('black books - 03x02 - Six of One.avi', 'Black Books - 03E02 - Elephants and Hens ( none - 18 March 2004 ).avi'),
                            ('Smallville.S07E10.HDTV.XviD-XOR.avi', 'Smallville - 07E10 - Bizarro ( none - dummy ).avi')]
        
    def testGetShowDetails(self):
        
        
        testShows = [ fn.getShowDetails( self.Tools.filetypesXML, fn.getMatchingShows() ) for fn in self.filenames ]
        
        assert [ len(ts.seasons) for ts in testShows ] == [1, 1, 1, 1, 1]
        assert [ len(ts.seasons[0].episodes) for ts in testShows ] == [1, 1, 1, 1, 1]
        
        
        correctShow1 = Show( 'Black Books', '30', 'imdbtvbackend', 'tt0262150' )
        correctShow1.addEpisode( Episode( '2', "Manny's First Day", '6 October 2000', 'none'), Season('1') )
        
        correctShow2 = Show( 'Spaced', '60', 'imdbtvbackend', 'tt0187664' )
        correctShow2.addEpisode( Episode( '3', 'Mettle', '9 March 2001', 'none'), Season('2') )
        
        correctShow3 = Show( 'C.S.I', '60', 'imdbtvbackend', 'tt0247082' )
        correctShow3.addEpisode( Episode( '13', 'Identity Crisis', '17 January 2002', 'none'), Season('2') )
        
        def compareShows(show, other) :
            if show.name != other.name or show.duration != other.duration or show.backend != other.backend or show.url != other.url :
                assert False
            elif show.seasons[0].name != other.seasons[0].name :
                assert False
            elif show.seasons[0].episodes[0].name != other.seasons[0].episodes[0].name or show.seasons[0].episodes[0].title != other.seasons[0].episodes[0].title or show.seasons[0].episodes[0].airdate != other.seasons[0].episodes[0].airdate or show.seasons[0].episodes[0].arc != other.seasons[0].episodes[0].arc :
                assert False
            else :
                return True
        
        assert compareShows( testShows[0], correctShow1 )
        assert compareShows( testShows[1], correctShow2 )
        assert compareShows( testShows[2], correctShow3 )
        
    def testGenerateFileName(self):
        #FIXME: More than one Style, different file suffixes, arcs.
        # generateFileName(Style=None)
        
        correctShow1 = Show( 'Black Books', '30', 'imdbtvbackend', 'tt0262150' )
        correctShow1.addEpisode( Episode( '2', "A test's test' & a test / # a test", '6 October 2000', 'none'), Season('1') )
        
        correctShow2 = Show( 'Spaced', '60', 'imdbtvbackend', 'tt0187664' )
        correctShow2.addEpisode( Episode( '3', "A test's test' & a test / # a test", '9 March 2001', 'none'), Season('2') )
        
        correctShow3 = Show( 'C.S.I', '60', 'imdbtvbackend', 'tt0247082' )
        correctShow3.addEpisode( Episode( '13', "Identity Crisis / # 4587", '17 January 2002', 'none'), Season('2') )
        
        self.FN = FileName('', self.database)
        self.FN.fileSuffix = '.avi'
        
        fileName1 = self.FN.generateFileName( correctShow1, self.Tools.filetypesXML, 'ext3', '%show.S%seasonE%episode.%title.%arc.%airdate' )
        fileName2 = self.FN.generateFileName( correctShow2, self.Tools.filetypesXML, 'ntfs', '%show.S%seasonE%episode.%title.%arc.%airdate'  )
        fileName3 = self.FN.generateFileName( correctShow3, self.Tools.filetypesXML, 'ext3', '%show.S%seasonE%episode.%title.%arc.%airdate'  )
        
        assert fileName1 == "Black Books.S01E02.A test's test' & a test or # a test.none.6 October 2000.avi"
        assert fileName2 == "Spaced.S02E03.A tests test and a test or No. a test.none.9 March 2001.avi"
        assert fileName3 == "C.S.I.S02E13.Identity Crisis or # 4587.none.17 January 2002.avi"
        
    def testRenameFile(self) :
        
        self.folder1 = Folder(os.path.join(self.Tools.rootDir, self.Tools.testDirs[0]), self.Tools.databaseDir)
        self.folder1.loadFiles()
        
        self.filename1 = FileName( 'blackbooks.s01e02.avi', self.database )
        self.filename1.getMatchingShows()
        
        self.filename1.generatePreview(self.Tools.filetypesXML, 'ext3', '%show - %seasonx%episode - %title ( %arc - %airdate )')
        
        assert os.listdir(self.folder1.path) == ['bb.s03e05.avi', 'blackbooks.s01e02.avi']
        
        self.filename1.renameFile(self.folder1.path)
        assert os.listdir(self.folder1.path) == ['bb.s03e05.avi', "Black Books - 01x02 - Manny's First Day ( none - 6 October 2000 ).avi"]
        
    def testRevertFile(self) :
        
        self.folder1 = Folder(os.path.join(self.Tools.rootDir, self.Tools.testDirs[0]), self.Tools.databaseDir)
        self.folder1.loadFiles()
        
        self.filename1 = FileName( 'blackbooks.s01e02.avi', self.database )
        self.filename1.getMatchingShows()
        self.filename1.generatePreview(self.Tools.filetypesXML, 'ext3', '%show - %seasonx%episode - %title ( %arc - %airdate )')
        
        assert os.listdir(self.folder1.path) == ['bb.s03e05.avi', 'blackbooks.s01e02.avi']
        self.filename1.renameFile(self.folder1.path)
        assert os.listdir(self.folder1.path) == ['bb.s03e05.avi', "Black Books - 01x02 - Manny's First Day ( none - 6 October 2000 ).avi"]
        self.filename1.revertFile(self.folder1.path)
        assert os.listdir(self.folder1.path) == ['bb.s03e05.avi', 'blackbooks.s01e02.avi']
        
class testFilesystems :
    """
    Test Filesystems Class.
    """
    def setUp(self) :
        self.FS = Filesystems() # Filesystem dir is None
    
    def testLoadFilesystems( self ) :
        self.Tools = Tools()
        self.Tools.createRootDir()
        self.Tools.createFilesystemXML()
        self.FS = Filesystems(self.Tools.filetypesXML)
        
        Ext3FS = self.FS.getFilesystem(Filesystem('ext3'))
        NTFSFS = self.FS.getFilesystem(Filesystem('ntfs'))
        Filesystem3 = Filesystem('FS3')
        
        assert self.FS.addFilesystem( Ext3FS ) == None
        assert self.FS.addFilesystem( Filesystem('ntfs') ) == None
        assert self.FS.addFilesystem( Filesystem3 ) == Filesystem3
        
        assert self.FS.getFilesystem( Filesystem3 ) == Filesystem3
        assert self.FS.getFilesystem( NTFSFS ) == NTFSFS
        assert self.FS.getFilesystem( Ext3FS ) == Ext3FS
        
        assert self.FS.removeFilesystem( NTFSFS ) == NTFSFS
        assert self.FS.removeFilesystem( NTFSFS ) == None
        assert self.FS.removeFilesystem( Ext3FS ) == Ext3FS
        assert self.FS.removeFilesystem( Ext3FS ) == None
        
        self.Tools.removeTempFiles()
        
    def testAddFilesystem( self ) :
        Filesystem1 = Filesystem('FS1')
        Filesystem2 = Filesystem('FS2')
        Filesystem3 = Filesystem('FS3')
        assert self.FS.addFilesystem( Filesystem1 ) == Filesystem1
        assert self.FS.addFilesystem( Filesystem1 ) == None
        assert self.FS.addFilesystem( Filesystem2 ) == Filesystem2
        assert self.FS.addFilesystem( Filesystem('FS2') ) == None
        assert self.FS.addFilesystem( Filesystem3 ) == Filesystem3
        
    def testGetFilesystem(self) :
        Filesystem1 = Filesystem('FS1')
        Filesystem2 = Filesystem('FS2')
        Filesystem3 = Filesystem('FS3')
        self.FS.addFilesystem( Filesystem1 )
        self.FS.addFilesystem( Filesystem2 )
        assert self.FS.getFilesystem( Filesystem1 ) == Filesystem1
        assert self.FS.getFilesystem( Filesystem3 ) == None
        assert self.FS.getFilesystem( Filesystem('FS2') ) == Filesystem2
        assert self.FS.getFilesystem( Filesystem('FS3') ) == None
        
    def testRemoveFilesystem(self) :
        Filesystem1 = Filesystem('FS1')
        Filesystem2 = Filesystem('FS2')
        Filesystem3 = Filesystem('FS3')
        self.FS.addFilesystem( Filesystem1 )
        self.FS.addFilesystem( Filesystem2 )
        assert self.FS.removeFilesystem( Filesystem1 ) == Filesystem1
        assert self.FS.removeFilesystem( Filesystem1 ) == None
        assert self.FS.removeFilesystem( Filesystem('FS3') ) == None
        assert self.FS.removeFilesystem( Filesystem('FS2') ) == Filesystem2

class testFilesystem :
    """
    Test Filesystem Class
    """
    def setUp( self ) :
        self.filesystem = Filesystem( "FileSystem" )
        
    def testAddChar( self ) :
        InvalidCharacter1 = InvChar( "Description", "002B", "plus" )
        InvalidCharacter2 = InvChar( "NewDescription", "002B", "plus" )
        InvalidCharacter3 = InvChar( "Description", "002F", "or" )
        assert self.filesystem.addChar( InvalidCharacter1 ) == InvalidCharacter1
        assert self.filesystem.addChar( InvalidCharacter1 ) == None
        assert self.filesystem.addChar( InvalidCharacter2 ) == None
        assert self.filesystem.addChar( InvalidCharacter3 ) == InvalidCharacter3
        
    def testGetChar( self ) :
        assert self.filesystem.chars == []
        InvalidCharacter1 = InvChar( "Description", "002B", "plus" )
        InvalidCharacter2 = InvChar( "NewDescription", "0026", "and" )
        self.filesystem.addChar( InvalidCharacter1 )
        self.filesystem.addChar( InvalidCharacter2 )
        assert self.filesystem.getChar( InvalidCharacter1 ) == InvalidCharacter1
        assert self.filesystem.getChar( InvChar( "Description", "002B", "ERROR" )) == None
        assert self.filesystem.getChar( InvalidCharacter2 ) == InvalidCharacter2
        assert self.filesystem.getChar( InvChar( "Description", "0000", "and" )) == None
        
    def testRemoveChar( self ) :
        InvalidCharacter1 = InvChar( "Description", "002B", "plus" )
        InvalidCharacter2 = InvChar( "NewDescription", "0026", "and" )
        InvalidCharacter3 = InvChar( "Description", "002F", "or" )
        self.filesystem.addChar( InvalidCharacter1 )
        self.filesystem.addChar( InvalidCharacter2 )
        assert self.filesystem.removeChar( InvalidCharacter1 ) == InvalidCharacter1
        assert self.filesystem.removeChar( InvalidCharacter1 ) == None
        assert self.filesystem.removeChar( InvChar( "Description", "002F", "or" ) ) == None
        assert self.filesystem.removeChar( InvChar( "NewDescription", "0026", "and" ) ) == InvalidCharacter2
        
    def testValidateString( self ) :
        InvalidCharacter1 = InvChar( "Description", "002B", "plus" )
        InvalidCharacter2 = InvChar( "NewDescription", "0026", "and" )
        InvalidCharacter3 = InvChar( "Description", "002F", "or" )
        self.filesystem.addChar( InvalidCharacter1 )
        self.filesystem.addChar( InvalidCharacter2 )
        self.filesystem.addChar( InvalidCharacter3 )
        assert self.filesystem.validateString( "test+test" ) == "testplustest"
        assert self.filesystem.validateString( "+test/test&test" ) == "plustestortestandtest"
        
