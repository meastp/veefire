#!/usr/bin/python

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

from dbapi import Database, Show, Season, Episode, Alias
from backendapi import Backends
from fileapi import Filesystems

import sys, os, re
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

class VeefireEditGTK:
    """
    The Veefire Database Editor
    """
    def __init__(self):
        #Set the Glade file
        self.gladefile = "veefireedit-gtk.glade"
        self.wTree = gtk.glade.XML(self.gladefile)
        
        #Create our dictionay and connect it
        dic = { "on_quitButton_clicked" : gtk.main_quit,
                "on_MainWindow_destroy" : gtk.main_quit,
                "on_addButton_clicked" : self.onAddShow,
                "on_removeButton_clicked" : self.onRemoveShow,
                "on_editButton_clicked" : self.onEditShow,
                "on_saveButton_clicked" : self.onSaveShow }
        self.wTree.signal_autoconnect(dic)
        
        self.database = Database()
        self.database.loadDB()
        
        self.store = gtk.ListStore( str, str )
        
        for Show in self.database.database :
            self.store.append( [ Show.name , Show.backend ] )
        
        self.view = self.wTree.get_widget("episodeView")
        self.view.set_model(self.store)
        
        render=gtk.CellRendererText()
        col=gtk.TreeViewColumn("Name",render,text=0)
        self.view.append_column(col)
        render=gtk.CellRendererText()
        col=gtk.TreeViewColumn("Backend",render,text=1)
        self.view.append_column(col)
        
        #set the selection option so that only one row can be selected
        sel=self.view.get_selection()
        sel.set_mode(gtk.SELECTION_SINGLE)
        
        #show the treeview
        self.view.show()
        
    def onAddShow( self, widget ) :
        
        addDlg = addShowDialog()
        result, showName, showBackend, showUrl, showFs = addDlg.run()
        
        if (result == 0):
            #print result
            #print showName
            #print showBackend
            #print showUrl
            #print showFs
            addShowResult = self.database.addShow( Show( showName, "None", showFs, showBackend, showUrl ) )
            if addShowResult == True :
                self.store.append( [ showName, showBackend ] )
            else :
                print "error: could not add show"
            
        if (result == -1):
            print "error: could not add show"
    
    def onEditShow( self, widget ) :
        
        selection = self.view.get_selection()
        result = selection.get_selected()
        if result: #result could be None
            model, iter = result
            editShowResult = self.database.getShow( model.get_value( iter, 0 ) )
            if editShowResult == False :
                print "error: could not get show"
            else :
                editDlg = editShowDialog(self.database, editShowResult )
                editResult = editDlg.run()
        
        if (editResult == 0):
            print result
            print showName
            print showBackend
            print showUrl
            print showFs
        if (editResult == -1):
            pass
    
    def onRemoveShow( self, widget ) :
        
        removeDlg = removeShowDialog()
        result = removeDlg.run()
        
        if (result == 0):
            selection = self.view.get_selection()
            result = selection.get_selected()
            if result: #result could be None
                model, iter = result
                removeShowResult = self.database.removeShow( model.get_value( iter, 0 ) )
                if removeShowResult == False :
                    print "error: could not remove show"
                else :
                    model.remove(iter)
        
        if (result == -1):
            print "error: could not remove show"
        
    def onSaveShow( self, widget ) :
        
        saveDlg = saveDatabaseDialog()
        result = saveDlg.run()
        
        if (result == 0):
            self.database.write()
        
        if (result == -1):
            pass
        
    
class editShowDialog() :
    '''
    Edit a show in the database.
    Add, remove or edit show properties, aliases and episodes.
    '''
    def __init__(self, db, Show) :
        self.gladefile = "veefireedit-gtk.glade"
        self.database = db
        self.editShow = Show
        
        #load the dialog from the glade file	  
        self.wTree = gtk.glade.XML( self.gladefile , "editDialog" )
        
        #Get the actual dialog widget
        self.dlg = self.wTree.get_widget("editDialog")
        
        #Create our dictionay and connect it
        dic = { "on_editButtonEpisodesAdd_clicked" : self.onEpisodeAdd,
                "on_editButtonEpisodesEdit_clicked" : self.onEpisodeEdit,
                "on_editButtonEpisodesRemove_clicked" : self.onEpisodeRemove,
                "on_editComboSeasons_changed" : self.onEpisodeSeasonComboBoxChanged,
                "on_editButtonAliasesAdd_clicked" : self.onAliasesAdd,
                "on_editButtonAliasesEdit_clicked" : self.onAliasesEdit,
                "on_editButtonAliasesRemove_clicked" : self.onAliasesRemove }
        self.wTree.signal_autoconnect(dic)
        
        self.loadValues()
        
    def onEpisodeAdd( self, widget ) :
        
        #load the dialog from the glade file  
        wTree = gtk.glade.XML( self.gladefile , "editDlgAddEpisode" )
        
        #Get the actual dialog widget
        dlg = wTree.get_widget("editDlgAddEpisode")
        
        label = wTree.get_widget("addItemEntry")
        spin = wTree.get_widget("addItemSpin")
        
        result = dlg.run()
        
        number = spin.get_value_as_int()
        text = label.get_text()
        
        dlg.destroy()
        
        if result == 0 :
            season = self.epSeasons.get_active_text()
            if self.editShow.getSeason(season) == False :
                print 'the selected season does not exist'
                return False
            if self.editShow.getSeason(season).getEpisode( number ) == True :
                print 'episode already exists!'
                return False
            self.editShow.addEpisode( Episode( str(number) , text, 'None') , season )
            self.onEpisodeSeasonComboBoxChanged( self.dlg )
            return True
        else :
            return False
        
    def onEpisodeEdit( self, widget ) :
        pass
    def onEpisodeRemove( self, widget ) :
        #load the dialog from the glade file  
        wTree = gtk.glade.XML( self.gladefile , "editDlgRemoveEpisode" )
        
        #Get the actual dialog widget
        dlg = wTree.get_widget("editDlgRemoveEpisode")
        
        selected = self.epEpisodes.get_active_text()
        if selected == "None" or selected == -1 or selected == "Episode" :
            return False
        
        result = dlg.run()
        
        dlg.destroy()
        
        if result == 0 :
            season = self.epSeasons.get_active_text()
            if self.editShow.getSeason( season ) != False :
                SelectedSeason = self.editShow.getSeason( season )
                print selected.split()
                SelectedEpisode = SelectedSeason.removeEpisode( selected.split()[0] )
                
            else :
                print 'the alias already exists.'
            return True
        else :
            return False
        
    def onEpisodeSeasonComboBoxChanged( self, widget ) :
        
        self.epEpisodes.get_model().clear()
        
        currentSeason = self.epSeasons.get_active_text()
        Season = self.editShow.getSeason(currentSeason)
        
        if Season != False :
            print str(Season.episodes)
            for Episode in Season.episodes :
                print Episode.name
                self.epEpisodes.append_text( Episode.name + ' -:- ' + Episode.title )
            self.epEpisodes.set_active(0)
            return True
        else :
            return False
        
    def onAliasesAdd( self, widget ) :
        #load the dialog from the glade file	  
        wTree = gtk.glade.XML( self.gladefile , "editDlgAddAlias" )
        
        #Get the actual dialog widget
        dlg = wTree.get_widget("editDlgAddAlias")
        
        label = wTree.get_widget("addAliasEntry")
        
        result = dlg.run()
        
        text = label.get_text()
        
        dlg.destroy()
        
        if result == 0 :
            if self.editShow.getAlias( Alias(text) ) == None :
                self.editShow.addAlias( Alias( text.lower() ) )
                self.onAliasesComboBoxChanged()
            else :
                print 'the alias already exists.'
            return True
        else :
            return False
        
    def onAliasesEdit( self, widget ) :
        #load the dialog from the glade file  
        wTree = gtk.glade.XML( self.gladefile , "editDlgEditAlias" )
        
        #Get the actual dialog widget
        dlg = wTree.get_widget("editDlgEditAlias")
        
        label = wTree.get_widget("editAliasEntry")
        
        selected = self.aliasAliases.get_active_text()
        if selected == "None" or selected == -1 or selected == "Alias" :
            return False
        
        label.set_text( selected )
        
        result = dlg.run()
        
        text = label.get_text()
        
        dlg.destroy()
        
        if result == 0 :
            if self.editShow.getAlias( Alias(selected) ) != None :
                newAlias = self.editShow.getAlias( Alias(selected) )
                newAlias.name = text.lower()
                self.onAliasesComboBoxChanged()
                for AliasN in self.editShow.alias :
                    print ':- ' + AliasN.name
            else :
                print 'the alias already exists.'
            return True
        else :
            return False
        
    def onAliasesRemove( self, widget ) :
        #load the dialog from the glade file  
        wTree = gtk.glade.XML( self.gladefile , "editDlgRemoveAlias" )
        
        #Get the actual dialog widget
        dlg = wTree.get_widget("editDlgRemoveAlias")
        
        selected = self.aliasAliases.get_active_text()
        if selected == "None" or selected == -1 or selected == "Alias" :
            return False
        
        result = dlg.run()
        
        dlg.destroy()
        
        if result == 0 :
            if self.editShow.getAlias( Alias(selected) ) != None :
                self.editShow.removeAlias( Alias( selected ) )
                self.onAliasesComboBoxChanged()
                for AliasN in self.editShow.alias :
                    print ':- ' + AliasN.name
            else :
                print 'the alias already exists.'
            return True
        else :
            return False
    
    def onAliasesComboBoxChanged( self ) :
        
        self.aliasAliases.get_model().clear()
        
        for Alias in self.editShow.alias :
            print Alias.name
            self.aliasAliases.append_text( Alias.name )
        self.aliasAliases.set_active(0)
        return True
    
    def loadValues( self ) :
        
        #General Tab
        self.showName = self.wTree.get_widget("editEntryShowName")
        self.showBackend = self.wTree.get_widget("editComboShowBackend")
        self.showUrl = self.wTree.get_widget("editEntryShowUrl")
        self.showFs = self.wTree.get_widget("editComboShowFs")
        self.showDuration = self.wTree.get_widget("editComboShowDuration")
        
        #Episodes Tab
        self.epSeasons = self.wTree.get_widget("editComboSeasons")
        self.epEpisodes = self.wTree.get_widget("editComboEpisodes")
        
        self.epAdd = self.wTree.get_widget("editButtonEpisodesAdd")
        self.epEdit = self.wTree.get_widget("editButtonEpisodesEdit")
        self.epRemove = self.wTree.get_widget("editButtonEpisodesRemove")
        
        #Aliases Tab
        self.aliasAliases = self.wTree.get_widget("editComboAliases")
        
        self.aliasAdd = self.wTree.get_widget("editButtonAliasesAdd")
        self.aliasEdit = self.wTree.get_widget("editButtonAliasesEdit")
        self.aliasRemove = self.wTree.get_widget("editButtonAliasesRemove")
        
        ### Initialize values
        
        #General
        i=1
        ShowSelected = 1
        for backend in Backends().getBackends() :
            self.showBackend.append_text( backend )
            if backend == self.editShow.backend :
                ShowSelected = i
            i+=1
        
        self.showBackend.set_active(ShowSelected)
        
        i=1
        ShowSelected = 1
        for filesystem in Filesystems().getFilesystems() :
            if backend == self.editShow.filesystem :
                ShowSelected = i
            self.showFs.append_text( filesystem )
            i+=1
        
        self.showFs.set_active(ShowSelected)
        
        self.showName.set_text( self.editShow.name )
        
        self.showUrl.set_text( self.editShow.url )
        
        # TODO: Fix duration
        
        #Episodes
        for Season in self.editShow.seasons :
            self.epSeasons.append_text( Season.name )
        #Episodes are added when season is selected
        
        #Alias
        for Alias in self.editShow.alias :
            self.aliasAliases.append_text( Alias.name )
        
    def run( self ):
        
        self.result = self.dlg.run()
        
        self.selectedShowName = self.showName.get_text()
        self.selectedShowBackend = self.showBackend.get_active_text()
        self.selectedShowUrl = self.showUrl.get_text()
        self.selectedShowFs = self.showFs.get_active_text()
        #self.selectedShowDuration = self.showName.get_active_text()
        
        self.modifiedShow = Show( self.selectedShowName, "None", self.selectedShowFs, self.selectedShowBackend, self.selectedShowUrl )
        
        #loops for episodes and aliases
        
        self.dlg.destroy()
        
        return self.result, self.modifiedShow
    
class saveDatabaseDialog() :
    '''
    Remove a show from the database.
    '''
    def __init__(self) :
        self.gladefile = "veefireedit-gtk.glade"
        
    def run(self):

        #load the dialog from the glade file	  
        self.wTree = gtk.glade.XML( self.gladefile , "saveDialog" )
        
        #Get the actual dialog widget
        self.dlg = self.wTree.get_widget("saveDialog")
        
        self.result = self.dlg.run()
        
        self.dlg.destroy()
        
        return self.result
    
class removeShowDialog() :
    '''
    Remove a show from the database.
    '''
    def __init__(self) :
        self.gladefile = "veefireedit-gtk.glade"
        
    def run(self):

        #load the dialog from the glade file	  
        self.wTree = gtk.glade.XML( self.gladefile , "removeDialog" )
        
        #Get the actual dialog widget
        self.dlg = self.wTree.get_widget("removeDialog")
        
        self.result = self.dlg.run()
        
        self.dlg.destroy()
        
        return self.result
    
class addShowDialog() :
    '''
    Add a show to the database.
    '''
    def __init__(self) :
        self.gladefile = "veefireedit-gtk.glade"
        
        
    def run(self):
        
        #load the dialog from the glade file	  
        self.wTree = gtk.glade.XML( self.gladefile , "addDialog" )
        
        self.showName = self.wTree.get_widget("entryShowName")
        self.showBackend = self.wTree.get_widget("comboShowBackend")
        self.showUrl = self.wTree.get_widget("entryShowUrl")
        self.showFs = self.wTree.get_widget("comboShowFs")
        self.showDuration = self.wTree.get_widget("comboShowDuration")
        
        #Get the actual dialog widget
        self.dlg = self.wTree.get_widget("addDialog")
        
        # Initialize values
        
        for backend in Backends().getBackends() :
            self.showBackend.append_text( backend )
        
        for filesystem in Filesystems().getFilesystems() :
            self.showFs.append_text( filesystem )
        
        # TODO: Fix duration
        
        self.result = self.dlg.run()
        
        self.selectedShowName = self.showName.get_text()
        self.selectedShowBackend = self.showBackend.get_active_text()
        self.selectedShowUrl = self.showUrl.get_text()
        self.selectedShowFs = self.showFs.get_active_text()
        #self.selectedShowDuration = self.showName.get_active_text()
        
        self.dlg.destroy()
        
        return self.result, self.selectedShowName, self.selectedShowBackend, self.selectedShowUrl, self.selectedShowFs
    
if __name__ == "__main__":
        hwg = VeefireEditGTK()
        gtk.main()
