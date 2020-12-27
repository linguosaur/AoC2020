import sys

class Cup:
	def __init__(self, label, nextCup, origCup, destCup):
		self.label = label
		self.nextCup = nextCup
		self.origCup = origCup
		self.destCup = destCup

class CupRing:

	def __init__(self):
		self.current = None
		self.cup1 = None

	def build(self, cupsString, mode2, numMode2Cups=1000000):
		cups = [int(x) for x in list(cupsString)]
		minCup, numCups = min(cups), len(cups)
		index = {cups[i]:i for i in range(numCups)}

		cupsList = [Cup(cups[0], None, None, None)]
		for i in range(numCups-1):
			cupsList.append(Cup(cups[i+1], None, None, None))
			cupsList[i].nextCup = cupsList[i+1]
		cupsList[-1].nextCup = cupsList[0]
		self.cup1 = cupsList[index[1]]

		for i in range(len(cupsList)):
			cupsList[i].destCup = cupsList[index[(cups[i]-2)%numCups+1]]
			cupsList[i].destCup.origCup = cupsList[i]

		if mode2:
			destCup = cupsList[index[numCups]]
			x = cupsList[-1]
			for i in range(numCups+1, numMode2Cups+1):
				x.nextCup = Cup(i, None, None, destCup)
				x = x.nextCup
				destCup.origCup = x
				destCup = x
			x.nextCup = cupsList[0]
			self.cup1.destCup = x

		self.current = cupsList[0]

	def getCups(start):
		if start != None:
			cupLabels = [start.label]
			x = start.nextCup
			while x != start and x != None:
				cupLabels.append(x.label)
				x = x.nextCup
	
		return cupLabels

	def remove(self, cupsToRemove=3):
		removed = self.current.nextCup
		x = removed
		lastRemoved = None
		for i in range(cupsToRemove):
			if i == cupsToRemove-1:
				lastRemoved = x
			x = x.nextCup
		self.current.nextCup = x
		lastRemoved.nextCup = None

		return removed

	def getRemovedLabels(removed):
		labels = []
		x = removed
		while x != None:
			labels.append(x.label)
			x = x.nextCup

		return labels

	def getDestination(self, removed):
		removedLabels = CupRing.getRemovedLabels(removed)
		destCup = self.current.destCup
		while destCup.label in removedLabels:
			destCup = destCup.destCup
		
		return destCup
	
	def putBack(destCup, removed):
		oldNextCup = destCup.nextCup
		destCup.nextCup = removed
		while removed.nextCup != None:
			removed = removed.nextCup
		removed.nextCup = oldNextCup


def play(cupsString, moves, mode2):
	cups = [int(x) for x in cupsString]
	minCups, numCups = min(cups), max(cups)
	cupsToRemove = 3

	cupRing = CupRing()
	cupRing.build(cupsString, mode2)
	for i in range(moves):
		#print('cups:', '  '.join([str(x) for x in CupRing.getCups(cupRing.current)]))
		#print('current:', cupRing.current.label)
		removed = cupRing.remove(cupsToRemove)
		#print('pick up:', '  '.join([str(x) for x in CupRing.getCups(removed)]))
		destCup = cupRing.getDestination(removed)
		#print('destination:', destCup.label)
		CupRing.putBack(destCup, removed)
		#print()
		cupRing.current = cupRing.current.nextCup

	if mode2:
		firstCup = cupRing.cup1.nextCup
		#print(firstCup.label, firstCup.nextCup.label)
		return firstCup.label * firstCup.nextCup.label

	return ''.join([str(x) for x in CupRing.getCups(cupRing.cup1)[1:]])

#startingCups = '389125467'
startingCups = '368195742'
print(play(startingCups, 100, False))
print(play(startingCups, 10000000, True))
