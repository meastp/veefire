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
        
        self.preferences.load()
        
        assert self.preferences.elementTree != None
        assert self.preferences.Options != None
        assert self.preferences.Preferences != None
        
    def testGetPreference(self):
        self.preferences.load()
        assert self.preferences['confirm-on-rename'] == 'true'
        assert self.preferences['naming-style'] == '2'
        
    def testSetPreference(self):
        self.preferences.load()
        assert self.preferences['confirm-on-rename'] == 'true'
        assert self.preferences['naming-style'] == '2'
        
        self.preferences['confirm-on-rename'] = 'false'
        self.preferences['naming-style'] = '1'
        
        assert self.preferences['confirm-on-rename'] == 'false'
        assert self.preferences['naming-style'] == '1'
        
    def testGetOption(self):
        self.preferences.load()
        assert self.preferences.getOptions('naming-style') == ['1', '2']
        
    def testAddOption(self):
        self.preferences.load()
        assert self.preferences.addOption('naming-style', '3') == ['1', '2', '3']
        
    def testRemoveOption(self):
        self.preferences.load()
        assert self.preferences.removeOption('naming-style', '2') == ['1']
        
    def testSave(self):
        self.preferences.load()
        self.preferences['confirm-on-rename'] = 'false'
        self.preferences['naming-style'] = '1'
        self.preferences.addOption('naming-style', '3')
        self.preferences.removeOption('naming-style', '2')
        self.preferences.save()
        self.preferences.load()
        assert self.preferences.getOptions('naming-style') == ['1', '3']
        assert self.preferences['confirm-on-rename'] == 'false'
        assert self.preferences['naming-style'] == '1'
        self.preferences2 = Preferences(self.Tools.preferencesXML)
        self.preferences2.load()
        assert self.preferences2.getOptions('naming-style') == ['1', '3']
        assert self.preferences2['confirm-on-rename'] == 'false'
        assert self.preferences2['naming-style'] == '1'
