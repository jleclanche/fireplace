from ..utils import *


##
# Minions

class UNG_011:
	"""Hydrologist"""
	def play(self):
		card_class = self.controller.hero.card_class
		has_secret_card_class = [CardClass.MAGE, CardClass.HUNTER, CardClass.PALADIN, CardClass.ROGUE]
		if cardClass in has_secret_card_class:
			yield GenericChoice(RandomCollectible(secret=True, card_class=card_class))
		else:
			yield GenericChoice(RandomCollectible(secret=True, card_class=CardClass.PALADIN))


class UNG_015:
	"""Sunkeeper Tarim"""
	play = Buff(ALL_MINIONS - SELF, "UNG_015e")


class UNG_015e:
	atk = SET(3)
	max_health = SET(3)


class UNG_953:
	"""Primalfin Champion"""
	# TODO deathrattle = Give(CONTROLLER, YOU_CAST_SPELLS_ON_THIS(SELF))
	pass


class UNG_962:
	"""Lightfused Stegodon"""
	play = Adapt(CONTROLLER, FRIENDLY_MINIONS + ID("CS2_101t"))


##
# Spells

class UNG_004:
	"""Dinosize"""
	play = Buff(TARGET, "UNG_004e")


class UNG_004e:
	atk = SET(10)
	max_health = SET(10)


class UNG_952:
	"""Spikeridged Steed"""
	play = Buff(TARGET, "UNG_952e")


class UNG_952e:
	deathrattle = Summon(CONTROLLER, "UNG_810")
	tags = {GameTag.DEATHRATTLE: True}


class UNG_954:
	"""The Last Kaleidosaur"""
	events = Play(CONTROLLER, SPELL, FRIENDLY_MINIONS).after(CompleteQuest(SELF))
	reward = Destroy(SELF), Give(CONTROLLER, "UNG_954t1")


class UNG_954t1:
	play = (
		Adapt(CONTROLLER, SELF),
		Adapt(CONTROLLER, SELF),
		Adapt(CONTROLLER, SELF),
		Adapt(CONTROLLER, SELF),
		Adapt(CONTROLLER, SELF)
	)


class UNG_960:
	"""Lost in the Jungle"""
	play = Summon(CONTROLLER, "CS2_101t") * 2


class UNG_961:
	"""Adaptation"""
	play = Adapt(CONTROLLER, TARGET)


##
# Weapons

class UNG_950:
	"""Vinecleaver"""
	events = Attack(FRIENDLY_HERO).after(Summon(CONTROLLER, "CS2_101t") * 2)
