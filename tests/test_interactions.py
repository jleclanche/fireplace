from utils import *


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
