import re, sys

mem = {}
byteLen = 36

def readInput(filename):
	return list(map(str.rstrip, open(filename).readlines()))

def chopBinPrefix(binStr):
	if binStr.count('b') > 0:
		binStr = binStr[binStr.index('b')+1:]
	
	return binStr

def getBinCompleteForm(binStr, bits):
	if len(binStr) < bits:
		binStr = (bits-len(binStr))*'0' + binStr
	elif len(binStr) > bits:
		binStr = binStr[-bits:]

	return binStr

def formatBinStr(rawBinStr, bits):
	return getBinCompleteForm(chopBinPrefix(rawBinStr), bits)

def applyMask(binStr, mask):
	binStrList = list(binStr)
	for i in range(len(mask)):
		if mask[i] != 'X':
			binStrList[i] = mask[i]

	return ''.join(binStrList)

def store(memInstruction, mask, bits):
	global mem
	match = re.fullmatch(r'mem\[(\d+)\] = (\d+)', memInstruction)
	if match:
		address, value = match.groups()
		formattedAddress = formatBinStr(bin(int(address)), bits)
		formattedBinValue = formatBinStr(bin(int(value)), bits)
		mem[formattedAddress] = applyMask(formattedBinValue, mask)

def getMask(maskInstruction):
	match = re.fullmatch(r'mask = ([X01]{36})', maskInstruction)
	if match:
		return match.group(1)

	return None

def runProgram(program):
	mask = ''
	for instruction in program:
		if instruction.startswith('mask'):
			mask = getMask(instruction)
		elif instruction.startswith('mem'):
			if len(mask) == byteLen:
				store(instruction, mask, byteLen)
			else:
				return False
		else: return False

	return True

def generateAddresses(maskedAddress):
	generatedAddresses, floatingIndices = [], []
	address, offset = maskedAddress, 0
	while address.count('X') > 0:
		floatingIndex = address.index('X')
		floatingIndices.append(offset+floatingIndex)
		address = address[floatingIndex+1:]
		offset += floatingIndex+1

	for i in range(2**len(floatingIndices)):
		bitsToAssign = formatBinStr(bin(i), len(floatingIndices))
		fixedAddress = list(maskedAddress)
		for j in range(len(floatingIndices)):
			fixedAddress[floatingIndices[j]] = bitsToAssign[j]
		generatedAddresses.append(''.join(fixedAddress))

	return generatedAddresses

def applyMask2(binStr, mask):
	binStrList = list(formatBinStr(binStr, byteLen))
	for i in range(len(mask)):
		if mask[i] != 'X':
			binStrList[i] = str(int(binStrList[i]) | int(mask[i]))
		else:
			binStrList[i] = 'X'

	return ''.join(binStrList)

def store2(memInstruction, mask, bits):
	global mem
	match = re.fullmatch(r'mem\[(\d+)\] = (\d+)', memInstruction)
	if match:
		address, value = match.groups()
		formattedAddress = formatBinStr(bin(int(address)), bits)
		formattedValue = formatBinStr(bin(int(value)), bits)
		maskedAddress = applyMask2(formattedAddress, mask)
		for address in generateAddresses(maskedAddress):
			mem[address] = formattedValue

def runProgram2(program):
	mask = ''
	for instruction in program:
		if instruction.startswith('mask'):
			mask = getMask(instruction)
		elif instruction.startswith('mem'):
			if len(mask) == byteLen:
				store2(instruction, mask, byteLen)
			else:
				return False
		else: return False

	return True

def sumMem(mem):
	total = 0
	for address in mem:
		total += int(mem[address],2)

	return total

program = readInput(sys.argv[1])
if runProgram(program):
	print(sumMem(mem))
else:
	print('Runtime error.')

mem.clear()

if runProgram2(program):
	print(sumMem(mem))
else:
	print('Runtime error.')
