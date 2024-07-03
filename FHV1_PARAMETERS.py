###healing parameters
followUpTime = 70 #days
useLinearSpring = False
kSpring = 100000.0 #N/mm
IFM = 'case A'                                       #case A, case B, 0.0mm, 0.01mm, 0.1mm, 0.25mm, 0.5mm, 1.0mm, 1.25mm, 1.5mm or 2.0mm

numberCPUs = 12

# EConnTiss = 3.0 #MPa                                #according to Simon et al.
EConnTiss = 1.85 #MPa                                #according to Kraaij et al. (2014), Martin et al. (1998), used by Gomez-Benito et al. (2005)
# nuConnTiss = 0.3                                    #according to Simon et al.
nuConnTiss = 0.167                                    #according to Lacroix and Prendergast (2002), used by Isaksson et al. (2005), Kelly and Prendergast (2005)

# ESoftCart = 200.0 #MPa                              #according to Simon et al.
# ESoftCart = 25.0 #MPa                               #Wehner et al.
ESoftCart = 27.055 #MPa                               #Martin et al. (2000), used by Gomez-Benito et al. (2007)
# ESoftCart = 1.0 #MPa                               #Tanck et al. https://doi.org/10.1016/j.bone.2004.02.015
# nuSoftCart = 0.45                                   #according to Simon et al.
nuSoftCart = 0.167                                   #Jurvelin et al. (1997), used by Lacroix and Prendergast (2002), Isaksson et al. (2005), Kelly and Prendergast (2005)
# expCart = 4.5                                       #exponent for cartilage in rule of mixtures for E

# EMnrlCart = 4000.0 #MPa                             #currently copied from wovBone
EMnrlCart = 320.0 #MPa                              #Mente and Lewis (1997), used by Prendergast et al. (1997)
# EMnrlCart = 100.0 #MPa                              #Tanck et al. https://doi.org/10.1016/j.bone.2004.02.015
nuMnrlCart = 0.2                                   #Roemhildt et al. (2012)

EWovBone = 1000.0 #MPa                              #Lacroix and Prendergast (2002), used by Isaksson et al. (2011)
# EWovBone = 4000.0 #MPa                              #according to Simon et al.
# nuWovBone = 0.36                                    #according to Simon et al.
nuWovBone = 0.3                                    #according to Rho et al. (1995), used by Lacroix and Prendergast (1999), Ament and Hofer (2000), Shefelbine et al. (2005), Wehner et al. (2010), 
# expWovBone = 3.1                                    #exponent for woven bone in rule of mixtures for E

ECortBone = 10000.0 #MPa                            #according to Lotz et al. (1991), used by Wehner et al. (2010), Simon et al. (2011), Wilson et al. (2017), Fu et al. (2022)
# nuCortBone = 0.36                                   #according to Simon et al.
nuCortBone = 0.325                                   #according to Cowin (1999), used by Isaksson et al. (2005)

fuzzyModel = 'Ansoms_v04'

load = 500.0 #N

# distanceForVicinity = 1.0 #mm
marrowRadius = 6.0 #mm
if IFM == 'case A':
    fractureEndRegion = 1.05 + 2 #mm
elif IFM == 'case B':
    fractureEndRegion = 1.55 + 2 #mm
perfusionThroughMarrowTime = 10 #days               #perfusion through bone marrow starts later
# callusRefElemVolume = 0.14 #mm^3                    #the tissue updates are scaled with refVolume/elemVolume to eliminate mesh dependency