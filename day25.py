import sys

def readInput(filename):
	return [int(line) for line in open(filename).read().rstrip().split()]

def transform(value, subjNum=7):
	value *= subjNum
	value %= 20201227
	return value

def getLoopSize(publicKey, subjNum=7):
	value, loops = 1, 0
	while value != publicKey:
		value = transform(value)
		loops += 1
	return loops

def getKey(loopSize, subjNum):
	value = 1
	for i in range(loopSize):
		value = transform(value, subjNum)
	return value

publicKey1, publicKey2 = readInput(sys.argv[1])
#publicKey1, publicKey2 = 5764801, 17807724
loopSize1, loopSize2 = getLoopSize(publicKey1), getLoopSize(publicKey2)
print('loopSize1:', loopSize1)
print('loopSize2:', loopSize2)

encryptionKey1, encryptionKey2 = getKey(loopSize1, publicKey2), getKey(loopSize2, publicKey1)
print('encryptionKey1:', encryptionKey1)
print('encryptionKey2:', encryptionKey2)
