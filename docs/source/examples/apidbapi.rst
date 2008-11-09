
Examples
---------------

.. include::
    python-interactive-shell.rst

**Example:**
    
    Load the current database files into Python objects, and print a nice formatted overview of it.  In this example, there is a database directory with the xml file in :ref:`database-xml-file`.
    

.. code-block:: python
    :linenos:
    
    from api.dbapi import Show, Episode, Season, Database
    
    db = Database('/home/meastp/testdb')
    db.loadDB()
    db.printDb()
    ####   Black Books   ####
    #       Season: 1
    #               Episode: Cooking the Books
    #               Episode: Manny's First Day
    #               Episode: The Grapes of Wrath
    #               Episode: The Blackout
    #               Episode: The Big Lock-Out
    #               Episode: He's Leaving Home
    #       Season: 2
    #               Episode: The Entertainer
    #               Episode: Fever
    #               Episode: The Fixer
    #               Episode: Blood
    #               Episode: Hello Sun
    #               Episode: A Nice Change
    #       Season: 3
    #               Episode: Manny Come Home
    #               Episode: Elephants and Hens
    #               Episode: Moo-Ma and Moo-Pa
    #               Episode: A Little Flutter
    #               Episode: The Travel Writer
    #               Episode: Party 

**Example:**
    
    Get Filesystem object by name.  The filetypes.xml is explained in :ref:`filetypes-xml`.
    

.. code-block:: python
    :linenos:
    
    from api.dbapi import Filesystems, Filesystem
    
    fs = Filesystems('/home/meastp/filetypes.xml')
    fs1 = fs.getFilesystem( Filesystem("ext3") )
    print fs1.validateString("thisis/324sdf@$3?+")
    #### OUTPUT
    #thisisor324sdf@$3?+
    ####
    
