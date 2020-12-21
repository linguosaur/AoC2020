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

def getMessages(startingRuleLabel, rules):
	oldDerivations, newDerivations = rules[startingRuleLabel], None
	while newDerivations != [] and newDerivations != oldDerivations:
		if newDerivations != None:
			oldDerivations = newDerivations
		alternateExpansions = expand(oldDerivations, rules)
		newDerivations = []
		for expansion in alternateExpansions:
			newDerivations += getDerivations(expansion)

	return [''.join(messages) for messages in newDerivations]

def countMatches(rules, messages, mode):
	matches42, matches31 = getMessages(42, rules), getMessages(31, rules)
	componentLen = len(matches42[0]) # all of them are the same length, it turns out

	count = 0
	for message in messages:
		num42s, num31s = 0, 0
		if len(message) % componentLen == 0:
			fits0, contiguous42s = True, True
			for i in range(int(len(message)/componentLen)):
				section = message[i*componentLen:(i+1)*componentLen]
				if section in matches42:
					if num31s == 0:
						num42s += 1
					else:
						contiguous42s = False
						break
				elif section in matches31:
					num31s += 1
				else: 
					fits0 = False
					break

			if fits0 and contiguous42s:
				if mode == 1:
					if (num42s, num31s) == (2, 1):
						count += 1
				elif mode == 2:
					if num42s >= 2 and num31s >= 1 and num42s > num31s:
						count += 1

	return count


rules, messages = readInput(sys.argv[1])
print(countMatches(rules, messages, 1))
print(countMatches(rules, messages, 2))
