# -*- coding: utf-8 -*-
"""
/***************************************************************************
 swdeDzeSearch
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
 This script initializes the plugin, making it known to QGIS.
"""


def name():
    return "Lokalizator działek ewid."


def description():
    return "Proste wyszukiwanie zbioru działek ewidencyjnych"


def version():
    return "Version 0.1"


def icon():
    return "icon.png"


def qgisMinimumVersion():
    return "1.8"

def author():
    return "Robert Dorna"

def email():
    return "robert.dorna@wp.eu"

def classFactory(iface):
    # load swdeDzeSearch class from file swdeDzeSearch
    from swdedzesearch import swdeDzeSearch
    return swdeDzeSearch(iface)
