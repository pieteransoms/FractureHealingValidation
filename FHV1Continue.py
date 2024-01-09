daysToAdd = 43

###restart matlab engine
matlabengine = matlab.engine.start_matlab()

daysPast = day
print '--- Continuing from day ' + str(daysPast+1) + ' onwards'

###loop
for day in range(daysPast+1, daysPast+1+daysToAdd):
    loopTic = time.clock()
    execfile(loopFile)
    loopToc = time.clock()
    print '--- Day ' + str(day) + '/' + str(int(daysPast + daysToAdd)) + ' done (total time: ' + str(int(loopToc-loopTic)) + ' seconds)'

###close txt file and quit matlab session
wb.save(resultsMap + '\FHV1.xls')
matlabengine.quit()