#!/usr/bin/python

from distutils.core import setup

setup(  name='veefire',
        version='0.5.0',
        description='TV file renamer',
        author='Mats Taraldsvik',
        author_email='mats.taraldsvik@gmail.com',
        url='https://launchpad.net/veefire/',
        packages=[ 'veefire' ],
        package_data={'veefire' : ['database/*.show', 'filetypes.xml', 'preferences.xml', 'veefire-gtk.glade' ]}, 
        data_files=[('', [ 'LICENSE']), ],
        requires=['BeautifulSoup'],
        )
