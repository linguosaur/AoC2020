import re, sys


validKeys = set(['byr','iyr','eyr','hgt','hcl','ecl','pid','cid'])

def readInput(filename):
	passports = []
	with open(filename) as inputFile:
		passports = inputFile.read().split('\n\n')
	passports = [dict([tuple(record.split(':')) for record in p.split()]) for p in passports]
	
	return passports

def isValid1(passport):
	global validKeys
	keysFound = set(passport.keys())
	if keysFound == validKeys or validKeys - keysFound == set(['cid']):
		return True

	return False

def isValidYear(yearStr, earliest, latest):
	year = int(yearStr)
	if re.fullmatch(r'\d{4}', yearStr) and year >= earliest and year <= latest:
		return True

	return False

def isValidHGT(hgtStr):
	match = re.fullmatch(r'(\d+)(cm|in)', hgtStr)
	if match:
		height, unit = int(match.group(1)), match.group(2)
		if unit == 'cm' and height >= 150 and height <= 193:
			return True
		if unit == 'in' and height >= 59 and height <= 76:
			return True

	return False

def isValidHCL(hcl):
	if re.fullmatch(r'#[0-9a-f]{6}', hcl):
		return True

	return False

def isValidECL(ecl):
	if re.fullmatch(r'amb|blu|brn|gry|grn|hzl|oth', ecl):
		return True

	return False

def isValidPID(pid):
	if re.fullmatch(r'\d{9}', pid):
		return True

	return False

def isValid2(passport):
	valid = isValidYear(passport['byr'], 1920, 2002)
	valid = valid and isValidYear(passport['iyr'], 2010, 2020)
	valid = valid and isValidYear(passport['eyr'], 2020, 2030)
	valid = valid and isValidHGT(passport['hgt'])
	valid = valid and isValidHCL(passport['hcl'])
	valid = valid and isValidECL(passport['ecl'])
	valid = valid and isValidPID(passport['pid'])

	return valid

def countValid1(passports):
	numValid = 0
	for passport in passports:
		if isValid1(passport):
			numValid += 1

	return numValid

def countValid2(passports):
	numValid = 0
	for passport in passports:
		if isValid1(passport) and isValid2(passport):
			numValid += 1

	return numValid


passports = readInput(sys.argv[1])
print(countValid1(passports))
print(countValid2(passports))
