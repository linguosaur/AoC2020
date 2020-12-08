import regex, sys

def readInput(inputFile):
	return list(map(str.rstrip, open(inputFile).readlines()))

def parseRule(rule):
	match = regex.match(r'(.+) bags contain (?:(\d+) (.+?) bags?, )*(\d+|no) (.+?|other) bags?\.', rule)

	innerBagsTuples = set([])
	if match:
		groups = match.groups()
		outerBag = groups[0]
		if groups[1] != None:
			#innerBagsTuples.add((int(groups[1]), groups[2]))
			for i in range(len(match.captures(2))):
				innerBagsTuples.add((int(match.captures(2)[i]), match.captures(3)[i]))
		if groups[3] != 'no':
			innerBagsTuples.add((int(groups[3]), groups[4]))

	return (outerBag, innerBagsTuples)

def makeRulesTable(rules):
	rulesTable = {}
	for rule in rules:
		outerBag, innerBags = parseRule(rule)
		rulesTable[outerBag] = innerBags

	return rulesTable

def makeReverseTable(rulesTable):
	revRulesTable = {}
	for outerBagColour, innerBagsTuples in rulesTable.items():
		for innerBagNum, innerBagColour in innerBagsTuples:
			if innerBagColour in revRulesTable:
				revRulesTable[innerBagColour].add(outerBagColour)
			else:
				revRulesTable[innerBagColour] = set([outerBagColour])

	return revRulesTable

def countBagColoursContaining(containedBagColour, revRulesTable):
	containingBagColours = revRulesTable[containedBagColour]
	newColours = containingBagColours

	while len(newColours) > 0:
		oldColours = newColours
		newColours = set([])
		for colour in oldColours:
			if colour in revRulesTable:
				newColours |= revRulesTable[colour]
		containingBagColours |= newColours

	return len(containingBagColours)

def countBagColoursContainedIn(containingBagColour, rulesTable):
	containedBagColourTuples = rulesTable[containingBagColour]
	count = 0

	for num, colour in containedBagColourTuples:
		count += num + num*countBagColoursContainedIn(colour, rulesTable)

	return count


rules = readInput(sys.argv[1])
rulesTable = makeRulesTable(rules)
revRulesTable = makeReverseTable(rulesTable)
print(countBagColoursContaining('shiny gold', revRulesTable))
print(countBagColoursContainedIn('shiny gold', rulesTable))
