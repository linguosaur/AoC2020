import sys

def readInput(filename):
	return open(filename).read().split()

def getSeatLoc(boardingPass):
	charMap = {'F':'0','B':'1','L':'0','R':'1'}
	row = int(''.join([charMap[char] for char in boardingPass[:7]]),2)
	col = int(''.join([charMap[char] for char in boardingPass[7:10]]),2)

	return (row,col)

def getSeatID(boardingPass):
	row,col = getSeatLoc(boardingPass)
	return row*8 + col

def findMissingSeats(boardingPasses):
	seatIDs = [getSeatID(bp) for bp in boardingPasses]
	return set(range(min(seatIDs),max(seatIDs)+1)) - set(seatIDs)


boardingPasses = readInput(sys.argv[1])
print(max([getSeatID(bp) for bp in boardingPasses]))
print(findMissingSeats(boardingPasses))
