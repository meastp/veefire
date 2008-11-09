
Examples
-----------

.. include::
    python-interactive-shell.rst

**Example:**
    
    Generate previews for every file name. In this example, there is a database directory with the xml file in :ref:`database-xml-file`. Also, we have some tv show files in our :ref:`test-directory` and the filetypes.xml as explained in :ref:`filetypes-xml`.
    
    .. warning::
        Remember that FileName.setCorrectShow() needs to be overloaded.
    

.. code-block:: python
    :linenos:
    
    from api.renameapi import Rename, Folder
    from api.renameapi import FileName as AbstractFileName
    from api.dbapi import Show, Episode, Season, Database

    # Overload our abstract function
    class NewFileName( AbstractFileName ) :
         def setCorrectShow( self, Shows ) :
                 return Shows[0]

    # Overload Folder to use NewFileName
    class NewFolder(Folder) :
        def loadFiles( self ) :
            self.database = Database( self.dbDir , self.shows )
            self.database.loadDB()
            self.fileNames = []
            for afile in os.listdir( self.path ) :
                if os.path.isfile( os.path.join( self.path, afile) ) :
                    aFileName = NewFileName( afile, self.database )
                    self.fileNames.append( aFileName )

    # Path to database and filetypes.xml file.
    me = Rename('/home/username/veefire/testdb' , '/home/username/veefire/filetypes.xml')
    me.addFolder(NewFolder('/home/username/veefire/test'))
    #me.addFolder(NewFolder('/home/meastp/username/test/anotherdirectory'))
    #me.addFolder(NewFolder('/home/meastp/username/yetanotherdirectory'))
    ms = me.getMatchingShows()
    for Folder in ms :
        print Folder.path
        for FileName in Folder.fileNames :
            print FileName.CorrectShow

    #### OUTPUT
    #/home/username/veefire/test
    #<api.dbapi.Show instance at 0x1d7acf8>
    #None
    #None
    #None
    #<api.dbapi.Show instance at 0x1d80a70>
    ####

    pv = me.generatePreviews()
    for Folder in pv :
        print Folder
        for item in Folder :
            print item

    #### OUTPUT
    #[('black.BooKs.s1e02.avi', "Black Books - S01E02 - Manny's First Day.avi"),
    # ('mash.1x15.avi', None), ('heroes.s01e15.avi', None), ('csi.s03e15.avi', None),
    # ('bb.03x03.avi', 'Black Books - S03E03 - Moo-Ma and Moo-Pa.avi')]
    #('black.BooKs.s1e02.avi', "Black Books - S01E02 - Manny's First Day.avi")
    #('mash.1x15.avi', None)
    #('heroes.s01e15.avi', None)
    #('csi.s03e15.avi', None)
    #('bb.03x03.avi', 'Black Books - S03E03 - Moo-Ma and Moo-Pa.avi')
    ####

    for Folder in ms :
        print Folder.path
        for FileName in Folder.fileNames :
            print FileName.generatedFileName , FileName.fileName

    #### OUTPUT
    #/home/username/veefire/test
    #Black Books - S01E02 - Manny's First Day.avi black.BooKs.s1e02.avi
    #None mash.1x15.avi
    #None heroes.s01e15.avi
    #None csi.s03e15.avi
    #Black Books - S03E03 - Moo-Ma and Moo-Pa.avi bb.03x03.avi
    ####

.. _test-directory:

Test Directory
---------------

    
    | **path** : /home/username/veefire/test
    |   
    | **contents**
    |       
    |       black.BooKs.s1e02.avi
    |       mash.1x15.avi
    |       heroes.s01e15.avi
    |       csi.s03e15.avi
    |       bb.03x03.avi
    
