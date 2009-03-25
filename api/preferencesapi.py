#!/usr/bin/env python

#    Copyright 2008 Mats Taraldsvik <mats.taraldsvik@gmail.com>

#    This file is part of veefire.

#    veefire is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    veefire is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with veefire.  If not, see <http://www.gnu.org/licenses/>.

'''
.. moduleauthor:: Mats Taraldsvik <mats.taraldsvik@gmail.com>

Contains classes for the Preferences.

'''

import xml.etree.ElementTree as ET
import os

class Preferences :
    def __init__(self, filename ):
        self.filename = os.path.abspath(filename)
        self.elementTree = None
        self.root = None
    def load(self):
        '''
        Loads the Preferencesfile into the dict.
        
        :param filename: Path to Preferences file.
        :type filename: string
        '''
        ## Root XML Tag
        self.elementTree = ET.parse( self.filename )
        self.root = self.elementTree.getroot()
        
    def getPreference(self, propertyName, keyName='key', valueName='value' ) :
        '''
        Get property value(s).
        
        :param propertyName: Name of property.
        :type propertyName: string
        :param keyName: Key name to get the value from ( single ).
        :type keyName: string or "key"
        :param valueName: Key name to get the values from ( list of values ).
        :type valueName: string or "key"
        :returns: Returns value of the key, or list of values.
        :rtype: string or list
        '''
        Element = self.root.find( propertyName )
        
        if Element.getchildren() == [] :
            return Element.get(keyName)
        else :
            return self.getPreferences( Element, valueName )
        
    def getPreferences(self, Element, valueName ) :
        
        return [ element.get(valueName) for element in Element.getchildren() ]
        
    def setPreference(self, propertyName, value, keyName='key') :
        '''
        Set a property value.
        
        :param propertyName: Name of property.
        :type propertyName: string
        :param value: New value.
        :type value: string
        :param keyName: Key to modify.
        :type keyName: string or "key"
        '''
        Element = self.root.find( propertyName )
        Element.set(keyName, value)
        
    def addPreferencesKey(self, propertyName, value, key='value') :
        '''
        Add a key value to a property with list of values.
        
        :param propertyName: Name of property.
        :type propertyName: string
        :param value: New value.
        :type value: string
        :param key: Key name.
        :type key: string or "value"
        '''
        Element = self.root.find( propertyName )
        for element in Element.getchildren() :
            if element.get(key) == value :
                return None
        ET.SubElement(Element, 'key', { key : value })
        
    def editPreferencesKey(self, propertyName, oldValue, newValue, key='value') :
        '''
        Edit a key value from a property with list of values.
        
        :param propertyName: Name of property.
        :type propertyName: string
        :param oldValue: Current value.
        :type oldValue: string
        :param newValue: New value.
        :type newValue: string
        :param key: Key name.
        :type key: string or "value"
        '''
        Element = self.root.find( propertyName )
        for element in Element.getchildren() :
            if element.get(key) == oldValue :
                element.set(key, newValue)
                return
        
    def removePreferencesKey(self, propertyName, value, key='value') :
        '''
        Remove a key value from a property with list of values.
        
        :param propertyName: Name of property.
        :type propertyName: string
        :param value: Value.
        :type value: string
        :param key: Key name.
        :type key: string or "value"
        '''
        Element = self.root.find( propertyName )
        for element in Element.getchildren() :
            if element.get(key) == value :
                Element.remove(element)
                return
        
    def save(self):
        '''
        Saves the dict to the Preferencesfile.
        '''
        self.elementTree.write( self.filename )
        
