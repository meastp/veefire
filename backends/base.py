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

Contains the base class for constructing backends.
'''

class BaseBackend :
    '''
    Base class for backends. All backends must inherit this.
    '''
    def __init__( self ) :
        pass
        
    def updateShows( self, Shows ) :
        '''
        Update Shows through a Backend.
        
        .. warning::
            This function is abstract. It raises an exception.
        
        :param Shows: Shows to update
        :type Shows: list of api.dbapi.Show objects
        :returns: Database of Show objects
        :rtype: :class:`api.dbapi.Database`
        '''
        
        raise NotImplementedError
