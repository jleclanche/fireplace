#!/usr/bin/env python
import sys; sys.path.append("..")
import random
from fireplace import cards
from fireplace.cards.heroes import *
from fireplace.exceptions import GameOver
from fireplace.game import Game
from fireplace.player import Player
from fireplace.utils import random_draft


def play_full_game():
	deck1 = random_draft(hero=MAGE)
	deck2 = random_draft(hero=WARRIOR)
	player1 = Player("Player1", deck1, MAGE)
	player2 = Player("Player2", deck2, WARRIOR)

	game = Game(players=(player1, player2))
	game.start()

	for player in game.players:
		print("Can mulligan %r" % (player.choice.cards))
		mull_count = random.randint(0, len(player.choice.cards))
		cards_to_mulligan = random.sample(player.choice.cards, mull_count)
		player.choice.choose(*cards_to_mulligan)

	while True:
		player = game.current_player

		heropower = player.hero.power
		if heropower.is_usable() and random.random() < 0.1:
			if heropower.has_target():
				heropower.use(target=random.choice(heropower.targets))
			else:
				heropower.use()
			continue

		# iterate over our hand and play whatever is playable
		for card in player.hand:
			if card.is_playable() and random.random() < 0.5:
				target = None
				if card.choose_cards:
					card = random.choice(card.choose_cards)
				if card.has_target():
					target = random.choice(card.targets)
				print("Playing %r on %r" % (card, target))
				card.play(target=target)

				if player.choice:
					choice = random.choice(player.choice.cards)
					print("Choosing card %r" % (choice))
					player.choice.choose(choice)

				continue

		# Randomly attack with whatever can attack
		for character in player.characters:
			if character.can_attack():
				character.attack(random.choice(character.targets))
			continue

		game.end_turn()


def test_full_game():
	try:
		play_full_game()
	except GameOver:
		print("Game completed normally.")


def main():
	cards.db.initialize()
	if len(sys.argv) > 1:
		numgames = sys.argv[1]
		if not numgames.isdigit():
			sys.stderr.write("Usage: %s [NUMGAMES]\n" % (sys.argv[0]))
			exit(1)
		for i in range(int(numgames)):
			test_full_game()
	else:
		test_full_game()


if __name__ == "__main__":
	main()
