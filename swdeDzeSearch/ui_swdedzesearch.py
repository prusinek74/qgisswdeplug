# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_swdedzesearch.ui'
#
# Created: Mon Jul  1 10:27:20 2013
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_swdeDzeSearch(object):
    def setupUi(self, swdeDzeSearch):
        swdeDzeSearch.setObjectName(_fromUtf8("swdeDzeSearch"))
        swdeDzeSearch.resize(422, 478)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/swdedzesearch/icons/swde-plug-search-22.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        swdeDzeSearch.setWindowIcon(icon)
        self.horizontalLayout_5 = QtGui.QHBoxLayout(swdeDzeSearch)
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label = QtGui.QLabel(swdeDzeSearch)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_4.addWidget(self.label)
        self.cmbxJEW = QtGui.QComboBox(swdeDzeSearch)
        self.cmbxJEW.setObjectName(_fromUtf8("cmbxJEW"))
        self.horizontalLayout_4.addWidget(self.cmbxJEW)
        self.chckJEWfiltr = QtGui.QCheckBox(swdeDzeSearch)
        self.chckJEWfiltr.setObjectName(_fromUtf8("chckJEWfiltr"))
        self.horizontalLayout_4.addWidget(self.chckJEWfiltr)
        self.horizontalLayout_4.setStretch(1, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_2 = QtGui.QLabel(swdeDzeSearch)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_3.addWidget(self.label_2)
        self.tbtnObrRefresh = QtGui.QToolButton(swdeDzeSearch)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/swdedzesearch/icons/view-refresh.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tbtnObrRefresh.setIcon(icon1)
        self.tbtnObrRefresh.setObjectName(_fromUtf8("tbtnObrRefresh"))
        self.horizontalLayout_3.addWidget(self.tbtnObrRefresh)
        self.cmbxOBR = QtGui.QComboBox(swdeDzeSearch)
        self.cmbxOBR.setObjectName(_fromUtf8("cmbxOBR"))
        self.horizontalLayout_3.addWidget(self.cmbxOBR)
        self.chckOBRfiltr = QtGui.QCheckBox(swdeDzeSearch)
        self.chckOBRfiltr.setObjectName(_fromUtf8("chckOBRfiltr"))
        self.horizontalLayout_3.addWidget(self.chckOBRfiltr)
        self.horizontalLayout_3.setStretch(2, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.label_3 = QtGui.QLabel(swdeDzeSearch)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_2.addWidget(self.label_3)
        self.leditDZE = QtGui.QLineEdit(swdeDzeSearch)
        self.leditDZE.setObjectName(_fromUtf8("leditDZE"))
        self.horizontalLayout_2.addWidget(self.leditDZE)
        self.chckDzeDokladnie = QtGui.QCheckBox(swdeDzeSearch)
        self.chckDzeDokladnie.setChecked(True)
        self.chckDzeDokladnie.setObjectName(_fromUtf8("chckDzeDokladnie"))
        self.horizontalLayout_2.addWidget(self.chckDzeDokladnie)
        self.pbtnDzeSearch = QtGui.QPushButton(swdeDzeSearch)
        self.pbtnDzeSearch.setObjectName(_fromUtf8("pbtnDzeSearch"))
        self.horizontalLayout_2.addWidget(self.pbtnDzeSearch)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.tabvDZE = QtGui.QTableView(swdeDzeSearch)
        self.tabvDZE.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.tabvDZE.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tabvDZE.setObjectName(_fromUtf8("tabvDZE"))
        self.verticalLayout.addWidget(self.tabvDZE)
        self.peditOut = QtGui.QPlainTextEdit(swdeDzeSearch)
        self.peditOut.setMaximumSize(QtCore.QSize(16777215, 60))
        self.peditOut.setReadOnly(True)
        self.peditOut.setObjectName(_fromUtf8("peditOut"))
        self.verticalLayout.addWidget(self.peditOut)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.pbtnLokalizuj = QtGui.QPushButton(swdeDzeSearch)
        self.pbtnLokalizuj.setObjectName(_fromUtf8("pbtnLokalizuj"))
        self.horizontalLayout.addWidget(self.pbtnLokalizuj)
        self.pbtnClose = QtGui.QPushButton(swdeDzeSearch)
        self.pbtnClose.setObjectName(_fromUtf8("pbtnClose"))
        self.horizontalLayout.addWidget(self.pbtnClose)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_5.addLayout(self.verticalLayout)

        self.retranslateUi(swdeDzeSearch)
        QtCore.QMetaObject.connectSlotsByName(swdeDzeSearch)

    def retranslateUi(self, swdeDzeSearch):
        swdeDzeSearch.setWindowTitle(QtGui.QApplication.translate("swdeDzeSearch", "swdeDzeSearch", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("swdeDzeSearch", "Jednostka ew.", None, QtGui.QApplication.UnicodeUTF8))
        self.chckJEWfiltr.setText(QtGui.QApplication.translate("swdeDzeSearch", "filtruj", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("swdeDzeSearch", "Obręb:", None, QtGui.QApplication.UnicodeUTF8))
        self.tbtnObrRefresh.setToolTip(QtGui.QApplication.translate("swdeDzeSearch", "<html><head/><body><p>odświeża listę obrębów, dla wybranej jednostki ewidencyjnej</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.tbtnObrRefresh.setText(QtGui.QApplication.translate("swdeDzeSearch", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.chckOBRfiltr.setText(QtGui.QApplication.translate("swdeDzeSearch", "filtruj", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("swdeDzeSearch", "Działka:", None, QtGui.QApplication.UnicodeUTF8))
        self.chckDzeDokladnie.setToolTip(QtGui.QApplication.translate("swdeDzeSearch", "<html><head/><body><p>Jeśli pole będzie odznaczone - zostaną wyszukane również działki o numerach podobnych do zadanego.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.chckDzeDokladnie.setText(QtGui.QApplication.translate("swdeDzeSearch", "dokładnie", None, QtGui.QApplication.UnicodeUTF8))
        self.pbtnDzeSearch.setText(QtGui.QApplication.translate("swdeDzeSearch", "szukaj", None, QtGui.QApplication.UnicodeUTF8))
        self.pbtnLokalizuj.setText(QtGui.QApplication.translate("swdeDzeSearch", "Lokalizuj na mapie", None, QtGui.QApplication.UnicodeUTF8))
        self.pbtnClose.setText(QtGui.QApplication.translate("swdeDzeSearch", "Zamknij", None, QtGui.QApplication.UnicodeUTF8))

import resources_rc
