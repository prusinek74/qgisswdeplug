# -*- coding: utf-8 -*-
"""
/***************************************************************************
 swdeDzeInfoDialog
                                 A QGIS plugin
 Wyświetla okno z informacją o wybranej działce ewidencyjnej z tabeli g5dze postgresowej bazy danych z zaimportowanymi danymi z plików swde
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
from ui_swdedzeinfo import Ui_swdeDzeInfo
# create the dialog for zoom to point


class swdeDzeInfoDialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_swdeDzeInfo()
        self.ui.setupUi(self)

    def setTextBrowser(self, output):
        self.ui.txtFeedback.setText(output)

    def clearTextBrowser(self):
        self.ui.txtFeedback.clear()
