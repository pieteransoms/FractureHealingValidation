###clear all objects
for object in dir():
    if object[0:2] != "__":
        del globals()[object]

###imports
from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from optimization import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *
from abaqus import *
from abaqusConstants import *
from odbAccess import *
from odbMaterial import *
from odbSection import *
from visualization import *
from caeModules import *
from operator import itemgetter
import sys
import math
import shutil
import time
import numpy as np
import itertools

initiationTic = time.clock()

scriptsMap = 'I:/FractureHealingValidation/1/Scripts'
resultsMap = 'I:/FractureHealingValidation/1/Results'
modelsMap = 'I:/FractureHealingValidation/1/Models'
currWorkDir = os.getcwd()

machine = socket.gethostname()
if machine == 'SET-L-ME-B21009':                                                                                    #personal laptop
    sys.path.insert(8, r'C:/SIMULIA/EstProducts/2020/win_b64/code/python2.7/lib/abaqus_plugins/findNearestNode')
    sys.path.insert(8, r'C:/Program Files/MATLAB/R2021b/extern/engines/python/build/lib')
    sys.path.insert(8, r'C:/Users/u0144313/AppData/Local/anaconda3/Lib/site-packages')
elif machine[4] == 'S':                                                                                             #VCL
    sys.path.insert(16, r'C:/SIMULIA/CAE/2017/win_b64/code/python2.7/lib/abaqus_plugins/findNearestNode')
    sys.path.insert(16, r'C:/Program Files/Matlab/R2021b/extern/engines/python/build/lib')
    sys.path.insert(16, r'C:/ProgramData/Anaconda3/Lib/site-packages')
import nearestNodeModule
import matlab.engine
matlabengine = matlab.engine.start_matlab()
import xlwt                                                                                                         #write parameters and results in excel file

###create a new database
Mdb()

###script files
parametersFile      = scriptsMap + '/FHV1_PARAMETERS.py'
writeParametersFile = scriptsMap + '/FHV1_WRITEPARAMETERS.py'
modelFile           = scriptsMap + '/FHV1_MODEL.py'
functionsFile       = scriptsMap + '/FHV1_FUNCTIONS.py'
loopFile            = scriptsMap + '/FHV1_LOOP.py'
callusStiffnessFile = scriptsMap + '/FHV1_CALLUSSTIFFNESS.py'
fractureHealingFile = scriptsMap + '/FHV1_FRACTUREHEALING.py'
strainsFile         = scriptsMap + '/FHV1_STRAINS.py'
materialUpdateFile  = scriptsMap + '/FHV1_MATERIALUPDATE.py'

###parameters
execfile(parametersFile)
execfile(writeParametersFile)

###part files
if IFM == 'case B':
    modelsMap = modelsMap + '/case B'
else:
    modelsMap = modelsMap + '/case A'

boneFile = modelsMap + '/Bone.inp'
callusFile = modelsMap + '/Callus.inp'

###functions
execfile(functionsFile)

###model
day = 0                                                                                                                     #set day = 0 for the functions in modelFile
execfile(modelFile)

initiationToc = time.clock()
print '--- Initiation complete after ' + str(int(initiationToc - initiationTic)) + ' seconds, now starting loop'

###loop
for day in range(1, int(followUpTime)+1):
    loopTic = time.clock()
    execfile(loopFile)
    loopToc = time.clock()
    print '--- Day ' + str(day) + '/' + str(int(followUpTime)) + ' done (total time: ' + str(int(loopToc-loopTic)) + ' seconds)'
    wb.save(resultsMap + '/FHV1.xls')

###close excel file and quit matlab session
wb.save(resultsMap + '/FHV1.xls')
matlabengine.quit()