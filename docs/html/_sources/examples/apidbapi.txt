
Examples
---------------

.. include::
    python-interactive-shell.rst

**Example:**
    
    Load the current database files into Python objects, and print a nice formatted overview of it.  In this example, there is a database directory with the xml file in :ref:`database-xml-file`.
    

.. doctest ::
    
    >>> from api.dbapi import Show, Episode, Season, Database
    >>> # import Tools to create a fake test directory.
    >>> # Remember to set the root path variable in tests/testproperties.py if you're not on Windows or Mac.
    >>> from tests.testproperties import Tools
    >>> tools = Tools()
    >>> tools.createRootDir()
    >>> tools.createDatabaseFiles()
    >>> db = Database(tools.databaseDir)
    >>> # Import the .show files from the database directory.
    >>> db.loadDB()
    >>> db.printDb()
    ####   C.S.I   ####
           Season: 1
                   Episode: Pilot
                   Episode: Cool Change
                   Episode: Crate 'n' Burial
                   Episode: Pledging Mr. Johnson
                   Episode: Friends &#38; Lovers
                   Episode: Who Are You?
                   Episode: Blood Drops
                   Episode: Anonymous
                   Episode: Unfriendly Skies
                   Episode: Sex, Lies and Larvae
                   Episode: I-15 Murders
                   Episode: Fahrenheit 932
                   Episode: Boom
                   Episode: To Halve and to Hold
                   Episode: Table Stakes
                   Episode: Too Tough to Die
                   Episode: Face Lift
                   Episode: $35K O.B.O.
                   Episode: Gentle, Gentle
                   Episode: Sounds of Silence
                   Episode: Justice Is Served
                   Episode: Evaluation Day
                   Episode: The Strip Strangler
           Season: 2
                   Episode: Burked
                   Episode: Chaos Theory
                   Episode: Overload
                   Episode: Bully for You
                   Episode: Scuba Doobie-Doo
                   Episode: Alter Boys
                   Episode: Caged
                   Episode: Slaves of Las Vegas
                   Episode: And Then There Were None
                   Episode: Ellie
                   Episode: Organ Grinder
                   Episode: You've Got Male
                   Episode: Identity Crisis
                   Episode: The Finger
                   Episode: Burden of Proof
                   Episode: Primum Non Nocere
                   Episode: Felonious Monk
                   Episode: Chasing the Bus
                   Episode: Stalker
                   Episode: Cats in the Cradle...
                   Episode: Anatomy of a Lye
                   Episode: Cross-Jurisdictions
                   Episode: The Hunger Artist
    ####   Spaced   ####
           Season: 1
                   Episode: Beginnings
                   Episode: Gatherings
                   Episode: Art
                   Episode: Battles
                   Episode: Chaos
                   Episode: Epiphanies
                   Episode: Ends
           Season: 2
                   Episode: Back
                   Episode: Change
                   Episode: Mettle
                   Episode: Help
                   Episode: Gone
                   Episode: Dissolution
                   Episode: Testkonflikt
    ####   Black Books   ####
           Season: 1
                   Episode: Cooking the Books
                   Episode: Manny's First Day
                   Episode: The Grapes of Wrath
                   Episode: The Blackout
                   Episode: The Big Lock-Out
                   Episode: He's Leaving Home
           Season: 2
                   Episode: The Entertainer
                   Episode: Fever
                   Episode: The Fixer
                   Episode: Blood
                   Episode: Hello Sun
                   Episode: A Nice Change
           Season: 3
                   Episode: Manny Come Home
                   Episode: Elephants and Hens
                   Episode: Moo-Ma and Moo-Pa
                   Episode: A Little Flutter
                   Episode: The Travel Writer
                   Episode: Party

