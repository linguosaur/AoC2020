import sys

def readInput(filename):
	treemap = []
	with open(filename) as inputfile:
		treemap = list(map(str.rstrip, inputfile.readlines()))

	return treemap

def countTreesOnRoute(treemap, rightStep, downStep):
	r,c,numTrees = 0,0,0
	rows, cols = len(treemap), len(treemap[0])
	treeSymbol = '#'
	while r < rows:
		if treemap[r][c] == treeSymbol:
			numTrees += 1
		c = (c + rightStep) % cols
		r += downStep

	return numTrees
	

treemap = readInput(sys.argv[1])
numTrees = countTreesOnRoute(treemap,3,1)
print(numTrees)
print(countTreesOnRoute(treemap,1,1)*countTreesOnRoute(treemap,3,1)*countTreesOnRoute(treemap,5,1)*countTreesOnRoute(treemap,7,1)*countTreesOnRoute(treemap,1,2))
