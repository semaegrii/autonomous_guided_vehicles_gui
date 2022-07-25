# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SplashWindow.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SplashScreen(object):
    def setupUi(self, SplashScreen):
        SplashScreen.setObjectName("SplashScreen")
        SplashScreen.resize(730, 508)
        self.centralwidget = QtWidgets.QWidget(SplashScreen)
        self.centralwidget.setObjectName("centralwidget")
        self.robot_border_frame = QtWidgets.QFrame(self.centralwidget)
        self.robot_border_frame.setGeometry(QtCore.QRect(530, -20, 192, 171))
        self.robot_border_frame.setStyleSheet("border:7px solid rgb(0, 119, 238);\n"
"border-radius: 20px;\n"
"background-color: rgb(236, 236, 236);")
        self.robot_border_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.robot_border_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.robot_border_frame.setObjectName("robot_border_frame")
        self.label = QtWidgets.QLabel(self.robot_border_frame)
        self.label.setGeometry(QtCore.QRect(0, 10, 191, 161))
        self.label.setStyleSheet("image: url(:/images/icons/agv_icons.png);")
        self.label.setText("")
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.optimak_logo_frame = QtWidgets.QFrame(self.centralwidget)
        self.optimak_logo_frame.setGeometry(QtCore.QRect(122, 90, 450, 261))
        self.optimak_logo_frame.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0.017, x2:1, y2:0.965864, stop:0 rgba(118, 118, 118, 255), stop:1 rgba(159, 159, 159, 255));\n"
"border-radius: 30px;")
        self.optimak_logo_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.optimak_logo_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.optimak_logo_frame.setObjectName("optimak_logo_frame")
        self.logo_frame = QtWidgets.QFrame(self.optimak_logo_frame)
        self.logo_frame.setGeometry(QtCore.QRect(0, -10, 161, 151))
        self.logo_frame.setStyleSheet("image: url(:/images/icons/OP-ENG.png);\n"
"background-color:none;")
        self.logo_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.logo_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.logo_frame.setObjectName("logo_frame")
        self.label_rd_center = QtWidgets.QLabel(self.optimak_logo_frame)
        self.label_rd_center.setGeometry(QtCore.QRect(160, 10, 181, 111))
        font = QtGui.QFont()
        font.setFamily("Berlin Sans FB")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_rd_center.setFont(font)
        self.label_rd_center.setStyleSheet("background-color: none;\n"
"color: rgb(0, 94, 189);")
        self.label_rd_center.setObjectName("label_rd_center")
        self.information_frame = QtWidgets.QFrame(self.optimak_logo_frame)
        self.information_frame.setGeometry(QtCore.QRect(131, 115, 291, 131))
        self.information_frame.setStyleSheet("background-color: rgb(221, 221, 221);\n"
"border-radius: 20px;\n"
"border: 7px solid rgb(151, 151, 151);")
        self.information_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.information_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.information_frame.setObjectName("information_frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.information_frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_description = QtWidgets.QLabel(self.information_frame)
        self.label_description.setStyleSheet("background-color: none;\n"
"border: none;\n"
"font: 8pt \"Siemens Sans Black\";")
        self.label_description.setText("")
        self.label_description.setAlignment(QtCore.Qt.AlignCenter)
        self.label_description.setObjectName("label_description")
        self.verticalLayout.addWidget(self.label_description)
        self.progressBar = QtWidgets.QProgressBar(self.information_frame)
        self.progressBar.setMaximumSize(QtCore.QSize(16777215, 25))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.progressBar.setFont(font)
        self.progressBar.setStyleSheet("QProgressBar{\n"
"    background-color: rgb(221, 221, 221);\n"
"    border:3px solid rgb(151, 151, 151);\n"
"    border-radius: 5px;\n"
"    text-align: center;\n"
"    color: rgb(0, 0, 0);}\n"
"QProgressBar::chunk{\n"
"    border-radius: 10px;\n"
"    background-color: qlineargradient(spread:pad, x1:0.933, y1:0.892045, x2:1, y2:1, stop:0 rgba(22, 238, 22, 206), stop:1 rgba(255, 255, 255, 255));\n"
"\n"
"}\n"
"")
        self.progressBar.setProperty("value", 5)
        self.progressBar.setTextVisible(False)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)
        self.listWidgetIslemler = QtWidgets.QListWidget(self.information_frame)
        font = QtGui.QFont()
        font.setFamily("Franklin Gothic Demi Cond")
        font.setPointSize(7)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.listWidgetIslemler.setFont(font)
        self.listWidgetIslemler.setStyleSheet("border: none;\n"
"font: 7pt \"Franklin Gothic Demi Cond\";")
        self.listWidgetIslemler.setObjectName("listWidgetIslemler")
        self.verticalLayout.addWidget(self.listWidgetIslemler)
        self.makine_frame = QtWidgets.QFrame(self.centralwidget)
        self.makine_frame.setGeometry(QtCore.QRect(0, 280, 251, 161))
        self.makine_frame.setStyleSheet("image: url(:/images/icons/strech_removed.png);")
        self.makine_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.makine_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.makine_frame.setObjectName("makine_frame")
        self.makine_border_frame = QtWidgets.QFrame(self.centralwidget)
        self.makine_border_frame.setGeometry(QtCore.QRect(10, 256, 234, 200))
        self.makine_border_frame.setStyleSheet("border:7px solid  rgb(0, 75, 156);\n"
"border-radius: 20px;\n"
"background-color: rgb(236, 236, 236);\n"
"")
        self.makine_border_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.makine_border_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.makine_border_frame.setObjectName("makine_border_frame")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(250, 355, 51, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("background-color: none;")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.makine_border_frame.raise_()
        self.robot_border_frame.raise_()
        self.optimak_logo_frame.raise_()
        self.makine_frame.raise_()
        self.label_2.raise_()
        SplashScreen.setCentralWidget(self.centralwidget)

        self.retranslateUi(SplashScreen)
        QtCore.QMetaObject.connectSlotsByName(SplashScreen)

    def retranslateUi(self, SplashScreen):
        _translate = QtCore.QCoreApplication.translate
        SplashScreen.setWindowTitle(_translate("SplashScreen", "MainWindow"))
        self.label_rd_center.setText(_translate("SplashScreen", "R&D CENTER \n"
"SOFTWARE \n"
"SOLUTIONS"))
        self.label_2.setText(_translate("SplashScreen", "@2021"))

import ikonlar_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    SplashScreen = QtWidgets.QMainWindow()
    ui = Ui_SplashScreen()
    ui.setupUi(SplashScreen)
    SplashScreen.show()
    sys.exit(app.exec_())

