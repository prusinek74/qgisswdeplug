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
"""
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from PyQt4.QtSql import *
#from PyQt4.QtCore import pyqtSlot,SIGNAL,SLOT

# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from swdedzesearchdialog import swdeDzeSearchDialog

import subprocess, os,  sys

class swdeDzeSearch:
    pguser =''
    pgbase = ''
    pguserpswd = ''
    pgserver = ''
    pgadmin = ''
    pgadminpswd = ''
    postgisQueryTmpPath = ''
    id_vLayer = ''

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/python/plugins/swdedzesearch"
        self.tmpPath = self.plugin_dir + "/tmp"
        # initialize locale
        localePath = ""
        locale = QSettings().value("locale/userLocale").toString()[0:2]

        if QFileInfo(self.plugin_dir).exists():
            localePath = self.plugin_dir + "/i18n/swdedzesearch_" + locale + ".qm"

        if QFileInfo(localePath).exists():
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = swdeDzeSearchDialog() 

        self.dzemodel = QSqlQueryModel(self.dlg)
        self.cmbjew_model = QSqlQueryModel(self.dlg)
        self.cmbobr_model = QSqlQueryModel(self.dlg)

    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(
            QIcon(":/plugins/swdedzesearch/icon.png"),
            u"Wyszukiwanie działek ewidencyjnych", self.iface.mainWindow())
        # connect the action to the run method
        QObject.connect(self.action, SIGNAL("triggered()"), self.run)

        # Add toolbar button and menu item
        if hasattr(self.iface, "addPluginToDatabaseMenu"):
            self.iface.addDatabaseToolBarIcon(self.action)
            self.iface.addPluginToDatabaseMenu("&SWDE", self.action)
        else:
            self.iface.addToolBarIcon(self.action)
            self.iface.addPluginToMenu("&SWDE", self.action)

        QObject.connect(self.dlg.ui.pbtnLokalizuj,SIGNAL("clicked()"),self.pbtnLokalizujClicked)
        QObject.connect(self.dlg.ui.pbtnClose,SIGNAL("clicked()"),self.pbtnCloseClicked)
        #self.dlg.ui.cmbxJEW.connect(self.dlg.ui.cmbxJEW,SIGNAL("currentIndexChanged(int)"),self.dlg, SLOT("self.cmbxJEWCurrentIndexChanged(int)"))
        QObject.connect(self.dlg.ui.chckJEWfiltr,SIGNAL("clicked()"),self.chckJEWfiltrClicked)
        QObject.connect(self.dlg.ui.tbtnObrRefresh,SIGNAL("clicked()"),self.tbtnObrRefreshClicked)
        QObject.connect(self.dlg.ui.pbtnDzeSearch,SIGNAL("clicked()"),self.pbtnDzeSearchClicked)

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
        #fragment kodu z wtyczki postgisQuery
        #dane dotyczace serwera odczytane z QSettings
        sett = QSettings('erdeproj', 'SWDE_qgis_plugin')
        self.pguser = sett.value('pguser', '', type=str)
        self.pgbase = sett.value('pgbase', '', type=str)
        self.pguserpswd = sett.value('pguserpswd', '', type=str)
        self.pgserver = sett.value('pgserver', '', type=str)
        db = QSqlDatabase.addDatabase("QPSQL")
        db.setHostName(self.pgserver)
        db.setDatabaseName(self.pgbase)
        db.setUserName(self.pguser)
        db.setPassword(self.pguserpswd)
        ok = db.open()
        #self.model.setQuery("select * from g5jew")
        self.cmbjew_model.setQuery("select id_zd, g5naz from g5jew")
        self.dlg.ui.cmbxJEW.setModel(self.cmbjew_model)
        self.dlg.ui.cmbxJEW.setModelColumn(1)
        self.cmbobr_model.setQuery("select g5nro, g5naz from g5obr")
        self.dlg.ui.cmbxOBR.setModel(self.cmbobr_model)
        self.dlg.ui.cmbxOBR.setModelColumn(1)
        self.dlg.ui.tabvDZE.setModel(self.dzemodel)
        #ostatecznie ponizsze sa ustawiane z poziomu qtdesignera
        #self.dlg.ui.tabvDZE.setSelectionBehavior(QAbstractItemView.SelectRows)
        #self.dlg.ui.tabvDZE.setSelectionMode(QAbstractItemView.SingleSelection)
        self.dlg.ui.tabvDZE.setColumnHidden(0,True)
        self.dlg.ui.tabvDZE.show()
        # show the dialog
        self.dlg.show()



    def pbtnCloseClicked(self):
        self.dlg.close()

    def tbtnObrRefreshClicked(self):
        if self.dlg.ui.chckJEWfiltr.isChecked():
            id_jew = self.cmbjew_model.data(self.cmbjew_model.index(self.dlg.ui.cmbxJEW.currentIndex(),0)).toString()
            sqlstr = "select g5nro, g5naz from g5obr where id_zd = '" + id_jew + "'"
            self.cmbobr_model.setQuery(sqlstr)

    def chckJEWfiltrClicked(self):
        pass

    def pbtnDzeSearchClicked(self):
        nr_dze = self.dlg.ui.leditDZE.text()
        sqlstr = u"SELECT tab_uid, g5dze.nr, (select g5naz from g5obr where g5nro = g5dze.id_zd || '.' ||g5dze.nrobr) as obręb, g5dze.g5pew, g5dze.g5idd, g5dze.id_zd, g5dze.nrobr FROM g5dze "
        if self.dlg.ui.chckDzeDokladnie.isChecked():
            sqlstr += " where nr = '" + nr_dze + "' "
        else:
            sqlstr += " where nr like '" + nr_dze + "%' "
        sqlwhere = ""
        if self.dlg.ui.chckJEWfiltr.isChecked():
            id_jew = self.cmbjew_model.data(self.cmbjew_model.index(self.dlg.ui.cmbxJEW.currentIndex(),0)).toString()
            sqlwhere += " and id_zd = '" + id_jew + "' "
        if self.dlg.ui.chckOBRfiltr.isChecked():
            id_obr = stringBetweenChar(self.cmbobr_model.data(self.cmbobr_model.index(self.dlg.ui.cmbxOBR.currentIndex(),0)).toString(),".",1)
            if len(sqlwhere)>0:
                sqlwhere += " and "
            else:
                sqlwhere += " where "
            sqlwhere += "nrobr = '" + id_obr + "'"

        sqlstr+=sqlwhere
        self.dzemodel.setQuery(sqlstr)
        self.dlg.ui.tabvDZE.setColumnHidden(0,True)

    def pbtnLokalizujClicked(self):
        select = self.dlg.ui.tabvDZE.selectionModel()
        sqlstr = "select * from g5dze where "
        wherestr = ""
        for sel in select.selectedRows():
            uid = sel.data(Qt.DisplayRole).toString()
            if len(wherestr)== 0:
                wherestr = "tab_uid = '" + uid + "' "
            else:
                wherestr += " or tab_uid = '" + uid + "' "

        sqlstr += wherestr
        self.showVLayer(sqlstr)


#@brief executing the Query via pgsql2shp and adding the resulting shape to map canvas
#@param string query
#@return  none
#@author Dr. Horst Duester
#@date 10. March 2009
#@version 1.0
#@todo
    def showVLayer(self, query):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.postgisQueryTmpPath = QDir.tempPath()
        print self.postgisQueryTmpPath
        tmpLayerDef = self.createShapeFileName(self.postgisQueryTmpPath)
        file = tmpLayerDef[0]
        layerName = tmpLayerDef[1]

#  PG serverdefinintion holen
        dbName = self.pgbase
        dbUser = self.pguser
        dbHost = self.pgserver
        dbPort = '5432' #TODO ustawić w ustawieniach sett rowniez port
        dbPasswd = self.pguserpswd
        query = query.replace('"','\\"')

        cmdHost = ""
        cmdUser = ""
        cmdPasswd = ""

        if len(dbHost) != 0:
            cmdHost = "-h "+dbHost
        if len(dbUser) != 0:
            cmdUser = "-u "+dbUser
        if len(dbPasswd) != 0:
            cmdPasswd = "-P "+dbPasswd
     

        osCmd = unicode("pgsql2shp -f \""+str(file)+"\" "+cmdHost+" "+cmdUser+" -p "+str(dbPort)+" "+cmdPasswd+" "+str(dbName)+" \""+query+"\"", 'latin1')
#     qmessageBox.information(None,'',osCmd)
        proc = subprocess.Popen(osCmd.encode('latin1'),
                           shell=True,
                           stdin=subprocess.PIPE,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE
                           )
        stdout_value, stderr_value = proc.communicate()
        #self.dlg.txtOutput.setText(stdout_value+stderr_value)
        #usunięcie starej mapy    
        uri = file
        sett = QSettings('erdeproj', 'SWDE_qgis_plugin')
        self.id_vLayer = sett.value('id_vLayer', '', type=str)
        if len(self.id_vLayer) > 0:
            QgsMapLayerRegistry.instance().removeMapLayer(self.id_vLayer)

        vLayer = QgsVectorLayer(uri,  layerName,  "ogr")
        self.id_vLayer = vLayer.id()
        sett.setValue('id_vLayer', self.id_vLayer)
        canvas = self.iface.mapCanvas()
        #symbol = QgsMarkerSymbolV2.createSimple( { 'color' : '255,0,0' } )
        #vLayer.setRendererV2( QgsSingleSymbolRendererV2( symbol ) )
        #symbols = vLayer.rendererV2().symbols() 
	#symbol = symbols[0]
	#symbol.setFillColor(QColor.fromRgb(250,0,0)) 
        #rect = canvas.extent()
        #rect = vLayer.extent()
        canvas.setExtent(vLayer.extent()) 
        try:
            QgsMapLayerRegistry.instance().addMapLayer(vLayer)         
        except:
            QgsMapLayerRegistry.instance().addMapLayers([vLayer])
         
        QApplication.restoreOverrideCursor()
        QApplication.setOverrideCursor(Qt.ArrowCursor)  
        pass
    
#@brief define the temporary shape file name
#@param String path to the temporary folder
#@return  tmpShapeName
#@author Dr. Horst Duester
#@date 10. March 2009
#@version 1.0
#@todo
    def createShapeFileName(self, myPath):
        myTempShape = str(myPath) + "/SwdeDzeSearchQuery.shp"
        myTempLayer = "SwdeDzeSearchQuery" 
     
        #while os.path.isfile(unicode(myTempShape,'latin1')):
        #    myTempShape = str(myPath) + "querytmp" + str(i) + ".shp"
        #    myTempLayer = "querytmp" + str(i)
        
        myLayer = []   
        myLayer.append(myTempShape)
        myLayer.append(myTempLayer)
        print myTempShape 
        return myLayer
#==================================================================

def stringBetweenChar(string, char, nr):
    #wyszukuje lancuch znakow pomiedzy okreslonymi w char znakami
    #nr - okresla pomiedzy ktorym (pierwszym) wystapieniem znaku
    #a kolejnym znajduje sie szukany ciag. Jesli nr okresla ostatnie
    #wystapienie znaku char w string-u zostanie wyszukany ciag do konca
    #stringa
    char_pos = -1 #pozycja znaku w ciagu
    char_wyst = 0 # kolejne wystapienie char w ciagu
    char_nextpos = -1 # pozycja kolejnego wystapienia znaku w ciagu

    if nr == 0: #czyli od poczatku stringa do pierwszego znaku
        char_pos = 0
        i = 0
        for ch in string:
            if ch  == char:
                char_nextpos = i
                break
            i = i + 1
    else:
        i = 0
        for ch in string:
            if ch == char:
                char_wyst = char_wyst + 1
                if char_wyst == nr:
                    char_pos = i + 1
                elif char_wyst == nr+1:
                    char_nextpos = i
                    break
            i = i + 1

    if char_pos != -1: #czyli znaleziono znak
        if char_nextpos == -1: #czyli trzeba czytac do konca linii
            char_nextpos = len(string)
        return  string[char_pos:char_nextpos]
    else:
        return -1

