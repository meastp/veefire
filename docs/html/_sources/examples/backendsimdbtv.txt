
Examples
---------------

.. include::
    python-interactive-shell.rst

**Example:**::

    Update shows against imdbtv.

.. code-block:: python
    :linenos:
    
    from api.dbapi import Show, Episode, Season, Database
    from backends.imdbtv import Backend
    
    Showlist = [ Show( "Black Books", "30", "ext3" , "imdbtvbackend", "tt0262150" ) ,
                 Show( "The IT Crowd", "30", "ext3" , "imdbtvbackend", "tt0487831" ) ,
                 Show( "Life on Mars", "60", "ext3" , "imdbtvbackend", "tt0478942" ) ]
    
    backend = Backend()
    
    DB = backend.updateShows( Showlist )
    
    DB.printDb()
    
    ## OUTPUT ##
    
    ####   Black Books   ####
    #Season: 1
    #       Episode: Cooking the Books
    #       Episode: Manny's First Day
    #       Episode: The Grapes of Wrath
    #       Episode: The Blackout
    #       Episode: The Big Lock-Out
    #       Episode: He's Leaving Home
    #Season: 2
    #       Episode: The Entertainer
    #       Episode: Fever
    #       Episode: The Fixer
    #       Episode: Blood
    #       Episode: Hello Sun
    #       Episode: A Nice Change
    #Season: 3
    #       Episode: Manny Come Home
    #       Episode: Elephants and Hens
    #       Episode: Moo-Ma and Moo-Pa
    #       Episode: A Little Flutter
    #       Episode: The Travel Writer
    #       Episode: Party
    ####   The IT Crowd   ####
    #Season: 1
    #       Episode: Yesterday's Jam
    #       Episode: Calamity Jen
    #       Episode: Fifty-Fifty
    #       Episode: The Red Door
    #       Episode: The Haunting of Bill Crouse
    #       Episode: Aunt Irma Visits
    #Season: 2
    #       Episode: The Work Outing
    #       Episode: Return of the Golden Child
    #       Episode: Moss and the German
    #       Episode: The Dinner Party
    #       Episode: Smoke and Mirrors
    #       Episode: Men Without Women
    ####   Life on Mars   ####
    #Season: 1
    #       Episode: Episode #1.1
    #       Episode: Episode #1.2
    #       Episode: Episode #1.3
    #       Episode: Episode #1.4
    #       Episode: Episode #1.5
    #       Episode: Episode #1.6
    #       Episode: Episode #1.7
    #       Episode: Episode #1.8
    #Season: 2
    #       Episode: Episode #2.1
    #       Episode: Episode #2.2
    #       Episode: Episode #2.3
    #       Episode: Episode #2.4
    #       Episode: Episode #2.5
    #       Episode: Episode #2.6
    #       Episode: Episode #2.7
    #       Episode: Episode #2.8
    ####
    
    

.. note::
    The url should be the part after "/title/" in the url.
    
    | 
    | *http://www.imdb.com/title/tt0262150/episodes*
    | 
    | relative url is:
    | 
    | *tt0262150*
    
