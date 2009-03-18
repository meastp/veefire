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

import sys
import os
import copy
from api.dbapi import Database, Alias, Season
from api.backendapi import Backends, BackendInterface
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

##
#
# Overloads.
#
##

class NewFileName(FileName):
    def setCorrectShow( self, Shows ) :
        '''
        If there is an Episode conflict, resolve it with a dialog.
        '''
        dialog = gtk.Dialog(title='Conflict', parent=None, flags=0, buttons=None)
        dialog.vbox.pack_start(gtk.Label(self.fileName))
        for index, show in enumerate(Shows) :
            dialog.add_button(button_text=show.name, response_id=index )
        dialog.show_all()
        responseid = dialog.run()
        dialog.destroy()
        return Shows[responseid]

class NewFolder(Folder) :
    '''
    Overload the Folder class to use NewFileName.
    '''
    def loadFiles( self ) :
        self.database = Database( self.dbDir , self.shows )
        self.database.loadDB()
        self.fileNames = []
        for afile in os.listdir( self.path ) :
            if os.path.isfile( os.path.join( self.path, afile) ) :
                aFileName = NewFileName( afile, self.database )
                self.fileNames.append( aFileName )

class NewBackendInterface(BackendInterface):
    '''
    If there is an episode conflict, resolve it with a dialog.
    '''
    def solveEpisodeConflicts(self, firstEpisode, secondEpisode):
        dlg = ChooseEpisodeDialog(firstEpisode, secondEpisode)
        result = dlg.run()
        if result == 1 :
            return secondEpisode
        return firstEpisode

class VeefireGTK:
    """
    Veefire GTK Interface
    """
    def __init__(self):
        
        ##
        # Initialize Glade file
        ##
        
        self.gladefile = "veefire-gtk.glade"
        self.wTree = gtk.glade.XML(self.gladefile)
        
        dic = {  "on_MainWindow_destroy" : gtk.main_quit,
                  "on_mainRevertButton_clicked" : self.mainRevertButtonClicked,
                 "on_mainRenameButton_clicked" : self.mainRenameButtonClicked,
                 "on_mainPreferencesButton_clicked" : self.mainPreferencesButtonClicked,
                 "on_mainAboutButton_clicked" : self.mainAboutButtonClicked,
                 "on_previewPreviewButton_clicked" : self.previewPreviewButtonClicked,
                 "on_previewSelectFolderButton_clicked" : self.previewSelectFolderButtonClicked,
                 "on_showsEditShowsButton_clicked" : self.showsEditShowsButtonClicked,
                 "on_showsUpdateButton_clicked" : self.showsUpdateButtonClicked }
        
        self.wTree.signal_autoconnect(dic)
        
        ##
        # Initialize Database and Rename
        ##
        
        self.database = Database(Tools.databaseDir)
        self.database.loadDB()
        
        self.rename = Rename( Tools.databaseDir, Tools.filetypesXML )
        
        ##
        # Main Buttons (Disable those buttons that depends on other functions)
        ##
        
        self.mainRevertButton = self.wTree.get_widget("mainRevertButton")
        self.mainRevertButton.set_sensitive(False)
        
        self.mainRenameButton = self.wTree.get_widget("mainRenameButton")
        self.mainRenameButton.set_sensitive(False)
        
        ##
        # Preview Buttons (Disable those buttons that depends on other functions)
        ##
        
        self.previewPreviewButton = self.wTree.get_widget("previewPreviewButton")
        self.previewPreviewButton.set_sensitive(False)
        
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
        
        self.showsView.show()
        
    def mainRevertButtonClicked (self, widget) :
        pass
        
    def mainRenameButtonClicked (self, widget) :
        self.mainRevertButton.set_sensitive(True)
        
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
            if len(self.previewStore) > 0 : # Keep button disables if there are no entries.
                self.previewPreviewButton.set_sensitive(True)
            else :
                self.previewPreviewButton.set_sensitive(False)
                self.mainRenameButton.set_sensitive(False)
                self.mainRevertButton.set_sensitive(False)
        
    def previewPreviewButtonClicked (self, widget) :
        #FIXME: Style and filesystem
        self.previewStore.clear()
        for folder in self.rename.generatePreviews('ext3') :
            for files in folder :
                if files[1] != None :
                    self.previewStore.append( files )
        self.mainRenameButton.set_sensitive(True)
        
    def showsEditShowsButtonClicked (self, widget) :
        model, row = self.showsView.get_selection().get_selected()
        show = model.get_value( row, 2 ) # 2 is our object column.
        
        showDialog = EditShowDialog(show, self.database)
        result = showDialog.run()
        
        self.showsStore.clear()
        self.database.loadDB()
        for Show in self.database.database :
            self.showsStore.append([ Show.name, Show.backend, Show ])
        
    def showsUpdateButtonClicked (self, widget) :
        self.database.writeDB()
        se = NewBackendInterface(Tools.databaseDir)
        se.updateDatabase()
        self.database.loadDB()
        
class PreferencesDialog :
    '''
    Preferences.
    '''
    #TODO: Implement.
    def __init__(self) :
        self.gladefile = "veefire-gtk.glade"
        
        ##
        # Initialize dialog from Glade file.
        ##
        
        self.wTree = gtk.glade.XML( self.gladefile , "preferencesDialog" )
        self.dlg = self.wTree.get_widget("preferencesDialog")
    def run(self):
        self.result = self.dlg.run()
        self.dlg.destroy()
        return self.result
        
class AboutDialog :
    '''
    Information about veefire.
    '''
    def __init__(self) :
        self.gladefile = "veefire-gtk.glade"
        
        ##
        # Initialize dialog from Glade file.
        ##
        
        self.wTree = gtk.glade.XML( self.gladefile , "aboutDialog" )
        self.dlg = self.wTree.get_widget("aboutDialog")
        
    def run(self):  
        self.result = self.dlg.run()
        self.dlg.destroy()
        return self.result
        
class ChooseEpisodeDialog :
    '''
    The dialog for episode conflict in the updateDatabase-function.
    '''
    def __init__(self, firstEpisode, secondEpisode) :
        self.gladefile = "veefire-gtk.glade"
        self.dbEp = firstEpisode
        self.upEp = secondEpisode
        
        ##
        # Initialize dialog from Glade file.
        ##
        
        self.wTree = gtk.glade.XML( self.gladefile , "chooseEpisodeDialog" )
        self.dlg = self.wTree.get_widget("chooseEpisodeDialog")
        
    def run(self):  
        
        ##
        # Set dbEpisode
        ##
        
        self.dbTitle = self.wTree.get_widget("dbTitle")
        self.dbTitle.set_label('<i>' + self.dbEp.title + '</i>')
        
        self.dbEpisode = self.wTree.get_widget("dbEpisode")
        self.dbEpisode.set_label('Episode ' + self.dbEp.name)
        
        self.dbArc = self.wTree.get_widget("dbArc")
        self.dbArc.set_label('( <b>Arc:</b> <i>' + self.dbEp.arc + '</i> )')
        
        self.dbAirdate = self.wTree.get_widget("dbAirdate")
        self.dbAirdate.set_label('( <b>Aired:</b> <i>' + self.dbEp.airdate + '</i> )')
        
        ##
        # Set upEpisode
        ##
        
        self.upTitle = self.wTree.get_widget("upTitle")
        self.upTitle.set_label('<i>' + self.upEp.title + '</i>')
        
        self.upEpisode = self.wTree.get_widget("upEpisode")
        self.upEpisode.set_label('Episode ' + self.upEp.name)
        
        self.upArc = self.wTree.get_widget("upArc")
        self.upArc.set_label('( <b>Arc:</b> <i>' + self.upEp.arc + '</i> )')
        
        self.upAirdate = self.wTree.get_widget("upAirdate")
        self.upAirdate.set_label('( <b>Aired:</b> <i>' + self.upEp.airdate + '</i> )')
        
        
        self.result = self.dlg.run()
        self.dlg.destroy()
        
        return self.result
        
class EditShowDialog :
    '''
    Database/Show editor.
    '''
    def __init__(self, Show, database) :
        
        ##
        # Initialize dialog from Glade file.
        ##
        
        self.gladefile = "veefire-gtk.glade"
        self.wTree = gtk.glade.XML( self.gladefile , "editShowDialog" )
        self.dlg = self.wTree.get_widget("editShowDialog")
        
        ##
        # Global variables, load values
        ##
        
        self.database = database
        self.Show = Show
        
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
        '''
        Right-click menu for Episodes.
        '''
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
        '''
        Right-click menu for Aliases.
        '''
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
        
        exists = False
        alias = Alias(text)
        #result = self.Show.addAlias( alias )
        for row in self.editShowAliasesStore :
            print row[0]
            print alias.name
            if row[0] == alias.name :
                exists = True
        
        print exists
        if exists == False :
            self.editShowAliasesStore.append( [ alias.name, alias ] )
        
    def showAliasesMenuRemove( self, widget ):
        model, row = self.editShowAliasesView.get_selection().get_selected()
        self.editShowAliasesStore.remove(row)
        
    def run(self):  
        result = self.dlg.run()
        
        name = self.name.get_text()
        url = self.url.get_text()
        backend = self.liststore[self.backend.get_active()][0]
        duration = str(self.duration.get_value())
        
        self.dlg.destroy()
        
        GTK_RESPONSE_SAVE = 0
        GTK_RESPONSE_REVERT = -1
        
        if result == GTK_RESPONSE_SAVE :
            
            self.Show.name = name
            self.Show.url = url
            self.Show.duration = duration
            self.Show.backend = backend
            
            self.Show.alias = [ ]
            for row in self.editShowAliasesStore :
                self.Show.addAlias( row[1] )
            
            self.Show.seasons = [ ]
            for row in self.editShowEpisodesStore :
                self.Show.addEpisode( copy.deepcopy(row[4]), Season(row[3].name) )
            
            self.database.write()
        
        return result

if __name__ == "__main__":
        hwg = VeefireGTK()
        gtk.main()
        Tools.removeTempFiles()
