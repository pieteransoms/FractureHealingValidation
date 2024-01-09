###update callusMaterialNames
updateCallusMaterialNames(callusProperties)
callusMaterialNames = updatedCallusMaterialNames

# for elementLabel in range(1,numberCallusElements+1):
    # softCartConc = callusProperties[elementLabel-1, 2]
    # mnrlCartConc = callusProperties[elementLabel-1, 3]
    # wovBoneConc  = callusProperties[elementLabel-1, 4]
    # connTissConc = 1.0-wovBoneConc-mnrlCartConc-softCartConc
    # E  =  EWovBone*wovBoneConc**3 +  ESoftCart*softCartConc**3 +  EMnrlCart*mnrlCartConc**3 +  EConnTiss*connTissConc**3                             #based on experimental relation from Carter and Hayes (1977), used by Shefelbine et al. (2005) and Simon et al. (2011)
    # nu = nuWovBone*wovBoneConc**3 + nuSoftCart*softCartConc**3 + nuMnrlCart*mnrlCartConc**3 + nuConnTiss*connTissConc**3
    # myModel.Material(name='CallusMaterial' + str(elementLabel))
    # myModel.materials['CallusMaterial' + str(elementLabel)].Elastic(table=((E, nu), ))
    

###update elementToTissueAssignment
elementToTissueAssignment = {tissueCompositions[tissue]: [] for tissue in range(len(tissueCompositions))}                               #clear tissueAssignment
for elementLabel in range(1,numberCallusElements+1):                                                                                    #add elementLabels to tissueAssignment
    elementToTissueAssignment[callusMaterialNames[elementLabel-1]].append(elementLabel)
for tissueComposition in tissueCompositions:                                                                                            #assign sections to all elements in each 'bucket'
    if len(elementToTissueAssignment[tissueComposition]) == 1:
        part['CallusPart'].SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE, 
            region=Region(elements=part['CallusPart'].elements[
            elementToTissueAssignment[tissueComposition][0]:elementToTissueAssignment[tissueComposition][0]+1]),                    #meshsequence required
            sectionName=tissueComposition.replace('.',''), thicknessAssignment=FROM_SECTION)
    if len(elementToTissueAssignment[tissueComposition]) > 1:
        part['CallusPart'].SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE, 
            region=Region(elements=part['CallusPart'].elements.sequenceFromLabels(elementToTissueAssignment[tissueComposition])), 
            sectionName=tissueComposition.replace('.',''), thicknessAssignment=FROM_SECTION)

###write results
resultsSheet.write(day, 2, str(sum((np.ones(numberCallusElements)-callusProperties[:, 2]-callusProperties[:, 3]-callusProperties[:, 4])*callusElemVolumes)/sum(callusElemVolumes)))
resultsSheet.write(day, 3, str(sum(callusProperties[:, 2]*callusElemVolumes)/sum(callusElemVolumes)))
resultsSheet.write(day, 4, str(sum(callusProperties[:, 3]*callusElemVolumes)/sum(callusElemVolumes)))
resultsSheet.write(day, 5, str(sum(callusProperties[:, 4]*callusElemVolumes)/sum(callusElemVolumes)))