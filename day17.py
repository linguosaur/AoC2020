import sys

def readInput(filename):
	return [list(line) for line in open(filename).read().split()]

class PockDim:

	def __init__(self, initCubesChart, dims):
		self.dims = dims
		self.activeCubes = set([])
		for r in range(len(initCubesChart)):
			for c in range(len(initCubesChart[0])):
				if initCubesChart[r][c] == '#':
					self.activeCubes.add(tuple((dims-2)*[0] + [r,c]))

	def getActiveAreaBounds(self):
		if len(self.activeCubes) == 0:
			return None

		bounds = []
		for dim in range(self.dims):
			dimValues = [cube[dim] for cube in self.activeCubes]
			bounds.append((min(dimValues), max(dimValues)))

		return tuple(bounds)

	def getNextCube(self, cube, bounds):
		if cube == None:
			return tuple([minVal for minVal, maxVal in bounds])

		nextCube, increment = list(cube), True
		dim = self.dims - 1
		while increment:
			nextCube[dim] = cube[dim] + 1
			minVal, maxVal = bounds[dim]
			if nextCube[dim] > maxVal:
				if dim == 0:
					return None
				nextCube[dim] = minVal
				dim -= 1
			else:
				increment = False

		return tuple(nextCube)

	def printCubes(self):
		bounds = self.getActiveAreaBounds()
		(minR, maxR), (minC, maxC) = bounds[-2:]
		
		iterator = self.getNextCube(None, bounds)
		coordsHead = iterator[:-2]

		print('Slice: ', coordsHead,'\n')
		while iterator != None:
			if iterator[:-2] != coordsHead:
				coordsHead = iterator[:-2]
				print('Slice: ', coordsHead,'\n')
			
			if iterator in self.activeCubes:
				sys.stdout.write('#')
			else:
				sys.stdout.write('.')

			r, c = iterator[-2:]
			if c == maxC:
				sys.stdout.write('\n')

			iterator = self.getNextCube(iterator, bounds)
			if iterator != None and iterator[:-2] != coordsHead:
				print()
		
		sys.stdout.write('\n')
	
	def getCube(self, coord):
		if coord in self.activeCubes:
			return '#'
		return '.'
	
	def areAdjacent(self, coords1, coords2):
		for dim in range(self.dims):
			if abs(coords1[dim] - coords2[dim]) > 1:
				return False

		return coords1 != coords2

	def getAdjacentActives(self, coord):
		return [activeCube for activeCube in self.activeCubes if self.areAdjacent(activeCube, coord)]
	
	def shouldBeActive(self, coord):
		adjacentActives = self.getAdjacentActives(coord)
		stayActive = coord in self.activeCubes and len(adjacentActives) in [2,3]
		activate = coord not in self.activeCubes and len(adjacentActives) == 3

		return stayActive or activate
	
	def setNextCubes(self):
		newActives = set([])
		bounds = list(self.getActiveAreaBounds())

		for dim in range(self.dims):
			minVal, maxVal = bounds[dim]
			bounds[dim] = (minVal-1, maxVal+1)

		iterator = self.getNextCube(None, bounds)
		while iterator != None:
			if self.shouldBeActive(iterator):
				newActives.add(iterator)
			iterator = self.getNextCube(iterator, bounds)

		self.activeCubes = newActives

	def cycle(self, cycles):
		for i in range(cycles):
			self.setNextCubes()
			#print('After ', i+1, ' cycle(s):', '\n')
			#self.printCubes()

	def countActives(self):
		return len(self.activeCubes)


cubesChart = readInput(sys.argv[1])
pockDim3D = PockDim(cubesChart, 3)
#print('Before any cycles:', '\n')
#pockDim3D.printCubes()
pockDim3D.cycle(6)
print(pockDim3D.countActives())

pockDim4D = PockDim(cubesChart, 4)
#print('Before any cycles:', '\n')
#pockDim4D.printCubes()
pockDim4D.cycle(6)
print(pockDim4D.countActives())
