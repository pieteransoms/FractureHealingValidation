###remove external fixator
###spring
if useLinearSpring:
    del mdb.models['BoneModel'].rootAssembly.engineeringFeatures.springDashpots['Spring']
###alternative to spring: nonlinear connector section
else:
    del mdb.models['BoneModel'].sections['ExtFixatorConnSect']

###COMPRESSION
###change force to 1N
myModel.loads['Load'].setValues(cf2=-1.0, distributionType=UNIFORM, field='')

###remove redundant BC
del mdb.models['BoneModel'].boundaryConditions['ExtFixatorBC']

###run second job
jobName = 'CallusStiffnessCompressionJob'
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

###extract stiffness and write in resultsSheet
###open odb file
odbFile = currWorkDir + '/' + jobName + '.odb'
myOdb = openOdb(path = odbFile, readOnly = False)
###extract displacement
displacement = -myOdb.steps['LoadingStep'].historyRegions['Node ASSEMBLY.2'].historyOutputs['U2'].data[-1][1]                                                               #displacement of AttachPoint2
callusStiffnessCompression = 1/displacement
resultsSheet.write(day, 11, callusStiffnessCompression)
###close odb file
myOdb.close()

###BENDING
###change force to 1N transversally
myModel.loads['Load'].setValues(cf1=1.0, cf2=0.0, distributionType=UNIFORM, field='')

###change BC
myModel.boundaryConditions['AttachPoint2BC'].setValuesInStep(stepName='LoadingStep', u1=FREED, u2=0.0)

###run second job
jobName = 'CallusStiffnessBendingJob'
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

###extract stiffness and write in resultsSheet
###open odb file
odbFile = currWorkDir + '/' + jobName + '.odb'
myOdb = openOdb(path = odbFile, readOnly = False)
###extract displacement
displacement = myOdb.steps['LoadingStep'].historyRegions['Node ASSEMBLY.2'].historyOutputs['U1'].data[-1][1]                                                               #displacement of AttachPoint2
callusStiffnessBending = 1/displacement
resultsSheet.write(day, 12, callusStiffnessBending)
###close odb file
myOdb.close()

###TORSION
###change force to 1Nmm torsion
del myModel.loads['Load']
myModel.Moment(cm2=1.0, createStepName='LoadingStep', distributionType=UNIFORM, field='', localCsys=None, 
    name='Moment', region=myAssembly.sets['AttachPoint2Set'])

###change BC
myModel.boundaryConditions['AttachPoint2BC'].setValuesInStep(stepName='LoadingStep', u1=0.0, u2=FREED)

###run second job
jobName = 'CallusStiffnessTorsionJob'
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

###extract stiffness and write in resultsSheet
###open odb file
odbFile = currWorkDir + '/' + jobName + '.odb'
myOdb = openOdb(path = odbFile, readOnly = False)
###extract displacement
rotation = myOdb.steps['LoadingStep'].historyRegions['Node ASSEMBLY.2'].historyOutputs['UR2'].data[-1][1]                                                               #rotation of AttachPoint2
callusStiffnessTorsion = 1/rotation
resultsSheet.write(day, 13, callusStiffnessTorsion)
###close odb file
myOdb.close()

###bring external fixator back
###spring
if useLinearSpring:
    myAssembly.engineeringFeatures.TwoPointSpringDashpot(axis=NODAL_LINE, dashpotBehavior=OFF, dashpotCoefficient=0.0, 
        name='Spring', regionPairs=((Region(referencePoints=(myAssembly.referencePoints[refPoint1.id], )), 
        myAssembly.sets['AttachPoint2Set']), ), springBehavior=ON, springStiffness=kSpring)
###alternative to spring: nonlinear connector section
else:
    myModel.ConnectorSection(name='ExtFixatorConnSect', translationalType=AXIAL)                                                                                            #nonlinear spring defined as a connector
    if IFM == 'case A':
        myModel.sections['ExtFixatorConnSect'].setValues(behaviorOptions=(ConnectorElasticity(behavior=NONLINEAR,
            table=( (-1000.0    , -0.358696), 
                    (-102.83843 , -0.16366 ), 
                    (-100.0     , -0.021739), 
                    ( 0.0       ,  0.0     )), independentComponents=(), components=(1, )), ))
    elif IFM == 'case B':
        myModel.sections['ExtFixatorConnSect'].setValues(behaviorOptions=(ConnectorElasticity(behavior=NONLINEAR,
            table=( (-1000.0    , -1.358696), 
                    (-122.925767, -1.168027), 
                    (-100.0     , -0.021739), 
                    ( 0.0       ,  0.0     )), independentComponents=(), components=(1, )), ))
    myModel.sections['ExtFixatorConnSect'].behaviorOptions[0].ConnectorOptions()
    myAssembly.WirePolyLine(mergeType=IMPRINT, meshable=False, points=((myAssembly.referencePoints[refPoint1.id], 
        myAssembly.sets['AttachPoint2Set'].vertices[0]), ))
    myAssembly.features.changeKey(fromName='Wire-1', toName='ExtFixatorWire')
    myAssembly.Set(edges=myAssembly.edges.findAt(((0.0,0.0,0.0),)), name='ExtFixatorWireSet')
    myAssembly.SectionAssignment(region=myAssembly.sets['ExtFixatorWireSet'], sectionName='ExtFixatorConnSect')

###bring original force back and remove moment
myModel.ConcentratedForce(cf2=-load, createStepName='LoadingStep', distributionType=UNIFORM, field='', 
    localCsys=None, name='Load', region=myAssembly.sets['AttachPoint2Set'])
del myModel.loads['Moment']

###bring original BC back
myModel.EncastreBC(createStepName='Initial', localCsys=None, name='ExtFixatorBC', 
    region=myAssembly.sets['RefPoint1Set'])