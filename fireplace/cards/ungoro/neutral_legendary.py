from ..utils import *


##
# Minions

class UNG_840:
	"""Hemet, Jungle Hunter"""
	play = Destroy(FRIENDLY_DECK + (COST <= 3))


class UNG_843:
	"""The Voraxx"""
	events = Play(CONTROLLER, SPELL, SELF).after(
		Summon(Play.CARD, "UNG_999t2t1").then(Battlecry(Summon.TARGET, Play.CARD))
	)


class UNG_851:
	"""Elise the Trailblazer"""
	play = Shuffle(CONTROLLER, "UNG_851t1")


class UNG_851t1:
	play = Give(CONTROLLER, RandomCollectible(card_set=27)) * 5  # CardSet.UNGORO


class UNG_900:
	"""Spiritsinger Umbra"""
	events = Summon(CONTROLLER, DEATHRATTLE).after(
		Deathrattle(Summon.CARD)
	)


class UNG_907:
	"""Ozruk"""
	play = Buff(SELF, "UNG_907e") * NUM_EMELMENTAL_PALYED_LAST_TURN


UNG_907e = buff(health=5)
