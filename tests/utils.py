import sys; sys.path.append("..")
import random
import fireplace.cards
from fireplace.cards.heroes import *
from hearthstone.enums import *
from fireplace.game import BaseGame, CoinRules, Game
from fireplace.brawls import *
from fireplace.player import Player
from fireplace.utils import random_draft
from fireplace.logging import log


# Token minions
ANIMATED_STATUE = "LOEA04_27"
GOLDSHIRE_FOOTMAN = "CS1_042"
TARGET_DUMMY = "GVG_093"
KOBOLD_GEOMANCER = "CS2_142"
SPELLBENDERT = "tt_010a"
CHICKEN = "GVG_092t"
IMP = "EX1_598"
MURLOC = "LOEA10_3"
WISP = "CS2_231"
WHELP = "ds1_whelptoken"

# Token spells
INNERVATE = "EX1_169"
MOONFIRE = "CS2_008"
CIRCLE_OF_HEALING = "EX1_621"
DREAM = "DREAM_04"
SILENCE = "EX1_332"
THE_COIN = "GAME_005"
HAND_OF_PROTECTION = "EX1_371"
TIME_REWINDER = "PART_002"
SOULFIRE = "EX1_308"
UNSTABLE_PORTAL = "GVG_003"

# Token weapon
LIGHTS_JUSTICE = "CS2_091"

# Debug spells
DAMAGE_5 = "XXX_002"
RESTORE_1 = "XXX_003"
DESTROY = "XXX_005"
DESTROY_DECK = "XXX_047"

# Collectible cards excluded from random drafts
BLACKLIST = (
	"GVG_007",  # Flame Leviathan
	"AT_022",  # Fist of Jaraxxus
	"AT_130",  # Sea Reaver
)

_draftcache = {}


def _draft(hero, exclude):
	# random_draft() is fairly slow, this caches the drafts
	if (hero, exclude) not in _draftcache:
		_draftcache[(hero, exclude)] = random_draft(hero, exclude + BLACKLIST)
	return _draftcache[(hero, exclude)], hero


_heroes = fireplace.cards.filter(collectible=True, type=CardType.HERO)


class BaseTestGame(CoinRules, BaseGame):
	def start(self):
		super().start()
		self.player1.max_mana = 10
		self.player2.max_mana = 10


def _select_heroes(hero1=None, hero2=None):
	if hero1 is None:
		hero1 = random.choice(_heroes)
	if hero2 is None:
		hero2 = random.choice(_heroes)
	return (hero1, hero2)


def _empty_mulligan(game):
	for player in game.players:
		if player.choice:
			player.choice.choose()


def prepare_game(hero1=None, hero2=None, exclude=(), game_class=BaseTestGame):
	log.info("Initializing a new game")
	heroes = _select_heroes(hero1, hero2)
	player1 = Player("Player1", *_draft(hero=heroes[0], exclude=exclude))
	player2 = Player("Player2", *_draft(hero=heroes[1], exclude=exclude))
	game = game_class(players=(player1, player2))
	game.start()
	_empty_mulligan(game)
	game.first_turn()

	return game


def prepare_empty_game(hero1=None, hero2=None, game_class=BaseTestGame):
	log.info("Initializing a new game with empty decks")
	heroes = _select_heroes(hero1, hero2)
	player1 = Player("Player1", [], heroes[0])
	player1.cant_fatigue = True
	player2 = Player("Player2", [], heroes[1])
	player2.cant_fatigue = True
	game = game_class(players=(player1, player2))
	game.start()
	_empty_mulligan(game)
	game.first_turn()

	return game
