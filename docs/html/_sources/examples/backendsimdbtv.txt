
Examples
---------------

.. include::
    python-interactive-shell.rst

**Example:**::

    Update shows against imdbtv.

.. doctest ::
    
    >>> from api.dbapi import Show, Episode, Season, Database
    >>> from backends.imdbtv import Backend
    >>> Showlist = [ Show( "Black Books", "30", "ext3" , "imdbtvbackend", "tt0262150" ) ,
    ... Show( "Spaced", "60", "ext3" , "imdbtvbackend", "tt0187664" ) ]
    >>> backend = Backend()
    >>> DB = backend.updateShows( Showlist )
    >>> # Updates the show database from the backend.
    >>> DB.printDb()
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
                   Episode: Leaves
    

.. note::
    The url should be the part after "/title/" in the url.
    
    | 
    | *http://www.imdb.com/title/tt0262150/episodes*
    | 
    | relative url is:
    | 
    | *tt0262150*
    
