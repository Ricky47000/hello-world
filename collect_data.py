#This file manages data from the temp directory

import os
import csv
import numpy as np

def create_dict(file):
    '''
    Read a csv file and fill a dict with the different columns
    Return a dict
    
    Example : data={'V_IV':[List of values] , 'I_IV':[List of values]}
    '''
    data = {}
    tab = csv.reader(file)
    column_name = next(tab) #column name in the csv file
    size = len(next(tab)) #column number in the csv file

    for i in range(size):
        data[column_name[i]] = [] #create one list for each key
    for row in tab :
        for i in range(size):
            data[column_name[i]].append(float(row[i])) #add values in the related list
    return data


def create_tableX(data_dict, my_tableX, flag, padName):
    '''
    Create or append X-values in an array

    Return an array
    '''
    for key in data_dict.keys():
        if key=='V_'+padName and flag==0 :
            my_tableX.append(data_dict[key])
        if key=='V_'+padName and flag==1 :
            liste=data_dict[key]
            liste_r=list(reversed(liste))
            my_tableX.append(liste_r)    

    return my_tableX


def create_tableY(data_dict, my_tableY, flag, padName):
    '''
    Create or append Y-values in an array

    Return an array
    '''
    for key in data_dict.keys():
        
        if key=='I_'+padName and flag == 0 :
            my_tableY.append(data_dict[key])
        if key=='I_'+padName and flag == 1 :
            liste=data_dict[key]
            liste_r=list(reversed(liste))
            my_tableY.append(liste_r)

    return my_tableY


def compliance_points(my_tableY,clamping):
    rows_list=[]
    for i in range(len(my_tableY)):
        if my_tableY[i]<-(0.99*clamping) or my_tableY[i]>(0.99*clamping):
            rows_list.append(i)
    return rows_list


def delete_row(my_table, rows_list):
    '''
    Allow the deletion of points

    Return an array 
    '''  
   
    #print("Debut :", np.shape(my_table))
    for row in rows_list[::-1]:
        
        #print("T", my_table[0][0])
        for i in range(len(my_table)):
            del my_table[i][row]
    
    return my_table