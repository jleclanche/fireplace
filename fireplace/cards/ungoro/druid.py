from ..utils import *


##
# Minions

class UNG_078:
	"""Tortollan Forager"""
	# TODO RandomPicker >= <=
	play = Give(CONTROLLER, RandomMinion(atk=[5, 6, 7, 8, 9, 10, 11, 12, 20]))


class UNG_086:
	"""Giant Anaconda"""
	deathrattle = Summon(CONTROLLER, RANDOM(FRIENDLY_HAND + MINION + (ATK >= 5)))


class UNG_100:
	"""Verdant Longneck"""
	play = Adapt(CONTROLLER, SELF)


class UNG_101:
	"""Shellshifter"""
	choose = ("EX1_165a", "EX1_165b")
	play = ChooseBoth(CONTROLLER) & Morph(SELF, "UNG_101t2")


class UNG_101a:
	play = Morph(SELF, "UNG_101t")


class UNG_101a:
	play = Morph(SELF, "UNG_101t1")


class UNG_109:
	"""Elder Longneck"""
	play = Find(FRIENDLY_HAND + MINION + (ATK >= 5)) & Adapt(CONTROLLER, SELF)


##
# Spells

class UNG_103:
	"""Evolving Spores"""
	play = Adapt(CONTROLLER, FRIENDLY_MINIONS)



class UNG_108:
	"""Earthen Scales"""
	play = Buff(TARGET, "UNG_108e").then(GainArmor(CONTROLLER, ATK(TARGET)))


class UNG_111:
	"""Living Mana"""
	def play(self):
		card = self.card("UNG_111t1")
		while self.controller.max_mana and card.is_summonable():
			yield GainMana(CONTROLLER, -1)
			yield Summon(CONTROLLER, card)


class UNG_111t:
	deathrattle = GainMana(CONTROLLER, 1)


class UNG_116:
	"""Jungle Giants"""
	events = Summon(CONTROLLER, MINION + (ATK >= 5)).after(CompleteQuest(SELF))
	reward = Destroy(SELF), Give(CONTROLLER, "UNG_116t")


class UNG_116t:
	play = Buff(FRIENDLY_DECK + MINION, "UNG_116te")


class UNG_116te:
	"""
	Romper Stompers - (Enchantment)
	Costs (0).
	https://hearthstone.gamepedia.com/Romper_Stompers
	"""
	cost = SET(0)
	events = REMOVED_IN_PLAY