# -*- coding: utf-8 -*-
"""
/***************************************************************************
 CreatePostgisSwdeDb
                                 A part of QGIS plugin
 odpowiada za tworzenie nowej postgisowej bazy dla danych z plików SWDE
                              -------------------
        begin                : 2013-06-23
        copyright            : (C) 2013 by Robert Dorna - robbur
        email                : robert.dorna@wp.eu
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from swdeimportdialog import swdeImportDialog

from rob_db_connection import RobDBBase
from rob_db_connection import RobDBTable
from datetime import datetime
import time
import unicodedata
import pyproj
import sys

class CreatePostgisSwdeDb:
 
    def __init__(self, host, db, template, postgisver,  user, admin, adminpswd):
        #print "connect w db = " + str(connect)
        self.host = host
        self.db = db
        self.user = user
        self.adminpswd = adminpswd
        self.postgisver = postgisver
        self.template = template

    def createDB(self):
        pass

    def createSwdeTables(self):
        pass
