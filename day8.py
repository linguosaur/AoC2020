import sys

def readInput(inputfile):
	return [tuple(line.split()) for line in list(map(str.rstrip, open(inputfile).readlines()))]

def runUntilLoop(program):
	accumulator, currentLine = 0, 0
	linesExecuted = []
	
	while currentLine not in linesExecuted and currentLine < len(program):
		linesExecuted.append(currentLine)
		command, arg = program[currentLine]
		if command == 'acc':
			accumulator += int(arg)
			currentLine += 1
		elif command == 'jmp':
			currentLine += int(arg)
		elif command == 'nop':
			currentLine += 1

	return linesExecuted, accumulator

def findNoLoopRun(origLinesExecuted, program):
	for lineNum in origLinesExecuted:
		editedProgram = program.copy()
		command, arg = editedProgram[lineNum]
		if command == 'jmp':
			editedProgram[lineNum] = ('nop', arg)
		elif command == 'nop':
			editedProgram[lineNum] = ('jmp', arg)
		else:
			continue
		
		linesExecuted, accumulator = runUntilLoop(editedProgram)
		if linesExecuted[-1] == len(program)-1:
			return linesExecuted, accumulator

program = readInput(sys.argv[1])
origLinesExecuted, accumulator = runUntilLoop(program)
print(accumulator)

linesExecuted, accumulator = findNoLoopRun(origLinesExecuted, program)
print(accumulator)
