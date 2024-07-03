###make model
myModel = mdb.Model(modelType=STANDARD_EXPLICIT, name='BoneModel')
myAssembly = myModel.rootAssembly
part = myModel.parts

###import parts
myModel.PartFromInputFile(inputFileName=boneFile)
part.changeKey(fromName='PART-1', toName='BonePart')
myModel.PartFromInputFile(inputFileName=callusFile)
part.changeKey(fromName='PART-1', toName='CallusPart')

numberCallusElements = len(part['CallusPart'].elements)
numberCallusNodes    = len(part['CallusPart'].nodes)
numberBoneElements   = len(part[  'BonePart'].elements)
numberBoneNodes      = len(part[  'BonePart'].nodes)
print(numberCallusElements)

###materials and sections
myModel.Material(name='Bone')
myModel.materials['Bone'].Elastic(table=((ECortBone, nuCortBone), ))
myModel.HomogeneousSolidSection(material='Bone', name='Bone section', thickness=None)
part['BonePart'].SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE, 
    region=Region(elements=part['BonePart'].elements), sectionName='Bone section', 
    thicknessAssignment=FROM_SECTION)
tissueCompositions = [
    'softCart{:.2f}mnrlCart{:.2f}wovBone{:.2f}'.format(softCartConc/100.0, mnrlCartConc/100.0, wovBoneConc/100.0)
    for softCartConc in range(0, 102, 2)
    for mnrlCartConc in range(0, 102, 2)
    for wovBoneConc in range(0, 102, 2)
    if softCartConc + mnrlCartConc + wovBoneConc <= 100  # Ensure the sum does not exceed 100
]
for tissueComposition in tissueCompositions:
    softCartConc = float(tissueComposition[8:12])
    mnrlCartConc = float(tissueComposition[20:24])
    wovBoneConc  = float(tissueComposition[31:35])
    connTissConc = 1.0-wovBoneConc-mnrlCartConc-softCartConc
    E  = (EWovBone-EConnTiss)*wovBoneConc**3 + (ESoftCart-EConnTiss)*softCartConc**3 + (EMnrlCart-EConnTiss)*mnrlCartConc**3 + EConnTiss                           #based on experimental relation from Carter and Hayes (1977), used by Shefelbine et al. (2005) and Simon et al. (2011)
    nu = nuWovBone*wovBoneConc + nuSoftCart*softCartConc + nuMnrlCart*mnrlCartConc + nuConnTiss*connTissConc
    myModel.Material(name=tissueComposition.replace('.',''))                                                        #Abaqus doesn't allow a point in the name
    myModel.materials[tissueComposition.replace('.','')].Elastic(table=((E, nu), ))
    myModel.HomogeneousSolidSection(material=tissueComposition.replace('.',''), 
        name=tissueComposition.replace('.',''), thickness=None)
elementToTissueAssignment = {tissueCompositions[tissue]: [] for tissue in range(len(tissueCompositions))}
elementToTissueAssignment['softCart0.00mnrlCart0.00wovBone0.00'] = list(range(1, numberCallusElements+1))           #initially all elements have tissue composition 'softCart0.0mnrlCart0.0wovBone0.0'
part['CallusPart'].SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE, 
    region=Region(elements=part['CallusPart'].elements.sequenceFromLabels(
    elementToTissueAssignment['softCart0.00mnrlCart0.00wovBone0.00'])), sectionName='softCart0.00mnrlCart0.00wovBone0.00'.replace('.',''), 
    thicknessAssignment=FROM_SECTION)

###assembly
myAssembly.DatumCsysByDefault(CARTESIAN)
myAssembly.Instance(dependent=ON, name='Bone', part=part['BonePart'])
myAssembly.Instance(dependent=ON, name='Callus', part=part['CallusPart'])
refPoint1 = myAssembly.ReferencePoint(point=(0.0, -20.0, 0.0))
myAssembly.features.changeKey(fromName='RP-1', toName='RefPoint1')
myAssembly.Set(name='RefPoint1Set', referencePoints=(myAssembly.referencePoints[refPoint1.id], ))
myAssembly.AttachmentPoints(name='AttachPoint2', points=((0.0, 20.0, 0.0), ), setName='AttachPoint2Set')
myAssembly.Set(name='AttachPoint2Set', vertices=myAssembly.vertices.findAt(((0.0, 20.0,0.0),)))
myAssembly.Set(elements=myAssembly.instances['Callus'].elements, name='CallusSet')

###functions
###callusProperties
makeCallusProperties(numberCallusElements)
###callusElemNodeConnectivity
if 'callusElemNodeConnectivity.npy' in os.listdir(modelsMap):
    callusElemNodeConnectivity = np.load(modelsMap + '/callusElemNodeConnectivity.npy')
    print '--- callusElemNodeConnectivity loaded from file'
else:
    tic = time.clock()
    makeCallusElemNodeConnectivity(numberCallusElements)
    np.save(modelsMap + '/callusElemNodeConnectivity.npy', callusElemNodeConnectivity)
    toc = time.clock()
    print '--- makeCallusElemNodeConnectivity took ' + str(int(toc - tic)) + ' seconds'
###boneElemNodeConnectivity
if 'boneElemNodeConnectivity.npy' in os.listdir(modelsMap):
    boneElemNodeConnectivity = np.load(modelsMap + '/boneElemNodeConnectivity.npy')
    print '--- boneElemNodeConnectivity loaded from file'
else:
    tic = time.clock()
    makeBoneElemNodeConnectivity(numberBoneElements)
    np.save(modelsMap + '/boneElemNodeConnectivity.npy', boneElemNodeConnectivity)
    toc = time.clock()
    print '--- makeBoneElemNodeConnectivity took ' + str(int(toc - tic)) + ' seconds'
###callusElemElemConnectivity
if 'callusElemElemConnectivity.npy' in os.listdir(modelsMap):
    callusElemElemConnectivity = np.load(modelsMap + '/callusElemElemConnectivity.npy')
    print '--- callusElemElemConnectivity loaded from file'
else:
    tic = time.clock()
    makeCallusElemElemConnectivity(numberCallusElements, callusElemNodeConnectivity)
    np.save(modelsMap + '/callusElemElemConnectivity.npy', callusElemElemConnectivity)
    toc = time.clock()
    print '--- makeCallusElemElemConnectivity took ' + str(int(toc - tic)) + ' seconds'
###callusNodeCoords
if 'callusNodeCoords.npy' in os.listdir(modelsMap):
    callusNodeCoords = np.load(modelsMap + '/callusNodeCoords.npy')
    print '--- callusNodeCoords loaded from file'
else:
    tic = time.clock()
    makeCallusNodeCoords(numberCallusNodes)
    np.save(modelsMap + '/callusNodeCoords.npy', callusNodeCoords)
    toc = time.clock()
    print '--- makeCallusNodeCoords took ' + str(int(toc - tic)) + ' seconds'
###boneNodeCoords
if 'boneNodeCoords.npy' in os.listdir(modelsMap):
    boneNodeCoords = np.load(modelsMap + '/boneNodeCoords.npy')
    print '--- boneNodeCoords loaded from file'
else:
    tic = time.clock()
    makeBoneNodeCoords(numberBoneNodes)
    np.save(modelsMap + '/boneNodeCoords.npy', boneNodeCoords)
    toc = time.clock()
    print '--- makeBoneNodeCoords took ' + str(int(toc - tic)) + ' seconds'
###makeCallusElemVolumes
if 'callusElemVolumes.npy' in os.listdir(modelsMap):
    callusElemVolumes = np.load(modelsMap + '/callusElemVolumes.npy')
    print '--- callusElemVolumes loaded from file'
else:
    tic = time.clock()
    makeCallusElemVolumes(callusElemNodeConnectivity, callusNodeCoords)
    np.save(modelsMap + '/callusElemVolumes.npy', callusElemVolumes)
    toc = time.clock()
    print '--- makeCallusElemVolumes took ' + str(int(toc - tic)) + ' seconds'
###callusElemCenterCoords
if 'callusElemCenterCoords.npy' in os.listdir(modelsMap):
    callusElemCenterCoords = np.load(modelsMap + '/callusElemCenterCoords.npy')
    print '--- callusElemCenterCoords loaded from file'
else:
    tic = time.clock()
    makeCallusElemCenterCoords(numberCallusElements, callusNodeCoords)
    np.save(modelsMap + '/callusElemCenterCoords.npy', callusElemCenterCoords)
    toc = time.clock()
    print '--- makeCallusElemCenterCoords took ' + str(int(toc - tic)) + ' seconds'
# ###callusElemElemDistances
# if 'callusElemElemDistances.npy' in os.listdir(modelsMap):
#     callusElemElemDistances = np.load(modelsMap + '/callusElemElemDistances.npy')
#     print '--- callusElemElemDistances loaded from file'
# else:
#     tic = time.clock()
#     makeCallusElemElemDistances(numberCallusElements, callusElemCenterCoords)
#     np.save(modelsMap + '/callusElemElemDistances.npy', callusElemElemDistances)
#     toc = time.clock()
#     print '--- makeCallusElemElemDistances took ' + str(int(toc - tic)) + ' seconds'
# ###callusClosestElements
# if 'callusClosestElements.npy' in os.listdir(modelsMap):
#     callusClosestElements = np.load(modelsMap + '/callusClosestElements.npy')
#     print '--- callusClosestElements loaded from file'
# else:
#     tic = time.clock()
#     makeCallusClosestElements(callusElemElemDistances, numberClosestElements)
#     np.save(modelsMap + '/callusClosestElements.npy', callusClosestElements)
#     toc = time.clock()
#     print '--- makeCallusClosestElements took ' + str(int(toc - tic)) + ' seconds'
###commonNodesCallusBone
if 'commonNodesCallusBone.npy' in os.listdir(modelsMap):
    commonNodesCallusBone = np.load(modelsMap + '/commonNodesCallusBone.npy')
    print '--- commonNodesCallusBone loaded from file'
    commonNodesBoneCallus = np.load(modelsMap + '/commonNodesBoneCallus.npy')
    print '--- commonNodesBoneCallus loaded from file'
else:
    tic = time.clock()
    makeCommonNodesCallusBone(callusNodeCoords, boneNodeCoords)
    np.save(modelsMap + '/commonNodesCallusBone.npy', commonNodesCallusBone)
    np.save(modelsMap + '/commonNodesBoneCallus.npy', commonNodesBoneCallus)
    toc = time.clock()
    print '--- makeCommonNodesCallusBone took ' + str(int(toc - tic)) + ' seconds'
###loadingNodes
if 'loadingNodes.npy' in os.listdir(modelsMap):
    loadingNodes = np.load(modelsMap + '/loadingNodes.npy')
    print '--- loadingNodes loaded from file'
else:
    tic = time.clock()
    makeLoadingNodes(boneNodeCoords)
    np.save(modelsMap + '/loadingNodes.npy', loadingNodes)
    toc = time.clock()
    print '--- makeLoadingNodes took ' + str(int(toc - tic)) + ' seconds'
###fixedNodes
if 'fixedNodes.npy' in os.listdir(modelsMap):
    fixedNodes = np.load(modelsMap + '/fixedNodes.npy')
    print '--- fixedNodes loaded from file'
else:
    tic = time.clock()
    makeFixedNodes(boneNodeCoords)
    np.save(modelsMap + '/fixedNodes.npy', fixedNodes)
    toc = time.clock()
    print '--- makeFixedNodes took ' + str(int(toc - tic)) + ' seconds'
###intercorticalElementLabels
if 'intercorticalElementLabels.npy' in os.listdir(modelsMap):
    intercorticalElementLabels = np.load(modelsMap + '/intercorticalElementLabels.npy')
    print '--- intercorticalElementLabels loaded from file'
else:
    tic = time.clock()
    makeIntercorticalElementLabels(callusElemCenterCoords)
    np.save(modelsMap + '/intercorticalElementLabels.npy', intercorticalElementLabels)
    toc = time.clock()
    print '--- makeIntercorticalElementLabels took ' + str(int(toc - tic)) + ' seconds'
###periostealElementLabels
if 'periostealElementLabels.npy' in os.listdir(modelsMap):
    periostealElementLabels = np.load(modelsMap + '/periostealElementLabels.npy')
    print '--- periostealElementLabels loaded from file'
else:
    tic = time.clock()
    makePeriostealElementLabels(callusElemCenterCoords)
    np.save(modelsMap + '/periostealElementLabels.npy', periostealElementLabels)
    toc = time.clock()
    print '--- makePeriostealElementLabels took ' + str(int(toc - tic)) + ' seconds'
###endostealElementLabels
if 'endostealElementLabels.npy' in os.listdir(modelsMap):
    endostealElementLabels = np.load(modelsMap + '/endostealElementLabels.npy')
    print '--- endostealElementLabels loaded from file'
else:
    tic = time.clock()
    makeEndostealElementLabels(callusElemCenterCoords)
    np.save(modelsMap + '/endostealElementLabels.npy', endostealElementLabels)
    toc = time.clock()
    print '--- makeEndostealElementLabels took ' + str(int(toc - tic)) + ' seconds'

###interaction
callusBoneContactNodes = np.full((numberCallusNodes), False, dtype = bool)                                          #initialize as all false, then change the right ones to True, these values are 
                                                                                                                    #used to calculate callusElemPositioning[:, 1]
for node in range(len(commonNodesCallusBone)):
    slaveNodeLabel = commonNodesCallusBone[node]
    masterNodeLabel = commonNodesBoneCallus[node]
    myModel.Tie(adjust=OFF, 
        master=Region(nodes=myAssembly.instances['Bone'].nodes.sequenceFromLabels((masterNodeLabel, )), ), 
        name='CallusNode'+str(slaveNodeLabel), positionToleranceMethod=COMPUTED, 
        slave=Region(nodes=myAssembly.instances['Callus'].nodes.sequenceFromLabels((slaveNodeLabel, ))), thickness=ON, tieRotations=ON)
    callusBoneContactNodes[slaveNodeLabel-1] = True
callusBoneContactNodes = np.array(np.where(callusBoneContactNodes))[0] + 1                                             #conversion from boolean values to labels

###callusElemPositioning
tic = time.clock()
makeCallusElemPositioning(numberCallusElements, callusBoneContactNodes)
toc = time.clock()
np.save(modelsMap + '/callusElemPositioning.npy', callusElemPositioning)
print '--- makeCallusElemPositioning took ' + str(int(toc - tic)) + ' seconds'
###set the adjacent values of perfusion and wovBoneConc
updateAdjPerfusion(numberCallusElements, callusProperties, callusElemElemConnectivity, callusElemPositioning)
callusProperties[:,1] = updatedAdjPerfusion
updateAdjWovBoneConc(numberCallusElements, callusProperties, callusElemElemConnectivity)
callusProperties[:,5] = updatedAdjWovBoneConc

myAssembly.Set(name='LoadingSet', nodes=myAssembly.instances['Bone'].nodes.sequenceFromLabels(tuple(loadingNodes)))
myModel.Coupling(controlPoint=myAssembly.sets['AttachPoint2Set'], couplingType=KINEMATIC, influenceRadius=WHOLE_SURFACE, localCsys=None, 
    name='AttachPoint2Coupling', surface= myAssembly.sets['LoadingSet'], u1=ON, u2=ON, u3=ON, ur1=ON, ur2=ON, ur3=ON)

###spring
if useLinearSpring:
    myAssembly.engineeringFeatures.TwoPointSpringDashpot(axis=NODAL_LINE, dashpotBehavior=OFF, dashpotCoefficient=0.0, 
        name='Spring', regionPairs=((Region(referencePoints=(myAssembly.referencePoints[refPoint1.id], )), 
        myAssembly.sets['AttachPoint2Set']), ), springBehavior=ON, springStiffness=kSpring)
###alternative to spring: nonlinear connector section
else:
    myModel.ConnectorSection(name='ExtFixatorConnSect', translationalType=AXIAL)                                        #nonlinear spring defined as a connector
    if IFM == '0.0mm':
        myModel.sections['ExtFixatorConnSect'].setValues(behaviorOptions=(ConnectorElasticity(behavior=NONLINEAR,
            table=( (-1000.0    , -0.000001),
                    ( 0.0       ,  0.0     )), independentComponents=(), components=(1, )), ))
    elif IFM == '0.01mm':
        myModel.sections['ExtFixatorConnSect'].setValues(behaviorOptions=(ConnectorElasticity(behavior=NONLINEAR,
            table=( (-1000.0    , -0.010001),
                    ( 0.0       , -0.01    ), 
                    ( 0.0       ,  0.0     )), independentComponents=(), components=(1, )), ))
    elif IFM == '0.1mm':
        myModel.sections['ExtFixatorConnSect'].setValues(behaviorOptions=(ConnectorElasticity(behavior=NONLINEAR,
            table=( (-1000.0    , -0.100001),
                    ( 0.0       , -0.1     ), 
                    ( 0.0       ,  0.0     )), independentComponents=(), components=(1, )), ))
        # myModel.sections['ExtFixatorConnSect'].setValues(behaviorOptions=(ConnectorElasticity(behavior=NONLINEAR,
            # table=( (-1000.0    , -0.217391), 
                    # ( 0.0       ,  0.0     )), independentComponents=(), components=(1, )), ))
    elif IFM == 'case A':
        myModel.sections['ExtFixatorConnSect'].setValues(behaviorOptions=(ConnectorElasticity(behavior=NONLINEAR,
            table=( (-1000.0    , -0.358696), 
                    (-102.83843 , -0.16366 ), 
                    (-100.0     , -0.021739), 
                    ( 0.0       ,  0.0     )), independentComponents=(), components=(1, )), ))
    elif IFM == '0.5mm':
        myModel.sections['ExtFixatorConnSect'].setValues(behaviorOptions=(ConnectorElasticity(behavior=NONLINEAR,
            table=( (-1000.0    , -1.500001),
                    ( 0.0       , -1.5     ), 
                    ( 0.0       ,  0.0     )), independentComponents=(), components=(1, )), ))
        # myModel.sections['ExtFixatorConnSect'].setValues(behaviorOptions=(ConnectorElasticity(behavior=NONLINEAR,
            # table=( (-1000.0    , -0.608696), 
                    # (-107.8612  , -0.4148  ), 
                    # (-100.0     , -0.021739), 
                    # ( 0.0       ,  0.0     )), independentComponents=(), components=(1, )), ))
    elif IFM == '1.0mm':
        myModel.sections['ExtFixatorConnSect'].setValues(behaviorOptions=(ConnectorElasticity(behavior=NONLINEAR,
            table=( (-1000.0    , -1.000001),
                    ( 0.0       , -1.0     ), 
                    ( 0.0       ,  0.0     )), independentComponents=(), components=(1, )), ))
        # myModel.sections['ExtFixatorConnSect'].setValues(behaviorOptions=(ConnectorElasticity(behavior=NONLINEAR,
            # table=( (-1000.0    , -1.108696), 
                    # (-117.9032  , -0.9169  ), 
                    # (-100.0     , -0.021739), 
                    # ( 0.0       ,  0.0     )), independentComponents=(), components=(1, )), ))
    elif IFM == 'case B':
        myModel.sections['ExtFixatorConnSect'].setValues(behaviorOptions=(ConnectorElasticity(behavior=NONLINEAR,
            table=( (-1000.0    , -1.358696), 
                    (-122.925767, -1.168027), 
                    (-100.0     , -0.021739), 
                    ( 0.0       ,  0.0     )), independentComponents=(), components=(1, )), ))
    elif IFM == '1.5mm':
        myModel.sections['ExtFixatorConnSect'].setValues(behaviorOptions=(ConnectorElasticity(behavior=NONLINEAR,
            table=( (-1000.0    , -1.500001),
                    ( 0.0       , -1.5     ), 
                    ( 0.0       ,  0.0     )), independentComponents=(), components=(1, )), ))
        # myModel.sections['ExtFixatorConnSect'].setValues(behaviorOptions=(ConnectorElasticity(behavior=NONLINEAR,
            # table=( (-1000.0    , -1.608696), 
                    # (-127.9472  , -1.4191  ), 
                    # (-100.0     , -0.021739), 
                    # ( 0.0       ,  0.0     )), independentComponents=(), components=(1, )), ))
    elif IFM == '2.0mm':
        myModel.sections['ExtFixatorConnSect'].setValues(behaviorOptions=(ConnectorElasticity(behavior=NONLINEAR,
            table=( (-1000.0    , -2.000001),
                    ( 0.0       , -2.0     ), 
                    ( 0.0       ,  0.0     )), independentComponents=(), components=(1, )), ))
        # myModel.sections['ExtFixatorConnSect'].setValues(behaviorOptions=(ConnectorElasticity(behavior=NONLINEAR,
            # table=( (-1000.0    , -2.108696), 
                    # (-137.9913  , -1.9213  ), 
                    # (-100.0     , -0.021739), 
                    # ( 0.0       ,  0.0     )), independentComponents=(), components=(1, )), ))
    myModel.sections['ExtFixatorConnSect'].behaviorOptions[0].ConnectorOptions()
    myAssembly.WirePolyLine(mergeType=IMPRINT, meshable=False, points=((myAssembly.referencePoints[refPoint1.id], 
        myAssembly.sets['AttachPoint2Set'].vertices[0]), ))
    myAssembly.features.changeKey(fromName='Wire-1', toName='ExtFixatorWire')
    myAssembly.Set(edges=myAssembly.edges.findAt(((0.0,0.0,0.0),)), name='ExtFixatorWireSet')
    myAssembly.SectionAssignment(region=myAssembly.sets['ExtFixatorWireSet'], sectionName='ExtFixatorConnSect')

###step
myModel.StaticStep(name='LoadingStep', nlgeom=ON, previous='Initial')

###boundary conditions
myModel.PinnedBC(createStepName='Initial', localCsys=None, name='BoneFixedBC', 
    region=Region(nodes=myAssembly.instances['Bone'].nodes.sequenceFromLabels(fixedNodes)))
myModel.EncastreBC(createStepName='Initial', localCsys=None, name='ExtFixatorBC', 
    region=myAssembly.sets['RefPoint1Set'])
myModel.DisplacementBC(amplitude=UNSET, createStepName='Initial', distributionType=UNIFORM, fieldName='', fixed=OFF, 
    localCsys=None, name='AttachPoint2BC', region=myAssembly.sets['AttachPoint2Set'], u1=0.0, u2=UNSET, u3=0.0, ur1=UNSET, ur2=UNSET, ur3=UNSET)

###load
myModel.ConcentratedForce(cf2=-load, createStepName='LoadingStep', distributionType=UNIFORM, field='', 
    localCsys=None, name='Load', region=myAssembly.sets['AttachPoint2Set'])

###field output
del myModel.fieldOutputRequests['F-Output-1']
myModel.FieldOutputRequest(createStepName='LoadingStep', name='F-Output-1', rebar=EXCLUDE, 
    region=myAssembly.sets['CallusSet'], sectionPoints=DEFAULT, variables=('LE', ), frequency=LAST_INCREMENT)

###history output
myModel.HistoryOutputRequest(createStepName='LoadingStep', name='H-Output-1', frequency=LAST_INCREMENT, 
    rebar=EXCLUDE, region=myAssembly.sets['AttachPoint2Set'], sectionPoints=DEFAULT, variables=('U2', ))

del mdb.models['Model-1']