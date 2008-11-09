
Examples
-----------------

.. include::
    python-interactive-shell.rst

**Example:**
    
    A backend must be able to get data based on Show objects.
    

.. code-block:: python
    :linenos:
    
    from api.dbapi import Show, Episode, Season, Database
    from backends.base import BaseBackend
    
    Showlist = [ Show( "Black Books", "30", "ext3" , "BaseBackend", "tt0262150" ) ,
                 Show( "The IT Crowd", "30", "ext3" , "BaseBackend", "tt0487831" ) ,
                 Show( "Life on Mars", "60", "ext3" , "BaseBackend", "tt0478942" ) ]
    
    backend = BaseBackend()
    
    DataBase = backend.updateShows( Showlist )
    
    ## OUTPUT ##
    
    NotImplementedError # This is an abstract function.
    
