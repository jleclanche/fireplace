#!/usr/bin/env python
import sys; sys.path.append("..")
import fireplace.heroes
import logging
import random
from fireplace.game import Game
from fireplace.player import Player
from fireplace.utils import randomDraft


logging.getLogger().setLevel(logging.DEBUG)


def main():
	deck1 = randomDraft(hero=fireplace.heroes.MAGE)
	deck2 = randomDraft(hero=fireplace.heroes.WARRIOR)
	player1 = Player(name="Player1")
	player1.prepare_deck(deck1, fireplace.heroes.MAGE)
	player2 = Player(name="Player2")
	player2.prepare_deck(deck2, fireplace.heroes.WARRIOR)

	game = Game(players=(player1, player2))
	game.start()

	while True:
		heropower = game.current_player.hero.power
		# always play the hero power, just for kicks
		if heropower.is_playable():
			if heropower.has_target():
				heropower.play(target=random.choice(heropower.targets))
			else:
				heropower.play()
		# iterate over our hand and play whatever is playable
		for card in game.current_player.hand:
			if card.is_playable():
				if card.has_target():
					card.play(target=random.choice(card.targets))
				else:
					card.play()
			else:
				print("Not playing", card)

		# Randomly attack with whatever can attack
		for character in game.current_player.characters:
			if character.can_attack():
				character.attack(random.choice(character.targets))

		game.end_turn()


if __name__ == "__main__":
	main()
