
Examples
-----------------

.. include::
    python-interactive-shell.rst

**Example:**
    
    Update the Database, using the backends to retrieve information. In this example, there is a database directory with the xml file in :ref:`database-xml-file`.
    

.. code-block:: python
    :linenos:
    
    from api.backendapi import BackendInterface
    
    se = BackendInterface('/home/username/testdb') #database directory
    
    #Now you can add new shows to the database, before updating.
    #testSession.addNewShow( Show( "Black Books", "30", "ext3" , "BaseBackend", "tt0262150" ) ) 
    
    print se.currentDB.database #our directory with the file is loaded
    #[<api.dbapi.Show instance at 0x1afad40>]
    
    se.updateDatabase()
    #### OUTPUT ( backendapi.py:92 = self.mergeDB.write(True) which gives this verbose output.
    #-----   <api.dbapi.Show instance at 0xe5dea8>
    #Black Books
    #{'duration': '30', 'url': 'tt0262150', 'backend': 'imdbtvbackend', 'name': 'Black Books', 'filesystem': 'ext3'}
    #---
    #1
    #<api.dbapi.Season instance at 0xe7c878>
    #[<api.dbapi.Episode instance at 0xe7cc68>, <api.dbapi.Episode instance at 0xe74680>,
    # <api.dbapi.Episode instance at 0xe6b440>, <api.dbapi.Episode instance at 0xe7d290>, 
    # <api.dbapi.Episode instance at 0xe7d1b8>, <api.dbapi.Episode instance at 0xe7d9e0>]
    #---
    #1
    #<api.dbapi.Episode instance at 0xe7cc68>
    #Cooking the Books
    #---
    #2
    #<api.dbapi.Episode instance at 0xe74680>
    #Manny's First Day
    #---
    #3
    #<api.dbapi.Episode instance at 0xe6b440>
    #The Grapes of Wrath
    #---
    #4
    #<api.dbapi.Episode instance at 0xe7d290>
    #The Blackout
    #---
    #5
    #<api.dbapi.Episode instance at 0xe7d1b8>
    #The Big Lock-Out
    #---
    #6
    #<api.dbapi.Episode instance at 0xe7d9e0>
    #He's Leaving Home
    #---
    #2
    #<api.dbapi.Season instance at 0xe7dab8>
    #[<api.dbapi.Episode instance at 0xe7da28>, <api.dbapi.Episode instance at 0xe7d440>,
    # <api.dbapi.Episode instance at 0xe7da70>, <api.dbapi.Episode instance at 0xe7db48>,
    # <api.dbapi.Episode instance at 0xe7db90>, <api.dbapi.Episode instance at 0xe7dbd8>]
    #---
    #1
    #<api.dbapi.Episode instance at 0xe7da28>
    #The Entertainer
    #---
    #2
    #<api.dbapi.Episode instance at 0xe7d440>
    #Fever
    #---
    #3
    #<api.dbapi.Episode instance at 0xe7da70>
    #The Fixer
    #---
    #4
    #<api.dbapi.Episode instance at 0xe7db48>
    #Blood
    #---
    #5
    #<api.dbapi.Episode instance at 0xe7db90>
    #Hello Sun
    #---
    #6
    #<api.dbapi.Episode instance at 0xe7dbd8>
    #A Nice Change
    #---
    #3
    #<api.dbapi.Season instance at 0xe7dcb0>
    #[<api.dbapi.Episode instance at 0xe7dc20>, <api.dbapi.Episode instance at 0xe7db00>,
    # <api.dbapi.Episode instance at 0xe7dc68>, <api.dbapi.Episode instance at 0xe7dd40>,
    # <api.dbapi.Episode instance at 0xe7dd88>, <api.dbapi.Episode instance at 0xe7ddd0>]
    #---
    #1
    #<api.dbapi.Episode instance at 0xe7dc20>
    #Manny Come Home
    #---
    #2
    #<api.dbapi.Episode instance at 0xe7db00>
    #Elephants and Hens
    #---
    #3
    #<api.dbapi.Episode instance at 0xe7dc68>
    #Moo-Ma and Moo-Pa
    #---
    #4
    #<api.dbapi.Episode instance at 0xe7dd40>
    #A Little Flutter
    #---
    #5
    #<api.dbapi.Episode instance at 0xe7dd88>
    #The Travel Writer
    #---
    #6
    #<api.dbapi.Episode instance at 0xe7ddd0>
    #Party
    #-----
    ### UPDATED FILE CONTENT ###
    # <tvshow><showproperties backend="imdbtvbackend" ... Rest of string omitted
    ####
    

**Example:**
    
    Get backend names.
    

.. code-block:: python
    :linenos:
    
    from api.backendapi import Backends
    se = Backends()
    se.getBackends('/home/username/veefire/backends')
    # Files in directory
    #imdbtvbackend.py~
    #base.py~
    #imdbtv.py~
    #__init__.py
    #base.py
    #__init__.pyc
    #imdbtv.py
    #base.pyc
    #imdbtv.pyc
    #### OUTPUT
    #['imdbtvbackend']
    


