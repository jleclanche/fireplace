from ..utils import *


##
# Minions

class UNG_078:
	"""Tortollan Forager"""
	play = Give(CONTROLLER, RandomMinion(atk=list(range(5, 30))))


class UNG_086:
	"""Giant Anaconda"""
	deathrattle = Summon(CONTROLLER, RANDOM(FRIENDLY_HAND + (ATK >= 5)))


class UNG_100:
	"""Verdant Longneck"""
	play = Adapt(SELF)


class UNG_101:
	"""Shellshifter"""
	choose = ("UNG_101a", "UNG_101b")
	play = ChooseBoth(CONTROLLER) & Morph(SELF, "UNG_101t3")


class UNG_101a:
	play = Morph(SELF, "UNG_101t")


class UNG_101b:
	play = Morph(SELF, "UNG_101t2")


class UNG_109:
	"""Elder Longneck"""
	play = Find(FRIENDLY_MINIONS + (ATK >= 5)) & Adapt(SELF)


##
# Spells

class UNG_103:
	"""Evolving Spores"""
	play = Adapt(FRIENDLY_MINIONS)


class UNG_108:
	"""Earthen Scales"""
	play = Buff(TARGET, "UNG_108e").then(GainArmor(FRIENDLY_HERO, ATK(Buff.TARGET)))


UNG_108e = buff(+1, +1)


class UNG_111:
	"""Living Mana"""
	play = (MANA(CONTROLLER) > 0) & (
		FULL_BOARD | (
			GainEmptyMana(CONTROLLER, -1),
			Summon(CONTROLLER, "UNG_111t1"),
			Battlecry(SELF, None)
		)
	)


class UNG_111t1:
	deathrattle = GainEmptyMana(CONTROLLER, 1)


class UNG_116:
	"""Jungle Giants"""
	progress_total = 5
	quest = Summon(CONTROLLER, MINION + (ATK >= 5)).after(AddProgress(SELF, Summon.CARD))
	reward = Give(CONTROLLER, "UNG_116t")


class UNG_116t:
	play = Buff(FRIENDLY_DECK + MINION, "UNG_116te")


class UNG_116te:
	cost = SET(0)
	events = REMOVED_IN_PLAY
