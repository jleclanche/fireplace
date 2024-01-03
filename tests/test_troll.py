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
