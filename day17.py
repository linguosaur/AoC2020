import sys

def readInput(filename):
	return [list(line) for line in open(filename).read().split()]

class PockDim3D:

	def __init__(self, initCubesChart):
		self.activeCubes = set([])
		for r in range(len(initCubesChart)):
			for c in range(len(initCubesChart[0])):
				if initCubesChart[r][c] == '#':
					self.activeCubes.add((0,r,c))

	def getActiveAreaBounds(self):
		levels, rows, cols = [z for z,r,c in self.activeCubes], [r for z,r,c in self.activeCubes], [c for z,r,c in self.activeCubes]
		return ((min(levels), max(levels)), (min(rows), max(rows)), (min(cols), max(cols)))

	def printCubes(self):
		((minZ,maxZ),(minR,maxR), (minC,maxC)) = self.getActiveAreaBounds()
		for z in range(minZ, maxZ+1):
			print('z=', z,'\n')
			for r in range(minR, maxR+1):
				for c in range(minC, maxC+1):
					if (z,r,c) in self.activeCubes:
						sys.stdout.write('#')
					else:
						sys.stdout.write('.')
				sys.stdout.write('\n')
			sys.stdout.write('\n')
	
	def getCube(self, level, row, col):
		if (level, row, col) in self.activeCubes:
			return '#'
		return '.'
	
	def areAdjacent(coords1, coords2):
		(z1,r1,c1), (z2,r2,c2) = coords1, coords2
		return coords1 != coords2 and abs(z1-z2) <= 1 and abs(r1-r2) <= 1 and abs(c1-c2) <= 1

	def getAdjacentActives(self, level, row, col):
		return [(z,r,c) for (z,r,c) in self.activeCubes if PockDim3D.areAdjacent((z,r,c),(level,row,col))]
	
	def shouldBeActive(self, level, row, col):
		adjacentActives = self.getAdjacentActives(level, row, col)
		stayActive = (level,row,col) in self.activeCubes and len(adjacentActives) in [2,3]
		activate = (level,row,col) not in self.activeCubes and len(adjacentActives) == 3

		return stayActive or activate
	
	def setNextCubes(self):
		newActives, cycles = set([]), 0
		(minZ, maxZ), (minR, maxR), (minC, maxC) = self.getActiveAreaBounds()
	
		for z in range(minZ-1, maxZ+1+1):
			for r in range(minR-1, maxR+1+1):
				for c in range(minC-1, maxC+1+1):
					if self.shouldBeActive(z, r, c):
						newActives.add((z,r,c))

		self.activeCubes = newActives

	def cycle(self, cycles):
		for i in range(cycles):
			self.setNextCubes()
			#print('After ', i+1, ' cycle(s):', '\n')
			#self.printCubes()

	def countActives(self):
		return len(self.activeCubes)

class PockDim4D:

	def __init__(self, initCubesChart):
		self.activeCubes = set([])
		for r in range(len(initCubesChart)):
			for c in range(len(initCubesChart[0])):
				if initCubesChart[r][c] == '#':
					self.activeCubes.add((0,0,r,c))

	def getActiveAreaBounds(self):
		wizzes = [w for w,z,r,c in self.activeCubes]
		levels = [z for w,z,r,c in self.activeCubes]
		rows = [r for w,z,r,c in self.activeCubes]
		cols = [c for w,z,r,c in self.activeCubes]

		return ((min(wizzes), max(wizzes)), (min(levels), max(levels)), (min(rows), max(rows)), (min(cols), max(cols)))

	def printCubes(self):
		((minW, maxW), (minZ,maxZ),(minR,maxR), (minC,maxC)) = self.getActiveAreaBounds()
		for w in range(minW, maxW+1):
			for z in range(minZ, maxZ+1):
				print('z=', z, 'w=', w, '\n')
				for r in range(minR, maxR+1):
					for c in range(minC, maxC+1):
						if (w,z,r,c) in self.activeCubes:
							sys.stdout.write('#')
						else:
							sys.stdout.write('.')
					sys.stdout.write('\n')
				sys.stdout.write('\n')
	
	def getCube(self, level, row, col):
		if (wiz, level, row, col) in self.activeCubes:
			return '#'
		return '.'
	
	def areAdjacent(coords1, coords2):
		(w1,z1,r1,c1), (w2,z2,r2,c2) = coords1, coords2
		return coords1 != coords2 and abs(w1-w2) <= 1 and abs(z1-z2) <= 1 and abs(r1-r2) <= 1 and abs(c1-c2) <= 1

	def getAdjacentActives(self, cubeLoc):
		return [(w,z,r,c) for (w,z,r,c) in self.activeCubes if PockDim4D.areAdjacent((w,z,r,c),cubeLoc)]
	
	def shouldBeActive(self, cubeLoc):
		adjacentActives = self.getAdjacentActives(cubeLoc)
		stayActive = cubeLoc in self.activeCubes and len(adjacentActives) in [2,3]
		activate = cubeLoc not in self.activeCubes and len(adjacentActives) == 3

		return stayActive or activate
	
	def setNextCubes(self):
		newActives, cycles = set([]), 0
		(minW, maxW), (minZ, maxZ), (minR, maxR), (minC, maxC) = self.getActiveAreaBounds()

		for w in range(minW-1, maxW+1+1):
			for z in range(minZ-1, maxZ+1+1):
				for r in range(minR-1, maxR+1+1):
					for c in range(minC-1, maxC+1+1):
						if self.shouldBeActive((w,z,r,c)):
							newActives.add((w,z,r,c))
	
		self.activeCubes = newActives

	def cycle(self, cycles):
		for i in range(cycles):
			self.setNextCubes()
			#print('After ', i+1, ' cycle(s):', '\n')
			#self.printCubes()

	def countActives(self):
		return len(self.activeCubes)

cubesChart = readInput(sys.argv[1])
pockDim3D = PockDim3D(cubesChart)
#print('Before any cycles:', '\n')
#pockDim3D.printCubes()
pockDim3D.cycle(6)
print(pockDim3D.countActives())

pockDim4D = PockDim4D(cubesChart)
#print('Before any cycles:', '\n')
#pockDim4D.printCubes()
pockDim4D.cycle(6)
print(pockDim4D.countActives())
