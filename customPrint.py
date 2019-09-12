from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from printGui import Ui_WindowPrint
from Curve_Trace_Reporting_Tool import *
from customReport import *


class MainPrint(QMainWindow, Ui_WindowPrint):
	def __init__(self,parent=None):
		super(MainPrint, self).__init__(parent)
		self.parent = parent
		self.setupUi(self)
		self.listViewName.hide()
		self.radioButtonSelection.clicked.connect(self.with_selection)
		self.listViewNamewithLim.hide()
		self.listViewNamewithRef.hide()
		self.radioButtonSelectionwithLim.clicked.connect(self.with_selectionLim)
		self.radioButtonSelectionwithRef.clicked.connect(self.with_selectionRef)
		self.pushButtonPrint.clicked.connect(self.actionPrint)
		self.selectedFiles=[]
		self.sel_item=[]
		self.label.setText("Max. number of figures : " +str(len(self.parent.main_mfiles)))



	def checkInput(self, title, path_pdf, path1):
		'''
		Check if user inputs are correct
		'''
		#print(path_pdf, title, number)
		flag = 1
		if os.path.exists(path1) == True :
			if title == '' or path_pdf == '' or len(os.listdir(path1)) == 0 :
				flag = 1
			else :
				flag = 0
		else :
			flag = 1
		return flag

	def actionPrint(self) :
		'''
		Process the printing GUI
		'''
		path_savefig = self.parent.path_fig+'\\'   # Path figures
		cqc_number=''
		text=''
		comment = ''
		path_pdf = QFileDialog.getExistingDirectory(self, 'Choose Backup folder', "Please, choose a folder to save the PDF report")  # Open the File Dialog Window

		while (len(text) == 0) or text+'.pdf' in os.listdir(path_pdf):
			text, ok = QInputDialog.getText(self, 'Title', 'Enter a report name:')
			if not ok :
				break
		title_report= text+".pdf"

		choix = QMessageBox.information(self, "Information", "Do you want to put a CQC number ?", QMessageBox.Yes | QMessageBox.No)
		if choix == QMessageBox.Yes : 
			while(len(cqc_number) == 0):
				cqc_number, ok = QInputDialog.getText(self, 'CQC Number', 'Enter a CQC number:')

		choix1 = QMessageBox.information(self, "Information", "Do you want to add a comment", QMessageBox.Yes | QMessageBox.No)
		if choix1 == QMessageBox.Yes : 
			while(len(comment) == 0 or  len(comment) > 300):
				comment, ok = QInputDialog.getText(self, 'Comment(s)', 'Enter your comment (300')


		choix2, valid = QInputDialog.getItem(self, "Number of charts per page", "Choose a number ", ("8", "15", "28"), 1)
		if valid == False :
			choix2 = 15
		
		if self.radioButtonSelection.isChecked() :
			folder = "All\\"
			self.sel=[]
			num_sel=[]
			A=self.listViewName.selectionModel()
			self.sel_item =A.selectedIndexes()
			for item in self.sel_item :
				num_sel.append(item.row())
			self.sel=self.get_name(num_sel)

		elif self.radioButtonSelectionwithLim.isChecked() :
			folder = "AllwithLimit\\"
			self.sel=[]
			num_sel=[]
			B=self.listViewNamewithLim.selectionModel()
			self.sel_item=B.selectedIndexes()
			for item in self.sel_item :
				num_sel.append(item.row())
			self.sel=self.get_name(num_sel)

		elif self.radioButtonSelectionwithRef.isChecked() :
			folder = "RefwithLimit\\"
			self.sel=[]
			num_sel=[]
			C = self.listViewNamewithRef.selectionModel()
			self.sel_item= C.selectedIndexes()
			for item in self.sel_item :
				num_sel.append(item.row())
			self.sel=self.get_name(num_sel)

		elif self.radioButtonRef.isChecked() :
			self.sel = []
			folder = "RefwithLimit\\"

		elif self.radioButtonFailwithLim.isChecked() :
			self.sel = []
			folder = "OnlyFail\\"

		elif self.radioButtonAllwithLim.isChecked() :
			self.sel=[]
			folder = "AllwithLimit\\"

		elif self.radioButtonAll.isChecked():
			self.sel = []
			folder = "All\\"

		else:
			self.sel = []
			folder = "1Device\\"
	
		if self.checkInput(text, path_pdf, path_savefig+folder) == 0:
			if len(cqc_number) > 0 :
				create_report_cqc(title_report, cqc_number, path_savefig, folder, self.sel, comment, path_pdf, choix2)
			else :
				create_report(title_report, path_savefig, folder, self.sel, comment, path_pdf, choix2)

			os.startfile(path_pdf+"//"+title_report) #Open PDF
			self.close()
		else :
			msgbox = QMessageBox.critical(self, "Warning", "Wrong user inputs. Cannot make the report.\n Please check the documentation")
			if msgbox == 1024 :
				self.close()
		
			
	def with_selection(self) :
		
		self.model=QStandardItemModel(self.listViewName)
		
		for ind, file in enumerate(self.parent.main_mfiles) :
			item=QStandardItem(file.replace("m_", "").replace(".csv", ""))
			self.model.appendRow(item)
		self.listViewName.setModel(self.model)
		self.listViewName.show()

		
	def with_selectionLim(self) :
		
		self.model=QStandardItemModel(self.listViewNamewithLim)
		
		for ind, file in enumerate(self.parent.main_mfiles) :
			item=QStandardItem(file.replace("m_", "").replace(".csv", ""))
			self.model.appendRow(item)
		self.listViewNamewithLim.setModel(self.model)
		self.listViewNamewithLim.show()

	def with_selectionRef(self) :
		
		self.model=QStandardItemModel(self.listViewNamewithRef)
		
		for ind, file in enumerate(self.parent.main_mfiles) :
			item=QStandardItem(file.replace("m_", "").replace(".csv", ""))
			self.model.appendRow(item)
		self.listViewNamewithRef.setModel(self.model)
		self.listViewNamewithRef.show()

	def get_name(self, num_sel):
		names =[]
		for ind, val in enumerate(self.parent.main_mfiles):
			if ind in num_sel:
				names.append(val)
		return names



if __name__ == '__main__':
	import sys
	from PyQt5 import QtGui
	import numpy as np


	app = QApplication(sys.argv)
	main = MainPrint()                       # create the application 
   
	main.show()                             # show the application

	sys.exit(app.exec_())                   # close the GUI event loop
