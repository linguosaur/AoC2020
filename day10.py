import sys

def readInput(filename):
	return [int(line) for line in list(map(str.rstrip, open(filename).readlines()))]

def getJoltDiffs(joltages):
	sortedJoltages = [0] + sorted(joltages) 
	sortedJoltages += [sortedJoltages[-1]+3]
	joltDiffs = []
	for i in range(len(sortedJoltages)-1):
		joltDiffs.append(sortedJoltages[i+1] - sortedJoltages[i])

	return joltDiffs

def getJoltDiffDistribution(joltages):
	joltDiffs = getJoltDiffs(joltages)
	joltDiffDistribution = max(joltDiffs)*[0]
	for joltDiff in range(len(joltDiffDistribution)):
		joltDiffDistribution[joltDiff] = joltDiffs.count(joltDiff+1)

	return tuple(joltDiffDistribution)

# count consecutive streaks of 1's, minus the first one
# with 'day10input.txt', joltage differences are either 1 and 3
def getOptionalStreaks(joltDiffs):
	optionalStreaks = []
	optionalStreak = 0
	for i in range(len(joltDiffs)):
		if joltDiffs[i] == 1:
			optionalStreak += 1
		elif joltDiffs[i] == 3:
			if optionalStreak > 0:
				optionalStreak -= 1
			optionalStreaks.append(optionalStreak)
			optionalStreak = 0

	return optionalStreaks

# with 'day10input.txt', joltage differences are either 1 and 3
def countArrangements(joltages):
	sortedJoltages = [0] + sorted(joltages) 
	sortedJoltages += [sortedJoltages[-1]+3]
	joltDiffs = getJoltDiffs(joltages)

	optionalStreaks = getOptionalStreaks(joltDiffs)
	arrangements = 1
	for streak in optionalStreaks:
		if streak == 3:
			arrangements *= 2**streak - 1
		elif streak < 3:
			arrangements *= 2**streak

	return arrangements


joltages = readInput(sys.argv[1])
joltDiffDistribution = getJoltDiffDistribution(joltages)
print(joltDiffDistribution[0]*joltDiffDistribution[2])
print(countArrangements(joltages))
