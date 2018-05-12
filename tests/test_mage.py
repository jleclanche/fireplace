"""
All the unit test cases are sorted by its ID
Test for its description is automatically tested by test_carddb.py
This test suites will ignore it and cover basic and complex situations
"""


from utils import *


def test_flame_lance():
	# now the prepare_game includes neutral cards
	game = prepare_game(CardClass.MAGE)

	# assume that I am controlling player1
	my_spell = game.player1.give("AT_001")
	my_minion = game.player1.give(WISP).play()

	# basic information of the card
	assert my_spell.cost == 5
	assert my_spell.type == CardType.SPELL

	# my minion should die
	my_spell.play(target=my_minion)
	assert len(game.player1.field) == 0
