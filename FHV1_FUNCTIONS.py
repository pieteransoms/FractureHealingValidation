'''
overview of functions:
makeCallusProperties                    -> callusProperties                                                 performed once

makeCallusElemNodeConnectivity          -> callusElemNodeConnectivity                                       performed once
makeBoneElemNodeConnectivity            -> boneElemNodeConnectivity                                         performed once
makeCallusElemElemConnectivity          -> callusElemElemConnectivity                                       performed once

makeCallusElemPositioning               -> callusElemPositioning                                            performed once

makeCallusNodeCoords                    -> callusNodeCoords                                                 performed once
makeBoneNodeCoords                      -> boneNodeCoords                                                   performed once

makeCallusElemVolumes                   -> callusElemVolumes                                                performed once
makeCallusElemCenterCoords              -> callusElemCenterCoords                                           performed once

makeCallusElemElemDistances             -> callusElemElemDistances                                          performed once
makeCallusElementsInVicinity            -> callusElementsInVicinity                                         performed once

makeCommonNodesCallusBone               -> commonNodesCallusBone                                            performed once

makeLoadingNodes                        -> loadingNodes                                                     performed once
makeFixedNodes                          -> fixedNodes                                                       performed once

makeIntercorticalElementLabels          -> intercorticalElementLabels                                       performed once
makePeriostealElementLabels             -> periostealElementLabels                                          performed once
makeEndostealElementLabels              -> endostealElementLabels                                           performed once

updatePerfusion                         -> updatedPerfusion                                                 performed every iteration
updateWovBoneConc                       -> updatedWovBoneConc                                               performed every iteration
updateMnrlCartConc                      -> updatedMnrlCartConc                                              performed every iteration
updateSoftCartConc                      -> updatedSoftCartConc                                              performed every iteration
updateAdjPerfusion                      -> updatedAdjPerfusion                                              performed every iteration
updateAdjWovBoneConc                    -> updatedAdjWovBoneConc                                            performed every iteration
updateCallusMaterialNames               -> updatedCallusMaterialNames                                       performed every iteration

'''

def makeCallusProperties(numberCallusElements):
    global callusProperties
    '''
    callusProperties = [[(0)elem1Perfusion, (1)elem1AdjPerfusion, (2)elem1SoftCartConc, (3)elem1MnrlCartConc, (4)elem1WovBoneConc, (5)elem1AdjWovBoneConc, (6)elem1DistStrain, (7)elem1DilaStrain],
                        [(0)elem2Perfusion, (1)elem2AdjPerfusion, (2)elem2SoftCartConc, (3)elem2MnrlCartConc, (4)elem2WovBoneConc, (5)elem2AdjWovBoneConc, (6)elem2DistStrain, (7)elem2DilaStrain],
                                                                                                   ...
                        [(0)elem~Perfusion, (1)elem~AdjPerfusion, (2)elem~SoftCartConc, (3)elem~MnrlCartConc, (4)elem~WovBoneConc, (5)elem~AdjWovBoneConc, (6)elem~DistStrain, (7)elem~DilaStrain]]
        size = numberCallusElements x 8
        dtype = float (single precision)
    '''

    callusProperties = np.zeros((numberCallusElements, 8), dtype = float)                                               #initialize as zeros

###

def makeCallusElemNodeConnectivity(numberCallusElements):
    global callusElemNodeConnectivity
    '''
    callusElemNodeConnectivity = [[elem1Node1, elem1Node2, elem1Node3, elem1Node4],
                                  [elem2Node1, elem2Node2, elem2Node3, elem2Node4],
                                                        ...
                                  [elem~Node1, elem~Node2, elem~Node3, elem~Node4]]
        size = numberCallusElements x 4
        dtype = int
    '''

    callusElemNodeConnectivity = np.array([myAssembly.instances['Callus'].elements[label-1].connectivity 
        for label in range(1, numberCallusElements+1)], dtype = int)
    callusElemNodeConnectivity += 1                                                                                     #the node labels obtained in the line above have to be incremented with 1 to be correct

###

def makeBoneElemNodeConnectivity(numberBoneElements):
    global boneElemNodeConnectivity
    '''
    boneElemNodeConnectivity = [[elem1Node1, elem1Node2, elem1Node3, elem1Node4],
                                [elem2Node1, elem2Node2, elem2Node3, elem2Node4],
                                                      ...
                                [elem~Node1, elem~Node2, elem~Node3, elem~Node4]]
        size = numberBoneElements x 4
        dtype = int
    '''

    boneElemNodeConnectivity = np.array([myAssembly.instances['Bone'].elements[label-1].connectivity 
        for label in range(1, numberBoneElements+1)], dtype = int)
    boneElemNodeConnectivity += 1                                                                                       #the node labels obtained in the line above have to be incremented with 1 to be correct

###

def makeCallusElemElemConnectivity(numberCallusElements, callusElemNodeConnectivity):
    global callusElemElemConnectivity
    '''
    callusElemElemConnectivity = [[elem1FirstNeighbors (x4), elem1SecondNeighbors (x25), elem1ThirdNeighbors (x150)],
                                  [elem2FirstNeighbors (x4), elem2SecondNeighbors (x25), elem2ThirdNeighbors (x150)],
                                                                  ...
                                  [elem~FirstNeighbors (x4), elem~SecondNeighbors (x25), elem~ThirdNeighbors (x150)]]
        length = numberCallusElements x 129
        dtype = int
    firsfNeighbors have a face in common
    firstNeighbors = faceAdjElem1,  faceAdjElem2, faceAdjElem3,  faceAdjElem4
        length = 4
    secondNeighbors have a line in common
    secondNeighbors = lineAdjElem1,  lineAdjElem2, ...,  lineAdjElem25
        length = 25
    thirdNeighbors have a point in common
    thirdNeighbors = pointAdjElem1, pointAdjElem2, ..., pointAdjElem150
        length = 100
    '''

    firstNeighbors  = np.zeros((numberCallusElements,   4), dtype = int)                                                #intialize as zeros
    secondNeighbors = np.zeros((numberCallusElements,  25), dtype = int)                                                #intialize as zeros, oversized to accomodate a maximum of 25 second neighbors
    thirdNeighbors  = np.zeros((numberCallusElements, 150), dtype = int)                                                #intialize as zeros, oversized to accomodate a maximum of 150 third neighbors
    for elementLabel in range(1, numberCallusElements+1):
        elementsWithNodeInCommon = []                                                                                   #this list will contain other elements that have (a) node(s) in common
        for node in callusElemNodeConnectivity[elementLabel-1,:]:
            elementsWithNodeInCommon.append(np.where(callusElemNodeConnectivity == node)[0]+1)
        elementsWithNodeInCommon = np.concatenate(elementsWithNodeInCommon)
        unique, counts = np.unique(elementsWithNodeInCommon, return_counts=True)
        threeNodesInCommon = np.where(counts == 3)[0]                                                                   #3 nodes in common:  firstNeighbors
        twoNodesInCommon   = np.where(counts == 2)[0]                                                                   #2 nodes in common: secondNeighbors
        oneNodeInCommon    = np.where(counts == 1)[0]                                                                   #1  node in common:  thirdNeighbors
        for i in range(len(threeNodesInCommon)):
            firstNeighbors[elementLabel-1, i]  = unique[threeNodesInCommon[i]]
        for i in range(len(twoNodesInCommon)):
            secondNeighbors[elementLabel-1, i] = unique[twoNodesInCommon[i]]
        for i in range(len(oneNodeInCommon)):
            thirdNeighbors[elementLabel-1, i]  = unique[oneNodeInCommon[i]]
    callusElemElemConnectivity = np.concatenate((firstNeighbors, secondNeighbors, thirdNeighbors), axis=1)

###

def makeCallusElemPositioning(numberCallusElements, callusBoneContactNodes):
    global callusElemPositioning
    '''
    callusElemPositioning = [[elem1Peripheral, elem1BoneContact, elem1EndoCortical, elem1FractureEndContact],
                             [elem2Peripheral, elem2BoneContact, elem2EndoCortical, elem2FractureEndContact],
                                                                ...
                             [elem~Peripheral, elem~BoneContact, elem~EndoCortical, elem~FractureEndContact]]
        size = numberCallusElements x 4
        dtype = bool
    '''

    callusElemPositioning = np.full((numberCallusElements, 4), False, dtype = bool)                                     #initialize as all false
    callusElemPositioning[:, 0] = np.array([callusElemElemConnectivity[:, 3] == 0])                                     #peripheral if not four first neighbors (position four is '0')
    for elementLabel in range(1, numberCallusElements+1):
        if len(np.intersect1d(callusBoneContactNodes, callusElemNodeConnectivity[elementLabel-1, :])) == 3:             #if 3 nodes in common with bone, then boneContact is true
            callusElemPositioning[elementLabel-1, 1] = True
            # print elementLabel
    callusElemPositioning[:, 2] = np.array(np.sqrt(callusElemCenterCoords[:, 0]**2
        + callusElemCenterCoords[:, 2]**2) < marrowRadius, dtype = bool)                                                #if centerCoords in range THEN endoCortical
    callusElemPositioning[:, 3] = np.logical_and(callusElemPositioning[:, 1],
        np.array(np.absolute(callusElemCenterCoords[:, 1]) < fractureEndRegion), dtype = bool)                          #if boneContact and y value small enough, then fractureEndContact

###

def makeCallusNodeCoords(numberCallusNodes):
    global callusNodeCoords
    '''
    callusNodeCoords = [[node1XCoord, node1YCoord, node1ZCoord],
                        [node2XCoord, node2YCoord, node2ZCoord],
                                         ...
                        [node~XCoord, node~YCoord, node~ZCoord]]
        size = numberCallusNodes x 3
        dtype = float (single precision)
    '''

    callusNodeCoords = np.array([myAssembly.instances['Callus'].nodes[label-1].coordinates 
        for label in range(1, numberCallusNodes+1)], dtype = float)

###

def makeBoneNodeCoords(numberBoneNodes):
    global boneNodeCoords
    '''
    boneNodeCoords = [[node1XCoord, node1YCoord, node1ZCoord],
                      [node2XCoord, node2YCoord, node2ZCoord],
                                       ...
                      [node~XCoord, node~YCoord, node~ZCoord]]
        size = numberBoneNodes x 3
        dtype = float (single precision)
    '''

    boneNodeCoords = np.array([myAssembly.instances['Bone'].nodes[label-1].coordinates 
        for label in range(1, numberBoneNodes+1)], dtype = float)

###

def makeCallusElemVolumes(callusElemNodeConnectivity, callusNodeCoords):
    global callusElemVolumes
    '''
    callusElemVolumes = [volElement1, volElement2, ..., volElement~]
        length = numberCallusElements
        dtype = float(single precision)
    '''

    callusElemVolumes = np.zeros((numberCallusElements), dtype = float)                                                 #initialize as zeros
    for elementLabel in range(1, numberCallusElements+1):
        connNodes = callusElemNodeConnectivity[elementLabel-1, :]
        [x1, y1, z1] = callusNodeCoords[connNodes[0]-1]
        [x2, y2, z2] = callusNodeCoords[connNodes[1]-1]
        [x3, y3, z3] = callusNodeCoords[connNodes[2]-1]
        [x4, y4, z4] = callusNodeCoords[connNodes[3]-1]
        matrix = np.array([[x1, x2, x3, x4],
                           [y1, y2, y3, y4],
                           [z1, z2, z3, z4],
                           [ 1,  1,  1,  1]])
        callusElemVolumes[elementLabel-1] = abs(np.linalg.det(matrix)/6.0)

###

def makeCallusElemCenterCoords(numberCallusElements, callusNodeCoords):
    global callusElemCenterCoords
    '''
    callusElemCenterCoords = [[elem1XCoord, elem1YCoord, elem1ZCoord],
                              [elem2XCoord, elem2YCoord, elem2ZCoord],
                                              ...
                              [elem~XCoord, elem~YCoord, elem~ZCoord]]
        size = numberCallusElements x 3
        dtype = float (single precision)
    '''

    callusElemCenterCoords = np.zeros((numberCallusElements, 3), dtype = float)                                         #initialize as zeros
    for elementLabel in range(1, numberCallusElements+1):
        connNodes = callusElemNodeConnectivity[elementLabel-1, :]
        callusElemCenterCoords[elementLabel-1, :] = np.transpose(np.array(np.sum( 
            [callusNodeCoords[connNodes[0]-1], callusNodeCoords[connNodes[1]-1], 
            callusNodeCoords[connNodes[2]-1], callusNodeCoords[connNodes[3]-1]],0))/4)
###

def makeCallusElemElemDistances(numberCallusElements, callusElemCenterCoords):
    global callusElemElemDistances
    '''
    callusElemElemDistances = [[distElem1Elem1, distElem1Elem2, ..., distElem1Elem~],
                               [distElem2Elem1, distElem2Elem2, ..., distElem2Elem~],
                                                       ...
                               [distElem~Elem1, distElem~Elem2, ..., distElem~Elem~]]
        size = numberCallusElements x numberCallusElements
        dtype = float (single precision)
    '''

    callusElemElemDistances = np.zeros((numberCallusElements, numberCallusElements), dtype = float)                     #initialize as all zeros
    for elemLabel1 in range(1, numberCallusElements+1):                                                                 #loop only over top half of matrix, copy later to bottom half
        for elemLabel2 in range(elemLabel1+1, numberCallusElements+1):
            callusElemElemDistances[elemLabel1-1, elemLabel2-1] = np.sqrt(np.sum(np.square(
                callusElemCenterCoords[elemLabel1-1,:]-callusElemCenterCoords[elemLabel2-1, :])))
    callusElemElemDistances = np.maximum(callusElemElemDistances, np.transpose(callusElemElemDistances))                #make symmetric

###

def makeCallusElementsInVicinity(callusElemElemDistances, distanceForVicinity):
    global callusElementsInVicinity
    '''
    callusElementsInVicinity = [[elem1CloseElem1, elem1CloseElem2, ...],
                                [elem2CloseElem1, elem2CloseElem2, ...],
                                                  ...
                                [elem~CloseElem1, elem~CloseElem2, ...]]
    '''
    pass

###

def makeCommonNodesCallusBone(callusNodeCoords, boneNodeCoords):
    global commonNodesCallusBone
    global commonNodesBoneCallus
    '''
    commonNodes... = [commonNode1, commonNode2, ..., commonNode~]                                                      #the coordinates of the nodes are used to find common nodes
        length = numberCommonNodes (not defined)
        dtype = int
    '''

    callusNodeCoordsSet = set([tuple(x) for x in callusNodeCoords])
    boneNodeCoordsSet = set([tuple(x) for x in boneNodeCoords])
    commonNodeCoordsCallusBone = np.array([x for x in callusNodeCoordsSet & boneNodeCoordsSet])
    commonNodesCallusBone = np.array([np.where(np.all(callusNodeCoords == commonNodeCoordsCallusBone[i], 
        axis = 1))[0][0] + 1 for i in range(len(commonNodeCoordsCallusBone))])
    commonNodesBoneCallus = np.array([np.where(np.all(boneNodeCoords == commonNodeCoordsCallusBone[i], 
        axis = 1))[0][0] + 1 for i in range(len(commonNodeCoordsCallusBone))])

###

def makeLoadingNodes(boneNodeCoords):
    global loadingNodes
    '''
    loadingNodes = [loadingNode1, loadingNode2, ..., loadingNode~]
        length = numberLoadingNodes (not defined)
        dtype = int
    '''

    loadingNodes = np.array(np.where(boneNodeCoords[:, 1] > 19)[0], dtype = int) + 1

###

def makeFixedNodes(boneNodeCoords):
    global fixedNodes
    '''
    loadingNodes = [fixedNode1, fixedNode2, ..., fixedNode~]
        length = numberFixedNodes (not defined)
        dtype = int
    '''

    fixedNodes = np.array(np.where(boneNodeCoords[:, 1] < -19)[0], dtype = int) + 1

###

def makeIntercorticalElementLabels(callusElemCenterCoords):
    global intercorticalElementLabels
    '''
    intercorticalElementLabels = [elementLabel1, elementLabel2, ..., elementLabel~]
        length = numberIntercorticalElementLabels (not defined)
        dtype = int
    '''

    radiusList = np.sqrt(callusElemCenterCoords[:, 0]**2 + callusElemCenterCoords[:, 2]**2)
    elementsWithinRadius = np.array(np.where(radiusList < 8)[0], dtype = int) + 1
    elementsOutsideRadius = np.array(np.where(radiusList > 6)[0], dtype = int) + 1
    heightList = callusElemCenterCoords[:, 1]
    if IFM == 'case A':
        elementsWithinHeight = np.array(np.where(np.absolute(heightList) < 1.05)[0], dtype = int) + 1
    elif IFM == 'case B':
        elementsWithinHeight = np.array(np.where(np.absolute(heightList) < 1.65)[0], dtype = int) + 1
    intercorticalElementLabels = np.intersect1d(np.intersect1d(elementsWithinRadius, elementsOutsideRadius), elementsWithinHeight)

###

def makePeriostealElementLabels(callusElemCenterCoords):
    global periostealElementLabels
    '''
    periostealElementLabels = [elementLabel1, elementLabel2, ..., elementLabel~]
        length = numberPeriostealElementLabels (not defined)
        dtype = int
    '''

    radiusList = np.sqrt(callusElemCenterCoords[:, 0]**2 + callusElemCenterCoords[:, 2]**2)
    elementsWithinRadius = np.array(np.where(radiusList < 13)[0], dtype = int) + 1
    elementsOutsideRadius = np.array(np.where(radiusList > 8)[0], dtype = int) + 1
    heightList = callusElemCenterCoords[:, 1]
    elementsWithinHeight = np.array(np.where(np.absolute(heightList) < 3)[0], dtype = int) + 1
    periostealElementLabels = np.intersect1d(np.intersect1d(elementsWithinRadius, elementsOutsideRadius), elementsWithinHeight)

###

def makeEndostealElementLabels(callusElemCenterCoords):
    global endostealElementLabels
    '''
    endostealElementLabels = [elementLabel1, elementLabel2, ..., elementLabel~]
        length = numberEndostealElementLabels (not defined)
        dtype = int
    '''

    radiusList = np.sqrt(callusElemCenterCoords[:, 0]**2 + callusElemCenterCoords[:, 2]**2)
    endostealElementLabels = np.array(np.where(radiusList < 6)[0], dtype = int) + 1                                       #former elementsWithinRadius
    # heightList = callusElemCenterCoords[:, 1]
    # elementsWithinHeight = np.array(np.where(np.absolute(heightList) < 1.5)[0], dtype = int) + 1
    # endostealElementLabels = np.intersect1d(elementsWithinRadius, elementsWithinHeight)

###

def updatePerfusion(numberCallusElements, callusProperties, outputMatrix):
    global updatedPerfusion
    updatedPerfusion = np.maximum(np.zeros(numberCallusElements), 
        callusProperties[:, 0] + outputMatrix[:, 0], dtype = float)                                                     #update value and check if >= 0.0
    updatedPerfusion = np.minimum(np.ones(numberCallusElements), updatedPerfusion, dtype = float)                       #check if <= 1.0

###

def updateWovBoneConc(numberCallusElements, callusProperties, outputMatrix):
    global updatedWovBoneConc
    updatedWovBoneConc = callusProperties[:, 4] + outputMatrix[:, 3]                                                    #update value
    updatedWovBoneConc = np.minimum(np.ones(numberCallusElements), updatedWovBoneConc, dtype = float)                   #check if <= 1.0
    updatedWovBoneConc = np.maximum(np.zeros(numberCallusElements), updatedWovBoneConc, dtype = float)                  #check if >= 0.0

###

def updateMnrlCartConc(numberCallusElements, callusProperties, outputMatrix):
    global updatedMnrlCartConc
    updatedMnrlCartConc = callusProperties[:, 3] + outputMatrix[:, 2]                                                   #update value
    updatedMnrlCartConc = np.minimum(np.ones(numberCallusElements) - callusProperties[:, 4], 
        updatedMnrlCartConc, dtype = float)                                                                             #check if <= 1.0 - wovBoneConc
    updatedMnrlCartConc = np.maximum(np.zeros(numberCallusElements), updatedMnrlCartConc, dtype = float)                #check if >= 0.0

###

def updateSoftCartConc(numberCallusElements, callusProperties, outputMatrix):
    global updatedSoftCartConc
    updatedSoftCartConc = callusProperties[:, 2] + outputMatrix[:, 1]                                                   #update value
    updatedSoftCartConc = np.minimum(np.ones(numberCallusElements) - callusProperties[:, 3] - callusProperties[:, 4], 
        updatedSoftCartConc, dtype = float)                                                                             #check if <= 1.0 - wovBoneConc - mnrlCartConc
    updatedSoftCartConc = np.maximum(np.zeros(numberCallusElements), updatedSoftCartConc, dtype = float)                #check if >= 0.0

###

def updateAdjPerfusion(numberCallusElements, callusProperties, callusElemElemConnectivity, callusElemPositioning):
    global updatedAdjPerfusion
    firstNeighborPerfusionValues  = np.array(callusProperties[callusElemElemConnectivity[:, :4]-1, 0] * 
                                    (callusElemElemConnectivity[:, :4] != 0).astype(int))                               #perfusion values of first neighbor elements
    # secondNeighborPerfusionValues = np.array(callusProperties[callusElemElemConnectivity[:, 4:29]-1, 0] * 
                                    # (callusElemElemConnectivity[:, :4] != 0).astype(int))                               #perfusion values of second neighbor elements
    # thirdNeighborPerfusionValues  = np.array(callusProperties[callusElemElemConnectivity[:, 29:]-1, 0] * 
                                    # (callusElemElemConnectivity[:, :4] != 0).astype(int))                               #perfusion values of third neighbor elements

    adjPerfusionSoftTiss = 0.3 * np.logical_and(callusElemPositioning[:, 0],                                            #adjPerfusionSoftTiss = 0.3 if peripheral[:, 0] AND
        np.logical_not(np.logical_or(callusElemPositioning[:, 1], callusElemPositioning[:, 2])))                        #       not (boneContact[:, 1] OR endoCortical[:, 2])
    adjPerfusionEndoCortical = min(0.9, (0.8/63.0*float(day) + 0.1)) * np.logical_and(
        callusElemPositioning[:, 0], np.logical_and(np.logical_not(callusElemPositioning[:, 1]), 
        callusElemPositioning[:, 2]))                                                                                   #adjPerfusionEndoCortical = 0.1/0.9 if peripheral[:, 0] AND not boneContact[:, 1] AND endoCortical[:, 2])
    adjPerfusionBoneContact = 1.0 * np.logical_and(callusElemPositioning[:, 1], 
        np.logical_not(callusElemPositioning[:, 3]))                                                                    #adjPerfusionBoneContact = 1 if boneContact[:, 1] AND not fractureEndContact[:, 3]
    adjPerfusionPeripheral = adjPerfusionBoneContact + adjPerfusionSoftTiss + adjPerfusionEndoCortical
    updatedAdjPerfusion = np.amax(np.concatenate((firstNeighborPerfusionValues, 
        #secondNeighborPerfusionValues * 0.75, thirdNeighborPerfusionValues * 0.5,
        np.reshape(adjPerfusionPeripheral, (numberCallusElements, 1))), axis = 1), axis=1)                              #maximum value of perfusion in an adjacent element

# def updateAdjPerfusion(numberCallusElements, callusProperties, callusElemElemConnectivity, callusElemPositioning):
#     global updatedAdjPerfusion
#     firstNeighborPerfusionValues  = np.array(callusProperties[callusElemElemConnectivity[:, :4]-1, 0] * 
#                                     (callusElemElemConnectivity[:, :4] != 0).astype(int))                               #perfusion values of first neighbor elements
#     # secondNeighborPerfusionValues = np.array(callusProperties[callusElemElemConnectivity[:, 4:29]-1, 0] * 
#                                     # (callusElemElemConnectivity[:, :4] != 0).astype(int))                               #perfusion values of second neighbor elements
#     # thirdNeighborPerfusionValues  = np.array(callusProperties[callusElemElemConnectivity[:, 29:]-1, 0] * 
#                                     # (callusElemElemConnectivity[:, :4] != 0).astype(int))                               #perfusion values of third neighbor elements
#     if day < perfusionThroughMarrowTime:
#         adjPerfusionNotBoneContact = 0.3 * np.logical_and(callusElemPositioning[:, 0],                                  #adjPerfusionNotBoneContact = 0.3 if peripheral[:, 0] AND
#             np.logical_not(np.logical_or(callusElemPositioning[:, 1], callusElemPositioning[:, 2])))                    #       not (boneContact[:, 1] OR endoCortical[:, 2])
#     else:
#         adjPerfusionNotBoneContact = 0.3 * np.logical_and(callusElemPositioning[:, 0], 
#             np.logical_not(callusElemPositioning[:, 1]))                                                                #adjPerfusionNotBoneContact = 0.3 if peripheral[:, 0] AND not boneContact[:, 1]
#     adjPerfusionBoneContact = 1.0 * np.logical_and(callusElemPositioning[:, 1], 
#         np.logical_not(callusElemPositioning[:, 3]))                                                                    #adjPerfusionBoneContact = 1 if boneContact[:, 1] AND not fractureEndContact[:, 3]
#     adjPerfusionPeripheral = adjPerfusionBoneContact + adjPerfusionNotBoneContact
#     updatedAdjPerfusion = np.amax(np.concatenate((firstNeighborPerfusionValues, 
#         #secondNeighborPerfusionValues * 0.75, thirdNeighborPerfusionValues * 0.5,
#         np.reshape(adjPerfusionPeripheral, (numberCallusElements, 1))), axis = 1), axis=1)                              #maximum value of perfusion in an adjacent element

###

def updateAdjWovBoneConc(numberCallusElements, callusProperties, callusElemElemConnectivity):
    global updatedAdjWovBoneConc
    adjWovBoneConcValues = np.array(callusProperties[callusElemElemConnectivity[:, :4]-1, 4] * 
                                    (callusElemElemConnectivity[:, :4] != 0).astype(int))                               #wovBoneConc values of all adjacent elements
    adjWovBoneConcPeripheral = callusElemPositioning[:, 1] * 1.0                                                        #adjWovBoneConcPeripheral = 1 if boneContact
    updatedAdjWovBoneConc = np.amax(np.concatenate((adjWovBoneConcValues, 
        np.reshape(adjWovBoneConcPeripheral, (numberCallusElements, 1))), axis = 1), axis=1)                            #maximum value of wovBoneConc in an adjacent element

###

def updateCallusMaterialNames(callusProperties):                                                                        #softCart = softCartConc
    global updatedCallusMaterialNames                                                                                   #woveBone = mnrlCartConc + wovBoneConc
    #updatedCallusMaterialNames = ['softCartX.XXmnrlCartX.XXwovBoneX.XX']*numberCallusElements
    roundedSoftCartConc = np.round(callusProperties[:, 2] / 0.02) * 0.02
    roundedMnrlCartConc = np.round(callusProperties[:, 3] / 0.02) * 0.02
    roundedWovBoneConc  = np.round(callusProperties[:, 4] / 0.02) * 0.02
    overshoot = np.maximum(roundedSoftCartConc + roundedMnrlCartConc + roundedWovBoneConc - np.ones(numberCallusElements), 
        np.zeros(numberCallusElements))                                                                                 #due to rounding, sum can be >1.0 (='overshoot')
    roundedSoftCartConc = np.absolute(np.round_(roundedSoftCartConc - overshoot, decimals=2))                           #this 'overshoot' is subtracted from roundedSoftCartConc
    roundedSoftCartConcStr = np.array(["{:.2f}".format(np.round(i, 2)) for i in roundedSoftCartConc])
    roundedMnrlCartConcStr = np.array(["{:.2f}".format(np.round(i, 2)) for i in roundedMnrlCartConc])
    roundedWovBoneConcStr  = np.array(["{:.2f}".format(np.round(i, 2)) for i in  roundedWovBoneConc])
    updatedCallusMaterialNames = [''.join(i) for i in 
        zip(['softCart'] * numberCallusElements, roundedSoftCartConcStr, 
            ['mnrlCart'] * numberCallusElements, roundedMnrlCartConcStr, 
            [ 'wovBone'] * numberCallusElements,  roundedWovBoneConcStr)]