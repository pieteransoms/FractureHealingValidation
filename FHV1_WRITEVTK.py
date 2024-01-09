#Run this script in the command window:
#python I:\FractureHealingValidation\1\Scripts\FHV1_WRITEVTK.py

###clear all objects
for object in dir():
    if object[0:2] != '__':
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
callusNodeCoords = np.load(modelsMap + '/callusNodeCoords.npy')
callusElemNodeConnectivity = np.load(modelsMap + '/callusElemNodeConnectivity.npy')
callusElemNodeConnectivityVTK = callusElemNodeConnectivity - 1                                                                      #subtract 1 from all node labels to obtain correct model in ParaView 
nodes = callusNodeCoords 
elements = [('tetra', callusElemNodeConnectivityVTK)]
initialZeros = np.zeros(len(callusElemNodeConnectivityVTK))
initialOnes = np.ones(len(callusElemNodeConnectivityVTK))
callusElemPositioning = np.load(modelsMap + '/callusElemPositioning.npy')
cell_data = {'perfusion': [initialZeros], 'cartConc': [initialZeros], 'softCartConc': [initialZeros], 'mnrlCartConc': [initialZeros], 'wovBoneConc': [initialZeros], 'mnrlCart+BoneConc': [initialZeros], 'connTissConc': [initialOnes], 'distStrain': [initialZeros], 'dilaStrain': [initialZeros]}
# cell_data = {'peripheral': [(callusElemPositioning[:, 0]).astype(float)], 'boneContact': [(callusElemPositioning[:, 1]).astype(float)], 'endoCortical': [(callusElemPositioning[:, 2]).astype(float)], 'fractureEndContact': [(callusElemPositioning[:, 3]).astype(float)]}

meshio.write_points_cells(resultsMap + '/callusProperties/vtk/callusPropertiesDay' + str(0) + '.vtk', nodes, elements, cell_data=cell_data, file_format='vtk')

for day in range(1,100):
    callusProperties = np.load(resultsMap + '/callusProperties/npy/callusPropertiesDay' + str(day) + '.npy')
    cell_data = {'perfusion': [callusProperties[:, 0]], 'cartConc': [np.add(callusProperties[:, 2], callusProperties[:, 3])], 'softCartConc': [callusProperties[:, 2]], 'mnrlCartConc': [callusProperties[:, 3]], 'wovBoneConc': [callusProperties[:, 4]], 'mnrlCart+BoneConc': [np.add(callusProperties[:, 3], callusProperties[:, 4])], 'connTissConc': [initialOnes - callusProperties[:, 2] - callusProperties[:, 3] - callusProperties[:, 4]], 'distStrain': [callusProperties[:, 6]], 'dilaStrain': [callusProperties[:, 7]]}
    meshio.write_points_cells(resultsMap + '/callusProperties/vtk/callusPropertiesDay' + str(day) + '.vtk', nodes, elements, cell_data=cell_data, file_format='vtk')
    print('Day ' + str(day) + ' done')