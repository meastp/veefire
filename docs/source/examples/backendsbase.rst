
Examples
-----------------

.. include::
    python-interactive-shell.rst

**Example:**
    
    A backend must be able to get data based on Show objects.
    

.. doctest ::
    
    >>> from veefire.api.dbapi import Show, Episode, Season, Database
    >>> from veefire.backends.base import BaseBackend
    >>> Showlist = [ Show( "Black Books", "30", "BaseBackend", "tt0262150" ) ,
    ... Show( "The IT Crowd", "30", "BaseBackend", "tt0487831" ) ,
    ... Show( "Life on Mars", "60", "BaseBackend", "tt0478942" ) ]
    >>> backend = BaseBackend()
    >>> DataBase = backend.updateShows( Showlist )
    Traceback (most recent call last):
      File "/usr/lib/python2.5/doctest.py", line 1228, in __run
        compileflags, 1) in test.globs
      File "<doctest default[4]>", line 1, in <module>
        DataBase = backend.updateShows( Showlist )
      File "/home/meastp/Development/Launchpad/veefire/features/example-tests/backends/base.py", line 46, in updateShows
        raise NotImplementedError
    NotImplementedError
    >>> # Function for BaseBackend is abstract and must be overloaded.
    
