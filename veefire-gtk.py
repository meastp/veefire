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
from api.renameapi import Rename, Folder, FileName

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
    Veefire GTK Interface
    """
    def __init__(self):
        #Set the Glade file
        self.gladefile = "veefire-gtk.glade"
        self.wTree = gtk.glade.XML(self.gladefile)
        
        #Create our dictionay and connect it
        dic = { "on_MainWindow_destroy" : gtk.main_quit,
                "on_mainRevertButton_clicked" : self.mainRevertButtonClicked,
                "on_mainRenameButton_clicked" : self.mainRenameButtonClicked,
                "on_mainPreferencesButton_clicked" : self.mainPreferencesButtonClicked,
                "on_mainAboutButton_clicked" : self.mainAboutButtonClicked,
                "on_previewUpdateButton_clicked" : self.previewUpdateButtonClicked,
                "on_previewSelectFolderButton_clicked" : self.previewSelectFolderButtonClicked,
                "on_showsEditButton_clicked" : self.showsEditShowsButtonClicked,
                "on_showsUpdateButtonClicked" : self.showsUpdateButtonClicked }
        self.wTree.signal_autoconnect(dic)
        
        ##
        #
        # Tools class for testing.
        #
        ##
        from tests.testproperties import Tools
        
        self.Tools = Tools()
        self.Tools.createRootDir()
        self.Tools.createDatabaseFiles()
        
        self.database = Database(self.Tools.databaseDir)
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
        self.showsView.set_model(self.showsStore)
        
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
        
    def mainRevertButtonClicked (self, widget) :
        pass
    def mainRenameButtonClicked (self, widget) :
        pass
    def mainPreferencesButtonClicked (self, widget) :
        preferencesDlg = PreferencesDialog()
        preferencesDlg.run()
    def mainAboutButtonClicked (self, widget) :
        aboutDlg = AboutDialog()
        aboutDlg.run()
    def previewUpdateButtonClicked (self, widget) :
        pass
    def previewSelectFolderButtonClicked (self, widget) :
        pane = PreviewPane()
        response, folderlist = pane.onSelectFolder()
        if response == gtk.RESPONSE_ACCEPT :
            print folderlist
            self.previewStore.clear()
            rename = Rename( self.Tools.databaseDir, self.Tools.filetypesXML )
            for folder in folderlist :
                rename.addFoldersRecursively( Folder(folder) )
            for folder in rename.folders :
                self.previewStore.append( [ folder.path, 'None' ] )
    def showsEditShowsButtonClicked (self, widget) :
        pass
    def showsUpdateButtonClicked (self, widget) :
        pass
class PreviewPane :
    def __init__ (self) :
        self.gladefile = "veefire-gtk.glade"
    def onSelectFolder (self) :
        selectfolder = gtk.FileChooserDialog(title=None, 
                                            parent=None, 
                                            action=gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER, 
                                            buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
                                            gtk.STOCK_OK, gtk.RESPONSE_ACCEPT), 
                                            backend=None)
        
        selectfolder.set_select_multiple(True)
        result = selectfolder.run()
        selected = selectfolder.get_filenames()
        selectfolder.destroy()
        return result, selected
    def onUpdate (self) :
        pass
class ShowsPane :
    def __init__ (self) :
        pass
    def onEditShows (self) :
        pass
    def onUpdateDb (self) :
        pass
class PreferencesDialog :
    def __init__(self) :
        self.gladefile = "veefire-gtk.glade"
    def run(self):  
        self.wTree = gtk.glade.XML( self.gladefile , "preferencesDialog" )
        self.dlg = self.wTree.get_widget("preferencesDialog")
        self.result = self.dlg.run()
        self.dlg.destroy()
        return self.result
class AboutDialog :
    def __init__(self) :
        self.gladefile = "veefire-gtk.glade"
    def run(self):  
        self.wTree = gtk.glade.XML( self.gladefile , "aboutDialog" )
        self.dlg = self.wTree.get_widget("aboutDialog")
        self.result = self.dlg.run()
        self.dlg.destroy()
        return self.result

if __name__ == "__main__":
        hwg = VeefireGTK()
        gtk.main()
        #self.Tools.removeTempFiles()
