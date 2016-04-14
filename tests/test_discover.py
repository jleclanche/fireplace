from utils import *

DISCOVER_TEST_CLASS_STR = MAGE
DISCOVER_TEST_CLASS = CardClass.MAGE

MUSEUM_CURATOR = "LOE_006"
DARK_PEDDLER = "LOE_023"
JEWELED_SCARAB = "LOE_029"


def _setup_normal():
	return prepare_empty_game(DISCOVER_TEST_CLASS_STR, DISCOVER_TEST_CLASS_STR)


def _setup_ragnaros():
	game = prepare_empty_game(DISCOVER_TEST_CLASS_STR, DISCOVER_TEST_CLASS_STR)

	majordomo = game.player1.give("BRM_027")
	majordomo.play()
	majordomo.destroy()
	assert game.player1.hero.id == "BRM_027h"
	game.end_turn(); game.end_turn()

	return game


def _setup_jaraxxus():
	game = prepare_empty_game(DISCOVER_TEST_CLASS_STR, DISCOVER_TEST_CLASS_STR)

	jaraxxus = game.player1.give("EX1_323")
	jaraxxus.play()
	assert game.player1.hero.id == "EX1_323h"
	game.end_turn(); game.end_turn()

	return game


def _discover_and_trash(game, card):
	game.player1.choice.choose(random.choice(game.player1.choice.cards))
	card.destroy()
	game.player1.discard_hand()
	game.end_turn(); game.end_turn()
	

def _discover_expecting_class(game, cardid, expectedclass, depth=None):
	if depth is None:
		depth = 10

	for d in range(depth):
		discover_card = game.player1.give(cardid)
		discover_card.play()
		for card in game.player1.choice.cards:
			assert card.data.card_class == expectedclass or card.data.card_class == CardClass.NEUTRAL

		_discover_and_trash(game, discover_card)


def _discover_disproving_class(game, cardid, disproveclass, depth=None):
	if depth is None:
		depth = 100

	success = False
	for d in range(depth):
		discover_card = game.player1.give(cardid)
		discover_card.play()
		for card in game.player1.choice.cards:
			if card.data.card_class != disproveclass and card.data.card_class != CardClass.NEUTRAL:
				success = True
				break

		_discover_and_trash(game, discover_card)

		if success:
			break

	assert success


def test_class_discover_as_ragnaros():
	game = _setup_ragnaros()
	_discover_expecting_class(game, DARK_PEDDLER, CardClass.WARLOCK)
	_discover_expecting_class(game, MUSEUM_CURATOR, CardClass.PRIEST)


def test_neutral_discover_as_ragnaros():
	game = _setup_ragnaros()
	_discover_disproving_class(game, JEWELED_SCARAB, DISCOVER_TEST_CLASS)


def test_class_discover_as_jaraxxus():
	game = _setup_jaraxxus()
	_discover_expecting_class(game, MUSEUM_CURATOR, CardClass.WARLOCK)


def test_neutral_discover_as_jaraxxus():
	game = _setup_jaraxxus()
	_discover_expecting_class(game, JEWELED_SCARAB, CardClass.WARLOCK)


def test_class_discover_as_collectible_hero():
	game = _setup_normal()
	_discover_expecting_class(game, DARK_PEDDLER, DISCOVER_TEST_CLASS)
	_discover_expecting_class(game, MUSEUM_CURATOR, DISCOVER_TEST_CLASS)


def test_neutral_discover_as_collectible_hero():
	game = _setup_normal()
	_discover_expecting_class(game, JEWELED_SCARAB, DISCOVER_TEST_CLASS)
	

def main():
	for name, f in globals().items():
		if name.startswith("test_") and callable(f):
			f()
	print("All tests ran OK")


if __name__ == "__main__":
	main()
