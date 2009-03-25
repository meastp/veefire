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

import os
from api.preferencesapi import Preferences
from testproperties import Tools

class testPreferences :
    """
    Test Preferences Class
    """
    def setUp(self) :
        self.Tools = Tools()
        self.Tools.createRootDir()
        self.Tools.createPreferencesXML()
        
        self.preferences = Preferences(self.Tools.preferencesXML)
        
    def tearDown(self):
        self.Tools.removeTempFiles()
        
    def testLoad(self):
        assert self.preferences.filename == self.Tools.preferencesXML
        assert self.preferences.elementTree == None
        assert self.preferences.root == None
        
        self.preferences.load()
        
        assert self.preferences.elementTree.getroot().items() == self.preferences.root.items()
        assert self.preferences.root.find('confirm-on-rename').items() == [('key', 'true')]
        assert [ item.items() for item in self.preferences.root.find('naming-style').getchildren() ] == [[('value', '1')], [('value', '2')]]
        
    def testGetPreference(self):
        self.preferences.load()
        assert self.preferences.getPreference('confirm-on-rename') == 'true'
        assert self.preferences.getPreference('naming-style') == [ '1', '2' ]
        
    def testSetPreference(self):
        self.preferences.load()
        assert self.preferences.getPreference('confirm-on-rename') == 'true'
        self.preferences.setPreference('confirm-on-rename', 'false')
        assert self.preferences.getPreference('confirm-on-rename') == 'false'
        
    def testAddPreferencesKey(self):
        self.preferences.load()
        assert [ item.items() for item in self.preferences.root.find('naming-style').getchildren() ] == [[('value', '1')], [('value', '2')]]
        self.preferences.addPreferencesKey('naming-style', '3')
        assert [ item.items() for item in self.preferences.root.find('naming-style').getchildren() ] == [[('value', '1')], [('value', '2')], [('value', '3')]]
        
    def testEditPreferencesKey(self):
        self.preferences.load()
        assert [ item.items() for item in self.preferences.root.find('naming-style').getchildren() ] == [[('value', '1')], [('value', '2')]]
        self.preferences.editPreferencesKey('naming-style', '2', '3')
        assert [ item.items() for item in self.preferences.root.find('naming-style').getchildren() ] == [[('value', '1')], [('value', '3')]]
        
    def testRemovePreferencesKey(self):
        self.preferences.load()
        assert [ item.items() for item in self.preferences.root.find('naming-style').getchildren() ] == [[('value', '1')], [('value', '2')]]
        self.preferences.removePreferencesKey('naming-style', '2')
        assert [ item.items() for item in self.preferences.root.find('naming-style').getchildren() ] == [[('value', '1')]]
        
    def testSave(self):
        self.preferences.load()
        assert [ item.items() for item in self.preferences.root.find('naming-style').getchildren() ] == [[('value', '1')], [('value', '2')]]
        self.preferences.addPreferencesKey('naming-style', '3')
        assert [ item.items() for item in self.preferences.root.find('naming-style').getchildren() ] == [[('value', '1')], [('value', '2')], [('value', '3')]]
        self.preferences.save()
        
        self.preferences.load()
        assert [ item.items() for item in self.preferences.root.find('naming-style').getchildren() ] == [[('value', '1')], [('value', '2')], [('value', '3')]]
        self.preferences.removePreferencesKey('naming-style', '2')
        assert [ item.items() for item in self.preferences.root.find('naming-style').getchildren() ] == [[('value', '1')], [('value', '3')]]
        self.preferences.save()
        
        self.preferences.load()
        assert [ item.items() for item in self.preferences.root.find('naming-style').getchildren() ] == [[('value', '1')], [('value', '3')]]
