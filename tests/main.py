#!/usr/bin/env python
import sys; sys.path.append("..")
import fireplace
import logging
import random

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

	# Play the coin
	coin = game.currentPlayer.getById("GAME_005")
	coin.play()

	if random.randint(0, 1):
		# novice should draw 1 card
		card = game.currentPlayer.give("EX1_015")
	else:
		# succubus should discard 1 card
		card = game.currentPlayer.give("EX1_306")
	card.play()
	game.endTurn()

	# play an archer on the opponent's minion
	archer = game.currentPlayer.give("CS2_189")
	archer.play(target=card)
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
