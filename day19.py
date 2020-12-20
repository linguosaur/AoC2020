import sys

TERMINALS = set(['a', 'b'])

def parseRules(rules):
	parsedRules = {}
	for rule in rules:
		for left, right in [rule.split(': ')]:
			if int(left) not in parsedRules:
				parsedRules[int(left)] = []
			for output in right.split(' | '):
				if output.count('"') == 0:
					parsedRules[int(left)].append(list(map(int, output.split())))
				else:
					parsedRules[int(left)].append([output[1:-1]])

	return parsedRules

def readInput(filename):
	rules, messages = [section.rstrip().split('\n') for section in open(filename).read().split('\n\n')]
	rules = parseRules(rules)
	return rules, messages

def expand(possibleOutputs, rules):
	return [[rules[item] if item in rules else [[item]] for item in output] for output in possibleOutputs]

def getDerivations(expansion):
	if len(expansion) == 1:
		return expansion[0]

	combos = getDerivations(expansion[1:])
	extendedCombos = []
	for i in range(len(expansion[0])):
		for j in range(len(combos)):
			extendedCombos.append(expansion[0][i] + combos[j])

	return extendedCombos

def matchesMessage(derivation, message):
	i = 0
	while i < min(len(derivation), len(message)) and derivation[i] in TERMINALS:
		if derivation[i] == message[i]:
			i += 1
		else: return False
	if i < len(derivation):
		i = -1
		while i >= -min(len(derivation), len(message)) and derivation[i] in TERMINALS:
			if derivation[i] == message[i]:
				i -= 1
			else: return False
	else:
		return ''.join(derivation) == message

	return True
	
def prune(derivations, message):
	i = 0
	while i < len(derivations):
		if not matchesMessage(derivations[i], message):
			derivations.pop(i)
		else:
			i += 1

def derivesMessage(startingRuleLabel, rules, message):
	oldDerivations, newDerivations = rules[startingRuleLabel], None
	while newDerivations != [] and newDerivations != oldDerivations:
		if newDerivations != None:
			oldDerivations = newDerivations
		alternateExpansions = expand(oldDerivations, rules)
		newDerivations = []
		for expansion in alternateExpansions:
			newDerivations += getDerivations(expansion)

		prune(newDerivations, message)
	
	return len(newDerivations) > 0

def countMatchingMessages(startingRuleLabel, rules, messages):
	count = 0
	for message in messages:
		derives = derivesMessage(startingRuleLabel, rules, message)
		print(derives)
		if derives:	count += 1

	return count

rules, messages = readInput(sys.argv[1])
print('rules:', rules)
print(countMatchingMessages(0, rules, messages))
