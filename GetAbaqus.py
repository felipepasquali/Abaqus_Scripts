import subprocess
import numpy as np
import csv

def Rotation(a,b,c):
	# Given 3 angles of rotation a(around x axis),b(around y axis),c(around z axis)
	# Return the final rotation matrix 
	ThX = np.matrix([[1,0,0],[0,np.cos(a),-np.sin(a)],[0,np.sin(a),np.cos(a)]])
	ThY = np.matrix([[np.cos(b),0,np.sin(b)],[0,1,0],[-np.sin(b),0,np.cos(b)]])
	ThZ = np.matrix([[np.cos(c),-np.sin(c),0],[np.sin(c),np.cos(c),0],[0,0,1]])
	return ThZ*ThY*ThX  

def GetMaxStress(sample,fileTemplate,fileModified):
	'''
	Function to run abaqus and get the max stress of a part based on the orientation
	IN
	sample: [1,3] array containing the the orientation angles
	fileTemplate: The original abaqus .inp file to serve as template
	fileModified: The file with the modified orientation
	OUT
	MaxStress: The maximum Von Mises Stress
	ElemLabel: Label of the element containing the Max Von Mises stress
	'''
	alpha,beta,gamma = sample[0],sample[1],sample[2]

	
	##### GENERATE .inp FILE TO CHANGE THE MATERIAL DIRECTION
	# This part of the script finds the material orientation line and modify it to the sampling points 
	a = np.dot(Rotation(alpha,beta,gamma),np.matrix([[1,0,0]]).T)
	b = np.dot(Rotation(alpha,beta,gamma),np.matrix([[0,1,0]]).T)

	fp = open(fileTemplate,'r')  
	dataFile = fp.readlines()
	fp.close()
	for cnt, line in enumerate(dataFile):
		if "*Orientation" in line:
			dataFile[cnt+1] =  (" %f,           %f,           %f,           %f,           %f,           %f\n " % (a[0],a[1],a[2],b[0],b[1],b[2]) )
	ff = open(fileModified,"w+")  
	ff.writelines(dataFile)
	ff.close()

	# CALL ABAQUS PYTHON TO GET THE MAXIMUM STRESS 
	# See the file RunAbaqus.py for more details
	# You need to change this path to your machine's abaqus path
	subprocess.call(['C:\\Program Files\\Abaqus\\Commands\\abq6145.bat', 'cae','noGUI=RunAbaqus.py'])
	
	# COLLECT THE MAX STRESS DATA
	fp = open("MaxStress.txt",'r') 
	readCsv = csv.reader(fp, delimiter=',')
	for row in readCsv:
		MaxStress = float(row[0])
		ElemLabel = int(row[1]) 
	fp.close()
	return MaxStress,ElemLabel