# -*- coding: utf-8 -*-
"""
/***************************************************************************
 swdeDzeSearchDialog
                                 A QGIS plugin
 Proste wyszukiwanie zbioru działek ewidencyjnych
                             -------------------
        begin                : 2013-06-10
        copyright            : (C) 2013 by Robert Dorna
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
from ui_swdedzesearch import Ui_swdeDzeSearch
# create the dialog for zoom to point


class swdeDzeSearchDialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_swdeDzeSearch()
        self.ui.setupUi(self)
