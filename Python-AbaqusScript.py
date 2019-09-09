# GO TO CMD / TYPE C:\py\Scripts\activate.bat
# Run python commands as if in Linux Terminal
import numpy as np
import csv
import matplotlib.pyplot as plt
from GetAbaqus import GetMaxStress
from smt.sampling_methods import Random
from smt.sampling_methods import LHS


##### GENERATE THE SAMPLING POINTS
#  In this example the sampling points are orientation angles alpha, beta, gamma
xlimits = np.array([
    [-np.pi, np.pi],
    [0., np.pi],
    [-np.pi, np.pi]
])
# sampling = Random(xlimits=xlimits)
sampling = LHS(xlimits=xlimits,criterion='maximin') # Latin Hypercube Sampling


num = 450 # number of samples
x = sampling(num)

finalResults = open("TrainingSet450LHS.txt",'w+')
fileTemplate = 'Job-1M.inp' # This is the template abaqus .inp file. You can generate this with the GUI
fileModified = 'Job-1.inp' # Output Input File that is modified for each iteration
for sample in range(0,x.shape[0]):

	alpha = x[sample, 0]
	beta = x[sample, 1]
	gamma = x[sample, 2] 
	Coord = [alpha,beta,gamma]
	MaxStress, ElemLabel = GetMaxStress(Coord,fileTemplate,fileModified)

	finalResults.write("%f, %f, %f, %f, %d \n" % (alpha,beta,gamma,MaxStress,ElemLabel))
	# print MaxStress
finalResults.close()
# TRAIN THE MODEL
print "Completed. The Results for %d are located in the File: FinalResults.txt " % num
