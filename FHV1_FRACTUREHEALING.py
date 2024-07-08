###files for the fuzzy analysis, this happens once on the first day
if day == 1:
    fuzzyFiles = []
    if fuzzyModel == 'Ansoms_v04':
        fuzzyFiles.append('/FHV1_FUZZY_Ansoms_v04.m')
        fuzzyFiles.append('/FHV1_FUZZY_Ansoms_v04.fis')
    for file in fuzzyFiles:
        if file in os.listdir(currWorkDir):
            os.remove(currWorkDir + '/' + file)                                                                                     #delete old version of file
            shutil.copy(scriptsMap+'/Fuzzy logic'+file, currWorkDir)                                                                #copy new file to currWorkDir
        else:
            shutil.copy(scriptsMap+'/Fuzzy logic'+file, currWorkDir)                                                                #copy new file to currWorkDir

###fuzzy input is collected in the inputMatrix and fuzzy output is returned in outputMatrix
inputMatrix = matlab.single(callusProperties.tolist())
if fuzzyModel == 'Ansoms_v04':
    outputMatrix = np.array(matlabengine.FHV1_FUZZY_Ansoms_v04(inputMatrix), dtype = float)                                         #outputMatrix contains change in perfusion, softCartConc, mnrlCartConc and wovBoneConc

###scaling outputMatrix to accomodate for mesh size
callusRefVolume = 0.07                                                                                                              #average value for normal mesh size is 0.03812, for rough mesh size is 0.07
scaleFactor = np.cbrt(refCallusElemVolume/avgCallusElemVolume)
outputMatrix[:, 0] = scaleFactor * outputMatrix[:, 0]
outputMatrix[:, 3] = scaleFactor * outputMatrix[:, 3]

###update callusProperties (calculation of update happens inside function, actual update has to happen outside function because callusProperties is a global function)
updatePerfusion(numberCallusElements, callusProperties, outputMatrix)
callusProperties[:, 0] = updatedPerfusion
updateAdjPerfusion(numberCallusElements, callusProperties, callusElemElemConnectivity, callusElemPositioning)
callusProperties[:, 1] = updatedAdjPerfusion
updateWovBoneConc(numberCallusElements, callusProperties, outputMatrix)
callusProperties[:, 4] = updatedWovBoneConc
updateMnrlCartConc(numberCallusElements, callusProperties, outputMatrix)
callusProperties[:, 3] = updatedMnrlCartConc
updateSoftCartConc(numberCallusElements, callusProperties, outputMatrix)
callusProperties[:, 2] = updatedSoftCartConc
updateAdjWovBoneConc(numberCallusElements, callusProperties, callusElemElemConnectivity)
callusProperties[:, 5] = updatedAdjWovBoneConc

###save callusProperties for visualization outside abaqus
np.save(resultsMap + '/callusProperties/npy/callusPropertiesDay' + str(day) + '.npy', callusProperties)