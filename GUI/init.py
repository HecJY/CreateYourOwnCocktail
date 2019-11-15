# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'init.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(684, 545)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(110, 160, 251, 61))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.num_src = QtWidgets.QLineEdit(Form)
        self.num_src.setGeometry(QtCore.QRect(360, 170, 251, 41))
        self.num_src.setObjectName("num_src")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(100, 280, 231, 51))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setKerning(False)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.sources = QtWidgets.QLineEdit(Form)
        self.sources.setGeometry(QtCore.QRect(360, 280, 251, 51))
        self.sources.setObjectName("sources")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(190, 60, 301, 51))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.show_source = QtWidgets.QPushButton(Form)
        self.show_source.setGeometry(QtCore.QRect(160, 390, 161, 41))
        self.show_source.setObjectName("show_source")
        self.create_btn = QtWidgets.QPushButton(Form)
        self.create_btn.setGeometry(QtCore.QRect(390, 390, 161, 41))
        self.create_btn.setObjectName("create_btn")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Number of sources expected:"))
        self.label_2.setText(_translate("Form", "Enter the expected source:"))
        self.label_3.setText(_translate("Form", "Create Your Own Cocktail"))
        self.show_source.setText(_translate("Form", "Show Available Souces"))
        self.create_btn.setText(_translate("Form", "Create!!"))

