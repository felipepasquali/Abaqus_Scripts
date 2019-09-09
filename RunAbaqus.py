from odbAccess import *
from abaqus import *
import job
import sys


# Runs Abaqus with the modified  .inp file
jobname = mdb.JobFromInputFile('Job-1','Job-1.inp') 
jobname.submit() 
jobname.waitForCompletion()

#Postprocessing: Reads the abaqus ODB file and extracts the maximum von misses stress and the location
odb = openOdb("C:\\SurrogateTest\\Job-1.odb")
# Values = odb.steps['Step-1'].frames[-1].fieldOutputs['S'].values
Field = odb.steps['Step-1'].frames[-1].fieldOutputs['S'].getScalarField(MISES)
maxp = max([ (g.data,g.elementLabel,g.integrationPoint) for g in Field.values ])
f = open("MaxStress.txt", "w")
f.write(("%f, %d, %d" % maxp))
f.close()



