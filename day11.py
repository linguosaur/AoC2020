import sys

def readInput(filename):
	return [list(line) for line in open(filename).read().split()]

def getAdjacentSeats(row, col, seatMap):
	return [seatMap[r][c] for r in range(max(0,row-1), min(len(seatMap),row+2)) for c in range(max(0,col-1), min(len(seatMap[0]),col+2)) if r != row or c != col]

def shouldOccupy(row, col, seatMap):
	return seatMap[row][col] == 'L' and '#' not in getAdjacentSeats(row, col, seatMap)

def shouldEmpty(row, col, seatMap):
	return seatMap[row][col] == '#' and getAdjacentSeats(row, col, seatMap).count('#') > 3

def getVisibleSeat(row, col, rowStep, colStep, seatMap):
	r, c = row + rowStep, col + colStep
	while r >= 0 and r < len(seatMap) and c >= 0 and c < len(seatMap[0]):
		if seatMap[r][c] != '.':
			return seatMap[r][c]
		r += rowStep
		c += colStep

	return '.'

def getVisibleSeats(row, col, seatMap):
	return [getVisibleSeat(row, col, rowStep, colStep, seatMap) for rowStep in [-1, 0, 1] for colStep in [-1, 0, 1] if rowStep != 0 or colStep != 0]

def shouldOccupy2(row, col, seatMap):
	return seatMap[row][col] == 'L' and '#' not in getVisibleSeats(row, col, seatMap)

def shouldEmpty2(row, col, seatMap):
	return seatMap[row][col] == '#' and getVisibleSeats(row, col, seatMap).count('#') > 4

def applyRules(seatMap):
	oldSeatMap, newSeatMap = seatMap, None

	while newSeatMap != oldSeatMap:
		if newSeatMap != None:
			oldSeatMap = newSeatMap
		newSeatMap = []
		for r in range(len(oldSeatMap)):
			newSeatMap.append([])
			for c in range(len(oldSeatMap[0])):
				newSeatMap[r].append(oldSeatMap[r][c])
				if shouldOccupy(r, c, oldSeatMap):
					newSeatMap[r][c] = '#'
				elif shouldEmpty(r, c, oldSeatMap):
					newSeatMap[r][c] = 'L'
	
	return newSeatMap

def applyRules2(seatMap):
	oldSeatMap, newSeatMap = seatMap, None

	while newSeatMap != oldSeatMap:
		if newSeatMap != None:
			oldSeatMap = newSeatMap
		newSeatMap = []
		for r in range(len(oldSeatMap)):
			newSeatMap.append([])
			for c in range(len(oldSeatMap[0])):
				newSeatMap[r].append(oldSeatMap[r][c])
				if shouldOccupy2(r, c, oldSeatMap):
					newSeatMap[r][c] = '#'
				elif shouldEmpty2(r, c, oldSeatMap):
					newSeatMap[r][c] = 'L'
	
	return newSeatMap

def getPrintable(seatMap):
	return '\n'.join(list(map(''.join, seatMap)))

def countOccupied(seatMap):
	return sum([row.count('#') for row in seatMap])


seatMap = readInput(sys.argv[1])
finalSeatMap = applyRules(seatMap)
print(getPrintable(finalSeatMap))
print(countOccupied(finalSeatMap))

print()

finalSeatMap2 = applyRules2(seatMap)
print(getPrintable(finalSeatMap2))
print(countOccupied(finalSeatMap2))
