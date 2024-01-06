from utils import *


def test_griftah():
	game = prepare_empty_game()
	game.player1.give("TRL_096").play()
	choiced = []
	for _ in range(2):
		card = game.player1.choice.cards[0]
		choiced.append(card)
		game.player1.choice.choose(card)
	assert len(game.player1.hand) == 1
	assert (
		choiced[0] in game.player1.hand and choiced[1] in game.player2.hand
	) ^ (
		choiced[1] in game.player1.hand and choiced[0] in game.player2.hand
	)


def test_hakkar():
	game = prepare_empty_game()
	hakkar = game.player1.give("TRL_541").play()
	hakkar.destroy()
	assert len(game.player1.deck) == 1
	assert game.player1.deck[0].id == "TRL_541t"
	assert len(game.player2.deck) == 1
	assert game.player2.deck[0].id == "TRL_541t"
	game.end_turn()
	assert len(game.player2.deck) == 2
	assert game.player2.deck[0].id == "TRL_541t"
	assert game.player2.deck[1].id == "TRL_541t"
	assert game.player2.hero.health == 27
	game.skip_turn()
	assert game.player2.hero.health == 21
	assert len(game.player2.deck) == 4


def test_overkill():
	game = prepare_game()
	wisp = game.player1.give(WISP).play()
	game.end_turn()
	direhorn = game.player2.give("TRL_232").play()
	game.skip_turn()
	direhorn.attack(wisp)
	assert len(game.player2.field) == 2


def test_overkill_spell():
	game = prepare_game()
	wisp = game.player1.give(WISP).play()
	arrow = game.player1.give("TRL_347")
	arrow.play(target=wisp)
	assert len(game.player1.field) == 1


def test_snapjaw_shellfighter():
	game = prepare_game()
	wisp = game.player1.give(WISP).play()
	shellfighter = game.player1.give("TRL_535").play()
	game.player1.give(MOONFIRE).play(target=wisp)
	assert wisp.damage == 0
	assert shellfighter.damage == 1


def test_treespeaker():
	game = prepare_game()
	game.player1.give("EX1_571").play()
	game.player1.give(WISP).play()
	game.player1.give("TRL_341").play()
	assert len(game.player1.field) == 5
	for i in range(3):
		assert game.player1.field[i].id == "TRL_341t"
	assert game.player1.field[3].id == WISP
	assert game.player1.field[4].id == "TRL_341"
