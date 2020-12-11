# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'welcome.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DialogWelcome(object):
    def setupUi(self, DialogWelcome):
        DialogWelcome.setObjectName("DialogWelcome")
        DialogWelcome.resize(600, 225)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("mfmc logo 2015 (square).png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        DialogWelcome.setWindowIcon(icon)
        self.groupBoxWelcome = QtWidgets.QGroupBox(DialogWelcome)
        self.groupBoxWelcome.setGeometry(QtCore.QRect(30, 20, 531, 161))
        self.groupBoxWelcome.setObjectName("groupBoxWelcome")
        self.pushButtonSel = QtWidgets.QPushButton(self.groupBoxWelcome)
        self.pushButtonSel.setGeometry(QtCore.QRect(390, 70, 91, 23))
        self.pushButtonSel.setObjectName("pushButtonSel")
        self.pushButtonExit = QtWidgets.QPushButton(self.groupBoxWelcome)
        self.pushButtonExit.setGeometry(QtCore.QRect(390, 110, 91, 23))
        self.pushButtonExit.setObjectName("pushButtonExit")
        self.pushButtonDir = QtWidgets.QPushButton(self.groupBoxWelcome)
        self.pushButtonDir.setGeometry(QtCore.QRect(390, 30, 91, 23))
        self.pushButtonDir.setObjectName("pushButtonDir")
        self.labelMFMC = QtWidgets.QLabel(self.groupBoxWelcome)
        self.labelMFMC.setGeometry(QtCore.QRect(10, 20, 311, 131))
        self.labelMFMC.setText("")
        self.labelMFMC.setPixmap(QtGui.QPixmap(":/mfmc logo 2015 (transparent).png"))
        self.labelMFMC.setScaledContents(True)
        self.labelMFMC.setObjectName("labelMFMC")

        self.retranslateUi(DialogWelcome)
        QtCore.QMetaObject.connectSlotsByName(DialogWelcome)

    def retranslateUi(self, DialogWelcome):
        _translate = QtCore.QCoreApplication.translate
        DialogWelcome.setWindowTitle(_translate("DialogWelcome", "Image to PDF Converter"))
        DialogWelcome.setWhatsThis(_translate("DialogWelcome", "Image to PDF Converter for Markham Family Medical Centre"))
        self.groupBoxWelcome.setTitle(_translate("DialogWelcome", "Image to PDF Converter"))
        self.pushButtonSel.setStatusTip(_translate("DialogWelcome", "Select files to convert to PDF"))
        self.pushButtonSel.setWhatsThis(_translate("DialogWelcome", "Select files to convert to PDF"))
        self.pushButtonSel.setText(_translate("DialogWelcome", "Select Files"))
        self.pushButtonExit.setStatusTip(_translate("DialogWelcome", "Exit from program"))
        self.pushButtonExit.setWhatsThis(_translate("DialogWelcome", "Exit from program"))
        self.pushButtonExit.setText(_translate("DialogWelcome", "Exit"))
        self.pushButtonDir.setStatusTip(_translate("DialogWelcome", "Select entire directory to convert to PDF"))
        self.pushButtonDir.setWhatsThis(_translate("DialogWelcome", "Select entire directory to convert to PDF"))
        self.pushButtonDir.setText(_translate("DialogWelcome", "Select Directory"))
import mfmcimg2pdf_rc