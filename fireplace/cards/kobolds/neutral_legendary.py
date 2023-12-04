from ..utils import *


##
# Minions

class LOOT_357:
	"""Marin the Fox"""
	play = Summon(OPPONENT, "LOOT_357l")


class LOOT_357l:
	entourage = ["LOOT_998h", "LOOT_998j", "LOOT_998l", "LOOT_998k"]
	deathrattle = Give(OPPONENT, RandomEntourage())


class LOOT_998h:
	play = Draw(CONTROLLER).then(Give(CONTROLLER, Copy(Draw.CARD)) * (
		MAX_HAND_SIZE(CONTROLLER) - Count(FRIENDLY_HAND)
	))


class LOOT_998j:
	play = Discover(CONTROLLER, RandomLegendaryMinion()).then(
		Summon(CONTROLLER, Discover.CARD) * 2
	)


class LOOT_998l:
	play = (Draw(CONTROLLER) * 3).then(Buff(Draw.CARD, "LOOT_998le"))


class LOOT_998le:
	cost = SET(0)
	events = REMOVED_IN_PLAY


class LOOT_998k:
	play = Morph(FRIENDLY_HAND, RandomLegendaryMinion())
