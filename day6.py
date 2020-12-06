import sys

def readInput(inputfile):
	return [line.split() for line in open(inputfile).read().split('\n\n')]

def countAnyoneYesQs(groupAnswers):
	return len(set(''.join(groupAnswers)))

def countAnyoneYesQsAll(groupsAnswers):
	return sum([countAnyoneYesQs(ans) for ans in groupsAnswers])

def countEveryoneYesQs(groupAnswers):
	return len(set.intersection(*[set(ans) for ans in groupAnswers]))

def countEveryoneYesQsAll(groupsAnswers):
	return sum([countEveryoneYesQs(ans) for ans in groupsAnswers])

allGroupsAnswers = readInput(sys.argv[1])
print(countAnyoneYesQsAll(allGroupsAnswers))
print(countEveryoneYesQsAll(allGroupsAnswers))
