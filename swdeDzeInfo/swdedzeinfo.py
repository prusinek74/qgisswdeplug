# -*- coding: utf-8 -*-
"""
/***************************************************************************
 swdeDzeInfo
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
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from swdedzeinfodialog import swdeDzeInfoDialog

from rob_db_connection import RobDBBase
from rob_db_connection import RobDBTable

class swdeDzeInfo:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "python/plugins/swdeDzeInfo"
        # initialize locale
        localePath = ""
        locale = QSettings().value("locale/userLocale").toString()[0:2]

        if QFileInfo(self.plugin_dir).exists():
            localePath = self.plugin_dir + "/i18n/swdeDzeInfo_" + locale + ".qm"

        if QFileInfo(localePath).exists():
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = swdeDzeInfoDialog()
        #dane dotyczace serwera odczytane z QSettings
        self.pguser =''
        self.pgbase = ''
        self.pguserpswd = ''
        self.pgserver = ''
        self.pgadmin = ''
        self.pgadminpswd = ''

    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(
            QIcon(":/plugins/swdedzeinfo/swde-plug-info-32b.png"),
            u"Informacje o działce ewidencyjnej", self.iface.mainWindow())
        # connect the action to the run method
        QObject.connect(self.action, SIGNAL("triggered()"), self.run)

        # Add toolbar button and menu item
        if hasattr(self.iface, "addPluginToDatabaseMenu"):
            self.iface.addDatabaseToolBarIcon(self.action)
            self.iface.addPluginToDatabaseMenu("&SWDE", self.action)
        else:
            self.iface.addToolBarIcon(self.action)
            self.iface.addPluginToMenu("&SWDE", self.action)

        QObject.connect(self.dlg.ui.pbtnSave,SIGNAL("clicked()"),self.pbtnSaveClicked)
        QObject.connect(self.dlg.ui.pbtnPrint,SIGNAL("clicked()"),self.pbtnPrintClicked)

    def unload(self):
        # Remove the plugin menu item and icon
        if hasattr(self.iface, "addPluginToDatabaseMenu"):
            self.iface.removePluginDatabaseMenu("&SWDE",self.action)
            self.iface.removeDatabaseToolBarIcon(self.action)
        else:
            self.iface.removePluginMenu("&SWDE",self.action)
            self.iface.removeToolBarIcon(self.action)
    # run method that performs all the real work
    def run(self):
	layer = self.iface.activeLayer()
        provider = layer.dataProvider()
        lname =  layer.name()
        provname =  provider.name()
        if layer and lname == 'g5dze' and provname == 'postgres' :
            nF = layer.selectedFeatureCount()
            features = layer.selectedFeatures()
            for f in features:
                map = f.attributeMap()
            if nF == 1:
                provider = layer.dataProvider()
                uid_dze = map[provider.fieldNameIndex('tab_uid')].toString()
                #uid_dze  =  '040601_256126'
                #dane dotyczace serwera odczytane z QSettings
                sett = QSettings('erdeproj', 'SWDE_qgis_plugin')
                self.pguser = sett.value('pguser', '', type=str)
                self.pgbase = sett.value('pgbase', '', type=str)
                self.pguserpswd = sett.value('pguserpswd', '', type=str)
                self.pgserver = sett.value('pgserver', '', type=str)

                self.dlg.setTextBrowser( self.dzeInfo(uid_dze))
                # show the dialog
                self.dlg.show()
            else:
                QMessageBox.critical(self.iface.mainWindow(),"Error", u"Musisz wybrać dokładnie jedną działkę, użyj narzędzia: <<Wybierz jeden obiekt>>")
        else:
            QMessageBox.critical(self.iface.mainWindow(),"Error",u"Nie wybrano żadnej warstwy lub warstwa nie jest prawidłową warstwą g5dze")

    def pbtnPrintClicked(self):
        dialog = QPrintDialog()
        if dialog.exec_() == QDialog.Accepted:
            self.dlg.ui.txtFeedback.document().print_(dialog.printer())

    def pbtnSaveClicked(self):
        filename = QFileDialog.getSaveFileName(self.dlg, 'Save File', '.')
        fname = open(filename + '.html', 'w')
        fname.write(self.dlg.ui.txtFeedback.toHtml())
        fname.close() 

    def dzeInfo(self, uid_dze):
        self.rdbase = RobDBBase(str(self.pgserver), str(self.pgbase), str(self.pguser), str(self.pguserpswd), 1)
        txt = ""

        uni = lambda s: s if type(s) == unicode else unicode(s,'utf-8','replace')

        cols = ['g5idd', 'nr', 'id_zd', 'g5idr', 'g5nos', 'g5wrt', 'g5dwr', 'g5pew', 'g5rzn', 'g5dww', 'g5radr', 'g5rpwl', 'g5rpwd', 'g5rjdr', 'g5dtw', 'g5dtu', 'g5rkrg', 'g5id2', 'g5id1', 'nrobr', 'tab_uid']
        g5dzeT = RobDBTable(self.rdbase, 'g5dze', cols, 1, 1)
	g5dzeT.where(['tab_uid'], [str(uid_dze)] )
        self.dlg.clearTextBrowser()
        self.dlg.setTextBrowser(g5dzeT.get_col_value('g5idd'))
        self.dlg.setTextBrowser(uid_dze)

        txt = "<HR><H3>PODSTAWOWE INFORMACJE</H3><HR>"
        txt += "<b>IDD: </b>" + g5dzeT.get_col_value('g5idd') + "<br>"
        txt += u"<b>nr działki: </b>" + g5dzeT.get_col_value('nr') + "<br>"
        txt += "<b>Pow. ew: </b>" + str(g5dzeT.get_col_value('g5pew')) + " m2 <br>" 
        nr_obr = g5dzeT.get_col_value('nrobr')
        nr_jew = g5dzeT.get_col_value('id_zd')
        id_jdr = g5dzeT.get_col_value('g5rjdr')
        dze_id1 = g5dzeT.get_col_value('g5id1')
        id_zd = g5dzeT.get_col_value('id_zd')
        dze_uid = g5dzeT.get_col_value('tab_uid')
        dze_radr = g5dzeT.get_col_value('g5radr')
        dze_rpwl = g5dzeT.get_col_value('g5rpwl')
        dze_rpwd = g5dzeT.get_col_value('g5rpwd')

        cols = ['g5nro', 'g5naz']
        g5obrT = RobDBTable(self.rdbase, 'g5obr', cols, 1, 1)
        g5obrT.where(['g5nro'], [nr_jew + "." + nr_obr])
        txt += u"<b>Obręb:</b> " + uni(g5obrT.get_col_value('g5naz')) + "(" + g5obrT.get_col_value('g5nro')+ ")<br>"
        cols = ['g5idj', 'g5naz']
        g5jewT = RobDBTable(self.rdbase, 'g5jew', cols, 1,1)
        g5jewT.where(['g5idj'], [nr_jew])
        txt += "<b>Jednostka ewidencyjna: </b>" + uni(g5jewT.get_col_value('g5naz')) + " (" + g5jewT.get_col_value('g5idj') + ")<br>"
        cols = ['g5id1', 'g5tjr', 'g5ijr', 'g5rgn']
        g5jdrT = RobDBTable(self.rdbase, 'g5jdr', cols, 1, 1)
        g5jdrT.where(['id_zd', 'g5id1'], [nr_jew, id_jdr])
        txt += "<b>Jednostka rejestrowa:</b>" + g5jdrT.get_col_value('g5ijr') + "<br><br>" 

        cols = ['g5ofu', 'g5ozu', 'g5ozk', 'g5pew']
        g5kluT = RobDBTable(self.rdbase, 'g5klu', cols, 1,1)
        g5kluT.where(['id_zd', 'g5rdze'], [nr_jew, dze_id1])
        txt  += u"<HR></HR><H3>UŻYTKI GRUNTOWE</H3><HR></HR>"
        txt += '<table><tr bgcolor="#BFBFBF" style="font-style: oblique;"><td>OFU</td><td>OZU</td><td>OZK</td><td>Powierzchnia.</td></tr>'
        for row in g5kluT.rows:
            txt += '<tr bgcolor="#E6E6FA"><td>' + uni(row[0]) + "</td><td>" + uni(row[1]) + "</td><td>" + uni(row[2])+ "</td><td>" + str(row[3]) + "</td></tr>"
        txt += "</table>"



        cols = ['g5ud', 'g5rwls', 'g5rpod', 'rpod_rodzaj']
        g5udzT = RobDBTable(self.rdbase, 'g5udz', cols, 1, 1)
        g5udzT.where(['id_zd', 'g5rwls'], [nr_jew, id_jdr])

        txt  += u"<HR></HR><H3>WłAŚCICIEL</H3><HR></HR>"
        txt += '<table><tr bgcolor="#BFBFBF" style="font-style: oblique;"><td>Udzial</td><td>Rodz podmiotu</td><td>Podmiot</td></tr>'
        for row in g5udzT.rows:
            pod_id = row[2]
            pod_rodz = row[3]
            udz = row[0]
            
            cols = ['g5nzw', 'g5pim', 'g5dim']
            g5osfT = RobDBTable(self.rdbase, 'g5osf', cols, 1, 1)

            
            if pod_rodz == "G5INS":
                cols = ['g5sti', 'g5npe', 'g5nsk', 'g5rgn', 'g5nip']
                g5insT = RobDBTable(self.rdbase, 'g5ins', cols, 1, 1)
                g5insT.where(['id_zd', 'g5id1'], [nr_jew, pod_id])
                npe = uni(g5insT.get_col_value('g5npe'))
                txt += '<tr bgcolor="#E6E6FA"><td>' + udz + "</td><td>INS</td><td>" + npe +  "</td></tr>"

            elif pod_rodz == "G5OSF":
                g5osfT.where(['id_zd', 'g5id1'], [nr_jew, pod_id])
                txt += '<tr bgcolor="#E6E6FA"><td>' + udz + "</td><td>OSF</td><td>" + uni(g5osfT.get_col_value('g5nzw')) + " " + uni(g5osfT.get_col_value('g5pim')) + " "  + uni(g5osfT.get_col_value('g5dim')) +  "</td></tr>"

            elif pod_rodz == "G5MLZ":
                cols = ['g5rmaz', 'g5rzona']
                g5mlzT = RobDBTable(self.rdbase, 'g5mlz', cols, 1, 1)
                g5mlzT.where(['id_zd', 'g5id1'], [nr_jew, pod_id])
                g5osfT.where(['id_zd', 'g5id1'], [nr_jew, g5mlzT.get_col_value('g5rmaz')])
                maz =  uni(g5osfT.get_col_value('g5nzw')) + " " + uni(g5osfT.get_col_value('g5pim')) + " "  + uni(g5osfT.get_col_value('g5dim'))
                g5osfT.where(['id_zd', 'g5id1'], [nr_jew, g5mlzT.get_col_value('g5rzona')])
                zona = uni(g5osfT.get_col_value('g5nzw'))+ " " + uni(g5osfT.get_col_value('g5pim')) + " "  + uni(g5osfT.get_col_value('g5dim'))

                txt += '<tr bgcolor="#E6E6FA"><td>' + udz + "</td><td>MLZ</td><td>" + maz + "," + zona + "</td></tr>"

        txt += "</table>"

        cols = ['g5rwd', 'g5ud', 'g5rwld', 'g5rpod', 'rpod_rodzaj']
        g5udwT = RobDBTable(self.rdbase, 'g5udw', cols, 1, 1)
        g5udwT.where(['id_zd', 'g5rwld'], [nr_jew, id_jdr])

        txt  += u"<HR></HR><H3>WŁADAJĄCY</H3><HR></HR>"
        txt += '<table><tr bgcolor="#BFBFBF" style="font-style: oblique;"><td>Udzial</td><td>Rodz podmiotu</td><td>Podmiot</td></tr>'
        for row in g5udzT.rows:
            pod_id = row[2]
            pod_rodz = row[3]
            udz = row[0]
            
            cols = ['g5nzw', 'g5pim', 'g5dim']
            g5osfT = RobDBTable(self.rdbase, 'g5osf', cols, 1, 1)

            
            if pod_rodz == "G5INS":
                cols = ['g5sti', 'g5npe', 'g5nsk', 'g5rgn', 'g5nip']
                g5insT = RobDBTable(self.rdbase, 'g5ins', cols, 1, 1)
                g5insT.where(['id_zd', 'g5id1'], [nr_jew, pod_id])
                npe = uni(g5insT.get_col_value('g5npe'))
                txt += '<tr bgcolor="#E6E6FA"><td>' + udz + "</td><td>INS</td><td>" + npe +  "</td></tr>"

            elif pod_rodz == "G5OSF":
                g5osfT.where(['id_zd', 'g5id1'], [nr_jew, pod_id])
                txt += '<tr bgcolor="#E6E6FA"><td>' + udz + "</td><td>OSF</td><td>" + uni(g5osfT.get_col_value('g5nzw')) + " " + uni(g5osfT.get_col_value('g5pim'))+ " "  + uni(g5osfT.get_col_value('g5dim')) +  "</td></tr>"

            elif pod_rodz == "G5MLZ":
                cols = ['g5rmaz', 'g5rzona']
                g5mlzT = RobDBTable(self.rdbase, 'g5mlz', cols, 1, 1)
                g5mlzT.where(['id_zd', 'g5id1'], [nr_jew, pod_id])
                g5osfT.where(['id_zd', 'g5id1'], [nr_jew, g5mlzT.get_col_value('g5rmaz')])
                maz =  uni(g5osfT.get_col_value('g5nzw')) + " " + uni(g5osfT.get_col_value('g5pim')) + " "  + uni(g5osfT.get_col_value('g5dim'))
                g5osfT.where(['id_zd', 'g5id1'], [nr_jew, g5mlzT.get_col_value('g5rzona')])
                zona = uni(g5osfT.get_col_value('g5nzw')) + " " + uni(g5osfT.get_col_value('g5pim')) + " "  + uni(g5osfT.get_col_value('g5dim'))

                txt += '<tr bgcolor="#E6E6FA"><td>' + udz + "</td><td>MLZ</td><td>" + maz + "," + zona + "</td></tr>"

        txt += "</table>"

        #dokumenty rpwl
        SQLstr = "SELECT g5kdk, g5dtd, g5dtp, g5syg, g5nsr, g5opd FROM g5dok where tab_uid = any(array["
        for dok_id in dze_rpwl:
            SQLstr += "'" + nr_jew + dok_id + "',"
        SQLstr = SQLstr.rstrip(',')
        SQLstr += "]);"
        res = self.rdbase.executeSQL(SQLstr)

        if res:
            txt  += u"<HR></HR><H3>DOKUMENTY POWIĄZANE</H3><HR></HR>"
            txt += '<table><tr bgcolor="#BFBFBF" style="font-style: oblique;"><td>KDK</td><td>DTD</td><td>DTP</td><td>SYG</td><td>NSR</td><td>OPD</td></tr>'
            for row in res:
                txt += '<tr bgcolor="#E6E6FA"><td>' + uni(row[0]) + "</td><td>" + uni(row[1]) +"</td><td>" + uni(row[2]) + "</td><td>" + uni(row[3]) + "</td><td>" + uni(row[4])  + "</td></tr>"

            txt += "</table>"




        return txt



