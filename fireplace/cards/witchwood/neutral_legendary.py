from ..utils import *


##
# Minions

class GIL_198:
	"""Azalina Soulthief"""
	# <b>Battlecry:</b> Replace your hand with a copy of your_opponent's.
	pass


class GIL_578:
	"""Countess Ashmore"""
	# [x]<b>Battlecry:</b> Draw a <b>Rush</b>, <b>Lifesteal</b>, and <b>Deathrattle</b>
	# card from your deck.
	pass


class GIL_620:
	"""Dollmaster Dorian"""
	# Whenever you draw a minion, summon a 1/1 copy of it.
	pass


class GIL_692:
	"""Genn Greymane"""
	# [x]<b>Start of Game:</b> If your deck has only even- Cost cards, your starting Hero
	# Power costs (1).
	events = GameStart.on(
		EvenCost(STARTING_DECK) & Buff(FRIENDLY_HERO_POWER, "GIL_692e")
	)


class GIL_692e:
	cost = SET(1)


class GIL_826:
	"""Baku the Mooneater"""
	# [x]<b>Start of Game:</b> If your deck has only odd- Cost cards, upgrade your Hero
	# Power.
	events = GameStart.on(
		OddCost(STARTING_DECK) & UPGRADE_HERO_POWER
	)
