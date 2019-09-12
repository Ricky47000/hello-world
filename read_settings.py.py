#This file collects data from the TSP file (in the lib directory)

import os
import re
import csv

def dict_parameters(folder,file):
	'''
	Create a dict of parameters
	'''
	parameters_dict={}
	
	path=folder
	file_open=open(path+file,'r+')
	
	allrows=file_open.readlines()
	for indice,line in enumerate(allrows):
		if "local" in str(line) and int(indice)<13:
			A=line.split(' ')[1]
			B=re.split(r'[} {\n]', A)
			parameters_dict[line.split(' ')[1].split('=')[0]]=[]
			for i in B[1:]:
				if i != '' and i != ',':
					parameters_dict[line.split(' ')[1].split('=')[0]].append(i.split(','))
	file_open.close()
	return parameters_dict


def read_srcrange(dict_param):
	'''
	Read the source range value
	'''
	r=[]
	if len(dict_param["Srcrange"]) > 0 :
		for i in range(len(dict_param["Srcrange"])) :
			smu_num = int(dict_param["Srcrange"][i][0])
			val = float(dict_param["Srcrange"][i][2])
			r.append([smu_num, val])
	return r


def read_measrange(dict_param):
	'''
	Read the measurement range value
	'''
	r=[]
	if len(dict_param["Measrange"]) > 0 :
		for i in range(len(dict_param["Measrange"])) :
			smu_num = int(dict_param["Measrange"][i][0])
			val = float(dict_param["Measrange"][i][2])
			r.append([smu_num, val])
	return r


def read_compliance(dict_param):
	'''
	Read the compliance (value of the clamping current) value
	'''
	r=[]
	if len(dict_param["Compliance"]) > 0 :
		for i in range(len(dict_param["Compliance"])) :
			smu_num = int(dict_param["Compliance"][i][0])
			val = float(dict_param["Compliance"][i][1])
			r.append([smu_num, val])
	return r


def read_common(dict_param):
	'''
	Read common settings (Look at the TSP file)
	'''
	r=[]
	if len(dict_param["Common"]) > 0 :
		for i in range(len(dict_param["Common"])) :
			sweep_num = int(dict_param["Common"][i][0].split("=")[-1])
			plc = float(dict_param["Common"][i][10].split("=")[-1])
			step_num = int(dict_param["Common"][i][13].split("=")[-1])
			r.append([sweep_num, plc, step_num])
	return r


def read_bias(dict_param):
	'''
	Read the bias value 
	'''
	r=[]
	if len(dict_param["Bias"]) > 0 :
		for i in range(len(dict_param["Bias"])) :
			smu_num = int(dict_param["Bias"][i][0])
			val = float(dict_param["Bias"][i][1])
			r.append([smu_num, val])
	return r


def read_step(dict_param):
	'''
	Read the sweep step value
	'''
	r=[]
	if len(dict_param["Step"]) > 0 :
		for i in range(len(dict_param["Step"])) :
			smu_num = int(dict_param["Step"][i][0])
			val_s = float(dict_param["Step"][i][1])
			val_e = float(dict_param["Step"][i][2])
			r.append([smu_num, val_s, val_e])
	return r


def read_sweep(dict_param):
	'''
	Read the sweep values (V Start, V End)
	'''
	r=[]
	if len(dict_param["Sweep"]) > 0 :
		for i in range(len(dict_param["Sweep"])) :
			smu_num = int(dict_param["Sweep"][i][0])
			val_s = float(dict_param["Sweep"][i][1])
			val_e = float(dict_param["Sweep"][i][2])
			r.append([smu_num, val_s, val_e])
	return r


def read_open(dict_param):
	'''
	This functions returns the name of "OPEN" SMUs
	'''
	r=[]
	if len(dict_param["Open"][0]) > 0 :
		for i in range(len(dict_param["Open"][0])) :
			smu_num = int(dict_param["Open"][0][i])
			r.append(smu_num)
	return r    


def read_sweep_direction(dict_param) :
	'''
	This functions reads the voltage sweep direction
	'''
	if len(dict_param["Sweep"] ) > 0 :
		start = dict_param["Sweep"][0][1]
		end = dict_param["Sweep"][0][2]
		if start > end :
			flag = 1
		else :
			flag = 0  
		return flag


def create_dict_setting(folder, file):
	'''
	This functions creates a dict with all the settings
	'''
	dict_param = dict_parameters(folder,file)
	a=read_sweep(dict_param)
	b=read_common(dict_param)
	c=read_compliance(dict_param)
	d=read_measrange(dict_param)
	e=read_srcrange(dict_param)
	f=read_step(dict_param)
	g=read_bias(dict_param)

	dico={}
	if len(dict_param["Open"]) > 0 :
		for i,val in enumerate(dict_param["Open"][0]) :
			dico["SMU"+str(val)]=["Open"]
	if len(dict_param["Sweep"]) > 0 :
		for i in range(len(dict_param["Sweep"])):
			if a[i][0] == c[i][0] == d[i][0] == e[i][0] :
				dico["SMU"+str(dict_param['Sweep'][0][0])]=["Sweep", a[i][1], a[i][2], b[0][0], read_sweep_direction(dict_param),c[i][1], d[i][1], e[i][1]]
			else : 
				print("Problem /CT_parameters_readingv2.py : Reading error setting")

	if len(dict_param["Step"]) > 0 :
		for i in range(len(dict_param["Step"])):
			# print(i, '/', len(dict_param["Step"]))
			dico["SMU"+str(dict_param['Step'][i][0])]=["Step", f[i][1], f[i][2], b[0][2],  read_sweep_direction(dict_param), c[i][1], d[i][1], e[i][1]]

	if len(dict_param['Bias']) > 0 :
		for i in range(len(dict_param["Bias"])):
			# print(i, '/', len(dict_param["Bias"]))
			dico["SMU"+str(dict_param['Bias'][i][0])]=["Bias", g[i][1]]
	
	return dico


def create_dict_pins(folder, file):
	'''
	This function creates a dict with pins connections
	'''
	data={}
	path=folder
	file_open=open(path+file,'r+')
	tab=csv.reader(file_open)
	column_name=next(tab) #column name in the csv file
	size=len(next(tab)) #column number in the csv file

	for i in range(size):
		data[column_name[i]]=[] #create one list for each key
	for row in tab :
		for i in range(size):
			if row[i] != '' :
				data[column_name[i]].append(int(float(row[i]))) #add values in the related list
	file_open.close()
	return data


if __name__ == '__main__':
	from tkinter import *
	import tkinter.filedialog as tkFileDialog

	# root=Tk()
	# root.withdraw()
	# folder=tkFileDialog.askdirectory(parent=root)
	# root.destroy()
	# #file="//lib//m_BAT_GND.tsp"
	# file="//temp//c_BATV2_Gnd.csv"
	# #file="//lib//itm.tsp"
	# # z=create_dict_setting(folder, file)
	# # print(z)
	# y = create_dict_pins(folder, file )
	# print(y)
	# # measurement_dict=dict_parameters(folder,file)
	# print(measurement_dict)
	# a=read_srcrange(measurement_dict)
	# print("Srcrange",a)
	# b=read_measrange(measurement_dict)
	# print("Measrange",b)
	# c=read_compliance(measurement_dict)
	# print("Compliance",c)
	# d=read_common(measurement_dict)
	# print("Common",d)
	# e=read_bias(measurement_dict)
	# print("Bias", e)
	# f=read_step(measurement_dict)
	# print("Step", f)
	# g=read_sweep(measurement_dict)
	# print("Sweep", g)
	# h=read_open(measurement_dict)
	# print("Open", h)