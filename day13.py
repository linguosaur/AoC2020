import sys
from math import ceil

def readInput(filename):
	earliestDeparture, busIDs = open(filename).read().split()
	return int(earliestDeparture), busIDs.split(',')

def getBoardingTime(earliestDeparture, busID):
	return busID*ceil(earliestDeparture/busID)

def getEarliestBoardingTimeAndBus(earliestDeparture, busIDs):
	earliestBoardingTime, earliestBus = None, None
	for busID in busIDs:
		if busID != 'x':
			boardingTime = getBoardingTime(earliestDeparture, int(busID))
			if earliestBoardingTime == None and earliestBus == None or boardingTime < earliestBoardingTime:
				earliestBoardingTime, earliestBus = boardingTime, int(busID)

	return (earliestBoardingTime, earliestBus)

def getCycles(base1, offset, base2, modulo):
	for i in range(base2):
		if (offset + base1*i) % base2 == modulo:
			return i

# e.g. bases: [17, 13, 19], modulos: [0, 11, 16]
def getLowestModuloMatch(bases, modulos):
	lowestModuloMatch, multipliedBases = 0, 1
	for i in range(1, len(bases)):
		multipliedBases *= bases[i-1]
		cycles = getCycles(multipliedBases, lowestModuloMatch, bases[i], modulos[i])
		lowestModuloMatch += multipliedBases*cycles

	return lowestModuloMatch
		
def getEarliestSeqStartTime(busIDs):
	bases, modulos = [], []
	for i in range(len(busIDs)):
		if busIDs[i] != 'x':
			bases.append(int(busIDs[i]))
			modulos.append(int(busIDs[i])-i%int(busIDs[i]))

	return getLowestModuloMatch(bases, modulos)

earliestDeparture, busIDs = readInput(sys.argv[1])
boardingTime, earliestBus = getEarliestBoardingTimeAndBus(earliestDeparture, busIDs)
print(earliestBus*(boardingTime-earliestDeparture))

print(getEarliestSeqStartTime(busIDs))
