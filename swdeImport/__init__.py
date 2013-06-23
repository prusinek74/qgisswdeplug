# -*- coding: utf-8 -*-
"""
/***************************************************************************
 swdeImport
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
 This script initializes the plugin, making it known to QGIS.
"""


def name():
    return "swde_import"


def description():
    return "wtyczka umożliwa import danych z plików swde do bazy postgis"


def version():
    return "Version 0.1"


def icon():
    return "icon.png"


def qgisMinimumVersion():
    return "1.8"

def author():
    return "Robert Dorna - robbur"

def email():
    return "robert.dorna@wp.eu"

def classFactory(iface):
    # load swdeImport class from file swdeImport
    from swdeimport import swdeImport
    return swdeImport(iface)
