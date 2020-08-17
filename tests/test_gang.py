from utils import *


def test_kabal_courier():
	game = prepare_game()
	courier = game.player1.give("CFM_649")
	courier.play()
	assert len(game.player1.choice.cards) == 3
	assert game.player1.choice.cards[0].card_class == CardClass.MAGE
	assert game.player1.choice.cards[1].card_class == CardClass.PRIEST
	assert game.player1.choice.cards[2].card_class == CardClass.WARLOCK
