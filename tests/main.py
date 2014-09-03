#!/usr/bin/env python
import sys; sys.path.append("..")
import fireplace
import logging
import random

logging.getLogger().setLevel(logging.DEBUG)


def prepare_game():
	print("Initializing a new game")
	deck1 = fireplace.Deck.randomDraft(hero=fireplace.heroes.MAGE)
	deck2 = fireplace.Deck.randomDraft(hero=fireplace.heroes.WARRIOR)
	player1 = fireplace.Player(name="Player1", deck=deck1)
	player2 = fireplace.Player(name="Player2", deck=deck2)
	game = fireplace.Game(players=(player1, player2))
	game.start()

	return game

def test_deathrattle():
	game = prepare_game()
	game.endTurn(); game.endTurn()

	loothoarder = game.currentPlayer.give("EX1_096")
	loothoarder.play()
	cardcount = len(game.currentPlayer.hand)

	game.endTurn()
	archer = game.currentPlayer.give("CS2_189")
	archer.play(target=loothoarder)

	assert len(game.currentPlayer.opponent.hand) == cardcount + 1


def test_mana():
	game = prepare_game()
	footman = game.currentPlayer.give("CS1_042")
	assert footman.cost == 1
	footman.play()
	assert footman.atk == 1
	assert footman.health == 2
	game.endTurn()

	# Play the coin
	coin = game.currentPlayer.getById("GAME_005")
	coin.play()
	assert game.currentPlayer.mana == 2

def test_card_draw():
	game = prepare_game()
	# pass turn 1
	game.endTurn()
	game.endTurn()

	# novice should draw 1 card
	card = game.currentPlayer.give("EX1_015")
	handlength = len(game.currentPlayer.hand)
	card.play()
	# hand should be 1 card played, 1 card drawn; same length
	assert len(game.currentPlayer.hand) == handlength
	game.endTurn()

	# succubus should discard 1 card
	card = game.currentPlayer.give("EX1_306")
	handlength = len(game.currentPlayer.hand)
	card.play()
	assert len(game.currentPlayer.hand) == handlength - 2

def test_end_turn_heal():
	game = prepare_game()

	footman = game.currentPlayer.give("CS1_042")
	footman.play()
	assert footman.health == 2
	game.endTurn()

	# play an archer on the footman
	archer = game.currentPlayer.give("CS2_189")
	archer.play(target=footman)
	assert footman.health == 1
	game.endTurn()

	healtotem = game.currentPlayer.give("NEW1_009")
	healtotem.play()
	game.endTurn()
	assert footman.health == 2
	game.endTurn()
	game.endTurn()
	# check it's still at max health after a couple of turns
	assert footman.health == 2


def test_auras():
	game = prepare_game()

	wisp1 = game.currentPlayer.give("CS2_231")
	wisp1.play()
	assert wisp1.atk == 1
	game.endTurn()

	# pass next two turns to gain some mana
	game.endTurn()
	game.endTurn()

	game.endTurn()
	game.endTurn()

	wisp2 = game.currentPlayer.give("CS2_231")
	wisp2.play()
	raidleader = game.currentPlayer.give("CS2_122")
	raidleader.play()
	assert raidleader.data.hasAura
	assert raidleader.atk == 2
	assert wisp1.atk == 1
	slot = wisp2.slots[0]
	assert wisp2.atk == 2
	wisp3 = game.currentPlayer.give("CS2_231")
	wisp3.play()
	assert wisp3.atk == 2



def main():
	test_deathrattle()
	test_mana()
	test_card_draw()
	test_end_turn_heal()
	test_auras()
	print("All tests ran OK")


if __name__ == "__main__":
	main()
