import sys
from functools import reduce
from operator import mul

def readInput(filename):
	images = [tile.split('\n') for tile in open(filename).read().rstrip().split('\n\n')]
	tiles = {}
	for image in images:
		idNo = int(image[0][len('Tile '):-len(':')])
		tiles[idNo] = Tile(idNo, image[1:])

	return tiles

class Puzzle:

	def __init__(self, tiles):
		self.tiles = tiles
		self.unmatched = set(tiles.keys())
		self.partlyMatched = set([])
		self.fullyMatched = set([])
		self.coordsToIdno = {}

	def recordMatchedTile(self, idno, fully):
		if fully:
			self.fullyMatched.add(idno)
			if idno in self.partlyMatched: 
				self.partlyMatched.remove(idno)
			if idno in self.unmatched:
				self.unmatched.remove(idno)
			return

		self.partlyMatched.add(idno)
		if idno in self.unmatched:
			self.unmatched.remove(idno)

	def getNeighbourCoords(coords, side):
		row, col = coords
		if side == 'top': return (row-1, col)
		if side == 'bottom': return (row+1, col)
		if side == 'left': return (row, col-1)
		if side == 'right': return (row, col+1)

	def getNewCoords(self, idno, sideWithNeigh=None, neighIdno=None):
		if neighIdno == None:
			return (0,0)

		neighRow, neighCol = self.tiles[neighIdno].loc
		return Puzzle.getNeighbourCoords((neighRow, neighCol), Tile.getOppositeSide(sideWithNeigh))

	def checkFit(self, idno, coords, checkedSide=None):
		for side in set(Tile.sides)-set([checkedSide]):
			neighCoords = Puzzle.getNeighbourCoords(coords, side)
			if neighCoords in self.coordsToIdno:
				neighIdno = self.coordsToIdno[neighCoords]
				tile, neigh = self.tiles[idno], self.tiles[neighIdno]
				tileEdge, neighEdge = tile.getEdge(side), neigh.getEdge(Tile.getOppositeSide(side))
				if tileEdge != Tile.reverseString(neighEdge):
					print(side, 'of', idno, 'does not fit with', Tile.getOppositeSide(side), 'of', neighIdno)
					return False

		return True

	def placeTile(self, idno, coords=(0,0)):
		tile = self.tiles[idno]
		tile.loc = coords
		self.coordsToIdno[tile.loc] = idno

	def getUnmatchedSides(self, tile):
		unmatchedSides = Tile.sides.copy()
		if tile.loc in [(0,0), None]: return unmatchedSides

		row, col = tile.loc
		for side in Tile.sides:
			if Puzzle.getNeighbourCoords((row, col), side) in self.coordsToIdno:
				unmatchedSides.remove(side)

		return unmatchedSides

	def getGrid(self):
		grid = []
		rows = [row for row, col in self.coordsToIdno.keys()]
		cols = [col for row, col in self.coordsToIdno.keys()]
		minRow, maxRow, minCol, maxCol = min(rows), max(rows), min(cols), max(cols)

		for row in range(minRow, maxRow+1):
			grid.append([])
			for col in range(minCol, maxCol+1):
				if (row, col) in self.coordsToIdno:
					grid[-1].append(self.coordsToIdno[(row, col)])
				else:
					grid[-1].append(None)

		return grid

	def printGrid(self):
		grid = self.getGrid()
		print('\nGrid:\n')
		for row in range(len(grid)):
			for col in range(len(grid[0])):
				if grid[row][col] != None:
					sys.stdout.write(repr(grid[row][col]) + ' ')
				else:
					sys.stdout.write('     ')
			print()	
		print()

	def getImage(self):
		grid = self.getGrid()
		image = []
		for row in range(len(grid)):
			for col in range(len(grid[0])):
				croppedImage = self.tiles[grid[row][col]].getCroppedImage()
				if col == 0:
					image += croppedImage
				else:
					for r in range(-1,-len(croppedImage)-1,-1):
						image[r] += croppedImage[r]

		return image

	def printImage(image):
		print('\nImage:')
		for row in image:
			print(row)
		print('\n')

	def getProduct(self):
		rows = [row for row, col in self.coordsToIdno.keys()]
		cols = [col for row, col in self.coordsToIdno.keys()]
		minRow, maxRow, minCol, maxCol = min(rows), max(rows), min(cols), max(cols)
		
		cornerIdnos = [self.coordsToIdno[(row,col)] for row, col in self.coordsToIdno.keys() if row in [minRow, maxRow] and col in [minCol, maxCol]]
		return reduce(mul, cornerIdnos)

	def matchTiles(self):
		firstTileID = next(iter(self.unmatched))
		self.placeTile(firstTileID)
		self.recordMatchedTile(firstTileID, False)

		while len(self.partlyMatched) > 0 and len(self.unmatched) > 0:
			tile1s = self.partlyMatched.copy()
			#print('tile1s:', tile1s)
			for idNo1 in tile1s:
				#print('idNo1:', idNo1)
				tile1 = self.tiles[idNo1]
				tile2matches = set([])
				for side1 in self.getUnmatchedSides(tile1):
					#print(side1)
					tile2s = self.unmatched.copy()
					#print('tile2s:', tile2s)
					for idNo2 in tile2s:
						#print('\tidNo2:', idNo2)
						tile2 = self.tiles[idNo2]
						for side2 in self.getUnmatchedSides(tile2):
							#print('\t',side2)
							if tile1.matchTile(tile2, side1, side2):
								tile2matches.add((idNo2, Tile.getOppositeSide(side1), idNo1))
								break

				#print('tile2matches:', tile2matches)
				if len(tile2matches) == 1:
					idNo2, sideWithNeigh, idNo1 = next(iter(tile2matches))
					self.placeTile(idNo2, self.getNewCoords(idNo2, sideWithNeigh, idNo1))
					self.recordMatchedTile(idNo2, False)
				else:
					for idNo2, sideWithNeigh, idNo1 in tile2matches:
						coords2 = self.getNewCoords(idNo2, sideWithNeigh, idNo1)
						if self.checkFit(idNo2, coords2, sideWithNeigh):
							self.placeTile(idNo2, coords2)
							self.recordMatchedTile(idNo2, False)
				self.printGrid()
				self.recordMatchedTile(idNo1, True)

	def matchPattern(imageCrop, pattern):
		for row in range(len(imageCrop)):
			for col in range(len(imageCrop[0])):
				if pattern[row][col] == '#':
					if imageCrop[row][col] != '#':
						return False

		return True

	def countPatterns(image, pattern):
		tile = Tile(None, image)
		matches, rotations = 0, 0
		patternRows, patternCols = len(pattern), len(pattern[0])

		while rotations < 8:
			image = tile.image
			for row in range(len(image)-patternRows):
				for col in range(len(image[0])-patternCols):
					imageCrop = [image[r][col:col+patternCols] for r in range(row, row+patternRows)]
					if Puzzle.matchPattern(imageCrop, pattern):
						print('(', row, ',', col ,')')
						matches += 1
			
			if matches > 0:
				return matches

			tile.rotateCW90()
			rotations += 1
			print('rotate')
			if rotations == 4:
				tile.flip(True)
				print('horizontal flip')
	
		return matches
	
	def getRoughness(image, pattern):
		patternCount = Puzzle.countPatterns(image, pattern)
		poundsInPattern = sum([row.count('#') for row in pattern])
		poundsInImage = sum([row.count('#') for row in image])

		return poundsInImage - patternCount*poundsInPattern

class Tile:

	sides = ['top', 'right', 'bottom', 'left']

	def __init__(self, idNo, image):
		self.idNo = idNo
		self.image = image
		self.sideLen = len(image)
		self.loc = None

	def reverseString(string):
		return ''.join([string[i] for i in range(len(string)-1,-1,-1)])

	def getEdge(self, side): # all edges run clockwise
		if side == 'top': return self.image[0]
		if side == 'right': return self.getColumn(self.sideLen-1, True)
		if side == 'bottom': return Tile.reverseString(self.image[-1])
		if side == 'left': return self.getColumn(0, False)

	def getColumn(self, col, topToBottom):
		rowNums = list(range(len(self.image)))
		if not topToBottom:
			rowNums.reverse()
		return ''.join([self.image[row][col] for row in rowNums])

	def getOppositeSide(side):
		return Tile.sides[(Tile.sides.index(side)+2) % len(Tile.sides)]

	def getNextSideCW(side):
		return Tile.sides[(Tile.sides.index(side)+1) % len(Tile.sides)]

	def flip(self, horizontal):
		if horizontal:
			self.image = [Tile.reverseString(line) for line in self.image]
		else: # flip vertically
			self.image = [self.image[i] for i in range(len(self.image)-1,-1,-1)]
		return self

	def rotateCW90(self):
		self.image = [self.getColumn(col, False) for col in range(self.sideLen)]
		return self

	def matchTile(self, tile2, side1, side2):
		edge1, edge2 = self.getEdge(side1), tile2.getEdge(side2)
		
		if edge1 == edge2 or edge1 == Tile.reverseString(edge2):
			print('Match between', side1, 'of', self.idNo, 'and', side2, 'of', tile2.idNo)
			if edge1 == edge2:
				if side2 in ['top', 'bottom']:
					print(tile2.idNo, 'horizontal flip')
					tile2.flip(True)
				else: 
					print(tile2.idNo, 'vertical flip')
					tile2.flip(False)
			side2goal = Tile.getOppositeSide(side1)
			while side2 != side2goal:
				print(tile2.idNo, 'rotate clockwise 90 degrees')
				tile2.rotateCW90()
				side2 = Tile.getNextSideCW(side2)

			return True
	
		return False

	def getCroppedImage(self):
		return [''.join([self.image[row][1:len(self.image[row])-1]]) for row in range(1, len(self.image)-1)]

	def printTile(self):
		for line in self.image:
			print(line)


tiles = readInput(sys.argv[1])
puzzle = Puzzle(tiles)
puzzle.matchTiles()
print(puzzle.getProduct(), '\n')

# 3x20
seaMonster = []
seaMonster.append('                  # ')
seaMonster.append('#    ##    ##    ###')
seaMonster.append(' #  #  #  #  #  #   ')

image = puzzle.getImage()
Puzzle.printImage(image)
print(Puzzle.getRoughness(image, seaMonster))
