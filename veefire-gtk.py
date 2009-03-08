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
from api.dbapi import Database, Alias
from api.backendapi import Backends
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

# FIXME: Temporary overloads.

class NewFileName(FileName):
    def setCorrectShow( self, Shows ) :
        return Shows[0]

class NewFolder(Folder) :
    def loadFiles( self ) :
        self.database = Database( self.dbDir , self.shows )
        self.database.loadDB()
        self.fileNames = []
        for afile in os.listdir( self.path ) :
            if os.path.isfile( os.path.join( self.path, afile) ) :
                aFileName = NewFileName( afile, self.database )
                self.fileNames.append( aFileName )

#class NewBackendInterface(BackendInterface):
#    def solveEpisodeConflicts(self, firstEpisode, secondEpisode):
#        return firstEpisode

# FIXME: Above.

##
#
# Tools class for testing.
#
##
from tests.testproperties import Tools

Tools = Tools()
Tools.createRootDir()
Tools.createDatabaseFiles()
Tools.createFilesystemXML()
Tools.createTempFiles()
Tools.createBackendFiles()

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
                "on_previewPreviewButton_clicked" : self.previewPreviewButtonClicked,
                "on_previewSelectFolderButton_clicked" : self.previewSelectFolderButtonClicked,
                "on_showsEditShowsButton_clicked" : self.showsEditShowsButtonClicked,
                "on_showsUpdateButton_clicked" : self.showsUpdateButtonClicked }
        self.wTree.signal_autoconnect(dic)
        
        
        self.database = Database(Tools.databaseDir)
        self.database.loadDB()
        
        ##
        #
        # Initialize previewTree
        #
        ##
        
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
        
        ##
        #
        # Initialize showsTree
        #
        ##
        
        self.showsStore = gtk.ListStore( str, str, object )
        
        self.showsStore.clear()
        self.database = Database(Tools.databaseDir)
        self.database.loadDB()
        for Show in self.database.database :
            self.showsStore.append([ Show.name, Show.backend, Show ])
        
        self.showsView = self.wTree.get_widget("showsTree")
        self.showsView.set_model(self.showsStore)
        
        render=gtk.CellRendererText()
        col=gtk.TreeViewColumn("Name",render,text=0)
        self.showsView.append_column(col)
        render=gtk.CellRendererText()
        col=gtk.TreeViewColumn("Backend",render,text=1)
        self.showsView.append_column(col)
        col=gtk.TreeViewColumn()
        col.set_visible(False)
        self.showsView.append_column(col)
        
        #set the selection option so that only one row can be selected
        sel=self.showsView.get_selection()
        sel.set_mode(gtk.SELECTION_SINGLE)
        
        #show the treeview
        self.showsView.show()
        
        ##
        # Rename
        ##
        
        self.rename = Rename( Tools.databaseDir, Tools.filetypesXML )
        
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
    def previewSelectFolderButtonClicked (self, widget) :
        '''
        Adds the selected folders to the previewView, and generates previews.
        '''
        
        selectfolder = gtk.FileChooserDialog(title=None, 
                                            parent=None, 
                                            action=gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER, 
                                            buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
                                            gtk.STOCK_OK, gtk.RESPONSE_ACCEPT), 
                                            backend=None)
        
        selectfolder.set_select_multiple(True)
        result = selectfolder.run()
        folderlist = selectfolder.get_filenames()
        selectfolder.destroy()
        
        if result == gtk.RESPONSE_ACCEPT :
            self.previewStore.clear()
            self.rename = Rename( Tools.databaseDir, Tools.filetypesXML )
            for folder in folderlist :
                self.rename.addFoldersRecursively( NewFolder(folder) )
            self.rename.getMatchingShows()
            for folder in self.rename.folders :
                for files in folder.fileNames :
                    if files.CorrectShow != None :
                        self.previewStore.append( [ files.fileName, files.CorrectShow.name ] )
        
    def previewPreviewButtonClicked (self, widget) :
        #FIXME: Style and filesystem
        self.previewStore.clear()
        for folder in self.rename.generatePreviews('ext3') :
            for files in folder :
                if files[1] != None :
                    self.previewStore.append( files )
        
    def showsEditShowsButtonClicked (self, widget) :
        model, row = self.showsView.get_selection().get_selected()
        show = model.get_value( row, 2 ) # 2 is our object column.
        
        showDialog = EditShowDialog(show, self.database)
        result = showDialog.run()
        
        if result == gtk.RESPONSE_ACCEPT :
            pass
        
    def showsUpdateButtonClicked (self, widget) :
        pass
class PreviewPane :
    def __init__ (self) :
        self.gladefile = "veefire-gtk.glade"
    def onSelectFolder (self) :
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
class EditShowDialog :
    def __init__(self, Show, database) :
        
        self.database = database
        self.Show = Show
        
        self.gladefile = "veefire-gtk.glade"
        self.wTree = gtk.glade.XML( self.gladefile , "editShowDialog" )
        self.dlg = self.wTree.get_widget("editShowDialog")
        
        self.name = self.wTree.get_widget("editShowGeneralName")
        self.name.set_text(Show.name)
        self.url = self.wTree.get_widget("editShowGeneralURL")
        self.url.set_text(Show.url)
        
        self.backend = self.wTree.get_widget("editShowGeneralBackend")
        self.liststore = gtk.ListStore(str)
        self.backend.set_model(self.liststore)
        
        cellrenderer = gtk.CellRendererText()
        self.backend.pack_start(cellrenderer)
        self.backend.add_attribute(cellrenderer, 'text', 0)
        
        for backend in Backends().getBackends(Tools.BackendDirectory) :
            if backend == Show.backend :
                self.liststore.prepend([ backend ])
            else :
                self.liststore.append([ backend ])
        self.backend.set_active(0)
        
        self.duration = self.wTree.get_widget("editShowGeneralDuration")
        self.duration.set_value(float(Show.duration))
        
        ##
        # editShowAliases
        ##
        
        self.editShowAliasesStore = gtk.ListStore( str, object )
        
        self.editShowAliasesView = self.wTree.get_widget("editShowAliasesView")
        self.editShowAliasesView.set_model(self.editShowAliasesStore)
        
        render=gtk.CellRendererText()
        col=gtk.TreeViewColumn("Alias",render,text=0)
        self.editShowAliasesView.append_column(col)
        col=gtk.TreeViewColumn()
        col.set_visible(False)
        self.editShowAliasesView.append_column(col)
        col=gtk.TreeViewColumn()
        col.set_visible(False)
        self.editShowAliasesView.append_column(col)
        
        #Set the selection option so that only one row can be selected
        sel=self.editShowAliasesView.get_selection()
        sel.set_mode(gtk.SELECTION_SINGLE)
        
        #Show the treeview
        self.editShowAliasesView.show()
        self.editShowAliasesStore.clear()
        for Alias in Show.alias :
            self.editShowAliasesStore.append([ Alias.name , Alias ])
        
        ##
        # editShowEpisodes
        ##
        
        self.editShowEpisodesStore = gtk.ListStore( str, str, str, object, object )
        
        self.editShowEpisodesView = self.wTree.get_widget("editShowEpisodesView")
        self.editShowEpisodesView.set_model(self.editShowEpisodesStore)
        
        render=gtk.CellRendererText()
        col=gtk.TreeViewColumn("Season",render,text=0)
        self.editShowEpisodesView.append_column(col)
        render=gtk.CellRendererText()
        col=gtk.TreeViewColumn("Episode",render,text=1)
        self.editShowEpisodesView.append_column(col)
        render=gtk.CellRendererText()
        col=gtk.TreeViewColumn("Title",render,text=2)
        self.editShowEpisodesView.append_column(col)
        col=gtk.TreeViewColumn()
        col.set_visible(False)
        self.editShowEpisodesView.append_column(col)
        col=gtk.TreeViewColumn()
        col.set_visible(False)
        self.editShowEpisodesView.append_column(col)
        
        #Set the selection option so that only one row can be selected
        sel=self.editShowEpisodesView.get_selection()
        sel.set_mode(gtk.SELECTION_SINGLE)
        
        #Show the treeview
        self.editShowEpisodesView.show()
        self.editShowEpisodesStore.clear()
        for Season in Show.seasons :
            for Episode in Season.episodes :
                self.editShowEpisodesStore.append( [ Season.name, Episode.name, Episode.title, Season, Episode ])
        
        #Enable the selection callback
        self.wTree = gtk.glade.XML( self.gladefile , "editShowEpisodesMenu" )
        self.editShowEpisodesMenu = self.wTree.get_widget("editShowEpisodesMenu")
        self.editShowEpisodesMenuAdd = self.wTree.get_widget("editShowEpisodesMenuAdd")
        self.editShowEpisodesMenuRemove = self.wTree.get_widget("editShowEpisodesMenuRemove")
        
        self.editShowEpisodesView.connect('button_press_event', self.showEpisodesMenu )
        
        self.editShowEpisodesMenuAdd.connect('activate', self.showEpisodesMenuAdd )
        self.editShowEpisodesMenuRemove.connect('activate', self.showEpisodesMenuRemove )
        
        #Enable the selection callback
        self.wTree = gtk.glade.XML( self.gladefile , "editShowAliasesMenu" )
        self.editShowAliasesMenu = self.wTree.get_widget("editShowAliasesMenu")
        self.editShowAliasesMenuAdd = self.wTree.get_widget("editShowAliasesMenuAdd")
        self.editShowAliasesMenuRemove = self.wTree.get_widget("editShowAliasesMenuRemove")
        
        self.editShowAliasesView.connect('button_press_event', self.showAliasesMenu )
        
        self.editShowAliasesMenuAdd.connect('activate', self.showAliasesMenuAdd )
        self.editShowAliasesMenuRemove.connect('activate', self.showAliasesMenuRemove )
        
    def showEpisodesMenu(self, treeview, event):
        if event.button == 3:
            x = int(event.x)
            y = int(event.y)
            time = event.time
            pthinfo = treeview.get_path_at_pos(x, y)
            if pthinfo is not None:
                path, col, cellx, celly = pthinfo
                treeview.grab_focus()
                treeview.set_cursor( path, col, 0)
                self.editShowEpisodesMenu.popup( None, None, None, event.button, time)
            return 1
        
    def showEpisodesMenuAdd( self, widget ):
        pass
        
    def showEpisodesMenuRemove( self, widget ):
        model, row = self.editShowEpisodesView.get_selection().get_selected()
        self.editShowEpisodesStore.remove(row)
        
    def showAliasesMenu(self, treeview, event):
        if event.button == 3:
            x = int(event.x)
            y = int(event.y)
            time = event.time
            pthinfo = treeview.get_path_at_pos(x, y)
            if pthinfo is not None:
                path, col, cellx, celly = pthinfo
                treeview.grab_focus()
                treeview.set_cursor( path, col, 0)
                self.editShowAliasesMenu.popup( None, None, None, event.button, time)
            return 1
        
    def showAliasesMenuAdd( self, widget ):
        #base this on a message dialog  
        dialog = gtk.MessageDialog( None,
                                    gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,  
                                    gtk.MESSAGE_QUESTION,  
                                    gtk.BUTTONS_OK,  
                                    None)
        #dialog.set_markup('Please enter the alias:')  
        #create the text input field  
        entry = gtk.Entry()  
        #allow the user to press enter to do ok  
        #entry.connect("activate", responseToDialog, dialog, gtk.RESPONSE_OK)  
        #create a horizontal box to pack the entry and a label  
        hbox = gtk.HBox()  
        hbox.pack_start(gtk.Label("New Alias :"), False, 5, 5)  
        hbox.pack_end(entry)  
        #some secondary text  
        #dialog.format_secondary_markup("This will be used for <i>identification</i> purposes")  
        #add it and show it  
        dialog.vbox.pack_end(hbox, True, True, 0)  
        dialog.show_all()  
        #go go go  
        dialog.run()  
        text = entry.get_text()  
        dialog.destroy()  
        
        alias = Alias(text)
        result = self.Show.addAlias( alias )
        print result
        if result != None :
            self.editShowAliasesStore.append( [ alias.name, alias ] )
        
    def showAliasesMenuRemove( self, widget ):
        model, row = self.editShowAliasesView.get_selection().get_selected()
        self.editShowAliasesStore.remove(row)
        
    def run(self):  
        self.result = self.dlg.run()
        self.dlg.destroy()
        return self.result

if __name__ == "__main__":
        hwg = VeefireGTK()
        gtk.main()
        Tools.removeTempFiles()
