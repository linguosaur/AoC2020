import sys

def readInput(filename):
	return open(filename).read().rstrip().split()

class Floor:

	directions = set(['e', 'w', 'ne', 'nw', 'se', 'sw'])

	def __init__(self, tiles={}):
		self.tiles = tiles # True if black, False if white

	def parseTileDir(tileDirString):
		parsed = []
		strBuffer = ''
		for char in tileDirString:
			if len(strBuffer) == 0:
				if char in ['e','w']:
					parsed.append(char)
				else:
					strBuffer += char
			else:
				parsed.append(strBuffer+char)
				strBuffer = ''

		return parsed

	def parseTilesDir(tilesDirStrings):
		return [Floor.parseTileDir(string) for string in tilesDirStrings]

	def getNewLoc(tileDir, tileLoc):
		row, col = tileLoc
		dRow, dCol = 0, 0
		if len(tileDir) == 1:
			if tileDir[0] == 'e':
				dCol += 1
			else:
				dCol -= 1
		elif tileDir[0] in ['n','s']:
			if row % 2 == 0:
				if tileDir[1] == 'w':
					dCol -= 1
			else:
				if tileDir[1] == 'e':
					dCol += 1
			if tileDir[0] == 'n':
				dRow -= 1
			else:
				dRow += 1

		return (row+dRow, col+dCol)

	def getTileLoc(tileDirs, start=(0,0)):
		row, col = start
		for tileDir in tileDirs:
			row, col = Floor.getNewLoc(tileDir, (row, col))

		return (row, col)

	def getBlackBounds(self):
		rows = set([row for row, col in self.tiles.keys()])
		cols = set([col for row, col in self.tiles.keys()])
		
		return (min(rows), max(rows), min(cols), max(cols))

	def flipTile(self, tileLoc):
		if tileLoc in self.tiles:
			self.tiles[tileLoc] = not self.tiles[tileLoc]
		else:
			self.tiles[tileLoc] = True

	def flipTiles(self, tilesDirs):
		for tileDirs in tilesDirs:
			self.flipTile(Floor.getTileLoc(tileDirs))

	def getTileColour(self, tileLoc):
		if tileLoc in self.tiles:
			return self.tiles[tileLoc]
		return False

	def countBlackTiles(self):
		return list(self.tiles.values()).count(True)

	def countAdjacentBlackTiles(self, tileLoc):
		adjLocs = set([Floor.getNewLoc(tileDir, tileLoc) for tileDir in Floor.directions])

		adjColours = []
		for adjLoc in adjLocs:
			if adjLoc in self.tiles:
				adjColours.append(self.tiles[adjLoc])
			else:
				adjColours.append(False)

		return adjColours.count(True)

	def doFlip(self, tileLoc):
		numAdjBlackTiles = self.countAdjacentBlackTiles(tileLoc)
		if self.getTileColour(tileLoc) == True and (numAdjBlackTiles == 0 or numAdjBlackTiles > 2):
			return True
		if self.getTileColour(tileLoc) == False and numAdjBlackTiles == 2:
			return True

		return False

	def applyRules(self, days):
		for day in range(days):
			newFloor = Floor(self.tiles.copy())
			minRow, maxRow, minCol, maxCol = self.getBlackBounds()
			for row in range(minRow-1, maxRow+2):
				for col in range(minCol-1, maxCol+2):
					if self.doFlip((row, col)):
						newFloor.flipTile((row,col))
			#print('Day', day+1, ':', newFloor.countBlackTiles())
			self.tiles = newFloor.tiles.copy()

	def printTiles(self):
		for tileLoc, isBlack in self.tiles.items():
			colour = 'white'
			if isBlack: colour = 'black'
			print('Tile', tileLoc, 'is', colour, '.')

dirStrings = readInput(sys.argv[1])
floor = Floor()
tilesDirs = Floor.parseTilesDir(dirStrings)
floor.flipTiles(tilesDirs)
print(floor.countBlackTiles())

floor.applyRules(100)
print(floor.countBlackTiles())
