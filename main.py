import os
from read_settings import *
from collect_data import *
import copy
import numpy as np
from limit_cal import *
from ReadingXML import *


def get_setting(file, path_lib):
	'''
		This function collects settings from the test.
		Parameters : - file name
					 - path to the settings directory ("lib" direcotry)
		Return a dict of settings by SMU
		Example : dict = {'SMU1': ['Sweep', -1.0, 3.0, 81, 0, 0.001, 0.001, 20.0], 'SMU2':['Open'] }
		'''
	settings=[]
	curve_name=str(file).split('.')[0]                          	#Recuperate the reference curve name
	for setting_file in os.listdir(path_lib):
		if curve_name+str(".tsp") in setting_file:
			setting_open=open(path_lib+setting_file,'r+')           #Open the tsp file
			settings=create_dict_setting(path_lib, setting_file)
			setting_open.close()                                  #Close the tsp file
	return settings


def get_allpts(file, path_temp, flag_direction, padName) :
		'''
		This function recovers data from test file. Recovered data are used to draw final figures
		Parameters : - file name
					 - path to the data directory ("temp" direcotry)
					 - direction setting
					 - SMUs names
		Return 2 tables of data :  - 1 for x coordinates 
								   - 1 for y coordinates     
		'''	
		
		file_open=open(path_temp+file+'.csv', 'r+')                           		#Open the 1st csv file
		curve_name=str(file)                            							#Collect reference curve name
		data_dict=create_dict(file_open)                                			#Create a dictonnary for data

		data_X=[]                                                       			#Initialize a list
		data_Y=[]                                                       			#Initialize a list
		data_X=create_tableX(data_dict, data_X, flag_direction, padName[0])         #Fill in the list with voltage values (1st file)
		data_Y=create_tableY(data_dict, data_Y, flag_direction, padName[0])         # -- with current values (1st file)

		file_open.close()                                               			#Close the 1st csv file 
		
		appends = []
		files = os.listdir(path_temp)
		files.sort(key=natural_keys)												#Sort list
		for file1 in files:
			if file in file1.split('.')[0] and file+"_append" in file1.split('.')[0]:
				if file1.split('.')[0] not in appends:
					appends.append(file1.split('.')[0])
		#print("A = ", len(appends))
		appends.sort(key=natural_keys)  											#Sort the appends list
		
		for append_file in appends:
						if append_file+".csv" in os.listdir(path_temp): 
							append_open=open(path_temp+append_file+'.csv','r+')      #Open append file(s)
							append_dict=create_dict(append_open)                 	 #Create a dict for append files
							data_X=create_tableX(append_dict,data_X, flag_direction, padName[0]) 	#Fill in the list with V values
							data_Y=create_tableY(append_dict, data_Y, flag_direction, padName[0]) 	# ---- with I values
							append_open.close()
						
		return [data_X, data_Y]


def get_calpts(data_X, data_Y, compliance) :
	'''
	This function recovers data used to compute limits (correct lenght, delete compliance points)
	Parameters : 			 - compliance
							 - data_X
							 - data_Y
	Return 2 tables of data :  - 1 for x coordinates 
														 - 1 for y coordinates  
	'''
	del_rows=compliance_points(data_Y[0], compliance)        #Return a list of index not to be taken into account
	X=copy.deepcopy(data_X)                                  # copy the V table
	Y=copy.deepcopy(data_Y)                                  # -- I table
	X=delete_row(X, del_rows)                                # delete V values not to be taken into account
	Y=delete_row(Y, del_rows)                                # delete I values -----
	return [X, Y]


def get_pins(file, path_temp):
	'''
	This functions gives the pins configuration
	'''
	pins = []
	curve_name = str(file).split('.')[0]
	for pins_file in os.listdir(path_temp):
		if curve_name+str(".csv") in pins_file :
			pins_o = open(path_temp+pins_file, 'r+')
			pins = create_dict_pins(path_temp, pins_file)
			pins_o.close()
	return pins

def get_reference_curve(X, Y):
	'''
	This function computes the reference curve for each test.	
	Return a table : [refX, refY]
	'''
	ref=[]		
	median_X = []
	median_Y = []
	for j in range(len(X[0])):
			sampleX=[]                                          #Initialize a sample
			for i in range(len(X)):
					sampleX.append(X[i][j]) 
			median_X.append(np.median(sampleX))                 #Compute the median of the sample
	for j in range(len(Y[0])):
			sampleY=[]                                          #Initialize a sample
			for i in range(len(Y)):
					sampleY.append(Y[i][j])
			median_Y.append(np.median(sampleY))                 #Compute the median of the sample
			
	ref=[median_X, median_Y]                                  	#Create a table
	
	return ref


def get_limits(X, Y, nb_device, meas_range, src_range, ref, flag_direction, sweep_step, multiple):
	'''
	Parameters : - X
							 - Y
							 - number of device for each test
							 - measurement range for each test
							 - reference curve
							 - direction of the measurement (flag)
							 - Value of the sweep step
							 - Sigma (multiple)
	Return a table of limits ((x1, x2, y1, y2)
	'''
	limit_table=[]
	coord=[]                                                # initalize a list
	distanceX=[]
	distanceY=[]
	#print("size ref0", len(ref[0]))
	slopeT=cal_pente(ref[0], ref[1])                        # compute the slope of the tangent curve
	#print(len(slopeT))
	spec = get_spec(src_range, meas_range)
	specX = spec[0]
	specY = spec[1]
	derivative=cal_derivative(ref[0], ref[1], specY)				# compute the derivation 
	# If less than 10 devices, limits are calculated with the voltage step value and the measuring range value 
	if nb_device < 10 and nb_device > 0 : 
			for i in range(len(ref[1])):
					distanceX.append(Decimal(specX))
					distanceY.append(Decimal(specY))
					if slopeT[i] != 0 :
							coefN=-(1/(slopeT[i]))                          # Compute the slope of the normal curve
							coord.append(solve_equation(Decimal(ref[0][i]), Decimal(ref[1][i]), Decimal(coefN), distanceX[i], distanceY[i],specY, flag_direction)) #Compute the coordinates of the limits
							
					else :
							if flag_direction == 1:
									coord.append([Decimal(X[0][i]), Decimal(X[0][i]), Decimal(ref[1][i])-Decimal(distanceY[i]), Decimal(ref[1][i])+Decimal(distanceY[i])]) #Compute the coordinates of the limits
							else :
									coord.append([Decimal(ref[0][i]), Decimal(ref[0][i]), Decimal(ref[1][i])+Decimal(distanceY[i]), Decimal(ref[1][i])-Decimal(distanceY[i])])
	else :
			std=get_std(X, Y)	 #Std calcultation	                                             
			distanceY=limit_calculation_stat(std[1], multiple)        #Compute limit distance for the current
			for ind, val in enumerate(distanceY):
				if val < specY :
					distanceY[ind]=specY
			distanceX=limit_calculation_stat(std[0], multiple)        #Compute --- for the voltage
			ct = 0
			
			for ind2, val2 in enumerate(distanceX):
				if val2 < specX :
					ct += 1 
					distanceX[ind2]=specX
			
			for i in range(len(ref[1])):
					if slopeT[i] != 0 :
							coefN=-(1/(slopeT[i]))   # Compute the slope of the normal curve
							coord.append(solve_equation(Decimal(ref[0][i]), Decimal(ref[1][i]), Decimal(coefN), Decimal(distanceX[i]), Decimal(distanceY[i]), specY, flag_direction)) # compute the coordinates of the limits

					else :
							
							if flag_direction == 1 and abs(ref[1][i]) > distanceY[i] :
								coord.append([Decimal(X[0][i]), Decimal(X[0][i]), Decimal(ref[1][i])-Decimal(distanceY[i]), Decimal(ref[1][i])+Decimal(distanceY[i])]) # compute the coordinates of the limits
							else :
								coord.append([Decimal(X[0][i]), Decimal(X[0][i]), Decimal(ref[1][i])+Decimal(distanceY[i]), Decimal(ref[1][i])-Decimal(distanceY[i])]) # compute the coordinates of the limits

	if min(derivative) < -0.0004 : #Special case when big  negative variation for the derivative
			# print("derivee :", derivative)
			coord=process_special_case(coord, ref, slopeT)

	limX1=[]                                                    # initialize a list
	limX2=[]                                                    # ---
	limY1=[]                                                    # ---
	limY2=[]                                                    # ---
	for i in range(len(coord)):
			limX1.append(coord[i][0])                               # add coordinates into a list
			limX2.append(coord[i][1])                               # -----
			limY1.append(coord[i][2])                               # -----
			limY2.append(coord[i][3])                               # -----
	limit_table=[limX1, limX2, limY1, limY2]                                      # create a table of limit coordinates

	return limit_table


def process_special_case(coord, ref, slopeT) :
	'''
	This function manages the special case with another method of calculation
	'''
	stepY=[]                                            # initialize a list
	for i in range(len(ref[1])-1):
		stepY.append(abs(ref[1][i+1]-ref[1][i]))        # compute each current step
	stepYmean=np.mean(stepY)
	index=[]                                            # initialize a list
	for i in range(1,len(stepY)) :
		if stepY[i] > stepYmean*4 and slopeT[i] < 0.0 :
			index.append(i)
			index.append(i+1)                           # fill in the list with index of wrong coordinates
	#print(index)
	index=list(set(index)) 								# delete duplications into the list
	if len(index) > 0 :
		                       
		coord1=(slopeT[index[0]-1]*float(coord[index[-1]+1][0])+ord_origine(float(coord[index[0]-1][0]),float(coord[index[0]-1][2]),slopeT[index[0]-1]) )  # compute the coordinates of the limits
		coord2=(slopeT[index[-1]+1]*float(coord[index[0]-1][1])+ord_origine(float(coord[index[-1]+1][1]),float(coord[index[-1]+1][3]),slopeT[index[-1]+1]))# compute the coordinates of the limits
		for ind in index:
			coord[ind]=[ref[0][index[-1]+1], ref[0][index[0]-1], coord1, coord2] # insert new values into the list of coordinates
	
	return coord 


def get_failed_index(X, Y, limit_table, ref, nb_device, meas_range, src_range):
	'''
	This function searches failed curves for each test
	Parameters : - limit table
				 - reference curve
				 - X
				 - Y
				 - measurement range
				 - source range
	Return a list of failed curve index and a flag
	'''
	distance_X = []
	distance_Y = []
	index_fail = []
	flag_dev=[]
	
	
	spec = get_spec(src_range, meas_range) 					#Get CT specifications
	specX = spec[0] 										#Voltage specification
	specY = spec[1] 										#Current specification
	derivative = cal_derivative(ref[0], ref[1], specY)				#Compute the derivative
	constant_pts = is_constante(derivative, nb_device)   	#Get constant points 
	
	for j in range(len(X)):
		dev=[]
		for i in range(len(X[0])-1):

				#If the point isn't a constant point(not the same as the previous one), the limits voltage values are different from the ref voltage value
				#and the limits current values are different from the ref current value
				if i not in constant_pts and round(float(ref[0][i]),12) != round(float(limit_table[0][i]), 12) and round(float(ref[1][i]),12) != round(float(limit_table[2][i]), 12) :
					
					distance_X = abs(float(ref[0][i])-float(limit_table[0][i]))
					distance_Y = abs(float(ref[1][i])-float(limit_table[2][i]))
					shape=draw_square(ref[0][i], ref[1][i], distance_X, distance_Y) #Draw square
					flag_failure_shape=find_failed_curve(X[j][i], Y[j][i], shape, specX, specY) #Check if the point is inside the square
					dev.append(flag_failure_shape)
					if flag_failure_shape != 0 :
						index_fail.append(j) #Add the index of the failed curve
						#print("Function : get_failed_index / case 1 - append ", j, " point ", i," flag ", flag_failure_shape)

				#If the point isn't a constant point, the limits voltage values are equal to the ref voltage value
				#and the limits current values are different from the ref current value
				elif i not in constant_pts and round(float(ref[1][i]),12) == round(float(limit_table[2][i]),12) and round(ref[0][i],12) != round(float(limit_table[0][i]), 12) :
					flag_failure_X=find_failed_curveX(X[j][i],limit_table[0][i], limit_table[1][i])
					#To be sure, check if the current value of the point isn't a short
					if flag_failure_X == 0 and abs(Y[j][i]) < specY :
				
					 	flag_failure_Y=find_failed_curveYbis(X[j][i], Y[j][i], limit_table[2][i], limit_table[3][i], specY)
					 	dev.append(flag_failure_Y)
					 	if flag_failure_Y != 0 :
					 		index_fail.append(j) #Add the index of the failed curve
					 		#print("Function : get_failed_index / case 2 Y", i)

					else :	
						dev.append(flag_failure_X)
					dev.append(flag_failure_X)
					if flag_failure_X != 0 :
						#print("Function : get_failed_index / case 2 X", i)
						index_fail.append(j)
						
				#If the point isn't a constant point, the limits voltage values are different from the ref voltage value
				#and the limits current values are equal to the ref current value				
				elif i not in constant_pts and round(float(ref[1][i]),12) != round(float(limit_table[2][i]), 12) and round(ref[0][i],12) == round(float(limit_table[0][i]), 12) :
					flag_failure_Y=find_failed_curveY(X[j][i], Y[j][i], limit_table[2][i], limit_table[3][i], specX, specY)
					dev.append(flag_failure_Y)
					if flag_failure_Y != 0 :
						index_fail.append(j) #Add the index of the failed curve
						#print("Function : get_failed_index / case 3", i, flag_failure_Y)

				#All the other cases		
				else:
					flag_failure_Y=find_failed_curveY(X[j][i], Y[j][i], limit_table[2][i], limit_table[3][i], specX, specY)
					dev.append(flag_failure_Y)
					if flag_failure_Y != 0 :
						#print("Function : get_failed_index / case 4", i,"Flag : ", flag_failure_Y)
						#print("Why : ", limit_table[2][i], limit_table[3][i], Y[j][i],  )
						index_fail.append(j) #Add the index of the failed curve

		flag_dev.append(dev) #Add the figure to the main flag
	index_fail=list(set(index_fail))
	return [index_fail, flag_dev]


def erase_double(liste):
	'''
	Return a list without the duplicate value side by side
	'''
	liste_ver=[]
	liste_ver.append(liste[0])
	for val in liste:
		if val != liste_ver[-1]:
			liste_ver.append(val)
		else :
			pass
			
	return liste_ver

def class_deviation(flag):
	'''
	Return the classification for a failed curve
	'''
	deviation="GOOD" 
	if 4 in flag and 1 not in flag and 5 not in flag :
		deviation="SHORT"
		return deviation
	if 1 in flag :
		deviation="DEVIATION"
		return deviation
	if 5 == flag[0] or 5 == flag[-1] :
		deviation="OPEN"
		return deviation
	if 3 in flag and 2 not in flag :
		deviation="LEAK-P"
		return deviation
	if 2 in flag and 3 not in flag :
		deviation="LEAK-N"
		return deviation
	if 2 in flag and 3 in flag and 1 not in flag :
		deviation="LEAK-PN"
		return deviation
	if 5 in flag and 3 not in flag and 2 not in flag and 1 not in flag :
		deviation = "OPEN"
		return deviation
	return deviation