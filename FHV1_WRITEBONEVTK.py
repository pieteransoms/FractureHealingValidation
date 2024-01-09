#Run this script in the command window:
#python I:\FractureHealingValidation\1\Scripts\FHV1_WRITEBONEVTK.py

###clear all objects
for object in dir():
    if object[0:2] != "__":
        del globals()[object]

###imports
import numpy as np
import meshio
import time

###variables
scriptsMap = 'I:/FractureHealingValidation/1/Scripts'
resultsMap = 'I:/FractureHealingValidation/1/Results'
modelsMap = 'I:/FractureHealingValidation/1/Models'
# currWorkDir = os.getcwd()
parametersFile = scriptsMap + '/FHV1_PARAMETERS.py'
exec(open(parametersFile).read())
if detail == 'Debug':
    modelsMap = modelsMap + '/Debug'
if detail == 'VeryRough':
    modelsMap = modelsMap + '/VeryRough'
elif detail == 'Rough':
    modelsMap = modelsMap + '/Rough'
elif detail == 'Normal':
    modelsMap = modelsMap + '/Normal'
elif detail == 'Fine':
    modelsMap = modelsMap + '/Fine'
elif detail == 'VeryFine':
    modelsMap = modelsMap + '/VeryFine'
elif detail == 'case A':
    modelsMap = modelsMap + '/case A'
elif detail == 'case B':
    modelsMap = modelsMap + '/case B'

###load data and write to vtk file
boneNodeCoords = np.load(modelsMap + '/boneNodeCoords.npy')
boneElemNodeConnectivity = np.load(modelsMap + '/boneElemNodeConnectivity.npy')
boneElemNodeConnectivityVTK = boneElemNodeConnectivity - 1                                                                      #subtract all node labels by one to obtain correct model in ParaView
meshio.write_points_cells(modelsMap + '/bone.vtk', boneNodeCoords, 
    [('tetra', boneElemNodeConnectivityVTK)], file_format='vtk')
print('bone.vtk done')