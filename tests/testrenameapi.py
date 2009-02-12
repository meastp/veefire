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

import nose

from api.dbapi import Database
from api.renameapi import FileName

class testDatabase :
    """
    Test FileName Class
    """
    def setUp(self) :
        # Only make fakefiles where nothing else is possible.
        self.database = Database()
        self.filename1 = FileName( 'blackbooks.s01e02.avi', self.database )
        self.filename2 = FileName( 'blackbooks.1x03.avi', self.database )
        self.filename3 = FileName( 'blackbooks.s01E03.avi', self.database )
        
    def testGetMatchingShows(self) :
        # Depends on files
        assert False
    
    def testGeneratePreview(self) :
        # Depends on files
        assert False
