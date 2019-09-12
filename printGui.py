# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'window_print.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *

class Ui_WindowPrint(object):
	def setupUi(self, WindowPrint):
		WindowPrint.setObjectName("WindowPrint")
		WindowPrint.resize(532, 464)
		self.centralwidget = QtWidgets.QWidget(WindowPrint)
		self.centralwidget.setObjectName("centralwidget")
		self.Layout = QtWidgets.QVBoxLayout(self.centralwidget)
		self.Layout.setObjectName("Layout")
		self.Mainwidget = QtWidgets.QWidget(self.centralwidget)
		self.Mainwidget.setObjectName("Mainwidget")
		self.vLayout = QtWidgets.QGridLayout(self.Mainwidget)
		self.vLayout.setContentsMargins(0, 0, 0, 0)
		self.vLayout.setObjectName("vLayout")
		self.radioButtonAll = QtWidgets.QRadioButton(self.Mainwidget)
		self.radioButtonAll.setObjectName("radioButtonAll")
		self.vLayout.addWidget(self.radioButtonAll, 0, 0, 1, 1)
		self.radioButtonAllwithLim = QtWidgets.QRadioButton(self.Mainwidget)
		self.radioButtonAllwithLim.setObjectName("radioButtonAllwithLim")
		self.vLayout.addWidget(self.radioButtonAllwithLim, 1, 0 , 1, 1)
		self.radioButtonFailwithLim = QtWidgets.QRadioButton(self.Mainwidget)
		self.radioButtonFailwithLim.setObjectName("radioButtonFailwithLim")
		self.vLayout.addWidget(self.radioButtonFailwithLim, 2, 0, 1, 1)
		self.radioButtonSelection = QtWidgets.QRadioButton(self.Mainwidget)
		self.radioButtonSelection.setObjectName("radioButtonSelection")
		self.vLayout.addWidget(self.radioButtonSelection, 3, 0, 1, 1)
		self.listViewName = QtWidgets.QListView(self.Mainwidget)
		self.listViewName.setSelectionMode(QAbstractItemView.MultiSelection)
		self.listViewName.setObjectName("listViewName")
		self.vLayout.addWidget(self.listViewName, 4, 0, 1, 1)
		
		self.radioButtonSelectionwithLim = QtWidgets.QRadioButton(self.Mainwidget)
		self.radioButtonSelectionwithLim.setObjectName("radioButtonSelectionwithLim")
		self.vLayout.addWidget(self.radioButtonSelectionwithLim, 5, 0, 1, 1)

		self.listViewNamewithLim = QtWidgets.QListView(self.Mainwidget)
		self.listViewNamewithLim.setSelectionMode(QAbstractItemView.MultiSelection)
		self.listViewNamewithLim.setObjectName("listViewNamewithLim")
		self.vLayout.addWidget(self.listViewNamewithLim, 6, 0, 1, 1)

		self.radioButtonSelectionwithRef = QtWidgets.QRadioButton(self.Mainwidget)
		self.radioButtonSelectionwithRef.setObjectName("radioButtonSelectionwithRef")
		self.vLayout.addWidget(self.radioButtonSelectionwithRef, 7, 0, 1, 1)

		self.listViewNamewithRef = QtWidgets.QListView(self.Mainwidget)
		self.listViewNamewithRef.setSelectionMode(QAbstractItemView.MultiSelection)
		self.listViewNamewithRef.setObjectName("listViewNamewithRef")
		self.vLayout.addWidget(self.listViewNamewithRef, 8, 0, 1, 1)

		self.radioButtonRef = QtWidgets.QRadioButton(self.Mainwidget)
		self.radioButtonRef.setObjectName("radioButtonRef")
		self.vLayout.addWidget(self.radioButtonRef, 9, 0, 1, 1)

		self.radioButtonOneDevice = QtWidgets.QRadioButton(self.Mainwidget)
		self.radioButtonOneDevice.setObjectName("radioButtonOneDevice")
		self.vLayout.addWidget(self.radioButtonOneDevice, 10, 0, 1, 1)

		self.label = QtWidgets.QLabel(self.Mainwidget)
		self.label.setObjectName("label")
		self.Layout.addWidget(self.Mainwidget)
		self.Layout.addWidget(self.label)
		
		self.pushButtonPrint = QtWidgets.QPushButton(self.Mainwidget)
		self.pushButtonPrint.setObjectName("pushButtonPrint")
		self.Layout.addWidget(self.pushButtonPrint)
		
		WindowPrint.setCentralWidget(self.centralwidget)
		self.menubar = QtWidgets.QMenuBar(WindowPrint)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 632, 21))
		self.menubar.setObjectName("menubar")
		WindowPrint.setMenuBar(self.menubar)
		self.statusbar = QtWidgets.QStatusBar(WindowPrint)
		self.statusbar.setObjectName("statusbar")
		WindowPrint.setStatusBar(self.statusbar)

		self.retranslateUi(WindowPrint)
		QtCore.QMetaObject.connectSlotsByName(WindowPrint)

	def retranslateUi(self, WindowPrint):
		_translate = QtCore.QCoreApplication.translate
		WindowPrint.setWindowTitle(_translate("WindowPrint", "WindowPrint"))
		self.radioButtonAll.setText(_translate("WindowPrint", "All Curves"))
		self.radioButtonAllwithLim.setText(_translate("WindowPrint", "All Curves with Limits"))
		self.radioButtonFailwithLim.setText(_translate("WindowPrint", "Only Failling Curves with Limits"))
		self.radioButtonSelection.setText(_translate("WindowPrint", "Selection"))
		self.radioButtonSelectionwithLim.setText(_translate("WindowPrint", "Selection with Limits"))
		self.radioButtonSelectionwithRef.setText(_translate("WindowPrint", "Selection Ref with Limits"))
		self.radioButtonRef.setText(_translate("WindowPrint", "Reference Curves with Limits"))
		self.radioButtonOneDevice.setText(_translate("WindowPrint", "One Device"))
		self.label.setText(_translate("WindowPrint", "TextLabel"))
		self.pushButtonPrint.setText(_translate("WindowPrint", "Print"))


if __name__ == "__main__":
	import sys

	app = QApplication(sys.argv)
	WindowPrint = QMainWindow()
	ui = Ui_WindowPrint()
	ui.setupUi(WindowPrint)
	WindowPrint.show()
	sys.exit(app.exec_())

