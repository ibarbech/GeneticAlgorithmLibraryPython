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
        Dialog.resize(812, 537)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_3.addWidget(self.label)
        self.child_mode = QtGui.QComboBox(Dialog)
        self.child_mode.setObjectName(_fromUtf8("child_mode"))
        self.child_mode.addItem(_fromUtf8(""))
        self.child_mode.addItem(_fromUtf8(""))
        self.child_mode.addItem(_fromUtf8(""))
        self.child_mode.addItem(_fromUtf8(""))
        self.child_mode.addItem(_fromUtf8(""))
        self.child_mode.addItem(_fromUtf8(""))
        self.child_mode.addItem(_fromUtf8(""))
        self.verticalLayout_3.addWidget(self.child_mode)
        self.horizontalLayout_4.addLayout(self.verticalLayout_3)
        self.verticalLayout_9 = QtGui.QVBoxLayout()
        self.verticalLayout_9.setObjectName(_fromUtf8("verticalLayout_9"))
        self.label_7 = QtGui.QLabel(Dialog)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.verticalLayout_9.addWidget(self.label_7)
        self.selection_mode = QtGui.QComboBox(Dialog)
        self.selection_mode.setObjectName(_fromUtf8("selection_mode"))
        self.selection_mode.addItem(_fromUtf8(""))
        self.selection_mode.addItem(_fromUtf8(""))
        self.verticalLayout_9.addWidget(self.selection_mode)
        self.horizontalLayout_4.addLayout(self.verticalLayout_9)
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout_4.addWidget(self.label_2)
        self.mute = QtGui.QSpinBox(Dialog)
        self.mute.setMinimum(0)
        self.mute.setMaximum(100)
        self.mute.setProperty("value", 2)
        self.mute.setObjectName(_fromUtf8("mute"))
        self.verticalLayout_4.addWidget(self.mute)
        self.horizontalLayout_4.addLayout(self.verticalLayout_4)
        self.verticalLayout_5 = QtGui.QVBoxLayout()
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout_5.addWidget(self.label_3)
        self.elitism = QtGui.QSpinBox(Dialog)
        self.elitism.setMaximum(100)
        self.elitism.setProperty("value", 10)
        self.elitism.setObjectName(_fromUtf8("elitism"))
        self.verticalLayout_5.addWidget(self.elitism)
        self.horizontalLayout_4.addLayout(self.verticalLayout_5)
        self.verticalLayout_6 = QtGui.QVBoxLayout()
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout_6.addWidget(self.label_4)
        self.size_pool = QtGui.QSpinBox(Dialog)
        self.size_pool.setMaximum(100000)
        self.size_pool.setSingleStep(10)
        self.size_pool.setProperty("value", 1000)
        self.size_pool.setObjectName(_fromUtf8("size_pool"))
        self.verticalLayout_6.addWidget(self.size_pool)
        self.horizontalLayout_4.addLayout(self.verticalLayout_6)
        self.verticalLayout_7 = QtGui.QVBoxLayout()
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.label_5 = QtGui.QLabel(Dialog)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.verticalLayout_7.addWidget(self.label_5)
        self.cities = QtGui.QSpinBox(Dialog)
        self.cities.setMinimum(10)
        self.cities.setMaximum(200)
        self.cities.setProperty("value", 10)
        self.cities.setObjectName(_fromUtf8("cities"))
        self.verticalLayout_7.addWidget(self.cities)
        self.horizontalLayout_4.addLayout(self.verticalLayout_7)
        self.high_low = QtGui.QCheckBox(Dialog)
        self.high_low.setObjectName(_fromUtf8("high_low"))
        self.horizontalLayout_4.addWidget(self.high_low)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.verticalLayout.addLayout(self.verticalLayout_2)
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
        self.label.setText(_translate("Dialog", "CHILD MODE", None))
        self.child_mode.setItemText(0, _translate("Dialog", "CHILD_FLIP", None))
        self.child_mode.setItemText(1, _translate("Dialog", "CHILD_FLIP_TOURNAMENT_DETERMINISTIC", None))
        self.child_mode.setItemText(2, _translate("Dialog", "CHILD_FLIP_TOURNAMENT_PROBABILISTIC", None))
        self.child_mode.setItemText(3, _translate("Dialog", "CHILD_SPLIT", None))
        self.child_mode.setItemText(4, _translate("Dialog", "CHILD_SPLIT_TOURNAMENT_DETERMINISTIC", None))
        self.child_mode.setItemText(5, _translate("Dialog", "CHILD_SPLIT_TOURNAMENT_PROBABILISTIC", None))
        self.child_mode.setItemText(6, _translate("Dialog", "CHILD_MEAN", None))
        self.label_7.setText(_translate("Dialog", "SELECTION MODE", None))
        self.selection_mode.setItemText(0, _translate("Dialog", "FILL", None))
        self.selection_mode.setItemText(1, _translate("Dialog", "ROULETTE", None))
        self.label_2.setText(_translate("Dialog", "MUTE %", None))
        self.label_3.setText(_translate("Dialog", "ELITISM %", None))
        self.label_4.setText(_translate("Dialog", "SIZE POOL", None))
        self.label_5.setText(_translate("Dialog", "CITIES", None))
        self.high_low.setText(_translate("Dialog", "Sort high to low", None))
        self.dist.setText(_translate("Dialog", "TextLabel", None))
        self.stop.setText(_translate("Dialog", "Stop", None))
        self.init.setText(_translate("Dialog", "Init", None))
        self.start.setText(_translate("Dialog", "Start", None))

