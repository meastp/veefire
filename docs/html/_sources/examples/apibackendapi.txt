
Examples
-----------------

.. include::
    python-interactive-shell.rst

**Example:**
    
    Update the Database, using the backends to retrieve information. In this example, there is a database directory with the xml file in :ref:`database-xml-file`.
    

.. doctest ::
    
    >>> from veefire.api.backendapi import BackendInterface
    >>> # import Tools to create a fake test directory.
    >>> # Remember to set the root path variable in tests/testproperties.py if you're not on Windows or Mac.
    >>> from tests.testproperties import Tools
    >>> tools = Tools()
    >>> tools.createRootDir()
    >>> tools.createDatabaseFiles()
    >>> se = BackendInterface(tools.databaseDir) #database directory
    >>> # Optional : you can add new shows to the database, before updating.
    >>> # testSession.addNewShow( Show( "Black Books", "30", "ext3" , "BaseBackend", "tt0262150" ) ) 
    >>> print [ show.name for show in se.currentDB.database ]
    ['C.S.I', 'Spaced', 'Black Books']
    >>> # Automatically (dummy) solve conflicts.
    >>> class NewBackendInterface(BackendInterface):
    ...     def solveEpisodeConflicts(self, firstEpisode, secondEpisode):
    ...         return firstEpisode
    >>> re = NewBackendInterface(tools.databaseDir) #database directory
    >>> re.updateDatabase()
    >>> # Updates the database, and writes it to the database directory.

**Example:**
    
    Get backend names.
    

.. doctest::
    
    >>> from veefire.api.backendapi import Backends
    >>> # import Tools to create a fake test directory.
    >>> # Remember to set the root path variable in tests/testproperties.py if you're not on Windows or Mac.
    >>> from tests.testproperties import Tools
    >>> tools = Tools()
    >>> tools.createRootDir()
    >>> tools.createDatabaseFiles()
    >>> tools.createBackendFiles()
    >>> se = Backends()
    >>> se.getBackends(tools.BackendDirectory)
    ['imdbtvbackend']
    >>> # View the supported backends.
    

