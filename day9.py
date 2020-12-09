import sys

def readInput(filename):
	return [int(numString) for numString in open(filename).read().split()]

def checkSum(num, preamble):
	if len(preamble) > 1:
		for i in range(len(preamble)-1):
			for j in range(i+1,len(preamble)):
				if preamble[i] + preamble[j] == num:
					return True
		return False

	return None 
 
def findNonSum(numbers, preambleSize):
	if len(numbers) > preambleSize:
		i = preambleSize
		while checkSum(numbers[i], numbers[i-preambleSize:i]) and i < len(numbers):
			i += 1
		if i < len(numbers):
			return numbers[i]

	return None

def findNonSumRange(nonSum, numbers):
	for i in range(len(numbers)-1):
		rangeSize = 2
		total = sum(numbers[i:i+rangeSize])
		while total < nonSum and i + rangeSize < len(numbers):
			rangeSize += 1
			total = sum(numbers[i:i+rangeSize])
		
		if total == nonSum:
			return (i, rangeSize)

	return None

def findEncryptionWeakness(nonSum, numbers):
	i, rangeSize = findNonSumRange(nonSum, numbers)
	contiguousSet = numbers[i:i+rangeSize]

	return min(contiguousSet) + max(contiguousSet)


numbers = readInput(sys.argv[1])
preambleSize = 25

nonSum = findNonSum(numbers, preambleSize)
print(nonSum)

encryptionWeakness = findEncryptionWeakness(nonSum, numbers)
print(encryptionWeakness)
