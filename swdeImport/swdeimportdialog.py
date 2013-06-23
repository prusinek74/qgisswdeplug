# -*- coding: utf-8 -*-
"""
/***************************************************************************
 swdeImportDialog
                                 A QGIS plugin
 wtyczka umożliwa import danych z plików swde do bazy postgis
                             -------------------
        begin                : 2013-05-26
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

from PyQt4 import QtCore, QtGui
from ui_swdeimport import Ui_swdeImport
# create the dialog for zoom to point


class swdeImportDialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_swdeImport()
        self.ui.setupUi(self)
