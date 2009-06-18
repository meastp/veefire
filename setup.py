#!/usr/bin/python

from distutils.core import setup

setup(  name =  'veefire',
        version =   '0.5.0',
        description = "A TV file renamer",
        author =    'Mats Taraldsvik',
        author_email =  'mats.taraldsvik@gmail.com',
        url =   'https://launchpad.net/veefire/',
        packages =  ['veefire',
                    'veefire.api',
                    'veefire.backends'],
        package_data = {'veefire' : ['database/*.show', 'filetypes.xml', 'preferences.xml', 'veefire-gtk.glade' ]},
        )
