import re, sys

def readInput(filename):
	lines = []
	with open(filename) as inputfile:
		for line in inputfile:
			lines.append(line.rstrip())

	return lines

def countValidPasswords1(passwordLines):
	valid = 0
	for passwordLine in passwordLines:
		match = re.fullmatch(r'(\d+)-(\d+) ([a-z]): ([a-z]+)', passwordLine)
		(minFreq, maxFreq, char, password) = match.groups()
		freq = password.count(char)
		if freq >= int(minFreq) and freq <= int(maxFreq):
			valid += 1

	return valid

def countValidPasswords2(passwordLines):
	valid = 0
	for passwordLine in passwordLines:
		match = re.fullmatch(r'(\d+)-(\d+) ([a-z]): ([a-z]+)', passwordLine)
		(pos1, pos2, char, password) = match.groups()
		if (password[int(pos1)-1] == char) != (password[int(pos2)-1] == char):
			valid += 1

	return valid


passwordLines = readInput(sys.argv[1])
print(countValidPasswords1(passwordLines))
print(countValidPasswords2(passwordLines))
