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
        '''
        Initialize.
        
        :param filename: path to preferences file
        :type filename: string
        '''
        self.filename = os.path.abspath(filename)
        self.elementTree = None
        
    def load(self):
        '''
        Loads the Preferencesfile into the dict.
        
        :param filename: Path to Preferences file.
        :type filename: string
        '''
        self.elementTree = ET.parse( self.filename )
        
        self.Preferences = self.elementTree.getroot().find('preferences')
        self.Options = self.elementTree.getroot().find('options')
        
    def __getitem__(self, key) :
        '''
        Get property value.
        
        :param key: Name of property.
        :type key: string
        :rtype: string or None
        '''
        Element = self.Preferences.find( key )
        
        return Element.get('value')
        
    def __setitem__(self, key, value) :
        '''
        Set property value.
        
        :param key: Name of property.
        :type key: string
        :param value: Value of option.
        :type value: string
        :rtype: string or None
        '''
        Element = self.Preferences.find( key )
        OptionElement = self.Options.find( key )
        
        if OptionElement == None :
            Element.set('value', str(value))
            return value
        elif OptionElement != None and OptionElement.getchildren() != [] :
            Element.set('value', str(value))
            return value
        else :
            return None
        
    def getOptions(self, key ) :
        '''
        Get option value(s).
        
        :param key: Name of property/option.
        :type key: string
        :rtype: list or None
        '''
        Element = self.Options.find(key)
        
        return [ element.get('value') for element in Element.getchildren() ]
        
    def addOption(self, key, value ) :
        '''
        Add option value.
        
        :param key: Name of property/option.
        :type key: string
        :param value: Value of option.
        :type value: string
        :rtype: list or None
        '''
        Element = self.Options.find(key)
        
        if self.Preferences.find(key) == None :
            return None
        
        if value not in [ value for key, value in Element.items() ] :
            ET.SubElement(Element, 'option', { 'value' : str(value) })
            return self.getOptions(key)
        
    def removeOption(self, key, value) :
        '''
        Remove option value.
        
        :param key: Name of property/option.
        :type key: string
        :param value: Value of option.
        :type value: string
        :rtype: list or None
        '''
        Element = self.Options.find(key)
        
        for element in Element.getchildren() :
            if element.get('value') == value :
                Element.remove(element)
                return self.getOptions(key)
        
    def save(self):
        '''
        Saves the dict to the Preferencesfile.
        '''
        self.elementTree.write( self.filename )
