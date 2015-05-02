#!/usr/bin/env python
import sys; sys.path.append("..")
from fireplace import heroes
from fireplace import player
from fireplace import game
import logging
from fireplace.utils import randomDraft

logging.getLogger().setLevel(logging.DEBUG)


def main():

	deck1 = randomDraft(hero=heroes.MAGE)
	deck2 = randomDraft(hero=heroes.WARRIOR)
	player1 = player.Player(name="Player1")
	player1.prepareDeck(deck1, heroes.MAGE)
	player2 = player.Player(name="Player2")
	player2.prepareDeck(deck2, heroes.WARRIOR)

	gm = game.Game(players=(player1, player2))
	gm.start()

	while True:
		heropower = gm.currentPlayer.hero.power
		# always play the hero power, just for kicks
		if heropower.isPlayable():
			if heropower.hasTarget():
				heropower.play(target=heropower.targets[0])
			else:
				heropower.play()
		# iterate over our hand and play whatever is playable
		for card in gm.currentPlayer.hand:
			if card.isPlayable():
				if card.hasTarget():
					card.play(target=card.targets[0])
				else:
					card.play()
			else:
				print("Not playing", card)
		# attack with whatever minions can attack
		for minion in gm.currentPlayer.field:
			if minion.canAttack():
				minion.attack(gm.currentPlayer.opponent.hero)
		# attack with the hero
		if gm.currentPlayer.hero.canAttack():
			print("Attacking with the hero")
			gm.currentPlayer.hero.attack(gm.currentPlayer.opponent.hero)
		gm.endTurn()


if __name__ == "__main__":
	main()