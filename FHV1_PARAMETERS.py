###healing parameters
followUpTime = 56 #days
detail = 'case A'                                   #Debug, VeryRough (1.4mm), Rough (1.2mm), Normal (1mm), Fine (0.8mm) or VeryFine (0.6mm)
useLinearSpring = False
kSpring = 1000.0 #N/mm
IFM = 'skip'                                       #0.0mm, 0.01mm, 0.1mm, 0.25mm, 0.5mm, 1.0mm, 1.25mm, 1.5mm or 2.0mm

numberCPUs = 12

# tissueCompositionAtDays = [1, 7, 14, 21, 28, 35, 42]

EConnTiss = 3.0 #MPa                                #according to Simon et al.
nuConnTiss = 0.3                                    #according to Simon et al.

# ESoftCart = 200.0 #MPa                              #according to Simon et al.
ESoftCart = 25.0 #MPa                               #Wehner et al.
# ESoftCart = 1.0 #MPa                               #Tanck et al. https://doi.org/10.1016/j.bone.2004.02.015
nuSoftCart = 0.45                                   #according to Simon et al.
# expCart = 4.5                                       #exponent for cartilage in rule of mixtures for E

# EMnrlCart = 4000.0 #MPa                             #currently copied from wovBone
EMnrlCart = 100.0 #MPa                              #https://pubmed.ncbi.nlm.nih.gov/7931780/
# EMnrlCart = 100.0 #MPa                              #Tanck et al. https://doi.org/10.1016/j.bone.2004.02.015
nuMnrlCart = 0.36                                   #currently copied from wovBone

EWovBone = 1000.0 #MPa                              #according to Simon et al.
# EWovBone = 1000.0 #MPa                              #according to Simon et al.
nuWovBone = 0.36                                    #according to Simon et al.
# expWovBone = 3.1                                    #exponent for woven bone in rule of mixtures for E

ECortBone = 10000.0 #MPa                            #according to Simon et al.
nuCortBone = 0.36                                   #according to Simon et al.

ETi6Al4V = 114000.0 #MPa
nuTi6Al4V = 0.33

fuzzyModel = 'Ansoms_v03'                           #choice: Ansoms_v02, Ansoms_v03

load = 500.0 #N

distanceForVicinity = 1.0 #mm
marrowRadius = 6.0 #mm
fractureEndRegion = 2.5 #mm
perfusionThroughMarrowTime = 10 #days               #perfusion through bone marrow starts later
callusRefElemVolume = 0.14 #mm^3                    #the tissue updates are scaled with refVolume/elemVolume to eliminate mesh dependency