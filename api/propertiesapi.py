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

Contains classes for the properties.

'''

import xml.etree.ElementTree as ET
import os

class Properties :
    def __init__(self, filename ):
        self.filename = filename
        self.properties = dict()
    def load(self):
        '''
        Loads the propertiesfile into the dict.
        
        :param filename: Path to properties file.
        :type filename: string
        '''
            pfile = os.path.abspath( self.filename )
            
            ## Root XML Tag
            root = ET.parse( pfile ).getroot()
            
    def save(self):
        '''
        Saves the dict to the propertiesfile.
        '''
        pass
