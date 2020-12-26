import sys

def readInput(filename):
	return [[int(card) for card in deck[len('Player 1: '):].split()] for deck in open(filename).read().rstrip().split('\n\n')]

def getNextDecks(deck1, deck2, game=0, recursive=False):
	card1, card2 = deck1[0], deck2[0]

	if recursive:
		if len(deck1)-1 >= card1 and len(deck2)-1 >= card2:
			#print('Play sub-game:')
			results = play2(deck1[1:card1+1], deck2[1:card2+1], game+1)
			#print('Sub-game done.')
			#print('Player', results[0], 'wins the game!')
			if results[0] == 1:
				return (1, deck1[1:]+[card1,card2], deck2[1:])
			elif results[0] == 2:
				return (2, deck1[1:], deck2[1:]+[card2,card1])
			return None

	if card1 > card2:
		return (1, deck1[1:]+[card1,card2], deck2[1:])
	elif card2 > card1:
		return (2, deck1[1:], deck2[1:]+[card2,card1])

def play(deck1, deck2):
	while len(deck1) > 0 and len(deck2) > 0:
		winner, deck1, deck2 = getNextDecks(deck1, deck2)
		#print('Player', winner, 'wins the round!')
		#print('Player 1\'s deck:', ', '.join([str(card) for card in deck1]))
		#print('Player 2\'s deck:', ', '.join([str(card) for card in deck2]))

	if len(deck1) == 0:
		return (2, deck2)
	if len(deck2) == 0:
		return (1, deck1)
	return None

def play2(deck1, deck2, game=1):
	seenDecks = set([])
	while len(deck1) > 0 and len(deck2) > 0:
		#print('Game', game)
		if (tuple(deck1), tuple(deck2)) in seenDecks: return (1, deck1)

		seenDecks.add((tuple(deck1), tuple(deck2)))
		#print('Decks seen:', len(seenDecks))
		#print('Player 1\'s deck:', ', '.join([str(card) for card in deck1]))
		#print('Player 2\'s deck:', ', '.join([str(card) for card in deck2]))
		winner, deck1, deck2 = getNextDecks(deck1, deck2, game, True)
		#print('Player', winner, 'wins the round!')

	if len(deck1) == 0:
		return (2, deck2)
	if len(deck2) == 0:
		return (1, deck1)
	return None

def getScore(deck):
	return sum([deck[i]*(len(deck)-i) for i in range(len(deck))])

deck1, deck2 = readInput(sys.argv[1])
winner, winningDeck = play(deck1, deck2)
#print('Player', winner, 'wins the game!')
print(getScore(winningDeck))

winner, winningDeck = play2(deck1, deck2)
#print('Player', winner, 'wins the game!')
print(getScore(winningDeck))
