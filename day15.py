def getNext(lastNum, seqLen, indexLastSeen):
	if lastNum not in indexLastSeen:
		return 0
	return seqLen - 1 - indexLastSeen[lastNum]

def buildIndexLastSeen(seq):
	indexLastSeen = {}
	for i in range(len(seq)):
		indexLastSeen[seq[i]] = i

	return indexLastSeen

def extendToN(seq, n):
	seqLen = len(seq)
	indexLastSeen = buildIndexLastSeen(seq[:-1])
	lastNum = seq[-1]

	while seqLen < n:
		nextNum = getNext(lastNum, seqLen, indexLastSeen)
		indexLastSeen[lastNum] = seqLen - 1
		seqLen += 1
		lastNum = nextNum

	return lastNum


startingNums = [12,20,0,6,1,17,7]
n = 2020
print(extendToN(startingNums, n))

n = 30000000
print(extendToN(startingNums, n))
