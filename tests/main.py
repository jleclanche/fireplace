#!/usr/bin/env python
import sys; sys.path.append("..")
import fireplace
import logging

logging.getLogger().setLevel(logging.DEBUG)


def main():
	deck1 = fireplace.Deck.randomDraft(hero=fireplace.heroes.MAGE)
	deck2 = fireplace.Deck.randomDraft(hero=fireplace.heroes.WARRIOR)
	player1 = fireplace.Player(name="Player1", deck=deck1)
	player2 = fireplace.Player(name="Player2", deck=deck2)

	game = fireplace.Game(players=(player1, player2))
	game.start()

	footman = game.currentPlayer.give("CS1_042")
	footman.play()
	game.endTurn()

	novice = game.currentPlayer.give("EX1_015")
	# Play the coin
	coin = game.currentPlayer.getById("GAME_005")
	coin.play()
	# put novice on the board. it should draw 1 card
	novice.play()
	game.endTurn()

	# play an archer on the novice
	archer = game.currentPlayer.give("CS2_189")
	archer.play(target=novice)
	game.endTurn()

	# get a murloc tidehunter
	murloc = game.currentPlayer.give("EX1_506")
	# play it. it should summon a 1/1
	murloc.play()
	game.endTurn()

	archer = game.currentPlayer.give("CS2_189")
	healtotem = game.currentPlayer.give("NEW1_009")

	# play archer on footman, then play totem. totem will heal footman.
	archer.play(target=footman)
	healtotem.play()
	game.endTurn()

	print(game.player1.field)
	print(game.player2.field)



if __name__ == "__main__":
	main()
