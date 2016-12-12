# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(950, 537)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.dist = QtGui.QLabel(Dialog)
        self.dist.setObjectName(_fromUtf8("dist"))
        self.verticalLayout.addWidget(self.dist)
        self.graphicsView = QtGui.QGraphicsView(Dialog)
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.verticalLayout.addWidget(self.graphicsView)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.stop = QtGui.QPushButton(Dialog)
        self.stop.setObjectName(_fromUtf8("stop"))
        self.horizontalLayout.addWidget(self.stop)
        self.init = QtGui.QPushButton(Dialog)
        self.init.setObjectName(_fromUtf8("init"))
        self.horizontalLayout.addWidget(self.init)
        self.start = QtGui.QPushButton(Dialog)
        self.start.setObjectName(_fromUtf8("start"))
        self.horizontalLayout.addWidget(self.start)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.dist.setText(_translate("Dialog", "TextLabel", None))
        self.stop.setText(_translate("Dialog", "Stop", None))
        self.init.setText(_translate("Dialog", "Init", None))
        self.start.setText(_translate("Dialog", "Start", None))

