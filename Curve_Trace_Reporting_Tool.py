#!/usr/bin/env python
#-*- coding: utf-8 -*-

from MyWindow import Ui_MainWindow
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from folder_analysis import *
import matplotlib.pyplot as plt
import time
import shutil
from main import *
import numpy as np
from limit_cal import *
from matplotlib.ticker import EngFormatter
from mpldatacursor import DataCursor
from matplotlib.backends.backend_qt5agg import (FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from customPrint import *
from printGui import Ui_WindowPrint


class MainFunc(QMainWindow, Ui_MainWindow):
	def __init__(self, ):
		super(MainFunc, self).__init__()
		self.setupUi(self)

		self.widget_4.hide()				#Hide tab widget

		self.init_variables()

		# Menu Actions
		# Connect buttons to functions
		self.actionOpen.triggered.connect(self.fileDialog_open)
		self.actionExit.triggered.connect(self.close_window)
		self.actionPrint.triggered.connect(self.printing_window)
		self.actionHelp.triggered.connect(self.open_help)
		self.checkBox.clicked.connect(self.plot_allwithlim)
		self.checkBox_2.clicked.connect(self.plot_fail)
		self.checkBox_3.clicked.connect(self.plot_refwithlim)
		self.checkBox_4.clicked.connect(self.plot_all)
		self.checkBox_5.clicked.connect(self.plot_device)


	def init_variables(self):
		'''
		Initialize variables
		'''
		self.product_name = ''				#Product name
		self.main_cfiles = [] 				#List with pin-connection file names (Example : c_P1_BATV2_GND)
		self.main_mfiles = [] 				#List with measurement file name (Example : m_P1_BATV2_GND)

		self.path_temp = ''					#Data temp folder path
		self.path_lib = '' 					#Settings folder path
		self.path_ref = '' 					#Reference curves backup path
		self.path_fig = '' 					#Charts curves backup path
		self.path_limit = '' 				#Limits curves backup path

		self.deviceName= '' 				#Device name
		self.deviceNode='' 					#Device node 
		self.listTest=[] 					#List with tests names from xml-file
		self.padName=[] 					#List with SMU names

		self.fig = [] 						#List with all charts
		self.canvas = [] 					#List with all canvas
		self.toolbar = [] 					#List with all toolbars
		self.ax1f1 = []						#List with all curve-axis
		self.my_widget_list = [] 			#List with all matplotlib widgets
		self.my_layout_list = []			#List with all layouts for matplotlib widgets

		self.failure_list = [] 				#List with all failed curves index
		self.settings = []					#List with all settings
		self.pins_list = []					#List pins connections
		self.flag_deviation = [] 			#List with deviation classifications


	def open_help(self):
		os.startfile("Documentation Curve Trace Reporting Tool.pptx")


	def fileDialog_open(self):
		'''
		Open a window used to choose the device directory. After this choice, it calls the treatment function and creates new widgets for the graphs
		'''
		self.checkBox.setChecked(False)
		self.checkBox_2.setChecked(False)
		self.checkBox_3.setChecked(False)
		self.checkBox_4.setChecked(False)
		self.checkBox_5.setChecked(False)
		# Initialization
		self.widget_4.hide()  				#Hide tab widget
		self.rem_plot() 					#Remove all charts
		self.init_variables() 
		self.widget_4.show()                #Show tab widget
		self.checkBox_2.hide() 				#Hide tab "Failed Curves"

		# Choose folder for analysis
		self.folder = QFileDialog.getExistingDirectory(self, 'Choose an ACS Basic project')			#Open the file dialog window to select the folder
		self.product_name = str(self.folder).split("/")[-1] 									#Collect the product name
		flag = mainDirAnalysis(self.folder) 													#Flag older nalysis 
		
		if flag == 3 : 						#Flag = 3 --> Ok / Flag != 3 --> Nok
			self.path_temp = str(self.folder)+'\\temp\\' 										#Path to data
			self.path_lib = str(self.folder)+'\\lib\\' 											#Path to settings data (lib folder) 
			try : 
				self.read_xmlFile(str(self.folder)+'\\'+str(self.product_name) +'.xml') 		#Collect information from xml file
			except :
				msgbox = QMessageBox.critical(self, " XML Reading Error ","Can not parse the XML File.\nPlease, choose another project.")	
			#print(self.deviceName, self.product_name)
			if self.deviceName in self.product_name : 											#Match between the folder name and the device name (from the xml-file)
				self.main_processing(self.product_name, self.path_temp, self.path_lib) 			#Start analysis
				self.create_widget(len(self.main_mfiles)) 										#Create widgets for charts
			else :
				msgbox = QMessageBox.critical(self, " Match Error ","The XML file does not have the same name as the folder name.\nPlease, choose another project.")
		else :
			#Missing folder(s), no xml-file or more than a xml-file 
			msgbox = QMessageBox.critical(self, "Folder Error","The selected directory is not correct.\nPlease, choose another project.")


	def create_widget(self, length):       
		'''
		This function creates widget that will contain matplotlib window.
		'''
		for i in range(length):
			#Widget definition
			self.W=QWidget(self.scrollAreaWidgetContents)
			sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
			sizePolicy.setHorizontalStretch(0)
			sizePolicy.setVerticalStretch(0)
			self.W.setSizePolicy(sizePolicy)
			self.W.setMinimumSize(QtCore.QSize(525, 540))
			self.W.setMaximumSize(QtCore.QSize(525, 540))
			self.W.setObjectName("mplwindow"+str(i))
			self.L=QVBoxLayout(self.W)
			self.L.setContentsMargins(0, 0, 0, 0)
			self.L.setObjectName("mplvl"+str(i))
			self.my_widget_list.append(self.W)
			self.my_layout_list.append(self.L)
		j=0
		counter_row = 0
		for i in range(length): 			#Loop putting 3 matplotlib widgets per row
			if i % 3 == 0 :
				j = i/3
				counter_row = 0 
			self.gridLayout.addWidget(self.my_widget_list[i], j, counter_row, 1, 1) 			#Add widget to the layout
			counter_row += 1


	def close_window(self):
		'''
		This function closes the GUi.
		'''
		self.close()


	def printing_window(self) : 
		'''
		This function opens the printing GUI.
		'''
		if len(self.path_fig) > 0 :
			Print=MainPrint(self) 				#Call main printing function 
			Print.show() 						#Show the GUI
		else :
			QMessageBox.information(self, "Warning", "Please open a project before using the printing GUI.")



	def rem_plot(self):
		'''
		This function removes all graphs and creates charts widgets
		'''
		#Remove widgets
		for i in range(len(self.canvas)-1, -1, -1):
			self.my_layout_list[i].removeWidget(self.canvas[i]) 								#Remove the widget
			self.canvas[i].close()
			self.my_layout_list[i].removeWidget(self.toolbar[i]) 								#Remove the toolbar
			self.toolbar[i].close()

		#Reset variables
		self.canvas=[]
		self.toolbar=[]
		self.ax1f1=[]
		self.fig=[]

		#Draw charts
		self.create_fig()
		for ind2, file2 in enumerate(self.main_mfiles) :
			self.my_widget_list[ind2].show() 													#Show new widget


	def create_fig(self):
		'''
		Create the correct number of figures used to plot the graphs
		'''
		for i,file in enumerate(self.main_mfiles):
			fig1=plt.figure() 
			name=str(file)
			fig1.suptitle(name.replace("m_", "").replace(".csv", "").replace("_", " "), fontsize=14, fontweight='bold')		#Set a name on the chart
			self.fig.append(fig1) 			#Add the new figure to the figures list

	def addmpl(self, fig, num, folder):
		'''
		This function adds matplotlib window and a toolbar into a widget 
		'''
		self.canvas.append(FigureCanvas(fig))
		self.my_layout_list[num].addWidget(self.canvas[num])
		self.canvas[num].draw()
		self.canvas[num].print_figure(folder+"//"+str(self.main_mfiles[num].replace("m_", "").replace(".csv", ""))+'.png')
		self.toolbar.append(NavigationToolbar(self.canvas[num], self.my_widget_list[num], coordinates=True))
		self.my_layout_list[num].addWidget(self.toolbar[num])


	def format_axis(self, ax, file, index):
		'''
		This function sets axis parameters and legend
		'''
		#Set axis ticks
		ax.grid()
		formatterV = EngFormatter(unit='V')
		ax.xaxis.set_major_formatter(formatterV)
		formatterA = EngFormatter(unit='A')
		ax.yaxis.set_major_formatter(formatterA)
		ax.tick_params(axis='both', labelsize=11)
		ax.legend(loc = 'best', prop = {'size':11}) 											#Set the legend at the best position

		#Write additionnal information (Pin connections, Bias,... )
		string = ""  						#Init string 
		if "SMU1Hi" in str(self.pins_list[index]) :
			string += " SMU1: "+str(self.pins_list[index]["SMU1Hi"]).replace("[","").replace("]","  ")
		if "SMU2Hi" in str(self.pins_list[index]) :
			if "Bias" in self.settings[index]["SMU2"][0]:
				string += " SMU2 ("+str(self.settings[index]["SMU2"][1])+"V): "+str(self.pins_list[index]["SMU2Hi"]).replace("[","").replace("]","  ")
			else :
				string += " SMU2: "+str(self.pins_list[index]["SMU2Hi"]).replace("[","").replace("]","  ")
		if "SMU3Hi" in str(self.pins_list[index]) :
			if "Bias" in self.settings[index]["SMU4"][0]:
				string += " SMU3 ("+str(self.settings[index]["SMU3"][1])+"V): "+str(self.pins_list[index]["SMU3Hi"]).replace("[","").replace("]","  ")
			else :
				string += " SMU3: "+str(self.pins_list[index]["SMU3Hi"]).replace("[","").replace("]","  ")
		if "SMU4Hi" in str(self.pins_list[index]) :
			if "Bias" in self.settings[index]["SMU4"][0]:
				string += " SMU4 ("+str(self.settings[index]["SMU4"][1])+"V): "+str(self.pins_list[index]["SMU4Hi"]).replace("[","").replace("]","  ")
			else :
				string += " SMU4: "+str(self.pins_list[index]["SMU4Hi"]).replace("[","").replace("]","  ")
		if "IVCommonLo" in str(self.pins_list[index]) :
			string += "\n CommonLo:"+str(self.pins_list[index]["IVCommonLo"]).replace("[","").replace("]","  ")
		ax.set_title(string, fontsize=8) 	#Set the string as title


	def read_xmlFile(self, xmlFile):
		'''
		This function collects information from the xml-file
		'''
		root = parse_xml(xmlFile)
		self.deviceName, self.deviceNode = get_device_name(root) 								#Collect device name
		self.listTest =  get_test_mapping(self.deviceNode) 										#Collect the test model (mapping)
		self.padName = get_pad_name(self.deviceNode) 											#Collect SMUs name


	def create_newLim(self, files, path_temp, path_limit, path_ref, product_name, settings, data_cal):
		'''
		This function creates new limits and reference curves
		'''
		#Back Up
		try :
			os.makedirs(path_limit+product_name+"\\") 											#Create new folder for limits
			os.makedirs(path_ref+product_name+"\\") 											#Create new folder for reference curves
		except :
			QMessageBox.information(self, "Information", "Delete previous limits backup. ")

		#Limits an reference curves calculation
		multiple,valid = QInputDialog.getInt(self, "Sigma", "Enter a multiple for sigma ",6 , 1 ,9, 1) 	#Input value between 4 to 9
		if valid == True :
			#Draw progress bar
			progressBar2 = QProgressDialog("Calculation in progress...", "Cancel", 0, len(files), self)
			progressBar2.setWindowTitle("New limits calculation")
			progressBar2.setModal(True)
			progressBar2.show()
			for i, file in enumerate(files):
				progressBar2.setValue(i)
				nb_device=get_nb_device(file, self.path_temp) 							#Number of devices
				ref = get_reference_curve(data_cal[i][0], data_cal[i][1]) 				#Reference curve calculation
				if len(ref[0]) > 2 or len(ref[1]) > 2:
					limit_table=get_limits(data_cal[i][0], data_cal[i][1], nb_device, settings[i]["SMU1"][6], settings[i]["SMU1"][7], 
										ref, settings[i]["SMU1"][4], abs((settings[i]["SMU1"][2]-settings[i]["SMU1"][1])/settings[i]["SMU1"][3]), multiple) 	#Limits calculation
					save_limits(file, self.path_limit, product_name, limit_table) 					#Save limits
					save_reference(file, self.path_ref, product_name, ref) 							#Save reference curves
				else:
				
					QMessageBox.information(self, "Information", "Unable to calculate limits for the test :"+file+" \nPlease do the test again with more points.")
					
				if(progressBar2.wasCanceled()) :
					break
			progressBar2.setValue(len(files))
			QMessageBox.information(self, "Information", "End of calculation")


	def erase_folder(self, folder):
		'''
		This function deletes a folder
		'''
		shutil.rmtree(folder)


	def plot_allwithlim(self):
		'''
		This function displays charts with all curves, limits and reference curves
		'''
		if findLimits(self.product_name, self.path_limit) == 1 : # --> File folder_analysis.py
			#Uncheck all tabs except the selected one
			self.checkBox_2.setChecked(False)
			self.checkBox_3.setChecked(False)
			self.checkBox_4.setChecked(False)
			self.checkBox_5.setChecked(False)
			self.checkBox_5.setCheckable(False)
			self.checkBox_2.setCheckable(False)
			self.checkBox_3.setCheckable(False)
			self.checkBox_4.setCheckable(False)

			self.rem_plot() 
			
			if os.path.exists(self.path_fig+"AllwithLimit"):
				self.erase_folder(self.path_fig+"AllwithLimit")
			os.mkdir(self.path_fig+"AllwithLimit") 											#Create folder to save charts

			lines = []
			for ind,file in enumerate(self.main_mfiles):
				#Loop collect data, limits and ref and plot all in a chart
				data = get_allpts(file, self.path_temp, self.settings[ind]["SMU1"][4], self.padName) #Collect all data
				
				self.ax1f1=self.fig[ind].add_subplot(111)
				try :
					limits=recover_limits(file, self.path_limit, self.product_name)             #Collect limits 
					ref=recover_reference(file, self.path_ref,  self.product_name)             	#Collect reference curve 
					self.ax1f1.plot(limits[0],limits[2], '--r', linewidth = 2, label ='Limits') #Plot high limit
					self.ax1f1.plot(limits[1],limits[3], '--r', linewidth = 2)             		#Plot low limit
					self.ax1f1.plot(ref[0],ref[1], 'green' , linewidth = 2, label = 'Ref') 		#Plot ref
				except:
					msgBo = QMessageBox.information(self, "Information", "No Limits for the file :"+str(file))

				self.format_axis(self.ax1f1, file, ind)
				for i in range(len(data[0])):  
					line2, = self.ax1f1.plot(data[0][i], data[1][i], label = "Append "+str(i))     	#Plot all curves
					lines.append(line2) 															#Add line for the annotation/cursor

			for i in range(len(self.fig)):
				main.addmpl(self.fig[i],i,self.path_fig+"AllwithLimit") 					#See function def

			for i in range(len(lines)):
				DataCursor(lines[i], display='single', draggable=True, bbox=None, formatter='{label}'.format) 	#Add a cursor on the chart for each curve (just by clicking on the curve)

			self.checkBox_2.setCheckable(True)
			self.checkBox_3.setCheckable(True)
			self.checkBox_4.setCheckable(True)
			self.checkBox_5.setCheckable(True)
		else : 
			msgBox = QMessageBox.information(self, "Warning", "Limits not found for this product.")
			self.checkBox.setChecked(False)


	def plot_all(self):
		'''
		This function displays charts with all curves (NO LIMITS, NO REF CURVE)
		'''
		#Uncheck all tabs except the selected one
		self.checkBox_2.setChecked(False)
		self.checkBox_3.setChecked(False)
		self.checkBox.setChecked(False)
		self.checkBox_5.setChecked(False)
		self.checkBox_2.setCheckable(False)
		self.checkBox_3.setCheckable(False)
		self.checkBox.setCheckable(False)
		self.checkBox_5.setCheckable(False)

		self.rem_plot()
		
		if os.path.exists(self.path_fig+"All"):
			self.erase_folder(self.path_fig+"All")
		os.mkdir(self.path_fig+"All")  							#Create folder to save charts

		lines = []
		for ind, file in enumerate(self.main_mfiles):
			#Loop collect data and plot all in a charts
			data = get_allpts(file, self.path_temp, self.settings[ind]["SMU1"][4], self.padName) 	#Collect all data
			self.ax1f1 = self.fig[ind].add_subplot(111)
			self.format_axis(self.ax1f1, file, ind)
			for i in range(len(data[0])):  
				line1, = self.ax1f1.plot(data[0][i], data[1][i], label = "Append "+str(i))     						#Plot all curves
				lines.append(line1)
		for i in range(len(self.fig)):
			main.addmpl(self.fig[i],i,self.path_fig+"All")  	#See function def          
		for i in range(len(lines)):
			DataCursor(lines[i], display='single', draggable=True, bbox=None, formatter='{label}'.format) 			#Add a cursor on the chart for each curve (just by clicking on the curve)

		self.checkBox_2.setCheckable(True)
		self.checkBox_3.setCheckable(True)
		self.checkBox.setCheckable(True)
		self.checkBox_5.setCheckable(True)


	def plot_refwithlim(self):
		'''
		This function displays charts with limits and reference curves
		'''
		if findLimits(self.product_name, self.path_limit) == 1 :
			#Uncheck all tabs except the selected one
			self.checkBox_2.setChecked(False)
			self.checkBox.setChecked(False)
			self.checkBox_4.setChecked(False)
			self.checkBox_5.setChecked(False)
			self.checkBox_2.setCheckable(False)
			self.checkBox.setCheckable(False)
			self.checkBox_4.setCheckable(False)
			self.checkBox_5.setCheckable(False)

			self.rem_plot()

			
			if os.path.exists(self.path_fig+"RefwithLimit") :
				self.erase_folder(self.path_fig+"RefwithLimit")
			os.mkdir(self.path_fig+"RefwithLimit") #Create folder to save charts

			for ind, file in enumerate(self.main_mfiles) :
				self.ax1f1=self.fig[ind].add_subplot(111)
				try:
					limits=recover_limits(file, self.path_limit, self.product_name)             			#Collect limits 
					ref=recover_reference(file, self.path_ref,  self.product_name)             				#Collect reference curve .
					self.ax1f1.plot(limits[0],limits[2], 'x-r', linewidth = 2, label = 'Limits')            #Plot high limit
					self.ax1f1.plot(limits[1],limits[3], 'x-r', linewidth = 2)             					#Plot low limit
					self.ax1f1.plot(ref[0],ref[1], 'o-g' , linewidth = 2, label = 'Ref')             
				except:
					msgBo = QMessageBox.information(self, "Information", "No Limits for the file :"+str(file))


				
				self.format_axis(self.ax1f1, file, ind) 
			for i in range(len(self.fig)):
				main.addmpl(self.fig[i],i,self.path_fig+"RefwithLimit") 								#See function def

			self.checkBox_2.setCheckable(True)
			self.checkBox.setCheckable(True)
			self.checkBox_4.setCheckable(True)
			self.checkBox_5.setCheckable(True)
		else : 
			msgBox = QMessageBox.information(self, "Error Limits", "Limits not found for this product.")
			self.checkBox_3.setChecked(False)


	def plot_fail(self):
		'''
		This function displays all charts with failed curves, limits and ref
		'''
		#Uncheck all tabs except the selected one	
		if findLimits(self.product_name, self.path_limit) == 1 :	
			self.checkBox.setChecked(False)
			self.checkBox_3.setChecked(False)
			self.checkBox_4.setChecked(False)
			self.checkBox_5.setChecked(False)
			self.checkBox.setCheckable(False)
			self.checkBox_3.setCheckable(False)
			self.checkBox_4.setCheckable(False)
			self.checkBox_5.setCheckable(False)

			self.rem_plot()
			
			index_fail = []
			counter = 0
			
			if os.path.exists(self.path_fig+"OnlyFail") :
				self.erase_folder(self.path_fig+"OnlyFail")
			os.mkdir(self.path_fig+"OnlyFail") 																				#Create folder to save charts

			lines = []
			for ind2, file2 in enumerate(self.main_mfiles) :

				if  len(self.failure_list[ind2][0]) > 0 :
					# print("Function : plot_fail / file", file2)
					# print(self.failure_list[ind2][0])
					# print(self.flag_deviation[ind2])
					index_fail.append(ind2)
					data = get_allpts(file2, self.path_temp, self.settings[ind2]["SMU1"][4],  self.padName) #Collect all data
					self.ax1f1=self.fig[ind2].add_subplot(111)
					try :
						limits=recover_limits(file2, self.path_limit, self.product_name)              							#Collect limits 
						ref=recover_reference(file2, self.path_ref,  self.product_name)              							#Collect reference curve 
						self.ax1f1.plot(limits[0],limits[2], '--r',linewidth = 2,  label = 'Limits')         					#Plot high limit
						self.ax1f1.plot(limits[1],limits[3], '--r', linewidth = 2)         		
					except:
						msgBo = QMessageBox.information(self, "Information", "No Limits for the file :"+str(file2))
						#Plot low limit         
					self.failure_list[ind2][0].sort()
					self.ax1f1.plot(ref[0],ref[1], 'green' ,linewidth = 2, label = 'Ref')  
					self.format_axis(self.ax1f1, file2, ind2) 
					for k, j in enumerate(self.failure_list[ind2][0]):
						line4, =  self.ax1f1.plot(data[0][j], data[1][j], label = "Append"+str(j)+" : "+str(self.flag_deviation[ind2][k]) )		# Plot the failed curves
						lines.append(line4)
					
				elif len(self.failure_list[ind2][0]) == 0 :
					counter += 1
					#self.my_widget_list[ind2].hide()
		
					if counter == len(self.main_mfiles) :
						QMessageBox.information(self, "Information", "No Failed Curves")   
			for i in range(len(self.fig)):
				main.addmpl(self.fig[i],i,self.path_fig+"OnlyFail")  
		

			for i in range(len(lines)):
				DataCursor(lines[i], display='single', draggable=True, bbox=None, formatter='{label}'.format) 					#Add a cursor on the chart for each curve (just by clicking on the curve)
			for k, value in enumerate(os.listdir(self.path_fig+"OnlyFail")):
				self.delete_empty_fig(value, self.path_fig+"OnlyFail")

			self.checkBox_5.setCheckable(True)
			self.checkBox_4.setCheckable(True)
			self.checkBox_3.setCheckable(True)
			self.checkBox.setCheckable(True)
		else:
			msgBox = QMessageBox.information(self, "Warning", "Limits not found for this product.")
			self.checkBox_2.setChecked(False)


	def plot_device(self):
		'''
		This function displays all charts for a device with ref curve
		'''
		if findLimits(self.product_name, self.path_limit) == 1 :
		#Uncheck all tabs except the selected one
			self.checkBox.setChecked(False)
			self.checkBox_3.setChecked(False)
			self.checkBox_4.setChecked(False)
			self.checkBox_2.setChecked(False)
			self.checkBox.setCheckable(False)
			self.checkBox_3.setCheckable(False)
			self.checkBox_4.setCheckable(False)
			self.checkBox_2.setCheckable(False)
		
			self.rem_plot()

			A=[]
			for ind, file in  enumerate(self.main_mfiles):
				A.append(len(get_append(self.main_mfiles[ind], self.path_temp))) 				#Get the number of appends
			B = max(A)

			number,valid = QInputDialog.getInt(self, "Device Number", "Choose an Append Number", 0, 0 ,B, 1)
			if valid == False :
				self.checkBox_2.setCheckable(True)
				self.checkBox_4.setCheckable(True)
				self.checkBox_3.setCheckable(True)
				self.checkBox.setCheckable(True)
			else :
				if os.path.exists(self.path_fig+"1Device") :
					self.erase_folder(self.path_fig+"1Device")
				os.mkdir(self.path_fig+"1Device") 								#Create folder to save charts

				if len(self.failure_list) > 0:
					for ind, file in enumerate(self.main_mfiles):
						if  number <= A[ind] :	
							data = get_allpts(file, self.path_temp, self.settings[ind]["SMU1"][4], self.padName) 				#Collect all data
							self.ax1f1 = self.fig[ind].add_subplot(111)
							try:
								ref = recover_reference(file, self.path_ref, self.product_name) 												#Collect ref 
								self.ax1f1.plot(ref[0],ref[1], 'green' , label = 'Ref')   															#Plot ref curve    
							except:
								msgBox = QMessageBox.information(self, "Warning", "No reference found for the curve "+str(file))

							self.format_axis(self.ax1f1, file, ind)

							if number in self.failure_list[ind][0]:
								position = self.failure_list[ind][0].index(number) 																#Get index if existing failed curve 
								self.ax1f1.plot(data[0][number], data[1][number], label = "DUT : " +str(self.flag_deviation[ind][position]))    #Plot the curve with classification		
							else :
								self.ax1f1.plot(data[0][number], data[1][number], label = "DUT : Pass")

							
      
							self.ax1f1.legend(loc ='best', prop = {'size':11})	 																#Add the legend
					for i in range(len(self.fig)):
							main.addmpl(self.fig[i],i,self.path_fig+"1Device")  
					for k, value in enumerate(os.listdir(self.path_fig+"1Device")):
						self.delete_empty_fig(value, self.path_fig+"1Device")

				else :
					msgBox = QMessageBox.information(self, "Warning", "Please open the same project again in order to find potential failed curves.\nKeep limits, do not calculate limits again.")

					
				self.checkBox_2.setCheckable(True)
				self.checkBox_4.setCheckable(True)
				self.checkBox_3.setCheckable(True)
				self.checkBox.setCheckable(True)
		else :
				msgBox = QMessageBox.information(self, "Warning", "Reference curves not found for this product.")
				self.checkBox_5.setChecked(False)
				
	def delete_empty_fig(self, file, path_fig):
		if os.path.getsize(path_fig+"//"+file) < 11000 :
			os.remove(path_fig+"//"+file)



	def main_processing(self, product_name, path_temp, path_lib):
		'''
		Main function
		'''
		#print(self.listTest)
		for file in self.listTest:
			#Loop to fill lists with file names
			regexpC = r"c_(.)*" 
			regexpCbis = r"C_(.)*"														#Pattern to find correct name
			regexpM = r"m_(.)*" 
			regexpMbis = r"M_(.)*"															#Pattern to find correct name
			if re.match(regexpC, file) or re.match(regexpCbis, file):
				self.main_cfiles.append(file) 											#Fill tests names list
			if re.match(regexpM, file) or re.match(regexpMbis, file):
				self.main_mfiles.append(file) 											#Fill tests names list
		progressBar1 = QProgressDialog("Data Collecting", "Cancel", 0,  100, self)    	#Create a progress bar
		progressBar1.setWindowTitle("In progress...") 									#Set a title 
		prog = 0
		progressBar1.setModal(True) 
		progressBar1.show() 															#Show the progress bar
		progressBar1.setValue(prog) 													#Set a value to the progress bar
		
		if not len(self.main_cfiles) > 0 and not len(self.main_mfiles) > 0 :
			msgBox = QMessageBox.critical(self, "Error Files", "No test files found in the directory.\nCan not continue, try another folder.")
			progressBar1.close()

		elif len(self.main_cfiles) != len(self.main_mfiles):
			print(len(self.main_mfiles), len(self.main_cfiles))
			print(self.main_cfiles)
			print(self.main_mfiles)
			msgBox = QMessageBox.critical(self, "Error Files", "Number of c_files not equal to number of m_files.\nCan not continue, try another project.")
			progressBar1.close()
		else:
			prog=10
			progressBar1.setValue(prog)
			try :
				self.create_fig()                         								#Function call
			except :
				msgBox = QMessageBox.critical(self, "Error Charts ", "Problem creating charts.")
			prog=22
			progressBar1.setValue(prog)

			allData = [] 																#List with all data
			calData = [] 	
			error1 = 0															#List with all data without compiance points
			for ind, val in enumerate(self.main_mfiles):
				#print(val)
				try :
					self.settings.append(get_setting(val, path_lib))
					allData.append(get_allpts(val, path_temp, self.settings[ind]["SMU1"][4], self.padName)) 	#Fill all data list
					calData.append(get_calpts(allData[ind][0], allData[ind][1], self.settings[ind]["SMU1"][5]))					#Fill calc. data list
				except:
					error1 += 1
				# self.settings.append(get_setting(val, path_lib))
				# allData.append(get_allpts(val, path_temp, self.settings[ind]["SMU1"][4], self.padName)) 	#Fill all data list
				# calData.append(get_calpts(allData[ind][0], allData[ind][1], self.settings[ind]["SMU1"][5]))					#Fill calc. data listdir
			
				if len(self.main_mfiles) < 77:
					prog += 1
				else :
					prog += 0.5
				progressBar1.setValue(prog)

				if (progressBar1.wasCanceled()) :
					QMessageBox.warning(self, "Warning", "Stopped Collecting Data!")
					break

			if error1 > 0:
				msgBox = QMessageBox.critical(self, "Error Collecting data", "Problem to collect data.\nCan not continue, try another project.")
				self.__init__()

			error2 = 0
			file_wrong=[]
			for ind, file in enumerate(self.main_cfiles):
				try :
					self.pins_list.append(get_pins(file, path_temp))						#Fill  pins_list with pins connections
				except :
					error2 += 1
					file_wrong.append(file)

			if error2 > 0:
				msgBox = QMessageBox.critical(self, "Pin-Connection Files Error", "Problem to collect data from pin-connection file(s) : "+str(file_wrong)+".\nCan not continue, try another project.")

			try :
				f = open("saving_path.txt", "r") 										#Open txt file containing paths
				a=f.readlines() 														#Read file
				self.path_limit = str(a[1].split('\n')[0]) 								#Get limits backup path
				self.path_ref = str(a[2].split('\n')[0]) 								#Get reference curves backup path
				self.path_fig = str(a[3].split('\n')[0]) 								#Get charts backup path
				f.close()  																#Close file

			except :
				msgBox = QMessageBox.critical(self, "Error", "Problem Back Up Folder")
				self.__init__() 														#Reset

			prog = 100
			progressBar1.setValue(prog)
			if error1 == 0 and error2 == 0 :
				if product_name in os.listdir(self.path_limit) :
					choix = QMessageBox.information(self, "Information", "Existing limits for this product.\nNew Limits ?", QMessageBox.Yes | QMessageBox.No)
					if choix == QMessageBox.Yes : 
						self.create_newLim(self.main_mfiles, path_temp, self.path_limit, self.path_ref, product_name, self.settings, calData)		#Function call
						
						choix = QMessageBox.No
					if choix == QMessageBox.No :

						self.checkBox_2.show()
						progressBar3 = QProgressDialog("Loading ...", "Cancel", 0,  100, self)    													#Create a progress bar
						progressBar3.setWindowTitle("In progress ...")
						progressBar3.setValue(0)
						progressBar3.setModal(True)
						progressBar3.show()
						progressBar3.setValue(0)

						try :
							for i, file in enumerate(self.main_mfiles):
								try:
									product_limits = recover_limits(file, self.path_limit,  product_name)												#Collect limits
									product_ref = recover_reference(file, self.path_ref, product_name)													#Collect ref
									nb_device=get_nb_device(file, self.path_temp)															#Get number of devices
									self.failure_list.append(get_failed_index(calData[i][0], calData[i][1], product_limits, product_ref,            
																					nb_device, self.settings[i]["SMU1"][6], self.settings[i]["SMU1"][7]))  	#Fill failed curves list 
								except:
									self.failure_list.append([[],[]])  	#Fill failed curves list 
									QMessageBox.information(self, "Information", "No Limits for the file :"+file)
						except:
						 	msgBox = QMessageBox.critical(self, "Failed Curve Error", "Error for collecting limits and finding failed curves\n")
						 	self.__init__()
						progressBar3.setValue(25)
						self.flag_deviation=[] 											#Init classification flag
						progressBar3.setValue(50)
						for i,file  in enumerate(self.main_mfiles):
							dev=[]
							self.flag_deviation.append(dev)
							for ind in range(len(self.failure_list[i][1])):
								if ind in  self.failure_list[i][0] :      
									try:
									                      
										nfl=erase_double(self.failure_list[i][1][ind]) 		#Erase duplcate in the flag
										deviation=class_deviation(nfl)
										dev.append(deviation) 								#Add classification to the list
									except:
										QMessageBox.information(self, "Information", "No Limits for the file :"+file) 
						progressBar3.setValue(100)
						QMessageBox.information(self, "Information", "Please, choose a tab.")
				else :
					choice = QMessageBox.information(self, "Choice", "No limits for this product. \n Do you want to calculate new limits ?", QMessageBox.Yes | QMessageBox.No)
					if choice == QMessageBox.Yes :
						self.create_newLim(self.main_mfiles, path_temp, self.path_limit, self.path_ref, product_name, self.settings, calData)  		#Function call
			else : 
				self.widget_4.hide()				#Hide tab widget
				QMessageBox.information(self, "Information", "Please, select another folder/project")
				

					



if __name__ == '__main__':
	import sys, os
	from PyQt5 import QtGui

	app = QApplication(sys.argv)
	main = MainFunc()                       		#Create the application 
	#print( os.path.getsize("saving_path.txt"))
	if not os.path.exists("saving_path.txt"):
		msgBox = QMessageBox.information(main, "No Backup Directory", "Choose the location for the backup directory.")
		save_dir = QFileDialog.getExistingDirectory(main,'Create a Backup folder')
		main.path_backup = save_dir + str('\\CT Reporting Tool Backup')
		main.path_lim=save_dir+str('\\CT Reporting Tool Backup')+str('\\Limits')
		main.path_ref=save_dir+str('\\CT Reporting Tool Backup')+str('\\Ref')
		main.path_fig=save_dir+str('\\CT Reporting Tool Backup')+str('\\Fig')
		
		try :
			 os.makedirs(main.path_backup)
			 os.makedirs(main.path_lim) 			#Create directory
			 os.makedirs(main.path_ref)
			 os.makedirs(main.path_fig)
		except :
			msgBox = QMessageBox.critical(main, "Error", "Problem create backup folder")

		file_txt = open("saving_path.txt",'w') 		#Open the saving txt-file
		file_txt.write(main.path_backup +'\\'+'\n')
		file_txt.write(main.path_lim +'\\'+'\n') 	#Write path
		file_txt.write(main.path_ref +'\\'+'\n') 	#Write path
		file_txt.write(main.path_fig +'\\'+'\n') 	#Write path
		file_txt.close() 							#close the file

	main.show()                             		#Show the application
	sys.exit(app.exec_())                   		#Close the GUI event loop