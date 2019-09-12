import os
import csv
import math
import numpy as np
from decimal import *

def stat_std(sample):
	'''
	Return the standard deviation of a sample giving as parameters
	'''
	return(np.std(sample))

	
def stat_mean(sample):
	'''
	Return the average of a sample giving as parameters
	'''
	return (np.mean(sample))


def is_constante(derivee, nb_device):
	'''
	Return a table with index of points considered as constant
	'''
	constant_pts=[]
	if nb_device >= 10 :
		for i in range(len(derivee)):
			if abs(derivee[i]) <  max(derivee)/200:
				constant_pts.append(i)
	else :
		for i in range(len(derivee)):
			if abs(derivee[i]) <  max(derivee)/100:
				constant_pts.append(i)

	return constant_pts


def cal_derivative(my_tableX, my_tableY, stepY):
	'''
	Return the derivative of the curve 
	'''
	D=[]
	for i in range(len(my_tableX)-1):
		#print(i, my_tableY[i+1]-my_tableY[i])
		#if my_tableX[i] != my_tableX[i+1] and abs(float(my_tableY[i+1])-float(my_tableY[i])) > 0.5*stepY:
		if my_tableX[i] != my_tableX[i+1] :
			D.append((float(my_tableY[i])-float(my_tableY[i+1]))/(float(my_tableX[i])-float(my_tableX[i+1])))
		else :
			D.append(0)
		
	return D


def limit_calculation_stat(std, multiple):
	'''
	Return limits distance for each point
	'''
	distance=[]  
	for i in range(len(std)):
		distance.append(multiple*abs(std[i]))
		
	return distance
	
	
def cal_pente(X, Y):
	'''
	Return the slope value
	'''
	coef=[]
	for i in range(len(X)):
			if i == 0:
				coef.append((Y[i]-Y[i+1])/((X[i]-X[i+1])))
			elif i == len(X)-1:
				coef.append((Y[i-1]-Y[i])/((X[i-1]-X[i])))
			else :
				coef.append((Y[i-1]-Y[i+1])/((X[i-1]-X[i+1])))
	return coef


def coef_dirN(coef):
	'''
	Return the slope of the normal
	'''
	if coef !=0:
		coefN=-(1/coef)
	else :
		coefN=11000
		
	return coefN


def ord_origine(X, Y, coef):
	'''
	Return the value of y(0) (the intercept)
	'''
	return Y-coef*X


def get_spec(src_range, meas_range):
	'''
	This functions gets specifications from the Auto Curve Tracer specifications document 
	'''
	specY = 0.0
	specX = 0.0
	# Voltage range
	if float(src_range) == 0.2 :
		specX = (((float(src_range)*0.02)+0.000375)*0.015)+0.000225
	elif float(src_range) == 2.0 :
		specX = (((float(src_range)*0.02)+0.0006)*0.02)+0.000350
	elif float(src_range) == 20.0 :
		specX = (((float(src_range)*0.02)+0.005)*0.015)+0.005
	elif float(src_range) == 200.0 :
		specX = (((float(src_range)*0.02)+0.05)*0.015)+0.05
	# Current range
	elif float(src_range) == 0.0000001 :
		specY = (((float(src_range)*0.06)+0.0000000001)*0.06)+0.0000000001
	elif float(src_range) == 0.000001 :
		specY = (((float(src_range)*0.03)+0.0000000008)*0.025)+0.0000000005
	elif float(src_range) == 0.00001 :
		specY = (((float(src_range)*0.03)+0.000000005)*0.025)+0.0000000015
	elif float(src_range) == 0.0001 :
		specY = (((float(src_range)*0.03)+0.00000006)*0.02)+0.000000025
	elif float(src_range) == 0.001 :
		specY = (((float(src_range)*0.03)+0.0000003)*0.02)+0.0000002
	elif float(src_range) == 0.01 :
		specY = (((float(src_range)*0.03)+0.000006)*0.02)+0.0000025
	elif float(src_range) == 0.1 :
		specY = (((float(src_range)*0.03)+0.00003)*0.02)+0.00002
	else :
		print("NO src range available")

	# Voltage range
	if float(meas_range) == 0.2 :
		specX = (float(meas_range)*0.015) + 0.000225
	elif float(meas_range) == 2.0 :
		specX = (float(meas_range)*0.02) + 0.000350
	elif float(meas_range) == 20.0 :
		specX = (float(meas_range)*0.015) + 0.005
	elif float(meas_range) == 200.0 :
		specX = (float(meas_range)*0.015) + 0.05
	# Current range
	elif float(meas_range) == 0.0000001 :
		specY = (float(meas_range)*0.06) + 0.0000000001
	elif meas_range == 0.000001 :
		specY = (float(meas_range)*0.025)+0.0000000005
	elif float(meas_range) == 0.00001 :
		specY = (float(meas_range)*0.025) + 0.0000000015
	elif float(meas_range) == 0.0001 :
		specY = (float(meas_range)*0.02) + 0.000000025
	elif float(meas_range) == 0.001 :
		specY = (float(meas_range)*0.02) + 0.0000002
	elif float(meas_range) == 0.01 :
		specY = (float(meas_range)*0.02) + 0.0000025
	elif float(meas_range) == 0.1 :
		specY = (float(meas_range)*0.02) + 0.00002
	else :
		print("NO meas range available")
	if specX == 0.0 or specY == 0.0 :
		print("PROBLEM SPECIFICATIONS", specX, specY)
	else :
		return [specX, specY]


def solve_equation(x0, y0, coefN, stdX, stdY, meas_range, flag_direction):
	'''
	Return values of limits (High and Low) for the point (x0,y0)
	'''
	ordonneeN=Decimal(ord_origine(x0, y0, coefN))
	a=Decimal(1+(coefN*coefN))
	b=Decimal((2*coefN*ordonneeN)-(2*coefN*y0)-(2*x0))
	c=Decimal((ordonneeN*ordonneeN)-(2*y0*ordonneeN)+(x0*x0)+(y0*y0)-(stdY*stdY))
	delta = Decimal((b*b)-(4*a*c))
	
	if flag_direction == 1 :
		if delta <= 0 :   
			if (coefN) < 0 and coefN > -2000 :
				x1=x0-stdX
				x2=x0+stdX
				y1=y0
				y2=y0
			else:
				x1=x0
				x2=x0
				y1=y0+stdY
				y2=y0-stdY

				if abs(y0) < meas_range :
					y1= float(y0)+ meas_range
					y2= float(y0)- meas_range
					
		else:
			if coefN < -50000 or coefN > 50000 :
				x1=x0
				x2=x0
				y1=y0+stdY
				y2=y0-stdY
				if abs(y0) < meas_range :
					y1= float(y0)+meas_range
					y2= float(y0)-meas_range
			   
			elif coefN < 0 and coefN > -2000 :
				x1=x0-stdX
				x2=x0+stdX
				y1=y0
				y2=y0
		
			elif coefN < -2000 and coefN >-21000:
				x1=x0-stdX
				x2=x0+stdX
				y1=y0+stdY
				y2=y0-stdY
			
				if abs(y0) < meas_range :
					y1= float(y0)+meas_range
					y2= float(y0)-meas_range
	
			else :
				x1=Decimal((-float(b)-math.sqrt(delta))/float(2*a))
				x2=Decimal((-float(b)+math.sqrt(delta))/float(2*a))
				y1=Decimal(coefN*(x1)+ordonneeN)
				y2=Decimal(coefN*(x2)+ordonneeN)

				if abs(y0) < meas_range :
					y1= float(y0)+meas_range
					y2= float(y0)-meas_range

	else :
		if delta <= 0 :   
			if (coefN) < 0 and coefN > -2000 :
				x1=x0-stdX
				x2=x0+stdX
				y1=y0
				y2=y0
			else:
				x1=x0
				x2=x0
				y1=y0+(stdY)
				y2=y0-(stdY)
								  
				if abs(y0) < meas_range :
					y1= float(y0)+meas_range
					y2= float(y0)-meas_range
					
		else:
			if coefN < -50000 or coefN > 50000 :
				x1=x0
				x2=x0
				y1=y0+stdY
				y2=y0-stdY
				if abs(y0) < meas_range :
					y1= float(y0)+meas_range
					y2= float(y0)-meas_range
			   
			elif coefN < 0 and coefN > -2000 :
				#print("Function solve eq / case 2")
				x1=x0-2*stdX
				x2=x0+2*stdX
				y1=y0
				y2=y0
				
			elif coefN < -2000 and coefN >-21000:
				x1=x0-stdX
				x2=x0+stdX
				y1=y0+stdY
				y2=y0-stdY
				
				if abs(y0) < meas_range :
					y1= float(y0)+meas_range
					y2= float(y0)-meas_range
					
			else :
				#print("Function solve eq / case 4")
				x1=Decimal((-float(b)-math.sqrt(delta))/float(2*a))
				x2=Decimal((-float(b)+math.sqrt(delta))/float(2*a))
				if coefN > 0 :
					y1=Decimal(coefN*(x2)+ordonneeN)
					y2=Decimal(coefN*(x1)+ordonneeN)
				else :
					y1=Decimal(coefN*(x1)+ordonneeN)
					y2=Decimal(coefN*(x2)+ordonneeN)

				if abs(y0) < meas_range :
					y1= float(y0) + meas_range
					y2= float(y0) - meas_range
	
	return [x1, x2, y1, y2]


def find_failed_curve(X, Y, carre, specX, specY):
	'''
	Allow to find values out of limits

	Add +1 to the flag and return it
	'''
	flag=0
	pt1X=carre[0][0]
	pt2X=carre[0][1]
	pt3X=carre[0][2]
	pt4X=carre[0][3]
   
	pt1Y=carre[1][0]
	pt2Y=carre[1][1]
	pt3Y=carre[1][2]
	pt4Y=carre[1][3]

	#### For y-axis ####
	if Y < pt1Y or  Y < pt2Y :
		if X < -specX :
			if abs(Y) < 0.5*specY :
				flag = 5
			else :
				flag = 2
		elif X > +specX :
			if abs(Y) < 0.5*specY :
				flag = 5
			else :
				flag = 1
		else :
			flag = 4

	elif Y > pt3Y or Y > pt4Y:
		if X < -specX :
			if abs(Y) < 0.5*specY :
				flag = 5
			else :
				flag = 1
		elif X > +specX :
			if abs(Y) < 0.5*specY :
				flag = 5
			else :
				flag = 3
		else :
			flag = 4
	else :
		flag=0

	# if flag == 0 and pt1X != pt2X and pt4X != pt3X:
	# 	#### For x-axis ####
	# 	if X < pt1X-0.5*specX or  X < pt4X-0.5*specX:
	# 		 flag=3
	# 	elif X > pt2X+0.5*specX or  X > pt3X+0.5*specX:
	# 		flag=2
	# 	else :
	# 		flag=0

	return flag


def find_failed_curveX(X, LLx, HLx):
	'''
	Allow to find values out of limits

	Add special figure to the flag and return it
	'''
	flag = 0
	if X < LLx:
		flag = 3
	elif  X > HLx :
		flag = 2
	else :
		flag = 0   
		
	return flag


def find_failed_curveYbis(X, Y, HLy, LLy, specY):
	'''
	Allow to find values out of limits

	Add special figure to the flag and return it
	'''
	flag = 0
	if Y < LLy-specY :
		if X > 0 :
			if abs(Y) < 0.001*specY :
				flag = 5
			else :
				flag =1
		else : 
			flag = 2

	elif Y > HLy+specY :
		if X < 0 :
			if abs(Y) < 0.001*specY :
				flag = 5 
			else :
				flag = 1
		else :
			flag = 3

	else:
		flag = 0

	return flag


def find_failed_curveY(X, Y, HLy, LLy, specX, specY):
	'''
	Allow to find values out of limits

	Add sepcial figure to the flag and return it
	'''
	flag=0
	if Y < LLy :
		if X < -specX :
			flag = 2
		elif X > +specX :
			if abs(Y) < 0.001*specY :
				flag = 5
			else :
				flag = 1
		else :
			flag = 4
	elif Y > HLy :
		if X < -specX :
			if abs(Y) < 0.001*specY :
				flag = 5
			else :
				flag = 1
		elif X > +specX :
			flag = 3
		else :
			flag = 4
	else :
		flag=0
		
		
	return flag


def draw_square(X, Y, distanceX, distanceY):
	'''
	Draw a square with limits points
	'''
	x=np.array([float(X)-float(distanceX), float(X)+ float(distanceX),float(X)+float(distanceX),float(X)-float(distanceX),float(X)-float(distanceX)])
	y=np.array([float(Y)-float(distanceY),float(Y)-float(distanceY), float(Y)+float(distanceY), float(Y)+float(distanceY),float(Y)-float(distanceY)])
	return [x,y]


def recover_limits(name_file, limit_path, product_name):
	'''
	Recover limits from the folder where limits saved
	'''
	limit_dir=limit_path+product_name+"\\"
	
	for file1 in os.listdir(limit_dir):
		if file1.endswith('.csv') and str(name_file.split(".")[0])+"_limits" == file1.split(".")[0]:
			limit_dict={}
			
			file_open=open(limit_dir+file1, 'r+')
			tab=csv.reader(file_open)
			column_name=next(tab)
			size=len(column_name)
			for i in range(size):
				limit_dict[column_name[i]]=[]
			for row in tab :
				for j in range(size):
					limit_dict[column_name[j]].append(float(row[j]))
			file_open.close()

	limit_X1 = []
	limit_X2 = []
	limit_Y1 = []
	limit_Y2 = []
	for key in limit_dict.keys() :
		if key == 'limit_X1' :

			limit_X1 = (limit_dict[key])
		if key == 'limit_X2' :
			limit_X2 = (limit_dict[key])
		if key == 'limit_Y1' :
			limit_Y1 = (limit_dict[key])
		if key == 'limit_Y2' :
			limit_Y2 = (limit_dict[key])
		
	limits = [limit_X1, limit_X2, limit_Y1, limit_Y2]
	return limits


def recover_reference(name_file, reference_path, product_name):
	'''
	Recover limits from the folder where limits saved
	'''
	reference_dir=reference_path+product_name+"\\"
	
	for file1 in os.listdir(reference_dir):
		if file1.endswith('.csv') and name_file.split(".")[0]+"_ref"  == file1.split(".")[0]:
			#print("TEST CTLIM / Nom du fichier de limites : ",file1)
			reference_dict={}
			file_open=open(reference_dir+file1, 'r+')
			tab=csv.reader(file_open)
			column_name=next(tab)
			size=len(column_name)
			for i in range(size):
				reference_dict[column_name[i]]=[]
			for row in tab :
				for j in range(size):
					reference_dict[column_name[j]].append(float(row[j]))
			file_open.close()
			
	reference_X = []
	reference_Y = []
	for key in reference_dict.keys() :
		if key == 'ref_X' :
			reference_X = reference_dict[key]
		if key == 'ref_Y' :
			reference_Y = reference_dict[key]

	reference=[reference_X, reference_Y]
	return reference


def save_limits(file, limit_path, product_name, limit_table):
	'''
	Save limits in a folder
	'''
	
	fname=limit_path+product_name+"\\"+file.split(".")[0]+"_limits.csv"           # File name
	file=open(fname, 'w',encoding='utf8',newline='')    # Open csv file
	
	try :
		writer=csv.writer(file)
		writer.writerow(("limit_X1","limit_X2","limit_Y1", "limit_Y2"))
		for j in range(len(limit_table[0])):
			writer.writerow((limit_table[0][j],limit_table[1][j], limit_table[2][j], limit_table[3][j])) # Write limits coordinates into the csv file
	finally :
		file.close()                                    # Close the csv file


def save_reference(file, reference_path, product_name, ref):
	'''
	Save the reference curve  in a folder
	'''
	fname=reference_path+product_name+"\\"+file.split(".")[0]+"_ref.csv"           # File name
	file=open(fname, 'w',encoding='utf8',newline='')    # Open csv file
	
	try :
		writer=csv.writer(file)
		writer.writerow(("ref_X","ref_Y"))
		for j in range(len(ref[0])):
			writer.writerow((ref[0][j],ref[1][j])) # Write limits coordinates into the csv file
	finally :
		file.close()                                    # Close the csv file


def get_std(X, Y):
	'''
	This function puts in 2 different lists the computed standard deviation of each point
	Parameters : X and Y data
	Return a table with the standard deviation
	'''
	std=[]
	std_X=[]
	std_Y=[]
	for j in range(len(X[0])):
		sampleX=[]                                          # initialize a list
		for i in range(len(X)):
			sampleX.append(X[i][j])
		std_X.append(stat_std(sampleX))                      # compute the Std-Dev for each V sample

	for j in range(len(Y[0])):
		sampleY=[]
		for i in range(len(Y)):
			sampleY.append(Y[i][j])
		std_Y.append(stat_std(sampleY))                      # compute the Std-Dev for each I sample
		
	std=[std_X, std_Y]
	return std
