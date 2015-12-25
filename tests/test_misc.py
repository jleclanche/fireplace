from utils import *


def test_cheat_destroy_deck():
	game = prepare_game()
	game.player1.discard_hand()
	game.player2.discard_hand()
	game.player1.give(DESTROY_DECK).play(target=game.player2.hero)
	assert not game.player2.deck
	game.end_turn()

	assert not game.player2.hand
	assert game.player2.hero.health == 29
	game.player2.give(DESTROY_DECK).play(target=game.player1.hero)
	assert not game.player1.deck


def test_event_queue_heal():
	"""
	Test the event queue for mass hits.
	Events are supposed to be processed in two phases:
	1. Event queuing
	2. Triggers (in order of play)
	This means that playing a Refreshment Vendor on a board with a
	Shadowboxer, and two heroes damaged by 1 will result in the enemy
	hero being damaged by 28. Shadowboxer will trigger twice, after
	both heals have triggered.
	"""
	game = prepare_game()
	game.player1.give(MOONFIRE).play(target=game.player1.hero)
	game.player1.give(MOONFIRE).play(target=game.player2.hero)
	shadowboxer = game.player1.give("GVG_072")
	shadowboxer.play()
	vendor = game.player1.give("AT_111")
	vendor.play()
	assert game.player1.hero.health == 30
	assert game.player2.hero.health == 28


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
