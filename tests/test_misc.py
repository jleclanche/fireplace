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


def test_silence():
	game = prepare_game()
	minion = game.player1.summon("CS2_182")
	assert minion.health == 5
	game.player1.give("CS2_004").play(target=minion)
	assert minion.health == 7
	game.player1.give("GVG_015").play(target=minion)
	assert minion.health == 4
	game.player1.give("CS2_203").play(target=minion)
	assert minion.health == 4


def test_anubar_ambusher_cult_master():
	# https://github.com/jleclanche/fireplace/issues/126
	game = prepare_game()
	game.player1.discard_hand()
	cultmaster1 = game.player1.summon("EX1_595")
	ambusher1 = game.player1.summon("FP1_026")
	assert len(game.player1.hand) == 0
	ambusher1.destroy()
	assert len(game.player1.hand) == 2
	assert cultmaster1 in game.player1.hand
	game.skip_turn()

	game.player1.discard_hand()
	ambusher2 = game.player1.summon("FP1_026")
	cultmaster2 = game.player1.summon("EX1_595")
	assert len(game.player1.hand) == 0
	ambusher2.destroy()
	assert len(game.player1.hand) == 1
	assert cultmaster2 in game.player1.hand


def test_copy_voljin():
	game = prepare_empty_game()
	wisp = game.player1.give(WISP).play()
	voljin = game.player1.give("GVG_014").play(target=wisp)
	game.end_turn()
	game.player2.give("EX1_564").play(target=voljin)
	voljin_copy = game.player2.field[0]
	assert voljin_copy.atk == voljin.atk
	assert voljin_copy.health == voljin.health
