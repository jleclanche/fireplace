from utils import *


def test_kabal_courier():
	game = prepare_game()
	courier = game.player1.give("CFM_649")
	courier.play()
	assert len(game.player1.choice.cards) == 3
	assert CardClass.MAGE in game.player1.choice.cards[0].classes
	assert CardClass.PRIEST in game.player1.choice.cards[1].classes
	assert CardClass.WARLOCK in game.player1.choice.cards[2].classes
