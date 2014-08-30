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

	while True:
		for card in game.currentPlayer.hand:
			if card.isPlayable():
				if card.hasTarget():
					card.play(target=card.targets[0])
				else:
					card.play()
			else:
				print("Not playing", card)
		for minion in game.currentPlayer.field:
			if minion.canAttack():
				minion.attack(game.currentPlayer.opponent.hero)
		if game.currentPlayer.hero.canAttack():
			print("Attacking with the hero")
			game.currentPlayer.hero.attack(game.currentPlayer.opponent.hero)
		game.endTurn()


if __name__ == "__main__":
	main()
