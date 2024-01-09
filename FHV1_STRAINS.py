###open odb file
odbFile = currWorkDir + '/' + jobName + '.odb'
myOdb = openOdb(path = odbFile, readOnly = False)

###extract strains
E = np.array(myOdb.steps['LoadingStep'].frames[-1].fieldOutputs['LE'].bulkDataBlocks[0].data, dtype = float)
E11 = E[:, 0]
E22 = E[:, 1]
E33 = E[:, 2]

###distStrain
callusProperties[:, 6] = np.reshape(np.array(np.sqrt((np.square(E11-E22) + np.square(E22-E33) + np.square(E33-E11))/2), dtype = float), -1)

###dilaStrain
callusProperties[:, 7] = np.reshape(np.array((E11 + E22 + E33)/3, dtype = float), -1)

###extract displacement
displacement = -myOdb.steps['LoadingStep'].historyRegions['Node ASSEMBLY.2'].historyOutputs['U2'].data[-1][1]                                                               #displacement of AttachPoint2
resultsSheet.write(day, 0, str(day))
resultsSheet.write(day, 1, str(displacement))

###close odb file
myOdb.close()