# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Profile.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Profile_ui(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(931, 500)
        Dialog.setStyleSheet("background-color: rgb(94, 94, 94);")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(60, 100, 221, 91))
        self.label.setStyleSheet("font: 28pt \"MS Shell Dlg 2\";\n"
"color: rgb(255, 255, 255);")
        self.label.setObjectName("label")
        self.home = QtWidgets.QPushButton(Dialog)
        self.home.setGeometry(QtCore.QRect(20, 20, 141, 31))
        self.home.setStyleSheet("background-color: rgb(255, 0, 0);\n"
"color: rgb(255, 255, 255);")
        self.home.setObjectName("home")
        self.ViewHistory = QtWidgets.QPushButton(Dialog)
        self.ViewHistory.setGeometry(QtCore.QRect(200, 20, 141, 31))
        self.ViewHistory.setStyleSheet("background-color: rgb(255, 0, 0);\n"
"color: rgb(255, 255, 255);")
        self.ViewHistory.setObjectName("ViewHistory")
        self.test = QtWidgets.QPushButton(Dialog)
        self.test.setGeometry(QtCore.QRect(370, 20, 151, 31))
        self.test.setStyleSheet("background-color: rgb(255, 0, 0);\n"
"color: rgb(255, 255, 255);")
        self.test.setObjectName("test")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(290, 230, 81, 31))
        self.label_2.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 12pt \"MS Shell Dlg 2\";")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(270, 280, 111, 41))
        self.label_3.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 12pt \"MS Shell Dlg 2\";")
        self.label_3.setObjectName("label_3")
        self.name = QtWidgets.QLabel(Dialog)
        self.name.setGeometry(QtCore.QRect(400, 235, 241, 21))
        self.name.setStyleSheet("font: 14pt \"MS Shell Dlg 2\";\n"
"color: rgb(255, 255, 255);")
        self.name.setText("")
        self.name.setObjectName("name")
        self.email = QtWidgets.QLabel(Dialog)
        self.email.setGeometry(QtCore.QRect(400, 290, 241, 31))
        self.email.setStyleSheet("font: 14pt \"MS Shell Dlg 2\";\n"
"color: rgb(255, 255, 255);")
        self.email.setText("")
        self.email.setObjectName("email")
        self.logout = QtWidgets.QPushButton(Dialog)
        self.logout.setGeometry(QtCore.QRect(760, 20, 151, 31))
        self.logout.setStyleSheet("background-color: rgb(255, 0, 0);\n"
"color: rgb(255, 255, 255);")
        self.logout.setObjectName("logout")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "  Profile :"))
        self.home.setText(_translate("Dialog", "Home"))
        self.ViewHistory.setText(_translate("Dialog", "View History"))
        self.test.setText(_translate("Dialog", "Profile"))
        self.label_2.setText(_translate("Dialog", "  Name :"))
        self.label_3.setText(_translate("Dialog", "  Email Id :"))
        self.logout.setText(_translate("Dialog", "LogOut"))


