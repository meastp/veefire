
Examples
-----------

.. include::
    python-interactive-shell.rst

**Example:**
    
    Generate previews for every file name. In this example, there is a database directory with the xml file in :ref:`database-xml-file`. Also, we have some tv show files in our :ref:`test-directory` and the filetypes.xml as explained in :ref:`filetypes-xml`.
    
    .. warning::
        Remember that FileName.setCorrectShow() needs to be overloaded.
    

.. doctest ::
    
    >>> import os
    >>> from api.renameapi import Rename, Folder
    >>> from api.renameapi import FileName as AbstractFileName
    >>> from api.dbapi import Show, Episode, Season, Database
    >>> # import Tools to create a fake test directory.
    >>> # Remember to set the root path variable in tests/testproperties.py if you're not on Windows or Mac.
    >>> from tests.testproperties import Tools
    >>> tools = Tools()
    >>> tools.createRootDir()
    >>> tools.createDatabaseFiles()
    >>> tools.createFilesystemXML()
    >>> tools.createTempFiles()
    >>> # Overload our abstract function
    >>> class NewFileName( AbstractFileName ) :
    ...     def setCorrectShow( self, Shows ) :
    ...         return Shows[0]
    >>> # Overload Folder to use NewFileName
    >>> class NewFolder(Folder) :
    ...     def loadFiles( self ) :
    ...         self.database = Database( self.dbDir , self.shows )
    ...         self.database.loadDB()
    ...         self.fileNames = []
    ...         for afile in os.listdir( self.path ) :
    ...             if os.path.isfile( os.path.join( self.path, afile) ) :
    ...                 aFileName = NewFileName( afile, self.database )
    ...                 self.fileNames.append( aFileName )
    >>> me = Rename(tools.databaseDir , tools.filetypesXML)
    >>> # Paths to database and filetypes.xml file.
    >>> me.addFolder(NewFolder(os.path.join(tools.rootDir, tools.testDirs[0]), tools.databaseDir)).path
    '/tmp/veefire/Black Books'
    >>> # Add folder to rename-object.
    >>> # Alternatively, folders can be added recursively:
    >>> me.addFoldersRecursively( NewFolder(tools.rootDir, tools.databaseDir)).path
    '/tmp/veefire'
    >>> print [ folder.path for folder in me.folders ]
    ['/tmp/veefire/Black Books', '/tmp/veefire/Spaced', '/tmp/veefire/CSI', '/tmp/veefire/database']
    >>> me.removeFolder( NewFolder('/tmp/veefire/Spaced') ).path
    '/tmp/veefire/Spaced'
    >>> me.removeFolder( NewFolder('/tmp/veefire/CSI') ).path
    '/tmp/veefire/CSI'
    >>> me.removeFolder( NewFolder('/tmp/veefire/database') ).path
    '/tmp/veefire/database'
    >>> ms = me.getMatchingShows()
    >>> # Find correct shows from file name.
    >>> for Folder in ms :
    ...    print Folder.path
    ...    for FileName in Folder.fileNames :
    ...        print FileName.CorrectShow.name
    ...        print [ season.name for season in FileName.CorrectShow.seasons ]
    /tmp/veefire/Black Books
    Black Books
    ['1', '2', '3']
    Black Books
    ['1', '2', '3']
    >>> # Printed twice because there are two files from Black Books.
    >>> pv = me.generatePreviews('ext3')
    >>> # Generate new filenames from the database.
    >>> for Folder in pv :
    ...     print Folder
    ...     for item in Folder :
    ...         print item
    [('bb.s03e05.avi', 'Black Books - S03E05 - The Travel Writer.avi'), ('blackbooks.s01e02.avi', "Black Books - S01E02 - Manny's First Day.avi")]
    ('bb.s03e05.avi', 'Black Books - S03E05 - The Travel Writer.avi')
    ('blackbooks.s01e02.avi', "Black Books - S01E02 - Manny's First Day.avi")
    >>> for Folder in ms :
    ...     print Folder.path
    ...     for FileName in Folder.fileNames :
    ...         print FileName.generatedFileName , FileName.fileName
    /tmp/veefire/Black Books
    Black Books - S03E05 - The Travel Writer.avi bb.s03e05.avi
    Black Books - S01E02 - Manny's First Day.avi blackbooks.s01e02.avi

.. _test-directory:

Test Directory
---------------

    
    | **path** : /tmp/veefire/
    |
    | **contents**
    |       
    |       Black Books/black.BooKs.s1e02.avi
    |       Black Books/bb.s03e05.avi
    |       CSI/csiS01E11.avi
    |       CSI/CSI.2x12.avi
    |       Spaced/Spaced.2x4.avi
    |       Spaced/Spaced.S02E03.avi
    
**Example:**
    
    Get Filesystem object by name.  The filetypes.xml is explained in :ref:`filetypes-xml`.
    

.. doctest ::
    
    >>> from api.renameapi import Filesystems, Filesystem
    >>> # import Tools to create a fake test directory.
    >>> # Remember to set the root path variable in tests/testproperties.py if you're not on Windows or Mac.
    >>> from tests.testproperties import Tools
    >>> tools = Tools()
    >>> tools.createRootDir()
    >>> tools.createDatabaseFiles()
    >>> tools.createFilesystemXML()
    >>> fs = Filesystems(tools.filetypesXML)
    >>> fs1 = fs.getFilesystem( Filesystem("ext3") )
    >>> print fs1.validateString("thisis/324sdf/@$3?+")
    thisisor324sdfor@$3?+
    >>> fs2 = fs.getFilesystem( Filesystem("ntfs") )
    >>> print fs2.validateString("thisis/324sdf/@$3?+")
    thisisor324sdforatUSD3Qoplus
