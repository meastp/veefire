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
#    along with Foobar.  If not, see <http://www.gnu.org/licenses/>.

import sys
import os
from api.dbapi import Database

try:
    import pygtk
    pygtk.require("2.0")
except:
    pass
try:
    import gtk
    import gtk.glade
except:
    sys.exit(1)

class VeefireGTK:
    """
    The Veefire Database Editor
    """
    def __init__(self):
        #Set the Glade file
        self.gladefile = "veefire-gtk.glade"
        self.wTree = gtk.glade.XML(self.gladefile)
        
        #Create our dictionay and connect it
        dic = { "on_MainWindow_destroy" : gtk.main_quit,
                "on_mainRevertButton_clicked" : mainRevertButtonClicked,
                "on_mainRenameButton_clicked" : mainRenameButtonClicked,
                "on_mainPropertiesButton_clicked" : mainPropertiesButtonClicked,
                "on_mainAbouttButton_clicked" : mainAboutButtonClicked,
                "on_previewUpdateButton_clicked" : previewUpdateButtonClicked,
                "on_previewFolderButton_clicked" : previewFolderButtonClicked,
                "on_showsEditButton_clicked" : showsEditButtonClicked,
                "on_showsUpdateButtonClicked" : showsUpdateButtonClicked }
        self.wTree.signal_autoconnect(dic)
        
        # Load database
        self.database = Database()
        self.database.loadDB()
        
        #Initialize previewTree
        self.previewStore = gtk.ListStore( str, str )
        
        self.previewView = self.wTree.get_widget("previewTree")
        self.previewView.set_model(self.previewStore)
        
        render=gtk.CellRendererText()
        col=gtk.TreeViewColumn("Current",render,text=0)
        self.previewView.append_column(col)
        render=gtk.CellRendererText()
        col=gtk.TreeViewColumn("New",render,text=1)
        self.previewView.append_column(col)
        
        #Set the selection option so that only one row can be selected
        sel=self.previewView.get_selection()
        sel.set_mode(gtk.SELECTION_SINGLE)
        
        #Show the treeview
        self.previewView.show()
        
        #Initialize showsTree
        self.showsStore = gtk.ListStore( str, str )
        
        for Show in self.database.database :
            self.showsStore.append( [ Show.name , Show.backend ] )
        
        self.showsView = self.wTree.get_widget("showsTree")
        self.showsView.set_model(self.store)
        
        render=gtk.CellRendererText()
        col=gtk.TreeViewColumn("Name",render,text=0)
        self.showsView.append_column(col)
        render=gtk.CellRendererText()
        col=gtk.TreeViewColumn("Backend",render,text=1)
        self.showsView.append_column(col)
        
        #set the selection option so that only one row can be selected
        sel=self.showsView.get_selection()
        sel.set_mode(gtk.SELECTION_SINGLE)
        
        #show the treeview
        self.showsView.show()
        
def mainRevertButtonClicked (self) :
    pass
def mainRenameButtonClicked (self) :
    pass
def mainPropertiesButtonClicked (self) :
    pass
def mainAboutButtonClicked (self) :
    pass
def previewUpdateButtonClicked (self) :
    pass
def previewFolderButtonClicked (self) :
    pass
def showsEditButtonClicked (self) :
    pass
def showsUpdateButtonClicked (self) :
    pass
class PreviewPane :
    def __init__ (self) :
        pass
    def onSelectFolder (self) :
        pass
    def onUpdate (self) :
        pass
class ShowsPane :
    def __init__ (self) :
        pass
    def onEditShows (self) :
        pass
    def onUpdateDb (self) :
        pass
class PropertiesDialog :
    def __init__ (self) :
        pass
    def save (self) :
        pass
class AboutDialog :
    def __init__ (self) :
        pass

if __name__ == "__main__":
        hwg = VeefireGTK()
        gtk.main()
