import sys

def readInput(filename):
	rules, myTicket, otherTickets = open(filename).read().split('\n\n')

	rules = parseRules(rules)
	myTicket = [int(value) for value in myTicket[len('your ticket:\n'):].split(',')]
	otherTickets = [list(map(int, ticket.split(','))) for ticket in otherTickets[len('nearby tickets:\n'):].rstrip().split('\n')]

	return rules, myTicket, otherTickets

def parseRules(rules):
	rules = {tuple(rule.split(': ')) for rule in rules.split('\n')}
	formattedRules = {}
	for field, values in rules:
		valueRanges = []
		for valueRange in values.split(' or '):
			valueRanges.append(tuple([int(limit) for limit in valueRange.split('-')]))
		formattedRules[field] = valueRanges

	return formattedRules

def numInRange(num, valueRange):
	lowest, highest = valueRange
	return num >= lowest and num <= highest

def overlaps(range1, range2):
	lowest1, highest1 = range1
	lowest2, highest2 = range2
	if lowest2 > highest1 or lowest1 > highest2:
		return False

	return True

def mergeRanges(range1, range2):
	if overlaps(range1, range2):
		lowest1, highest1 = range1
		lowest2, highest2 = range2
		return [(min(lowest1, lowest2), max(highest1, highest2))]
	
	return [range1, range2]
		
def simplifyRanges(ranges):
	sortedRanges = sorted(ranges)
	mergedRanges = []
	if len(ranges) > 1:
		for i in range(len(sortedRanges[1:])):
			range1 = sortedRanges[0]
			if len(mergedRanges) > 0:
				range1 = mergedRanges.pop()
			mergedRanges += mergeRanges(range1, sortedRanges[i])

	return mergedRanges

def getValidRanges(rules):
	validRanges = set([])
	for field, valueRange in rules.items():
		validRanges |= set(valueRange)

	return simplifyRanges(validRanges)
			
def getInvalid(ticket, ranges):
	for num in ticket:
		valid = False
		for valueRange in ranges:
			if numInRange(num, valueRange):
				valid = True
				break
		if not valid:
			return num

	return None

def getErrorRate(tickets, rules):
	ranges = getValidRanges(rules)
	invalidValues = []
	for ticket in tickets:
		invalid = getInvalid(ticket, ranges)
		if invalid:
			invalidValues.append(invalid)

	return sum(invalidValues)

def getValidTickets(tickets, ranges):
	return [ticket for ticket in tickets if getInvalid(ticket, ranges) == None]

def getPossibleFields(values, rules):
	possibleFields = set(rules.keys())
	for value in values:
		invalidFields = set([])
		for field in possibleFields:
			ranges = rules[field]
			if not (numInRange(value, ranges[0]) or numInRange(value, ranges[1])):
				invalidFields.add(field)

		possibleFields -= invalidFields

	return set(possibleFields)

def getDecidedPositions(possibleFields):
	return {pos:possibleFields[pos] for pos in range(len(possibleFields)) if len(possibleFields[pos]) == 1}

def eliminateFields(possibleFields):
	possibleFieldsCopy = possibleFields.copy()
	decidedPositions = getDecidedPositions(possibleFieldsCopy)
	while len(decidedPositions) < len(possibleFieldsCopy):
		for pos in decidedPositions:
			decidedField = next(iter(decidedPositions[pos]))
			for pos2 in [x for x in range(len(possibleFieldsCopy)) if x != pos]:
				if decidedField in possibleFieldsCopy[pos2]:
					possibleFieldsCopy[pos2].remove(decidedField)
		decidedPositions = getDecidedPositions(possibleFieldsCopy)

	return possibleFieldsCopy

def getFields(tickets, rules):
	ranges = getValidRanges(rules)
	validTickets = getValidTickets(tickets, ranges)
	possibleFields = len(validTickets[0])*[None]

	for pos in range(len(validTickets[0])):
		possibleFields[pos] = getPossibleFields([ticket[pos] for ticket in validTickets], rules)

	possibleFields = eliminateFields(possibleFields)
		
	return possibleFields

def getDepartureValuesProduct(myTicket, otherTickets, rules):
	product = 1
	fields = getFields(otherTickets, rules)
	for pos in range(len(fields)):
		if next(iter(fields[pos])).startswith('departure '):
			product *= myTicket[pos]

	return product

rules, myTicket, otherTickets = readInput(sys.argv[1])
print(getErrorRate(otherTickets, rules))
print(getDepartureValuesProduct(myTicket, otherTickets, rules))
