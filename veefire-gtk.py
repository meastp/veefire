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

from api.dbapi import Database, Alias, Season, Show, Episode, Season
from api.backendapi import Backends, BackendInterface
from api.renameapi import Rename, Folder, FileName, Filesystems
from api.preferencesapi import Preferences

from tests.testimdbtv import testBackend
from backends.imdbtv import Backend

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

#When this is removed, the paths used in the program must also be modified.

from tests.testproperties import Tools

Tools = Tools()
Tools.createRootDir()
Tools.createDatabaseFiles()
Tools.createFilesystemXML()
Tools.createTempFiles()
Tools.createBackendFiles()
Tools.createPreferencesXML()

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
        print firstEpisode.name, firstEpisode.title, firstEpisode.airdate, firstEpisode.arc
        print secondEpisode.name, secondEpisode.title, secondEpisode.airdate, secondEpisode.arc
        dlg = ChooseEpisodeDialog(firstEpisode, secondEpisode)
        result = dlg.run()
        if result == 1 :
            return secondEpisode
        return firstEpisode

class imdbtvtest(testBackend) :
    """
    Test imdbtvbackend
    """
    def setUp(self) :
        self.backend = Backend()
        
        validShows1 = [ Show(  "Spaced", "60", "imdbtvbackend", "tt0187664" ) ]
        self.database1 = Database(Tools.databaseDir, validShows1)
        self.database1.loadDB()
        
        validShows2 = [ Show(  "Black Books", "30", "imdbtvbackend", "tt0262150" ) ]
        self.database2 = Database(Tools.databaseDir, validShows2)
        self.database2.loadDB()
        
    def tearDown(self):
        pass

##
#
# VeefireGTK.
#
##

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
                 "on_showsNewShowButton_clicked" : self.showsNewShowButtonClicked,
                 "on_showsDeleteShowButton_clicked" : self.showsDeleteShowButtonClicked,
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
        
        self.previewStore = gtk.ListStore( str, str, str, str, object )
        
        self.previewView = self.wTree.get_widget("previewTree")
        self.previewView.set_model(self.previewStore)
        
        render=gtk.CellRendererText()
        col=gtk.TreeViewColumn("Original Name",render,text=0)
        col.set_resizable(True)
        self.previewView.append_column(col)
        
        render=gtk.CellRendererText()
        col=gtk.TreeViewColumn("Current Name",render,text=1)
        col.set_resizable(True)
        col.set_visible(False)
        self.previewView.append_column(col)
        
        render=gtk.CellRendererText()
        col=gtk.TreeViewColumn("Show",render,text=2)
        col.set_resizable(True)
        col.set_visible(False)
        self.previewView.append_column(col)
        
        render=gtk.CellRendererText()
        col=gtk.TreeViewColumn("Preview",render,text=3)
        col.set_resizable(True)
        col.set_visible(False)
        self.previewView.append_column(col)
        
        col=gtk.TreeViewColumn()
        col.set_visible(False)
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
        preferences = Preferences(Tools.preferencesXML)
        preferences.load()
        
        if self.to_boolean(preferences['update-on-startup']) == True :
            #update warning
            dialog = gtk.MessageDialog( None,
                                        gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,  
                                        gtk.MESSAGE_QUESTION,  
                                        gtk.BUTTONS_OK,  
                                        None)
            hbox = gtk.HBox()  
            hbox.pack_start(gtk.Label("The Database will be updated."), False, 5, 5)  
            dialog.vbox.pack_end(hbox, True, True, 0)
            dialog.show_all()
            
            dialog.run()  
            dialog.destroy()
              
            
            if self.to_boolean(preferences['imdbtv-with-tests']) == True :
                testimdbtv = imdbtvtest()
                testimdbtv.setUp()
                testimdbtv.testDownloadShowList()
                testimdbtv.testGetShowDetails()
                testimdbtv.tearDown()
            
            se = NewBackendInterface(Tools.databaseDir)
            se.updateDatabase()
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
       
        
    def to_boolean(self, string ) :
        if string == "True" or string == "true" or string == True or string == 1 :
            return True
        else :
            return False
        
    def mainRevertButtonClicked (self, widget) :
        self.rename.revert()
        row = self.previewStore.get_iter_first()
        while( row != None ) :
            
            fileName = self.previewStore.get_value(row, 0)
            currentFileName = self.previewStore.get_value(row, 1)
            correctShowName = self.previewStore.get_value(row, 2)
            generatedFileName = self.previewStore.get_value(row, 3)
            FileName = self.previewStore.get_value(row, 4)
            
            self.previewStore.set_value(row, 0, FileName.fileName)
            self.previewStore.set_value(row, 1, FileName.currentFileName)
            self.previewStore.set_value(row, 2, FileName.CorrectShow.name)
            self.previewStore.set_value(row, 3, FileName.generatedFileName)
            
            row = self.previewStore.iter_next(row)
        
        self.previewView.columns_autosize()
        
        self.mainRevertButton.set_sensitive(False)
        self.mainRenameButton.set_sensitive(True)
        
    def mainRenameButtonClicked (self, widget) :
        preferences = Preferences(Tools.preferencesXML)
        preferences.load()
        if self.to_boolean(preferences['confirm-on-rename']) == True :
            #base this on a message dialog  
            dialog = gtk.MessageDialog( None,
                                        gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,  
                                        gtk.MESSAGE_QUESTION,  
                                        gtk.BUTTONS_OK_CANCEL,  
                                        None)
            hbox = gtk.HBox()  
            hbox.pack_start(gtk.Label("Do You Really Want To Rename?"), False, 5, 5)  
            dialog.vbox.pack_end(hbox, True, True, 0)  
            dialog.show_all()  
            result = dialog.run()
            dialog.destroy()
            
            if result == gtk.RESPONSE_CANCEL :
                return
            
        self.rename.rename()
        
        row = self.previewStore.get_iter_first()
        while( row != None ) :
            
            fileName = self.previewStore.get_value(row, 0)
            currentFileName = self.previewStore.get_value(row, 1)
            correctShowName = self.previewStore.get_value(row, 2)
            generatedFileName = self.previewStore.get_value(row, 3)
            FileName = self.previewStore.get_value(row, 4)
            
            self.previewStore.set_value(row, 0, FileName.fileName)
            self.previewStore.set_value(row, 1, FileName.currentFileName)
            self.previewStore.set_value(row, 2, FileName.CorrectShow.name)
            self.previewStore.set_value(row, 3, FileName.generatedFileName)
            
            row = self.previewStore.iter_next(row)
        
        currentNameColumn = self.previewView.get_column(1)
        currentNameColumn.set_visible(True)
        
        self.previewView.columns_autosize()
        
        self.mainRenameButton.set_sensitive(False)
        self.mainRevertButton.set_sensitive(True)
        
    def mainPreferencesButtonClicked (self, widget) :
        preferencesDlg = PreferencesDialog()
        result, preferences = preferencesDlg.run()
        
        GTK_RESPONSE_SAVE = 0
        GTK_RESPONSE_REVERT = -1
        if result == GTK_RESPONSE_SAVE :
            preferences.save()
        
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
                        self.previewStore.append( [ files.fileName, files.currentFileName, files.CorrectShow.name, files.generatedFileName, files ] )
            
            showNameColumn = self.previewView.get_column(2)
            showNameColumn.set_visible(True)
            
            self.previewView.columns_autosize()
            
            if len(self.previewStore) > 0 : 
                self.previewPreviewButton.set_sensitive(True)
            else : # Keep button disables if there are no entries.
                self.previewPreviewButton.set_sensitive(False)
                self.mainRenameButton.set_sensitive(False)
                self.mainRevertButton.set_sensitive(False)
        
    def previewPreviewButtonClicked (self, widget) :
        preferences = Preferences(Tools.preferencesXML)
        preferences.load()
        self.rename.generatePreviews(preferences['filesystem'], preferences['naming-style'])
        
        row = self.previewStore.get_iter_first()
        while( row != None ) :
            
            fileName = self.previewStore.get_value(row, 0)
            currentFileName = self.previewStore.get_value(row, 1)
            correctShowName = self.previewStore.get_value(row, 2)
            generatedFileName = self.previewStore.get_value(row, 3)
            FileName = self.previewStore.get_value(row, 4)
            
            self.previewStore.set_value(row, 0, FileName.fileName)
            self.previewStore.set_value(row, 1, FileName.currentFileName)
            self.previewStore.set_value(row, 2, FileName.CorrectShow.name)
            self.previewStore.set_value(row, 3, FileName.generatedFileName)
            
            row = self.previewStore.iter_next(row)
        
        showNameColumn = self.previewView.get_column(2)
        showNameColumn.set_visible(False)
        previewNameColumn = self.previewView.get_column(3)
        previewNameColumn.set_visible(True)
        
        self.previewView.columns_autosize()
        
        self.mainRenameButton.set_sensitive(True)
        
    def showsEditShowsButtonClicked (self, widget) :
        
        model, row = self.showsView.get_selection().get_selected()
        show = model.get_value( row, 2 ) # 2 is our object column.
        
        showDialog = EditShowDialog(show, self.database)
        result = showDialog.run()
        
        #Fix treeview. Should manipulate, if necessary.
        #self.showsStore.clear()
        #self.database.loadDB()
        #for Show in self.database.database :
        #    self.showsStore.append([ Show.name, Show.backend, Show ])
        
    def showsNewShowButtonClicked (self, widget) :
        
        show = Show('', '30', '', '')
        
        showDialog = EditShowDialog(show, self.database)
        result = showDialog.run()
        
        self.database.addShow(show)
        self.database.write()
        self.showsStore.append([ show.name, show.backend, show ])
        
    def showsDeleteShowButtonClicked (self, widget) :
        
        model, row = self.showsView.get_selection().get_selected()
        show = self.showsStore[row][2] # 2 is our object column.
        
        self.database.removeShow(show)
        self.database.delete(show)
        self.showsStore.remove(row)
        
    def showsUpdateButtonClicked (self, widget) :
        self.database.write()
        preferences = Preferences(Tools.preferencesXML)
        preferences.load()
        if self.to_boolean(preferences['imdbtv-with-tests']) == True :
            testimdbtv = imdbtvtest()
            testimdbtv.setUp()
            testimdbtv.testDownloadShowList()
            testimdbtv.testGetShowDetails()
            testimdbtv.tearDown()
        
        se = NewBackendInterface(Tools.databaseDir)
        se.updateDatabase()
        self.database.loadDB()
        
class PreferencesDialog :
    '''
    Preferences.
    '''
    def __init__(self) :
        self.gladefile = "veefire-gtk.glade"
        
        ##
        # Initialize dialog from Glade file.
        ##
        
        self.wTree = gtk.glade.XML( self.gladefile , "preferencesDialog" )
        self.dlg = self.wTree.get_widget("preferencesDialog")
        
    def to_boolean(self, string ) :
        if string == "True" or string == "true" or string == True or string == 1 :
            return True
        else :
            return False
        
    def changeNamingStyleLabel(self, widget ) :
        self.namingStyleComboBoxEntry = self.wTree.get_widget("naming-styleEntry")
        self.namingStyleLabel = self.wTree.get_widget("naming-styleLabel")
        
        Style = self.namingStyleComboBoxEntry.get_text()
        
        fileName = FileName( 'dummyName', 'dummyDB')
        fileName.fileSuffix = '' # generateFileName needs this attribute to be set.
        
        aShow = Show( "Black Books", "dummyDuration", "dummyBackend", "dummyUrl" )
        aShow.addEpisode( Episode( "2", "Sample Title", "6 November, 2008"), Season("1") )
        
        newLabel = fileName.generateFileName( aShow, Tools.filetypesXML, 'ext3', Style )
        self.namingStyleLabel.set_text(newLabel)
        
    def editFilesystem(self, widget ) :
        pass
        
    def initPreferences(self) :
        '''
        Get values from preferences.xml
        '''
        
        self.preferences = Preferences(Tools.preferencesXML)
        self.preferences.load()
        
        ##
        # Set General
        ##
        
        self.namingStyleComboBoxEntry = self.wTree.get_widget("naming-styleComboBoxEntry")
        
        self.namingStyleListstore = gtk.ListStore(str)
        self.namingStyleComboBoxEntry.set_model(self.namingStyleListstore)
        self.namingStyleComboBoxEntry.set_text_column(0)
        
        for style in self.preferences.getOptions('naming-style') :
            if style == self.preferences['naming-style'] :
                self.namingStyleListstore.prepend([ style ])
            else :
                self.namingStyleListstore.append([ style ])
        
        self.namingStyleEntry = self.wTree.get_widget("naming-styleEntry")
        self.namingStyleEntry.set_text( self.namingStyleListstore[0][0] )
        
        self.namingStyleComboBoxEntry.connect('changed', self.changeNamingStyleLabel )
        
        # set example to current preference.
        self.namingStyleLabel = self.wTree.get_widget("naming-styleLabel")
        
        Style = self.namingStyleEntry.get_text()
        
        fileName = FileName( 'dummyName', 'dummyDB')
        fileName.fileSuffix = '' # generateFileName needs this attribute to be set.
        
        aShow = Show( "Black Books", "dummyDuration", "dummyBackend", "dummyUrl" )
        aShow.addEpisode( Episode( "2", "Sample Title", "6 November, 2008"), Season("1") )
        
        newLabel = fileName.generateFileName( aShow, Tools.filetypesXML, 'ext3', Style )
        self.namingStyleLabel.set_text(newLabel)
        
        self.confirmOnRenameCheckButton = self.wTree.get_widget("confirm-on-renameCheckButton")
        self.confirmOnRenameCheckButton.set_active( self.to_boolean(self.preferences['confirm-on-rename']) )
        
        # Filesystem
        
        self.preferencesSelectFilesystemComboBox = self.wTree.get_widget("preferencesSelectFilesystemComboBox")
        
        
        self.preferencesSelectFilesystemListstore = gtk.ListStore(str)
        self.preferencesSelectFilesystemComboBox.set_model(self.preferencesSelectFilesystemListstore)
        
        for fs in Filesystems(Tools.filetypesXML).loadFilesystems() :
            if fs.name == self.preferences['filesystem'] :
                self.preferencesSelectFilesystemListstore.prepend([ fs.name ])
            else :
                self.preferencesSelectFilesystemListstore.append([ fs.name ])
        
        self.preferencesSelectFilesystemComboBox.set_active(0)
        
        self.preferencesEditFilesystemButton = self.wTree.get_widget("preferencesEditFilesystemButton")
        self.preferencesEditFilesystemButton.connect('clicked', self.editFilesystem )
        
        ##
        # Set Database
        ##
        
        self.updateOnStartupCheckButton = self.wTree.get_widget("update-on-startupCheckButton")
        self.updateOnStartupCheckButton.set_active( self.to_boolean(self.preferences['update-on-startup']) )
        
        ##
        # Set Backends
        ##
        
        self.imdbtvWithTestsCheckButton = self.wTree.get_widget("imdbtv-with-testsCheckButton")
        self.imdbtvWithTestsCheckButton.set_active( self.to_boolean(self.preferences['imdbtv-with-tests']) )
        
        
    def run(self):
        self.initPreferences()
        self.result = self.dlg.run()
        
        ##
        # Get General
        ##
        
        namingStyle = self.namingStyleEntry.get_text()
        if namingStyle != self.namingStyleListstore[0][0] :
            self.preferences['naming-style'] = namingStyle
        
        self.preferences['confirm-on-rename'] = str(self.confirmOnRenameCheckButton.get_active())
        
        self.preferences['filesystem'] = self.preferencesSelectFilesystemListstore[self.preferencesSelectFilesystemComboBox.get_active()][0]
        
        ##
        # Get Database
        ##
        
        self.preferences['update-on-startup'] = str(self.updateOnStartupCheckButton.get_active())
        
        ##
        # Get Backends
        ##
        
        self.preferences['imdbtv-with-tests'] = str(self.imdbtvWithTestsCheckButton.get_active())
        
        self.dlg.destroy()
        
        return self.result, self.preferences
        
class AboutDialog :
    '''
    Information about veefire.
    '''
    def __init__(self) :
        self.gladefile = "veefire-gtk.glade"
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
        
class AddEpisodeDialog :
    '''
    The dialog for episode conflict in the updateDatabase-function.
    '''
    def __init__(self) :
        self.gladefile = "veefire-gtk.glade"
        
        ##
        # Initialize dialog from Glade file.
        ##
        
        self.wTree = gtk.glade.XML( self.gladefile , "addEpisodeDialog" )
        self.dlg = self.wTree.get_widget("addEpisodeDialog")
        
    def run(self):  
        
        self.result = self.dlg.run()
        
        self.Name = self.wTree.get_widget("addEpisodeNumberSpin")
        name = str(int(self.Name.get_value()))
        
        self.Title = self.wTree.get_widget("addEpisodeTitleEntry")
        title = self.Title.get_text()
        
        self.Arc = self.wTree.get_widget("addEpisodeArcEntry")
        arc = self.Arc.get_text()
        
        self.Airdate = self.wTree.get_widget("addEpisodeAirdateEntry")
        airdate = self.Airdate.get_text()
        
        self.SeasonName = self.wTree.get_widget("addEpisodeSeasonNumberSpin")
        seasonname = str(int(self.SeasonName.get_value()))
        
        self.dlg.destroy()
        
        episode = Episode( name, title, airdate, arc )
        season = seasonname
        
        return self.result, episode, season

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
        # Name should not be editable - only if it's a new show.
        if self.Show.name != '' :
            self.name.set_editable(False)
        
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
            else :
                treeview.grab_focus()
                self.editShowEpisodesMenu.popup( None, None, None, event.button, time)
            return 1
        
    def showEpisodesMenuAdd( self, widget ):
        episodeDlg = AddEpisodeDialog()
        result, Episode, season = episodeDlg.run()
        #FIXME:Does this work? correct season?
        GTK_RESPONSE_ADD = 0
        GTK_RESPONSE_REVERT = -1
        
        if result == GTK_RESPONSE_ADD:
            NewSeason = self.Show.getSeason( Season(str(season)) )
            if NewSeason == None :
                NewSeason = Season(str(season))
            self.Show.addEpisode( Episode, NewSeason )
            self.editShowEpisodesStore.append([ NewSeason.name, Episode.name, Episode.title, NewSeason, Episode ])
        
    def showEpisodesMenuRemove( self, widget ):
        model, row = self.editShowEpisodesView.get_selection().get_selected()
        if row != None :
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
            else :
                treeview.grab_focus()
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
            if row[0] == alias.name :
                exists = True
        
        if exists == False :
            self.editShowAliasesStore.append( [ alias.name, alias ] )
        
    def showAliasesMenuRemove( self, widget ):
        model, row = self.editShowAliasesView.get_selection().get_selected()
        if row != None :
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
