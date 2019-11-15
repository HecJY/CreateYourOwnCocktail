# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'result.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form_R(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(855, 712)
        self.result_box = QtWidgets.QTextBrowser(Form)
        self.result_box.setGeometry(QtCore.QRect(90, 40, 681, 491))
        self.result_box.setObjectName("result_box")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(140, 550, 211, 51))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.satisify_btn = QtWidgets.QPushButton(Form)
        self.satisify_btn.setGeometry(QtCore.QRect(262, 627, 121, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.satisify_btn.setFont(font)
        self.satisify_btn.setObjectName("satisify_btn")
        self.no_btn = QtWidgets.QPushButton(Form)
        self.no_btn.setGeometry(QtCore.QRect(470, 630, 131, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.no_btn.setFont(font)
        self.no_btn.setObjectName("no_btn")
        self.cock_tail_name = QtWidgets.QLineEdit(Form)
        self.cock_tail_name.setGeometry(QtCore.QRect(350, 560, 291, 31))
        self.cock_tail_name.setObjectName("cock_tail_name")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Name Your Cocktail:"))
        self.satisify_btn.setText(_translate("Form", "Satisify"))
        self.no_btn.setText(_translate("Form", "Nah"))

