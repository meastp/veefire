.. _preferences-xml:

Preferences in veefire
========================

Preferences for veefire are kept in an xml-file, preferences.xml.

**Structure - the Preferences logic:**

 | *<preferences>*
 |   *<name-of-property value="propertyvalue" />* :class:`api.dbapi.Preferences` ( current preference )

 | *<options>*
 |   *<name-of-property>* :class:`api.dbapi.Preferences` ( preference ) 
 |      *<option value="optionvalue">* ( preference option )
 |      *<option value="optionvalue2">* ( preference option )
 |   *</name-of-property>*

**Example:**

.. code-block:: xml
    
﻿<?xml version="1.0" encoding="UTF-8"?>
<root>
  <preferences>
    <naming-style value="%show - S%seasonE%episode - %title"/>
    <confirm-on-rename value="true"/>
    <update-on-startup value="false"/>
    <imdbtv-with-tests value="false"/>
    <filesystem value="ext3" />
  </preferences>
  <options>
    <naming-style>
      <option value="%show - S%seasonE%episode - %title"/>
      <option value="%show.%seasonx%episode.%title"/>
    </naming-style>
  </options>
</root>
    

