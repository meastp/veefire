
Examples
---------------

.. include::
    python-interactive-shell.rst

**Example:**
    
    Manipulate the preferences.xml file ( :ref:`preferences-xml` ).
    

.. doctest ::
    
    >>> from api.preferencesapi import Preferences
    >>> # import Tools to create a fake test directory.
    >>> # Remember to set the root path variable in tests/testproperties.py if you're not on Windows or Mac.
    >>> from tests.testproperties import Tools
    >>> tools = Tools()
    >>> tools.createRootDir()
    >>> tools.createPreferencesXML()
    >>> preferences = Preferences(tools.preferencesXML)
    >>> # load preferences from preferences.xml
    >>> preferences.load()
    >>> # get property
    >>> print preferences['confirm-on-rename']
    true
    >>> # set property
    >>> preferences['confirm-on-rename'] = 'false'
    >>> # list options, if any
    >>> print preferences.getOptions('naming-style')
    ['%show - S%seasonE%episode - %title', '%show.%seasonx%episode.%title']
    >>> # add option
    >>> print preferences.addOption('naming-style', '3')
    ['%show - S%seasonE%episode - %title', '%show.%seasonx%episode.%title', '3']
    >>> # remove option
    >>> preferences.removeOption('naming-style', '%show - S%seasonE%episode - %title')
    ['%show.%seasonx%episode.%title', '3']
    >>> # save xml-file
    >>> preferences.save()


