###make and run job
jobName = 'BoneModelJob'
myJob = mdb.Job(atTime=None, contactPrint=OFF, description='', echoPrint=OFF, explicitPrecision=SINGLE, getMemoryFromAnalysis=True, historyPrint=OFF, 
    memory=90, memoryUnits=PERCENTAGE, model='BoneModel', modelPrint=OFF, multiprocessingMode=DEFAULT, name=jobName, nodalOutputPrecision=SINGLE, 
    numCpus=numberCPUs, numDomains=numberCPUs, numGPUs=2, queue=None, resultsFormat=ODB, scratch='', type=ANALYSIS, userSubroutine='', waitHours=0, waitMinutes=0)
if jobName + '.lck' in os.listdir(currWorkDir):  
    os.remove(currWorkDir + '/' + jobName + '.lck')
tic = time.clock()
myJob.submit(consistencyChecking=OFF)
myJob.waitForCompletion()
toc = time.clock()
print '--- Job ' + jobName + ' ran for ' + str(int(toc - tic)) + ' seconds'

###extract strains
execfile(strainsFile)

###fracture healing algorithm
tic = time.clock()
execfile(fractureHealingFile)
toc = time.clock()
print '--- Fracture healing at day ' + str(day) + ' ran for ' + str(int(toc - tic)) + ' seconds'

###update callus material
execfile(materialUpdateFile)