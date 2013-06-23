# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_swdedzeinfo.ui'
#
# Created: Tue Jun 11 13:21:21 2013
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_swdeDzeInfo(object):
    def setupUi(self, swdeDzeInfo):
        swdeDzeInfo.setObjectName(_fromUtf8("swdeDzeInfo"))
        swdeDzeInfo.resize(401, 459)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/swdedzeinfo/swde-plug-info-22b.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        swdeDzeInfo.setWindowIcon(icon)
        self.verticalLayout_2 = QtGui.QVBoxLayout(swdeDzeInfo)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.txtFeedback = QtGui.QTextBrowser(swdeDzeInfo)
        self.txtFeedback.setObjectName(_fromUtf8("txtFeedback"))
        self.verticalLayout.addWidget(self.txtFeedback)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(18, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pbtnPrint = QtGui.QPushButton(swdeDzeInfo)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/swdedzeinfo/document-print.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pbtnPrint.setIcon(icon1)
        self.pbtnPrint.setObjectName(_fromUtf8("pbtnPrint"))
        self.horizontalLayout.addWidget(self.pbtnPrint)
        self.pbtnSave = QtGui.QPushButton(swdeDzeInfo)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/swdedzeinfo/gtk-save.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pbtnSave.setIcon(icon2)
        self.pbtnSave.setObjectName(_fromUtf8("pbtnSave"))
        self.horizontalLayout.addWidget(self.pbtnSave)
        self.pbtnClose = QtGui.QPushButton(swdeDzeInfo)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/swdedzeinfo/exit.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pbtnClose.setIcon(icon3)
        self.pbtnClose.setObjectName(_fromUtf8("pbtnClose"))
        self.horizontalLayout.addWidget(self.pbtnClose)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(swdeDzeInfo)
        QtCore.QObject.connect(self.pbtnClose, QtCore.SIGNAL(_fromUtf8("clicked()")), swdeDzeInfo.hide)
        QtCore.QMetaObject.connectSlotsByName(swdeDzeInfo)

    def retranslateUi(self, swdeDzeInfo):
        swdeDzeInfo.setWindowTitle(QtGui.QApplication.translate("swdeDzeInfo", "swdeDzeInfo", None, QtGui.QApplication.UnicodeUTF8))
        self.pbtnPrint.setText(QtGui.QApplication.translate("swdeDzeInfo", "Drukuj", None, QtGui.QApplication.UnicodeUTF8))
        self.pbtnSave.setText(QtGui.QApplication.translate("swdeDzeInfo", "Zapisz do pliku", None, QtGui.QApplication.UnicodeUTF8))
        self.pbtnClose.setText(QtGui.QApplication.translate("swdeDzeInfo", "Zamknij", None, QtGui.QApplication.UnicodeUTF8))

import resources_rc
