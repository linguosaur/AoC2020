import re, sys

def readInput(filename):
	return list(map(str.rstrip, open(filename).readlines()))

def evalOp(threeItems, addOnly):
	if addOnly and threeItems[1] == '*': return threeItems

	threeItemsString = ''.join(threeItems)
	if re.fullmatch(r'\d+[\+\*]\d+', threeItemsString):
		return [str(eval(threeItemsString))]

	return threeItems

def simplifyStack(stack, addOnly):
	newStack = None
	while (newStack == None and len(stack) >= 3 or newStack != None and len(newStack) >= 3) and newStack != stack:
		if newStack != None:
			stack = newStack
		newStack = stack[:-3] + evalOp(stack[-3:], addOnly)
	
	if newStack != None:
		return newStack

	return stack

def evalExpression(parsedExpression, addFirst):
	stack, parenStack = [], []
	while len(parsedExpression) > 0:
		pop = parsedExpression.pop(0)
		stack.append(pop)

		if pop == '(':
			parenStack.append(len(stack)-1)
		elif pop == ')':
			openParenIndex = parenStack.pop()
			stack = stack[:openParenIndex] + [str(evalExpression(stack[openParenIndex+1:len(stack)-1], addFirst))]

		if len(parenStack) == 0:
			stack = simplifyStack(stack, addFirst)

	if len(stack) == 1:
		return int(stack[0])
	
	if addFirst:
		stack = simplifyStack(stack, False)
		if len(stack) == 1:
			return int(stack[0])

	return None

def parse(expression):
	return [char for char in expression if char != ' ']

def evalExpressionString(expression, addFirst):
	return evalExpression(parse(expression), addFirst)

def getSumFromExpressions(expressions, addFirst):
	return sum([evalExpressionString(expression, addFirst) for expression in expressions])
		

expressions = readInput(sys.argv[1])
print(getSumFromExpressions(expressions, False))
print(getSumFromExpressions(expressions, True))
