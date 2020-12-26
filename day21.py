import sys
from functools import reduce
from operator import itemgetter

def readInput(filename):
	foods = []
	for line in open(filename).read().rstrip().split('\n'):
		openParen = line.index('(')
		foods.append((set(line[:openParen-1].split()), set(line[openParen+len('contains ')+1:-1].split(', '))))

	return foods

def getAllAllergens(foods):
	return set.union(*[allergens for ingredients, allergens in foods])

def locateAllergens(foods):
	allergenToIngredient = {}
	for ingredients, allergens in foods:
		for allergen in allergens:
			if allergen in allergenToIngredient:
				allergenToIngredient[allergen] &= ingredients
			else:
				allergenToIngredient[allergen] = ingredients.copy()

	allAllergens = getAllAllergens(foods)
	allergensProcessed = set([])
	locatedAllergens = set([allergen for allergen in allAllergens if len(allergenToIngredient[allergen]) == 1])
	while len(allergensProcessed) < len(locatedAllergens):
		for allergen in locatedAllergens - allergensProcessed:
			problemIngredient = next(iter(allergenToIngredient[allergen]))
			for allergen2 in set(allergenToIngredient.keys())-set([allergen]):
				if problemIngredient in allergenToIngredient[allergen2]:
					allergenToIngredient[allergen2].remove(problemIngredient)
			allergensProcessed.add(allergen)
		locatedAllergens = set([allergen for allergen in allAllergens if len(allergenToIngredient[allergen]) == 1])

	return allergenToIngredient

def countSafeIngredients(allergenLocations, foods):
	dangerousIngredients = set.union(*allergenLocations.values())
	return sum([len(ingredients-dangerousIngredients) for ingredients, allergens in foods])

def getDangerousIngredients(allergenLocations):
	return ','.join([next(iter(ingredients)) for allergen, ingredients in sorted(allergenLocations.items(), key=itemgetter(0))])


foods = readInput(sys.argv[1])
allergenLocations = locateAllergens(foods)
print(countSafeIngredients(allergenLocations, foods))
print(getDangerousIngredients(allergenLocations))
