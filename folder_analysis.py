import os
import re

def mainDirAnalysis(directory):
	'''
	Check if "temp" and "lib" subdirectories are in the directory
	'''
	flagDir=is_correct(directory+str("\\")) #test if the main directory includes the right subdirectories (\lib and \temp) 
	return flagDir
	

def productName(directory):
	'''
	Return the product name
	'''
	return str(os.path.basename(directory)).split('_')[0]


def get_m_files(mainFile, directory):
	'''
	Return all the append test names 
	'''
	appName=[]
	fileName = "m"+mainFile[1:]
	for file in os.listdir(directory):
		if fileName.lower() == file.split(".")[0].lower()  :
			appName.append(file)
			for append_file in os.listdir(directory):
				regexp = r"m_(.)*.csv"
				if re.match(regexp, first_lower(append_file)) and fileName in append_file and fileName+"_append" in append_file :
				 appName.append(str(append_file).split('.')[0])
		elif fileName.lower()+"_neg" == file.split(".")[0].lower() and not "_append" in file :
			new = file.split(".")[0]
			appName.append(file)
			for append_file in os.listdir(directory):
				regexp = r"m_(.)*.csv"
				if re.match(regexp, first_lower(append_file)) and new in append_file and new+"_append" in append_file :
					appName.append(str(append_file).split('.')[0])
		elif fileName.lower()+"_pos" == file.split(".")[0].lower() and not "_append" in file :
			new = file.split(".")[0]
			appName.append(file)
			for append_file in os.listdir(directory):
				regexp = r"m_(.)*.csv"
				if re.match(regexp, first_lower(append_file)) and new in append_file and new+"_append" in append_file :
					appName.append(str(append_file).split('.')[0])
	return appName    


def get_append(mainFile, directory):
	'''
	This function returns all append files for each main file
	'''
	appendName=[]
	for file in os.listdir(directory):
		if mainFile.split('.')[0] in file.split(".")[0]  and  mainFile.split('.')[0]+'_append' in file.split('.')[0]:
			appendName.append(file)

	return appendName


def get_nb_device(file, path_temp):
	'''
	This function counts the number of append 
	Parameters : - name of a test
							 - path to the data directory ("temp" direcotry)
	Return the number of device for a test file
	'''
	curve_name = str(file).split('.')[0]
	nb_device=1                                             # 1st test file
	for append_file in os.listdir(path_temp):
				 if curve_name in append_file and curve_name+"_append" in append_file :
						 nb_device += 1
	return nb_device


def first_lower(s):
	if len(s) == 0:
		return s
	else:
		return s[0].lower() + s[1:]


def is_correct(directory):
	'''
	Test if the main directory includes the right subdirectories (\lib and \temp)
	'''
	flag=0
	subdirectories=os.listdir(directory)
	#print(subdirectories)
	for subdirectory in subdirectories:
		#print(subdirectory)
		if "lib" in subdirectory:
			flag +=1
		elif "temp" in subdirectory:
			flag +=1
		elif '.xml' in subdirectory :
			flag +=1
		
		else:
			flag=flag
	return flag


def findLimits(productName, limitsDir):
	'''
	Try to find if there is a ref directory for the "productName"
	Return 1 if there is already a directory with ref curves or limits
	'''
	flag=0
	if limitsDir != '' :
		limits=os.listdir(limitsDir)
	#print("Limits save in folder for products : ", limits)
		if productName in limits:
			flag=1
		else :
			flag = 0
	else :
		flag = 0
	return flag


def existingLimits(testsName, limitsDir):
	'''
	Return a flag if there are limits for each test
	'''
	flag=0
	for name in testsName:
		for file in os.listdir(limitsDir):
			if name+str("_limits") in file:
				#print("Les limites du test ", name, " existent deja")
				flag=1          
	return flag


def findRefCurve(testsName, refCurvesDir):
	'''
	Return a flag if there is a ref curve for each test
	'''
	flag=0
	for name in testsName:
		for file in os.listdir(refCurvesDir):
			if name+str("_ref") in file:
				flag=1
				#print("La courbe de ref existe deja")                  
	return flag


if __name__ == '__main__':
	from tkinter import *
	import tkinter.filedialog as tkFileDialog

	root=Tk()
	root.withdraw()
	folder=tkFileDialog.askdirectory(parent=root)
	root.destroy()

	a=mainDirAnalysis(folder)
	print(a)
	# b=get_main_files(folder+'\\temp\\')
	# d=[]
	# for file in b :
	#     c=get_m_files(file,folder+"\\temp\\")
	#     d.append(c)
	# e=get_main_m_files(d)
	# print(len(e), e)