# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AcilisPencere.ui'
##
# Created by: PyQt5 UI code generator 5.10.1
##
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AcilisPage(object):
    def setupUi(self, AcilisPage):
        AcilisPage.setObjectName("AcilisPage")
        AcilisPage.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(AcilisPage)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(AcilisPage)
        self.label.setMinimumSize(QtCore.QSize(150, 40))
        self.label.setMaximumSize(QtCore.QSize(80, 40))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.comboBoxKullanicilar = QtWidgets.QComboBox(AcilisPage)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.comboBoxKullanicilar.setFont(font)
        self.comboBoxKullanicilar.setObjectName("comboBoxKullanicilar")
        self.horizontalLayout.addWidget(self.comboBoxKullanicilar)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(AcilisPage)
        self.label_2.setMinimumSize(QtCore.QSize(150, 40))
        self.label_2.setMaximumSize(QtCore.QSize(80, 40))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.lineEditSifre = QtWidgets.QLineEdit(AcilisPage)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lineEditSifre.setFont(font)
        self.lineEditSifre.setObjectName("lineEditSifre")
        self.horizontalLayout_2.addWidget(self.lineEditSifre)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pushButtonLogin = QtWidgets.QPushButton(AcilisPage)
        self.pushButtonLogin.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.pushButtonLogin.setFont(font)
        self.pushButtonLogin.setStyleSheet("QPushButton{\n"
"    background-color: rgb(0, 255, 0);\n"
"    border: 2px solid;\n"
"    border-radius: 10px;\n"
"}\n"
"QPushButton::hover\n"
"{\n"
"    background-color: rgb(255, 255, 0);\n"
"\n"
"}")
        self.pushButtonLogin.setObjectName("pushButtonLogin")
        self.horizontalLayout_3.addWidget(self.pushButtonLogin)
        self.pushButtonCancel = QtWidgets.QPushButton(AcilisPage)
        self.pushButtonCancel.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.pushButtonCancel.setFont(font)
        self.pushButtonCancel.setStyleSheet("QPushButton{\n"
"    background-color: rgb(255,0, 0);\n"
"    border: 2px solid;\n"
"    border-radius: 10px;\n"
"}\n"
"QPushButton::hover\n"
"{\n"
"    background-color: rgb(255, 255, 0);\n"
"\n"
"}")
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.horizontalLayout_3.addWidget(self.pushButtonCancel)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi(AcilisPage)
        QtCore.QMetaObject.connectSlotsByName(AcilisPage)

    def retranslateUi(self, AcilisPage):
        _translate = QtCore.QCoreApplication.translate
        AcilisPage.setWindowTitle(_translate("AcilisPage", "Giriş Penceresi"))
        self.label.setText(_translate("AcilisPage", "KULLANICI  "))
        self.label_2.setText(_translate("AcilisPage", "ŞİFRE   "))
        self.pushButtonLogin.setText(_translate("AcilisPage", "GİRİŞ YAP"))
        self.pushButtonCancel.setText(_translate("AcilisPage", "VAZGEÇ"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AcilisPage = QtWidgets.QDialog()
    ui = Ui_AcilisPage()
    ui.setupUi(AcilisPage)
    AcilisPage.show()
    sys.exit(app.exec_())

