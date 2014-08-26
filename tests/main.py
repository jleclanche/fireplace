#!/usr/bin/env python
import sys; sys.path.append("..")
import fireplace
import logging

logging.getLogger().setLevel(logging.INFO)


def main():
	deck1 = fireplace.Deck.randomDraft(hero=fireplace.heroes.MAGE)
	deck2 = fireplace.Deck.randomDraft(hero=fireplace.heroes.WARRIOR)
	player1 = fireplace.Player(name="Player1", deck=deck1)
	player2 = fireplace.Player(name="Player2", deck=deck2)

	game = fireplace.Game(players=(player1, player2))
	game.start()

	# Turn 1 pass
	game.endTurn()

	logging.info("Giving player a Novice Engineer")
	card = game.player2.addToHand(fireplace.cards.Card.byId("EX1_015"))
	# put it on the board. it should draw 1 card
	card.play()

	print(game.player1.hand)
	print(game.player1.field)
	print(game.player2.hand)
	print(game.player2.field)


if __name__ == "__main__":
	main()
