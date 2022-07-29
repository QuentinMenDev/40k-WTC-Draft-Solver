import sys # standard libraries
import json
from pathlib import Path

import nashpy # 3rd party packages

def import_pairing_matrix(match = None, filename = 'input_matrix.txt', encoding = {'--':-8, '-':-4, '0':0, '+':4, '++':8}):
	path = get_path(match, filename)
	with path.open(encoding="UTF-8") as f:
		lines = f.read().splitlines()

	tmpLines = []
	for line in lines:
		if line.count('|') > 0:
			line = line.split('|')
		else:
			line = line.split()
		tmpLines.append(line)
	lines = tmpLines

	for line in lines:
		if (len(line) != len(lines[0])):
			print("The following line has a number of elements not equal to the number of elements in the first line:")
			print(line)
			sys.exit()

	matchups = []
	for i in range(2, len(lines)):
		matchups.append(lines[i])

	tmpMatchups = []
	for matchup in matchups:
		tmpMatchup = []
		for element in matchup:
			tmpMatchup.append(encoding[element])
		tmpMatchups.append(tmpMatchup)
	matchups = tmpMatchups

	matrix = {}

	friendCounter = 0
	for friend in lines[0]:
		row = {}
		foeCounter = 0
		for foe in lines[1]:
			row[foe] = matchups[friendCounter][foeCounter]
			foeCounter += 1
		matrix[friend] = row
		friendCounter += 1

	return matrix

def get_game_overview(game):
	support_value = get_game_overview_from_equilibria(game, game.support_enumeration())
	if support_value != None:
		return support_value

	vertex_value = get_game_overview_from_equilibria(game, game.vertex_enumeration())
	if vertex_value != None:
		return vertex_value

	lemke_howson_value = get_game_overview_from_equilibria(game, game.lemke_howson_enumeration())
	if lemke_howson_value != None:
		return lemke_howson_value

	return None

def evaluate_game(metagame_cache, game_array):
	game_hash = hash(game_array.tostring())

	if game_hash in metagame_cache:
		return metagame_cache[game_hash]
	else:
		game = nashpy.Game(game_array)
		game_overview = get_game_overview(game)
		metagame_cache[game_hash] = game_overview
		return game_overview

# Returns overview of first equilibrium.
def get_game_overview_from_equilibria(game, equilibria):
	for equilibrium in equilibria:
		row_strategy = equilibrium[0]
		column_strategy = equilibrium[1]
		value = game[row_strategy, column_strategy][0]
		return [row_strategy, column_strategy, value]

	return None

def print_overview(game_overview, roundTo = 3):
	round_row_strategy = [round(x, roundTo) for x in game_overview[0]]
	round_column_strategy = [round(x, roundTo) for x in game_overview[1]]
	round_value = round(game_overview[2], roundTo)
	print("Row strategy: ", round_row_strategy)
	print("Column strategy: ", round_column_strategy)
	print("Value: ", round_value)

# A game permutation consist of a pair.
# The first item is a permutation of a subset of the friendly team. The second the same of the enemy team.
# The key for a game permutation is the concatenation of player names in the above order.
def get_permutation_key(n, game_permutation):
	permutation_key = "Friends: "
	for i in range(0, n): # Add friends to key.
		permutation_key += game_permutation[0][i] + ", "
	
	permutation_key += "Enemies: "
	for i in range(0, n): # Add enemies to key.
		permutation_key += game_permutation[1][i]
		if (i < n - 1):
			permutation_key += ", "

	return permutation_key

def get_path(match, filename):
	if match == None:
		path = Path(__file__).parent / (filename)
	else:
		subfolder = "Matches/" + match
		path = Path(__file__).parent / (subfolder + "/" + filename)

	return path

def write_strategy_dictionary(path, strategy_dictionary):
	with path.open('w', encoding='utf-8') as f:
		json.dump(strategy_dictionary, f, ensure_ascii=False, indent=4)

def read_strategy_dictionary(path):
	with path.open() as data_file:    
		strategy_dictionary = json.load(data_file)

	return strategy_dictionary

def write_strategy_with_print_calls(match, strategy_dictionary, filename):
	strategy_path = get_path(match, filename)
	print("Writing file {} ...".format(strategy_path))
	write_strategy_dictionary(strategy_path, strategy_dictionary)
	print('    ...done.') 