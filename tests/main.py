#!/usr/bin/env python
import sys; sys.path.append("..")
import fireplace


def main():
	deck1 = fireplace.Deck.randomDraft(hero=fireplace.heroes.MAGE)
	deck2 = fireplace.Deck.randomDraft(hero=fireplace.heroes.WARRIOR)
	player1 = fireplace.Player(name="Player1", deck=deck1)
	player2 = fireplace.Player(name="Player2", deck=deck2)

	game = fireplace.Game(players=(player1, player2))
	game.start()

	# Let's give player1 a Novice Engineer
	card = game.player1.addToHand(fireplace.cards.Card.byId("EX1_015"))


	print(game.player1.hand)
	print(game.player2.hand)


if __name__ == "__main__":
	main()
