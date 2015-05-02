#!/usr/bin/env python
import sys; sys.path.append("..")
import fireplace.heroes
import logging
from fireplace.game import Game
from fireplace.player import Player
from fireplace.utils import randomDraft


logging.getLogger().setLevel(logging.DEBUG)


def main():
	deck1 = randomDraft(hero=fireplace.heroes.MAGE)
	deck2 = randomDraft(hero=fireplace.heroes.WARRIOR)
	player1 = Player(name="Player1")
	player1.prepareDeck(deck1, fireplace.heroes.MAGE)
	player2 = Player(name="Player2")
	player2.prepareDeck(deck2, fireplace.heroes.WARRIOR)

	game = Game(players=(player1, player2))
	game.start()

	while True:
		heropower = game.currentPlayer.hero.power
		# always play the hero power, just for kicks
		if heropower.isPlayable():
			if heropower.hasTarget():
				heropower.play(target=heropower.targets[0])
			else:
				heropower.play()
		# iterate over our hand and play whatever is playable
		for card in game.currentPlayer.hand:
			if card.isPlayable():
				if card.hasTarget():
					card.play(target=card.targets[0])
				else:
					card.play()
			else:
				print("Not playing", card)
		# attack with whatever minions can attack
		for minion in game.currentPlayer.field:
			if minion.canAttack():
				minion.attack(game.currentPlayer.opponent.hero)
		# attack with the hero
		if game.currentPlayer.hero.canAttack():
			print("Attacking with the hero")
			game.currentPlayer.hero.attack(game.currentPlayer.opponent.hero)
		game.endTurn()


if __name__ == "__main__":
	main()
