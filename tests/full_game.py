#!/usr/bin/env python
import sys; sys.path.append("..")
import random
from fireplace.cards.heroes import *
from fireplace.game import Game
from fireplace.player import Player
from fireplace.utils import random_draft


def main():
	deck1 = random_draft(hero=MAGE)
	deck2 = random_draft(hero=WARRIOR)
	player1 = Player(name="Player1")
	player1.prepare_deck(deck1, MAGE)
	player2 = Player(name="Player2")
	player2.prepare_deck(deck2, WARRIOR)

	game = Game(players=(player1, player2))
	game.start()

	for player in game.players:
		print("Can mulligan %r" % (player.choice.cards))
		mull_count = random.randint(0, len(player.choice.cards))
		cards_to_mulligan = random.sample(player.choice.cards, mull_count)
		player.choice.choose(*cards_to_mulligan)

	while True:
		heropower = game.current_player.hero.power
		# always play the hero power, just for kicks
		if heropower.is_usable():
			if heropower.has_target():
				heropower.use(target=random.choice(heropower.targets))
			else:
				heropower.use()
		# iterate over our hand and play whatever is playable
		for card in game.current_player.hand:
			if card.is_playable():
				target = None
				if card.choose_cards:
					card = random.choice(card.choose_cards)
				if card.has_target():
					target = random.choice(card.targets)
				print("Playing %r on %r" % (card, target))
				card.play(target=target)
			else:
				print("Not playing", card)

		# Randomly attack with whatever can attack
		for character in game.current_player.characters:
			if character.can_attack():
				character.attack(random.choice(character.targets))

		game.end_turn()


if __name__ == "__main__":
	main()
