###create workbook
wb = xlwt.Workbook()

###create sheets
paramSheet = wb.add_sheet('Parameters')
resultsSheet = wb.add_sheet('Results')

###write material parameters
paramSheet.write(0, 1, 'Connective tissue')
paramSheet.write(0, 2, 'Soft Cartilage')
paramSheet.write(0, 3, 'Mineralized Cartilage')
paramSheet.write(0, 4, 'Woven bone')
paramSheet.write(0, 5, 'Cortical bone')
# paramSheet.write(0, 6, 'Plate')
# paramSheet.write(0, 7, 'Screws')

paramSheet.write(1, 0, 'E [MPa]')
paramSheet.write(1, 1, EConnTiss)
paramSheet.write(1, 2, ESoftCart)
paramSheet.write(1, 3, EMnrlCart)
paramSheet.write(1, 4, EWovBone)
paramSheet.write(1, 5, ECortBone)
# paramSheet.write(1, 6, ETi6Al4V)
# paramSheet.write(1, 7, ETi6Al4V)

paramSheet.write(2, 0, 'nu')
paramSheet.write(2, 1, nuConnTiss)
paramSheet.write(2, 2, nuSoftCart)
paramSheet.write(2, 3, nuSoftCart)
paramSheet.write(2, 4, nuWovBone)
paramSheet.write(2, 5, nuCortBone)
# paramSheet.write(2, 6, nuTi6Al4V)
# paramSheet.write(2, 7, nuTi6Al4V)

###write healing parameters
paramSheet.write(5, 0, 'Fuzzy model')
paramSheet.write(5, 1, fuzzyModel)

###write detail information
paramSheet.write(6, 0, 'Max IFM')
paramSheet.write(6, 1, IFM)

###template for results
resultsSheet.write(0,  0, 'day')
resultsSheet.write(0,  1, 'displacement')
resultsSheet.write(0,  2, 'intercorticalSoftCartConc')
resultsSheet.write(0,  3, 'intercorticalMnrlCartConc')
resultsSheet.write(0,  4, 'intercorticalWovBoneConc')
resultsSheet.write(0,  5, 'periostealSoftCartConc')
resultsSheet.write(0,  6, 'periostealMnrlCartConc')
resultsSheet.write(0,  7, 'periostealWovBoneConc')
resultsSheet.write(0,  8, 'endostealSoftCartConc')
resultsSheet.write(0,  9, 'endostealMnrlCartConc')
resultsSheet.write(0, 10, 'endostealWovBoneConc')
if extractCallusStiffness:
    resultsSheet.write(0, 11, 'callusStiffnessCompression')
    resultsSheet.write(0, 12, 'callusStiffnessBending')
    resultsSheet.write(0, 13, 'callusStiffnessTorsion')