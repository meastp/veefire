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

class Paths :
    
    def __init__(self, rootDir):
        self.rootDir = rootDir
        
        ## Directories
        self.databaseDir = os.path.join(self.rootDir, 'database')
        self.BackendDirectory = os.path.join(self.rootDir, 'backends')
        
        ## Files
        self.filetypesXML = os.path.join(self.rootDir, 'filetypes.xml')
        self.preferencesXML = os.path.join(self.rootDir, 'preferences.xml')
