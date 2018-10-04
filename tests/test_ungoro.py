import pytest
from utils import *


def test_steam_surger():
	game = prepare_empty_game()
	handsize = len(game.player1.hand)
	game.player1.give("UNG_021").play()
	assert handsize == len(game.player1.hand)
	game.end_turn()
	game.end_turn()
	assert game.player1.elemental_played_last_turn == 1
	handsize = len(game.player1.hand)
	game.player1.give("UNG_021").play()
	assert handsize + 1 == len(game.player1.hand)


def test_jungle_giant():
	game = prepare_game()
	quest = game.player1.give("UNG_116")
	quest.play()
	assert quest == game.player1.secrets[0]
	hand_size = len(game.player1.hand)
	game.player1.summon("CS2_187")
	game.player1.summon("CS2_187")
	game.player1.summon("CS2_187")
	game.player1.summon("CS2_187")
	game.player1.summon("CS2_187")
	assert hand_size + 1 == len(game.player1.hand)
	assert len(game.player1.secrets) == 0
	reward = game.player1.hand[-1]
	assert reward.id == "UNG_116t"


def test_voraxx():
	game = prepare_game()
	voraxx = game.player1.give("UNG_843").play()
	spell = game.player1.give("CS2_087")
	spell.play(target = voraxx)
	assert len(game.player1.field) == 2
	assert game.player1.field[1].atk == 4


def test_ungoro_card_package():
	game = prepare_game()
	package = game.player1.give("UNG_851t1")
	hand_size = len(game.player1.hand)
	package.play()
	assert hand_size - 1 + 5 == len(game.player1.hand)
	for card in game.player1.hand[-5:]:
		assert card.data.card_set == 27


def test_golakka_crawler():
	game = prepare_game()
	crawler1 = game.player1.give("UNG_807")
	crawler1.play()
	assert crawler1.atk == 2
	crawler2 = game.player1.give("UNG_807")
	pirate = game.player2.summon("CFM_637")
	crawler2.play(target=pirate)


def test_curious_glimmerroot():
	game = prepare_game()
	glimmer = game.player1.give("UNG_035")
	glimmer.play()
	assert len(game.player1.choice.cards) == 3
	hand_size = len(game.player1.hand)
	game.player1.choice.choose(game.player1.choice.right_card)
	assert hand_size + 1 == len(game.player1.hand)
