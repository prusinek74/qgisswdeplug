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
from createpostgisswdedb import CreatePostgisSwdeDb
from datetime import datetime
import time
import unicodedata
import pyproj
import sys

#import rpdb2; rpdb2.start_embedded_debugger('haslo')#tylko na potrzeby debugowania z winpdb

class swdeImport:
    swde_file = ""
    ilosc_linii = ""
    pzgdic = {}
    pguser = ""
    pgbase = ""
    pguserpswd = ""
    pgserver = ""
    pgport = ""
    pgadmin = ""
    pgadminpswd = ""
    tmppath = ""
    ogr2ogrpath = ""
    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "python/plugins/swdeImport" #usunalem / na poczatku stringa
        # initialize locale
        localePath = ""
        locale = QSettings().value("locale/userLocale").toString()[0:2]

        if QFileInfo(self.plugin_dir).exists():
            localePath = self.plugin_dir + "/i18n/swdeimport_" + locale + ".qm"

        if QFileInfo(localePath).exists():
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = swdeImportDialog()

        self.swde_file = "" #nazwa pliku - pełna ścieżka - string
        self.f = 0          #obiekt typu file o ścieżce self.swde_file
        self.ilosc_linii = 0

        self.pzgdic = {}

        #dane dotyczace serwera odczytane z QSettings
        sett = QSettings('erdeproj', 'SWDE_qgis_plugin')
        self.pguser = sett.value('pguser', '', type=str)
        self.pgbase = sett.value('pgbase', '', type=str)
        self.pguserpswd = sett.value('pguserpswd', '', type=str)
        self.pgserver = sett.value('pgserver', '', type=str)
        self.pgport = sett.value('pgport', '5432', type=str)
        self.pgadmin = sett.value('pgadmin', '', type=str)
        self.pgadminpswd = sett.value('pgadminpswd', '', type=str)
        self.tmppath = sett.value('tmppath', '', type=str)
        self.ogr2ogrpath = sett.value('ogr2ogrpath', '', type=str)


    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(
            QIcon(":/plugins/swdeimport/swde-plug-import-22b.png"),
            u"Import danych z pliku SWDE", self.iface.mainWindow())
        # connect the action to the run method
        QObject.connect(self.action, SIGNAL("triggered()"), self.run)

        # Add toolbar button and menu item
        #self.iface.addToolBarIcon(self.action)
        #self.iface.addPluginToMenu(u"&swde_import", self.action)
        if hasattr(self.iface, "addPluginToDatabaseMenu"):
            self.iface.addDatabaseToolBarIcon(self.action)
            self.iface.addPluginToDatabaseMenu("&SWDE", self.action)
        else:
            self.iface.addToolBarIcon(self.action)
            self.iface.addPluginToMenu("&SWDE", self.action)

        self.connGuiSignals()#łączenie sygnałów z obiektami z GUI
        #ustawienie wartosci editow z zakladki ustawienia bazy danych
        self.dlg.ui.leditDBServer.setText(self.pgserver)
        self.dlg.ui.leditDBBaseName.setText(self.pgbase)
        self.dlg.ui.leditDBUser.setText(self.pguser)
        self.dlg.ui.leditDBPassword.setText(self.pguserpswd)
        #inicializacja tablicy items dla combobox z ukladami przestrzennymi
        self.cmb_pyproj4_items = {}
        try:
            pyproj4file = self.plugin_dir + u"/pyproj4str"
            f = open(pyproj4file, "r")
            try:
                second = 0
                key = ""
                value = ""
                for line in f.readlines():
                    line = line.rstrip('\n')
                    line = line.rstrip('\r')
                    if second == 0:
                        key = line
                        second = 1
                    else:
                        value = line
                        self.cmb_pyproj4_items [key] = value 
                        self.dlg.ui.cmbPyprojFrom.addItem(key, value)
                        self.dlg.ui.cmbPyprojTo.addItem(key, value)
                        second = 0

            finally:
                f.close()
        except IOError:
            self.dlg.ui.peditOutput.appendPlainText("error: " + pyproj4file)
            pass


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
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result == 1:
            # do something useful (delete the line containing pass and
            # substitute with your code)
            pass

    def connGuiSignals(self):
        #========Zakładka import===========
        #--------buttons
        QObject.connect(self.dlg.ui.pbtnAnalizaWykonaj,SIGNAL("clicked()"),self.pbtnAnalizaWykonajClicked)
        QObject.connect(self.dlg.ui.tbtnWybierzSWDEFile,SIGNAL("clicked()"),self.tbtnWybierzSWDEFileClicked)
        QObject.connect(self.dlg.ui.pbtnSWDEHeaderInfo,SIGNAL("clicked()"),self.pbtnSWDEHeaderInfoClicked)
        QObject.connect(self.dlg.ui.pbtnSWDEHeaderFull,SIGNAL("clicked()"),self.pbtnSWDEHeaderFullClicked)
        QObject.connect(self.dlg.ui.pbtnImportuj,SIGNAL("clicked()"),self.pbtnImportujClicked)
        QObject.connect(self.dlg.ui.pbtnDBSaveSettings,SIGNAL("clicked()"),self.pbtnDBSaveSettingsClicked)
        QObject.connect(self.dlg.ui.pbtnCreateSWDEDB,SIGNAL("clicked()"),self.pbtnCreateSWDEDBClicked)
        QObject.connect(self.dlg.ui.tbtnTmpFolder,SIGNAL("clicked()"),self.tbtnTmpFolderClicked)
        QObject.connect(self.dlg.ui.tbtnOgr2ogrFile,SIGNAL("clicked()"),self.tbtnOgr2ogrFileClicked)

        #--------edits and labels

        #--------checkboxes and radiobuttons

    def pbtnDBSaveSettingsClicked(self):
        sett = QSettings('erdeproj', 'SWDE_qgis_plugin')
        self.pgserver = self.dlg.ui.leditDBServer.displayText()
        self.pgbase = self.dlg.ui.leditDBBaseName.displayText()
        self.pguser = self.dlg.ui.leditDBUser.displayText()
        self.pguserpswd = self.dlg.ui.leditDBPassword.text()
        self.pgport = self.dlg.ui.leditDBPort.text()
        sett.setValue('pguser', self.pguser)
        sett.setValue('pgbase', self.pgbase)
        sett.setValue('pguserpswd', self.pguserpswd)
        sett.setValue('pgserver', self.pgserver)
        sett.setValue('pgport', self.pgport)

    def tbtnTmpFolderClicked(self):
        sett = QSettings('erdeproj', 'SWDE_qgis_plugin')
        self.tmppath = QFileDialog.getExistingDirectory(self.dlg, u'Wybierz lokalizację folderu plików tymczasowych', '.', QFileDialog.ShowDirsOnly)
        sett.setValue('tmppath', self.tmppath)
        self.dlg.ui.leditTmpFolder.setText(self.tmppath)

    def tbtnOgr2ogrFileClicked(self):
        sett = QSettings('erdeproj', 'SWDE_qgis_plugin')
        self.ogr2ogrfile = QFileDialog.getOpenFileName(self.dlg, u'Wybierz lokalizację pliku ogr2ogr.exe (systemy windows)', '.')
        sett.setValue('ogr2ogrfile', self.ogr2ogrfile)
        self.dlg.ui.leditOgr2ogrFile.setText(self.ogr2ogrfile)


    def pbtnCreateSWDEDBClicked(self):
        #do czasu calkowitego rozwiazania problemu, funkcja zostaje nieaktywna
        pass
        #sett = QSettings('erdeproj', 'SWDE_qgis_plugin')
        #pguser =  sett.value('pguser', '', type=str)
        #pgserver =  sett.value('pgserver', '', type=str)
        #pgbase = sett.value('pgbase', '', type=str)
        #pguserpswd = sett.value('pguserpswd', '', type=str)
        #pgowner = self.dlg.ui.leditOwner.text()
        ##chwilowo zmienna postgisver nie ma specjalnego znaczenia
        #postgisver = ""
        #if self.dlg.ui.rdbtnPostgis15.isChecked():
        #    postgisver = "1.5"
        #else:
        #    postgisver = "2.0"

        #newdb = CreatePostgisSwdeDb(pgserver, pgbase, postgisver, pgowner, pguser, pguserpswd)
        #newdb.createSwdeTables()

    def tbtnWybierzSWDEFileClicked(self):
        self.swde_file = QFileDialog.getOpenFileName(self.dlg, 'Wybierz plik SWDE', '.')
        self.dlg.ui.leditSWDEFile.setText(self.swde_file)

    def pbtnAnalizaWykonajClicked(self):
        self.swde_file = self.dlg.ui.leditSWDEFile.displayText()
        ##wypelnienie struktury słownikowej z rozwinięciami punktów granicznych
        self.pzgdic = {}
        dic_idx = ""
        rp = 0

        if self.swde_file != '':
            ilosc_linii = 0
            step = 0
            pgv = 0
            id_jed_rej = ""
            ilosc_pzg = 0
            try:
                self.f = open(str(self.swde_file.toUtf8()).decode('utf-8'), "r")
                try:
                    pgdlg = QProgressDialog(u"Chwilunia", "Przerwij...", 0, 0)
                    pgdlg.setLabelText(u"Czekaj, trwa analiza pliku SWDE.... ")
                    #pgdlg.setMinimumDuration(1000)
                    pgdlg.show()
                    QApplication.processEvents()
                    for line in self.f.readlines():
                        ilosc_linii+=1
                        if StringBetweenChar(line, ',', 0) == "NS" and StringBetweenChar(line, ',', 1) == "ZD":
                            id_jed_rej = StringBetweenChar(line, ',', 2)
                        pocz = StringBetweenChar(line, ',',0)
                        if pocz == "RP":
                            tab = StringBetweenChar(line, ',',2)
                            if tab == "G5PZG":
                                nr = StringBetweenChar(line, ',', 3)
                                rp = 1
                                dic_idx = nr
                        elif rp == 1:
                            y =StringBetweenChar(line, ',', 2)
                            x =StringBetweenChar(line, ',', 3)
                            dic_value = y +"," + x
                            self.pzgdic[nr] = dic_value
                            rp = 0
                            ilosc_pzg += 1
                        step += 1
                        if step == 10000:
                            QApplication.processEvents()
                            step = 0


                finally:
                    pgdlg.close()
                    #f.close() - przeniesiono do fukcji importu
            except IOError:
                self.dlg.ui.peditOutput.appendPlainText(u"IOError: błąd wczytania pliku swde")
        self.dlg.ui.leditLineInFile.setText(str(ilosc_linii))
        self.ilosc_linii = ilosc_linii
        self.dlg.ui.leditIDZD.setText(id_jed_rej)
        self.dlg.ui.leditIloscPZG.setText(str(ilosc_pzg))
        self.dlg.ui.peditOutput.clear()
        id_jed_rej = id_jed_rej.strip()
        if id_jed_rej !="":
            self.dlg.ui.peditOutput.appendPlainText("Znaleziony identyfikator jednostki rejestrowej: " + id_jed_rej + u" zostanie wykorzystany  w bazie do stworzenia kluczy obiektów. Jeśli chcesz użyć innego możesz go zastąpić wpisanym przez siebie tekstem")
        else:
            self.dlg.ui.peditOutput.appendPlainText(u"Nie znaleziono identyfikatora jednostki rejestrowej - musisz samodzielnie określić identyfikator zbioru danych, wpisując samodzielnie - litery i cyfry - najlepiej do 10 znaków. Nie używaj polskich liter")

    def pbtnSWDEHeaderInfoClicked(self):

        self.dlg.ui.peditSWDEHeader.clear()
        self.dlg.ui.peditOutput.appendPlainText("Start: " +  time.strftime("%Y-%m-%d %H:%M:%S"))
        try:
            f = open(str(self.swde_file.toUtf8()).decode('utf-8'), "r")
            try:
                i = 0 #licznik linii - nie ma sensu wczytywac całego pliku
                txt = ''
                for line in f.readlines():

                    #pocz = line[0:2]
                    pocz = StringBetweenChar(line, ',',0)
                    #print i, pocz
                    rodz_info = ""
                    opis = ""
                    opis_info = ""
                    i+=1
                    if pocz == "NS":
                        line = line.rstrip('\r')
                        line = line.rstrip('\n')
                        rodz_info = StringBetweenChar(line, ',',1)

                        #opis_info = unicodedata.normalize('NFKD',opis_info).decode('ascii', 'replace')
                        #opis_info = replacePlChars(StringBetweenChar(line, ',',2))
                        opis_info = unicode( StringBetweenChar(line, ',',2), self.txtCodec(), 'replace')

                        if rodz_info == u"DN":
                            opis = u"Data utworzenia pliku: "
                        elif rodz_info == u"TR":
                            opis = u"Nr identyfikacyjny jednostki tworzącej plik: "
                        elif rodz_info == u"TN":
                            opis = u"Nazwa jednostki tworzącej plik: "
                        elif rodz_info == u"TA":
                            opis = u"Adres jednostki tworzącej plik: "
                        elif rodz_info == u"TO":
                            opis = u"Imię i nazwisko wykonawcy: "
                        elif rodz_info == u"ZN":
                            opis = u"Nazwa systemu - źródła danych: "
                        elif rodz_info == u"ZR":
                            opis = u"Nr identyfikacyjny systemu - źródła danych: "
                        elif rodz_info == u"ZD":
                            opis = u"Nazwa zbioru danych - reprezentowanego obiektu: "
                        elif rodz_info == u"OP":
                            opis = u"Przeznaczenie danych: "
                        elif rodz_info == u"OR":
                            opis = u"Nr identyfikacyjny jednostki przeznaczenia: "
                        elif rodz_info == u"ON":
                            opis = u"Nazwa jednostki przeznaczenia: "
                        elif rodz_info == u"OA":
                            opis = u"Adres jednostki przeznaczenia: "
                        elif rodz_info == u"OO":
                            opis = u"Imię i nazwisko odbiorcy: "
                        elif rodz_info == u"UX":
                            opis = u"Nazwa układu współrzędnych: "
                        elif rodz_info == u"OS":
                            opis = u"Nazwa / numer strefy odwzorowania: "
                        elif rodz_info == u"NX":
                            opis = u"Nazwa pierwszej współrzędnej : "
                        elif rodz_info == u"NY":
                            opis = u"Nazwa drugiej wspolrzednej: "
                        elif rodz_info == u"NZ":
                            opis = u"Nazwa trzeciej wspolrzednej : "
                        elif rodz_info == u"UH":
                            opis = u"System wysokosci : "
                        elif rodz_info == u"HZ":
                            opis = u"Poziom odniesienia : "

                        txt += u"<b>" + rodz_info + u"</b>  - " + opis + opis_info + u"<br>"
                    
                    if i == 100:
                        break
                self.dlg.ui.peditSWDEHeader.setText(txt)
                    

            finally:
                txt = 'Plik zamkniety: ' + time.strftime("%Y-%m-%d %H:%M:%S")
                self.dlg.ui.peditOutput.appendPlainText(txt)
                f.close()
        
        except IOError:
            self.dlg.ui.peditOutput.appendPlainText("IOError:" +  time.strftime("%Y-%m-%d %H:%M:%S"))
            pass


    def pbtnSWDEHeaderFullClicked(self):
        self.dlg.ui.peditSWDEHeader.clear()
        self.dlg.ui.peditOutput.appendPlainText("Start: " +  time.strftime("%Y-%m-%d %H:%M:%S"))
        txtcodec = self.txtCodec()
        try:
            f = open(str(self.swde_file.toUtf8()).decode('utf-8'), "r")
            try:
                i = 0 #licznik linii - nie ma sensu wczytywac całego pliku
                txt = ''
                for line in f.readlines():
                    i+=1
                    txt += unicode(line, txtcodec, 'replace')


                    if i == 1000:
                        break
                self.dlg.ui.peditSWDEHeader.setText(txt) 

            finally:
                txt = 'Plik zamkniety: ' + time.strftime("%Y-%m-%d %H:%M:%S")
                self.dlg.ui.peditOutput.appendPlainText(txt)
                f.close()
        
        except IOError:
            self.dlg.ui.peditOutput.appendPlainText("IOError:" +  time.strftime("%Y-%m-%d %H:%M:%S"))
            pass

    def txtCodec(self):
        if self.dlg.ui.rdbtnKodowanieISO.isChecked():
            return  'iso8859_2'
        elif self.dlg.ui.rdbtnKodowanieWidnows.isChecked():
            return 'cp1250'
        elif self.dlg.ui.rdbtnKodowanieUTF.isChecked():
            return 'utf-8'
    #...................................................................................
    def pbtnImportujClicked(self):

        uni = lambda s: s if type(s) == unicode else unicode(s,'utf-8','replace')
        srid = str(self.dlg.ui.leditSRIDImport.text())
        if self.f == 0 or self.f.closed:
           QMessageBox.warning(self.dlg, 'Uwaga!!!',
                        u"Przed rozpoczęciem importu musisz wczytać plik oraz dokonać jego analizy")
        else:
            id_jed_rej =  self.dlg.ui.leditIDZD.text() #TODO sprawdzenie czy nie jest puste oraz sprawdzenie czy w bazie juz takiego nie ma (mozna to sprawdzenie wykonac podczas analizy) - rstrip na wszelki wypadek
            id_jed_rej  = str(id_jed_rej).rstrip()

            pyproj4strFrom = self.cmb_pyproj4_items[unicode(self.dlg.ui.cmbPyprojFrom.currentText(),'utf-8')]
            pyproj4strTo = self.cmb_pyproj4_items[unicode(self.dlg.ui.cmbPyprojTo.currentText(),'utf-8')]

            #lista column tablicowych - do innej obróbki niż pozostałe
            arrayCols = ['G5RADR', 'G5RPWL', 'G5RPWD', 'G5RKRG', 'G5RSKD', 'G5RDOK', 'G5RDZE', 'G5ROBJ']
            #słownik kolumn do zmiany nazwy - zmieniamy polskie znaki w nazwie kolumn bo trochę to broi przy pytaniach SQL
            plcharCols =  {u'G5RŻONA':'G5RZONA', u'G5RMĄŻ':'G5RMAZ', u'G5RPWŁ':'G5RPWL', u'G5RWŁ':'G5RWL', u'G5RWŁS':'G5RWLS', u'G5RWŁD':'G5RWLD'}
            g5Cols = {} #słownik zbudowany: {'nazwa_tabeli':Tablica_Column[]} - posluzy do inicjacji tabel - obiektow robdbtable 
            #inicjalizacja  bazy danych
            rdbase = RobDBBase(str(self.pgserver), str(self.pgbase), str(self.pguser), str(self.pguserpswd), 1)
            rdg5Table = {}  #słownik zawiera następującą strukturę: {'nazwa_tabeli': Obiekt_rdbtable}
            tableList = []  #tabela nazw tabel - wykorzystywane w roznych miejscach - miedzy innymi przy sprawdzeniu czy dana tabela została wybrana do importu
                            #jest to lista tabel, ktore beda brane pod uwage - glowny cel - kontrola nad danymi w trakcie pisania tego skryptu
            #okreslenie rodzaju importu
            if self.dlg.ui.rdbtnZwyklyImport.isChecked() or self.dlg.ui.rdbtnAktualizacja.isChecked():
                #sprawdzenie ktore z tabel mają być importowane - nie brane pod uwagę  wprzypadku importu testowego
                if self.dlg.ui.chckG5dze.isChecked():
                    tableList.append('G5DZE')
                if self.dlg.ui.chckG5obr.isChecked():
                    tableList.append('G5OBR')
                if self.dlg.ui.chckG5jew.isChecked():
                    tableList.append('G5JEW')
                if self.dlg.ui.chckG5jdr.isChecked():
                    tableList.append('G5JDR')
                if self.dlg.ui.chckG5adr.isChecked():
                    tableList.append('G5ADR')
                if self.dlg.ui.chckG5dze.isChecked():
                    tableList.append('G5DZE')
                if self.dlg.ui.chckG5udz.isChecked():
                    tableList.append('G5UDZ')
                if self.dlg.ui.chckG5udw.isChecked():
                    tableList.append('G5UDW')
                if self.dlg.ui.chckG5osf.isChecked():
                    tableList.append('G5OSF')
                if self.dlg.ui.chckG5ins.isChecked():
                    tableList.append('G5INS')
                if self.dlg.ui.chckG5mlz.isChecked():
                    tableList.append('G5MLZ')
                if self.dlg.ui.chckG5osz.isChecked():
                    tableList.append('G5OSZ')
                if self.dlg.ui.chckG5klu.isChecked():
                    tableList.append('G5KLU')
                if self.dlg.ui.chckG5uzg.isChecked():
                    tableList.append('G5UZG')
                if self.dlg.ui.chckG5dok.isChecked():
                    tableList.append('G5DOK')
                if self.dlg.ui.chckG5bud.isChecked():
                    tableList.append('G5BUD')
                if self.dlg.ui.chckG5lkl.isChecked():
                    tableList.append('G5LKL')
                if self.dlg.ui.chckG5zmn.isChecked():
                    tableList.append('G5ZMN')
                if self.dlg.ui.chckG5kkl.isChecked():
                    tableList.append('G5KKL')
                if self.dlg.ui.chckG5zmn.isChecked():
                    tableList.append('G5ZMN')


                Cols = ['G5IDJ', 'G5PEW', 'G5NAZ', 'G5DTW', 'G5DTU','G5RKRG']#g5jew
                g5Cols['G5JEW'] = Cols
                Cols = [ 'G5IDD',  'GEOM',    'NR', 'G5IDR', 'G5NOS', 'G5WRT', 'G5DWR', 'G5PEW', 'G5RZN', 'G5DWW', 'G5RADR', 'G5RPWL', 'G5RPWD', 'G5RKRG', 'G5RJDR', 'G5DTW', 'G5DTU'] #g5dze
                g5Cols['G5DZE'] = Cols
                Cols = [ 'G5NRO', 'G5PEW', 'G5NAZ', 'G5DTW', 'G5DTU', 'G5RKRG', 'G5RJEW', 'IDJEW'] #g5obr
                g5Cols['G5OBR'] = Cols
                Cols = ['G5PLC', 'G5PSL', 'G5NIP', 'G5NZW', 'G5PIM', 'G5DIM', 'G5OIM', 'G5MIM', 'G5OBL', 'G5DOS', 'G5RADR', 'G5STI', 'G5DTW', 'G5DTU'] #g5osf
                g5Cols['G5OSF'] = Cols
                Cols = [ 'G5STI', 'G5NPE', 'G5NSK', 'G5RGN', 'G5NIP', 'G5NZR', 'G5NRR', 'G5NSR', 'G5RADR', 'G5DTW', 'G5DTU'] #g5ins
                g5Cols['G5INS'] = Cols
                Cols = ['G5RZONA',  'G5RMAZ', 'G5DTW', 'G5DTU'] #g5mlz
                g5Cols['G5MLZ'] = Cols
                Cols = [ 'G5STI', 'G5NPE', 'G5NSK', 'G5RGN', 'G5NIP', 'G5RSKD', 'G5RADR', 'G5DTW', 'G5DTU'] #g5osz
                g5Cols['G5OSZ'] = Cols
                Cols = ['G5TJR', 'G5IJR', 'G5RGN', 'G5RWL', 'G5RWLS', 'G5RWLD', 'G5ROBR', 'G5DTW', 'G5DTU' ] #g5jdr
                g5Cols['G5JDR'] = Cols
                Cols = [ 'G5UD', 'G5RWLS', 'G5RPOD', 'G5DTW', 'G5DTU'] #g5udz
                g5Cols['G5UDZ'] = Cols
                Cols = [ 'G5RWD', 'G5UD', 'G5RWLD', 'G5RPOD', 'G5DTW', 'G5DTU'] #g5udw
                g5Cols['G5UDW'] = Cols
                Cols = [ 'G5OFU', 'G5OZU', 'G5OZK', 'G5PEW', 'G5RDZE', 'G5DTW', 'G5DTU'] #g5klu
                g5Cols['G5KLU'] = Cols
                Cols = [ 'G5IDT', 'G5OZU','G5OFU', 'G5PEW', 'G5RKRG', 'G5ROBR', 'G5DTW', 'G5DTU'] #g5uzg
                g5Cols['G5UZG'] = Cols
                Cols = ['G5KDK', 'G5DTD', 'G5DTP', 'G5SYG', 'G5NSR', 'G5OPD', 'G5RDOK', 'G5DTW', 'G5DTU'] #g5dok
                g5Cols['G5DOK'] = Cols
                Cols = ['G5TAR', 'G5NAZ', 'G5KRJ', 'G5WJD', 'G5PWJ', 'G5GMN', 'G5ULC', 'G5NRA', 'G5NRL', 'G5MSC', 'G5KOD', 'G5PCZ', 'G5DTW', 'G5DTU']#g5adr
                g5Cols['G5ADR'] = Cols
                Cols = ['G5IDB', 'G5FUZ', 'G5WRT', 'G5DWR', 'G5RBB', 'G5PEW', 'G5PEU', 'G5RZN', 'G5SCN', 'G5RADR', 'G5RPWL', 'G5RPWD', 'G5RKRG', 'G5RJDR','G5RDZE', 'G5DTU', 'G5DTW']#g5bud
                g5Cols['G5BUD'] = Cols
                Cols = ['G5IDK', 'G5OZU', 'G5OZK', 'G5PEW', 'G5RKRG', 'G5ROBR', 'G5DTW', 'G5DTU']
                g5Cols['G5KKL'] = Cols
                Cols = ['G5IDL', 'G5TLOK', 'G5PEW', 'G5PPP', 'G5LIZ', 'G5WRT', 'G5DWR', 'G5RJDR', 'G5RADR', 'G5RDOK', 'G5RBUD', 'G5DTW', 'G5DTU']
                g5Cols['G5LKL'] = Cols
                Cols = ['G5NRZ', 'G5STZ', 'G5DZZ', 'G5DTA', 'G5DTZ', 'G5NAZ', 'G5ROBJ', 'G5RDOK', 'G5DTW', 'G5DTU']
                g5Cols['G5ZMN'] = Cols



            elif self.dlg.ui.rdbtnImportTestowy.isChecked():
                #w przypadku importu testowego importować będziemy tylko jedną z trzech tabel (dze, obr, lub jew)
                # przy okazji opróżnimy zawartość dotychczasowych tabel testowych
                delSQLstr = "delete from "
                if self.dlg.ui.rdbtnTestowyJEW.isChecked():
                    tableList.append('G5JEW')
                    g5Cols['G5JEW'] = ['G5IDJ', 'G5PEW', 'G5NAZ', 'G5DTW', 'G5DTU','G5RKRG']#g5jew
                    delSQLstr += "g5jew_test;"
                elif self.dlg.ui.rdbtnTestowyOBR.isChecked():
                    tableList.append('G5OBR')
                    g5Cols['G5OBR'] = [ 'G5NRO', 'G5PEW', 'G5NAZ', 'G5DTW', 'G5DTU', 'G5RKRG', 'G5RJEW', 'IDJEW']
                    delSQLstr += "g5obr_test;"
                elif self.dlg.ui.rdbtnTestowyDZE.isChecked():
                    tableList.append('G5DZE')
                    g5Cols['G5DZE'] = [ 'G5IDD',  'GEOM',    'NR', 'G5IDR', 'G5NOS', 'G5WRT', 'G5DWR', 'G5PEW', 'G5RZN', 'G5DWW', 'G5RADR', 'G5RPWL', 'G5RPWD', 'G5RKRG', 'G5RJDR', 'G5DTW', 'G5DTU']
                    delSQLstr += "g5dze_test;"

                rdbase.executeSQL(delSQLstr)


            #nazwy kolumn muszą zostać podane dokładnie jak w bazie - czyli małymi literami
            #na przyszłość można to rozwiązać w samej RobDBTable
            #za zamianę liter na małe w tablicy odpowiada ta fikuśna konstrukcja: [x.lower() ....]
            for tableName in tableList:
                if self.dlg.ui.rdbtnImportTestowy.isChecked():
                    appendix = '_TEST'
                else:
                    appendix = ''
                rdg5Table[tableName] = RobDBTable(rdbase, tableName + appendix, [x.lower() for x in g5Cols[tableName]], 1, 1)

            G5Table = ""

            collist = []
            valuelist = []
            insertdic = {} # forma [nazwa_tabeli:ilosc_insertow] 
            arraylist = [] #wykorzystywana do przechowywania kolumn typu tablicaowego w formie [[col2, wart..], [col1, wart..], [col2, wart..]]
            arrayvalue = [] # wykorzystywane do przechowywania danych 1+ takich jak g5rkrg
            arrayname = '' # nazwa tablicy tożsama z nazwą kolumny w bazie
            pointslist = []
            point = []
            Kznak = ""  #znacznik + albo -, oznaczajacy czy okreslane sa punkty tworzace polygon czy
                        #wycinajace w nim dziure
            oldKznak = "0" #posluzy do sprawdzenia czy nastapila zmiana Kznak
            newPoly = 0
            polycount = 0

            ilosc_linii = self.ilosc_linii
            linianr = 0     #przyda sie w momencie gdy sie program wywali - okresli ktora linia pliku swde nabroiła
            obieg = 0       #bedzie wykorzystywane przy commit do bazy, ktore bedzie realizowane co np 100 pytań SQL
            txtcodec = self.txtCodec()
            transform = 0
            if self.dlg.ui.rdbtnImportTestowy.isChecked() == 0: #tylko jesli nie jest to import testowy
                transform = self.dlg.ui.chckTransform.isChecked()


            self.dlg.ui.peditOutput.appendPlainText("Krok 1. Start programu: " +  time.strftime("%Y-%m-%d %H:%M:%S"))

            pgdlg = QProgressDialog(u"Postęp", "Przerwij...", 0, 0)

            if self.dlg.ui.rdbtnAktualizacja.isChecked():
                #usuniecie wszystkich rekordow o id_zd
                pgdlg.setLabelText(u"Usuwanie rekordów ze zbioru danych o id =  " + id_jed_rej)
                pgdlg.show()
                #naprawde dziwna sprawa, ale bez tego dwukrotnie powtorzonego slepp-applicationevent 
                #dialog się nie odświerza
                time.sleep(0.1)
                QApplication.processEvents()
                time.sleep(0.1)
                QApplication.processEvents()
                self.dlg.ui.peditOutput.appendPlainText(u"Rozpoczęcie usuwania aktualizowanych rekordów: " +  time.strftime("%Y-%m-%d %H:%M:%S"))
                rdbase.executeSQL("SELECT g5sp_delfromtables('" + id_jed_rej + "');")
                self.dlg.ui.peditOutput.appendPlainText(u"Zakończono usuwanie aktualizowanych rekordów: " +  time.strftime("%Y-%m-%d %H:%M:%S"))
            #import_file = str(self.swde_file.toUtf8()).decode('utf-8')

            try:
                #self.f = open(self.swde_file "r")
                self.f.seek(0.0)
                try:
                    self.dlg.ui.peditOutput.appendPlainText(u"Krok 2. Rozpoczynam import pliku: " + self.f.name + " " +  time.strftime("%Y-%m-%d %H:%M:%S"))
                    i = 0;
                    pgval = 0; #value progress bara
                    linianr = 0
                    step = ilosc_linii/100
                    pgdlg.setRange(0,100)
                    pgdlg.setLabelText(u"Trwa aktualizacja bazy .... ")
                    #pgdlg.setMinimumDuration(1000)
                    pgdlg.show()
                    QApplication.processEvents()
                    przerwanie = 0 # wartość 1 będzie świadczyć o tym, że albo zostało przerwane przez użytkownika albo z powodu błędu
                                    #w takim przypadku  nie zostanie wykonany commit do bazy
                    for line in self.f.readlines():
                        if i == step:
                            pgval = pgval + 1
                            pgdlg.setValue(pgval)
                            #QApplication.processEvents()
                            i = 0
                        if  pgdlg.wasCanceled():
                            przerwanie = 1
                            break
                        line = unicode(line, txtcodec)
                        i= i + 1
                        linianr+=1 #przyda sie jak sie program wypierniczy

                        pocz = StringBetweenChar(line, ',',0)

                        if pocz == "RO" or pocz == "RD" or pocz == "RC":
                            #line = unicode(line, txtcodec)
                            G5Table =  StringBetweenChar(line, ',',2)
                            g5id1_value = StringBetweenChar(line,',',3)
                            g5id2_value = StringBetweenChar(line,',',4)
                        if line[0:3] == "P,P":
                            #self.dlg.ui.peditOutput.appendPlainText(u"znaleziono ciąg line 0:3 = P,P")
                            str1 =  StringBetweenChar(line, ',', 2)
                            #self.dlg.ui.peditOutput.appendPlainText(u"str1 = " + str1 + u" o długości " + str(len(str1)) )
                            if str1 == u"G5PZG":
                                #self.dlg.ui.peditOutput.appendPlainText(u"wlazło")
                                nr =  StringBetweenChar(line, ',', 3)
                                #self.dlg.ui.peditOutput.appendPlainText(u"nr = " + nr)
                                #strnr = nr.rstrip(';\r')# trzeba usuwac pojedynczo czyli tak jak poniżej
                                strnr = nr.rstrip()# czyli jakiekolwiek białe znaki niezaleznie czy \n \r itp
                                strnr = strnr.rstrip(';')
                                #self.dlg.ui.peditOutput.appendPlainText(u"strnr = " + strnr)
                                #oldline = line
                                #self.dlg.ui.peditOutput.appendPlainText(u"oldline = " + oldline)
                                line = "P,G," + self.pzgdic[strnr] + ",;\n"
                                #self.dlg.ui.peditOutput.appendPlainText(u"line = " + line)
                                #self.dlg.ui.peditOutput.appendPlainText(u"Zastąpiono ciąg P,P >>" + oldline + "<< na >>" + line + "<< " + time.strftime("%Y-%m-%d %H:%M:%S"))


                        if G5Table in tableList:
                            #line = unicode(line, txtcodec)
                            colname = ""
                            colvalue = ""
                            znacznik = StringBetweenChar(line, ',',0)
                            if znacznik == "D" or znacznik == "WG":
                                line = line.rstrip()
                                line = line.rstrip(';') # szczególnie linie ze znacznikami WG zakończone są średnikiem 
                                line = line.strip("'")
                                line = line.strip('"')
                                line = line.replace("'", '')
                                line = line.replace('"', "")
                                colname = StringBetweenChar(line,',',1)
                                #zamiana nazw kolumn z polskimi znakami
                                if colname in plcharCols:
                                    colname = plcharCols[colname] 
                                colvalue = StringBetweenChar(line,',',3)
                                #dzialania wspolne dla wszystkich tablic
                                if colname in g5Cols[G5Table]:
                                    #G5RDZE w G5KLU nie jest typu tablicowego, natomiast w g5BUD
                                    #jest. Na szczescie w g5klu nie ma żadnego pola tablicowego
                                    if colname in arrayCols and G5Table != 'G5KLU':
                                        arraylist.append([colname,colvalue])

                                    else:
                                        collist.append(colname)
                                        valuelist.append(colvalue)

                                    #dzialania nietypowe
                                    #TODO przewidziec dla g5obr wyluskanie numeru obrebu do osobnego pola
                                    if colname == 'G5IDD' and G5Table == "G5DZE": #trzeba wyluskac numer dzialki i zapisac do oddzielnej kolumny
                                        #nr_dzialki = StringBetweenChar(colvalue, '.', 2)
                                        collist.append(u'nr')
                                        valuelist.append(StringBetweenChar(colvalue, '.', 2))
                                        #nr obrębu też się przyda
                                        collist.append(u'nrobr')
                                        valuelist.append(StringBetweenChar(colvalue, '.', 1))


                                    if colname == 'G5RPOD': #dla tabel g5udz i g5udw - wyglada to nastepujaco: "WG,G5RPOD,G5OSF,5465;"
                                                            #a więc najpierw mamy określenie do jakiej tabeli jest dowiązanie (osf, ins, mlz czy osz)
                                                            #a potem wartość wiązania w danej tabeli. Należy więc jeszcze wyciągnąć wartość po drugim ','
                                        collist.append(u'rpod_rodzaj')
                                        pod_rodzaj = StringBetweenChar(line, ',', 2)
                                        valuelist.append(pod_rodzaj)
                                        #kolumna zawierajaca polaczone ze soba wartosci 
                                        collist.append(u'id_podmiot')
                                        valuelist.append(colvalue + pod_rodzaj)
                                

                            elif znacznik == "K":
                                Kznak = StringBetweenChar(line, ',',1)#czyli albo '+;' albo '-;'
                                Kznak = Kznak[0]#pozostawienie tylko + albo -
                                newPoly = 1
                                polycount+=1
                               
                            elif znacznik == "P":
                                yvalue = StringBetweenChar(line, ',',2)
                                xvalue = StringBetweenChar(line, ',',3)
                                #print "xv:", xvalue, "yv:", yvalue
                                if transform == 1 :
                                    p1 = pyproj.Proj(pyproj4strFrom)
                                    p2 = pyproj.Proj(pyproj4strTo)
                                    x92, y92 = pyproj.transform(p1,p2,xvalue,yvalue)
                                    value = str(x92) + " " + str(y92)
                                else:
                                    value = xvalue + " " + yvalue
                                point.append( polycount)
                                point.append(newPoly)
                                point.append(Kznak)
                                point.append(value) 
                                pointslist.append(point)
                                #print point
                                point = []
                                newPoly = 0

                            elif znacznik[0] == "X": #czyli koniec definicji recordu
                                #print "2 line", line
                                #print "2 znacznik = ", znacznik, collist, valuelist
                                p = ""
                                p1 = ""
                                if len(pointslist)>0:
                                    for points in pointslist:
                                        if points[1] == 1:#newPoly
                                            #p1 = points[3]
                                            if points[0] == 1:#czyli pierwszy i byc moze jedyny polygon
                                                if srid == -1: #niezdefiniowany układ
                                                    p = "POLYGON(("
                                                else:
                                                    p = "@ST_GeomFromText(\'POLYGON(("
                                            else: #czyli ewentualne kolejne polygony
                                                p = p + p1 + "),("
                                            p1 = points[3]
                                        p = p + points[3] + ','
                                    if srid == -1:
                                        p = p + p1 + "))"
                                    else:
                                        p = p + p1 + "))\'," + srid + ")"
                                    collist.append("geom")
                                    valuelist.append(p)

                                #dodanie kolumn tablicowych
                                if len(arraylist) > 0:
                                    old_col = ''
                                    arraystr = "ARRAY["
                                    arraylist.sort()
                                    for col, val in arraylist:
                                        if old_col == '': #startujemy
                                            old_col = col
                                        if  col == old_col:
                                            arraystr += "\'"+ val + "\',"
                                        else: #nastąpiła zmiana columny
                                            arraystr = arraystr.rstrip(",")
                                            arraystr += "]"
                                            collist.append(old_col)
                                            valuelist.append(arraystr)
                                            old_col = col
                                            arraystr = "ARRAY[\'" + val + "\',"
                                    collist.append(old_col)
                                    arraystr = arraystr.rstrip(",")
                                    arraystr += ']'
                                    valuelist.append(arraystr)
                                    arraylist = []

                                #dodatnie id_jed_rej do kazdej tabeli
                                collist.append("id_zd")
                                valuelist.append(id_jed_rej)
                                #dodanie id1 i id2 do kazdej z tabel
                                collist.append("g5id1")
                                valuelist.append(g5id1_value)
                                collist.append("g5id2")
                                valuelist.append(g5id2_value)
                                #dodanie unikatowej kolumny - będzie stanowiła klucz główny w całej bazie
                                collist.append('tab_uid')
                                valuelist.append(id_jed_rej+g5id1_value)


                                #sprawdzenie czy jest jeszcze jakas tablica, ktora nie zostala dodana do valuelist
                                if len(arrayvalue)>0:
                                    collist.append(arrayname)
                                    values = ""
                                    for value in arrayvalue:
                                        values += "\'" + value.strip('[]') + "\',"
                                    values = values.rstrip(",")#usuniecie ostatniego przecinka
                                    valuelist.append(u"ARRAY[" + values + "]")
                                    arrayname = ''
                                    arrayvalue = []

                                rdg5Table[G5Table].insert(0, collist, valuelist)
                                if G5Table in insertdic:
                                    insertdic[G5Table] += 1
                                else:
                                    insertdic[G5Table] = 1

                                QApplication.processEvents() 
                                #obieg+=1
                                #if obieg == 1000:
                                #    rdbase.commit()
                                #    obieg = 0
                                obieg+=1
                                collist = []
                                valuelist = []
                                pointslist = []
                                Kznak = ""
                                polycount = 0
                                G5Table = ""

                                if self.dlg.ui.rdbtnImportTestowy.isChecked() and self.dlg.ui.rdbtnTestowyJEW.isChecked():
                                    #w tym przypadku nie ma co dalej ciągnąć pętli
                                    break
                        #i = i+1
                except Exception, ex:
                    cols = "["
                    values = "["
                    for col in collist:
                        cols +=  col + ", "
                    for value in valuelist:
                        values += value + ", "
                    cols += "]"
                    values += "]"
                    self.dlg.ui.peditOutput.appendPlainText(u"błąd: " + uni(G5Table) + " " +  uni(cols) + " " + uni(values) + "rekord nr: " + uni(str(obieg)) + "line = " + uni(line)+ " error: " + uni(str(ex)) )
                    przerwanie = 1

                finally:
                    if przerwanie == 1:
                        rdbase.rollback()
                        self.dlg.ui.peditOutput.appendPlainText("anulowano zapis do bazy: " + str(obieg) + u" rekordów: " + str(insertdic))
                    else:
                        rdbase.commit()
                        insstr = ""
                        for tab, ilosc in insertdic.items():
                            insstr += tab + ':' + str(ilosc) + '; '
                        self.dlg.ui.peditOutput.appendPlainText("zapisano do bazy: " + str(obieg) + u" rekordów: " + insstr)
                    #self.dlg.ui.peditOutput.appendPlainText("przerobiono lini: " + str(linianr))
                    #self.dlg.ui.peditOutput.appendPlainText(u"Plik zamknięty: " +  time.strftime("%Y-%m-%d %H:%M:%S"))
                    self.f.close()
            
            except IOError:
                self.dlg.ui.peditOutput.appendPlainText("IOError: " +  time.strftime("%Y-%m-%d %H:%M:%S"))

            #print "przerobiono lini: " + str(linianr)
            self.dlg.ui.peditOutput.appendPlainText("przerobiono lini: " + str(linianr))
            self.dlg.ui.peditOutput.appendPlainText("Koniec programu: " +  time.strftime("%Y-%m-%d %H:%M:%S"))


        def pzgExtend(self, swd_file):

            #krok 1 - wczytanie danych z pliku swde do struktury słownikowej
            self.dlg.ui.peditOutput.appendPlainText("Wczytywanie pliku: " + swd_file + " " +  time.strftime("%Y-%m-%d %H:%M:%S"))
            dic_conv_file =  swd_file + ".tmp"
            dic = {}
            dic_idx = ""
            try:
                f = open(swd_file, "r")
                i = 0
                try:
                    rp = 0
                    for line in f.readlines():
                        pocz = StringBetweenChar(line, ',',0)
                        if pocz == "RP":
                            tab = StringBetweenChar(line, ',',2)
                            if tab == "G5PZG":
                                nr = StringBetweenChar(line, ',', 3)
                                rp = 1
                                dic_idx = nr
                        elif rp == 1:
                            y =StringBetweenChar(line, ',', 2) 
                            x =StringBetweenChar(line, ',', 3) 
                            dic_value = y +"," + x
                            dic[nr] = dic_value
                            rp = 0
                            i += 1

                finally:
                    self.dlg.ui.peditOutput.appendPlainText(u"ilość puntów granicznych do zamiany: " + str(i))
                    f.close()
                    self.dlg.ui.peditOutput.appendPlainText(u"wczytano zawartośc pliku " + swd_file + " " +  time.strftime("%Y-%m-%d %H:%M:%S"))
            except IOError:
                   return 0
            

            #ponowne wczytanie pliku i zapisanie do nowego
            try:
                f = open(swd_file, "r")
                cf_dic = open(dic_conv_file, "w")
                try:
                    for line in f.readlines():
                        if line[0:3] == "P,P":
                            string =  StringBetweenChar(line, ',', 2)
                            #print string
                            if string == "G5PZG":
                                nr =  StringBetweenChar(line, ',', 3)
                                strnr = nr.rstrip(';\r')
                                new_line = "P,G,"+dic[strnr] + ",;\n"
                                cf_dic.write(new_line)
                        else:
                            cf_dic.write(line)
                finally:
                    f.close()
                    cf_dic.close()
                    self.dlg.ui.peditOutput.appendPlainText("Zapisano plik tymczasowy: " + dic_conv_file +  time.strftime("%Y-%m-%d %H:%M:%S"))
                    return 1
            except IOError:
                return 0

#==================================================================

def StringBetweenChar(string, char, nr):
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



















