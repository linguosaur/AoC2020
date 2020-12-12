import sys

TURNS = ['L','R']
HEADINGS = ['E','S','W','N']
HEADINGS_TO_COORDS = {'E':(1,0),'S':(0,-1),'W':(-1,0),'N':(0,1)}

def readInput(filename):
	return [(line[0],int(line[1:])) for line in open(filename).read().split()]

def getNewHeading(turn, degrees, oldHeading):
	return HEADINGS[int((HEADINGS.index(oldHeading) + (2*int(turn=='R')-1)*degrees/90) % len(HEADINGS))]

def getNewLoc1(command, dist, loc, heading):
	direction = command 
	if command == 'F':
		direction = heading

	x, y = loc
	dx, dy = HEADINGS_TO_COORDS[direction]
	return (x + dx*dist, y + dy*dist)

def runInstructions1(instructions, loc, heading):
	for instruction in instructions:
		command, arg = instruction

		if command in HEADINGS + ['F']:
			loc = getNewLoc1(command, arg, loc, heading)
		elif command in TURNS:
			heading = getNewHeading(command, arg, heading)
	
	return (loc, heading)

def rotate(turn, degrees, waypoint):
	x, y = waypoint
	direction = 2*int(turn == 'R')-1
	for i in range(int(abs(degrees/90))):
		x, y = direction*y, -direction*x
	
	return (x, y)

def getNewWaypoint(command, dist, waypoint):
	x, y = waypoint
	dx, dy = HEADINGS_TO_COORDS[command]
	return (x + dx*dist, y + dy*dist)

def getNewLoc2(arg, loc, waypoint):
	x, y = loc
	dx, dy = waypoint
	return (x + arg*dx, y + arg*dy)

def runInstructions2(instructions, loc, waypoint):
	for instruction in instructions:
		command, arg = instruction
		if command in HEADINGS:
			waypoint = getNewWaypoint(command, arg, waypoint)
		elif command in TURNS:
			waypoint = rotate(command, arg, waypoint)
		elif command == 'F':
			loc = getNewLoc2(arg, loc, waypoint)

	return (loc, waypoint)

def getManhattanDist(loc1, loc2):
	return abs(loc2[0]-loc1[0]) + abs(loc2[1]-loc1[1])

instructions = readInput(sys.argv[1])
initLoc, initHeading = (0,0), 'E'
finalLoc, heading = runInstructions1(instructions, initLoc, initHeading)
print(getManhattanDist(initLoc, finalLoc))

initHeading = (10,1)
finalLoc, finalWaypoint = runInstructions2(instructions, initLoc, initHeading)
print(getManhattanDist(initLoc, finalLoc))
