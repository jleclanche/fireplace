from utils import *


def test_event_queue_heal():
	game = prepare_game()
	shadowboxer1 = game.player1.give("GVG_072")
	shadowboxer1.play()
	shadowboxer2 = game.player1.give("GVG_072")
	shadowboxer2.play()
	game.player1.give(MOONFIRE).play(target=shadowboxer1)
	game.player1.give(MOONFIRE).play(target=shadowboxer2)
	circle = game.player1.give("EX1_621")
	circle.play()
	assert game.player2.hero.health == 26


def test_event_queue_summon():
	game = prepare_empty_game()
	game.player1.give(WISP).play()
	game.player1.give(WISP).play()
	game.end_turn()

	buzzard = game.player2.give("CS2_237")
	buzzard.play()
	reaver = game.player2.give("AT_130")
	reaver.shuffle_into_deck()

	assert reaver in game.player2.deck

	unleash = game.player2.give("EX1_538")
	unleash.play()

	assert reaver in game.player2.hand
	assert buzzard.health == 1
	assert len(game.player2.field) == 1
