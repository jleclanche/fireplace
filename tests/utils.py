import sys; sys.path.append("..")
import logging
import random
import fireplace.cards
from fireplace.cards.heroes import *
from fireplace.enums import *
from fireplace.game import Game
from fireplace.player import Player
from fireplace.utils import random_draft


logging.getLogger().setLevel(logging.DEBUG)


# Token minions
GOLDSHIRE_FOOTMAN = "CS1_042"
TARGET_DUMMY = "GVG_093"
KOBOLD_GEOMANCER = "CS2_142"
SPELLBENDERT = "tt_010a"
WISP = "CS2_231"
WHELP = "ds1_whelptoken"
WARSONG_COMMANDER = "EX1_084"

# Token spells
MOONFIRE = "CS2_008"
CIRCLE_OF_HEALING = "EX1_621"
DREAM = "DREAM_04"
SILENCE = "EX1_332"
THE_COIN = "GAME_005"
HAND_OF_PROTECTION = "EX1_371"
TIME_REWINDER = "PART_002"
SOULFIRE = "EX1_308"

# Debug spells
RESTORE_1 = "XXX_003"
DESTROY_DECK = "XXX_047"

# Collectible cards excluded from random drafts
BLACKLIST = (
	"GVG_007",  # Flame Leviathan
)

_draftcache = {}


def _draft(hero, exclude):
	# random_draft() is fairly slow, this caches the drafts
	if (hero, exclude) not in _draftcache:
		_draftcache[(hero, exclude)] = random_draft(hero, exclude + BLACKLIST)
	return _draftcache[(hero, exclude)]


_heroes = fireplace.cards.filter(collectible=True, type=CardType.HERO)


class BaseTestGame(Game):
	def start(self):
		super().start()
		self.player1.max_mana = 10
		self.player2.max_mana = 10


def prepare_game(hero1=None, hero2=None, exclude=(), game_class=BaseTestGame):
	print("Initializing a new game")
	if hero1 is None:
		hero1 = random.choice(_heroes)
	if hero2 is None:
		hero2 = random.choice(_heroes)
	deck1 = _draft(hero=hero1, exclude=exclude)
	deck2 = _draft(hero=hero2, exclude=exclude)
	player1 = Player(name="Player1")
	player1.prepare_deck(deck1, hero1)
	player2 = Player(name="Player2")
	player2.prepare_deck(deck2, hero2)
	game = game_class(players=(player1, player2))
	game.start()

	return game


def prepare_empty_game(game_class=BaseTestGame):
	player1 = Player(name="Player1")
	player1.prepare_deck([], random.choice(_heroes))
	player1.cant_fatigue = True
	player2 = Player(name="Player2")
	player2.prepare_deck([], random.choice(_heroes))
	player2.cant_fatigue = True
	game = game_class(players=(player1, player2))
	game.start()

	return game
