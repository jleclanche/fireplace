from ..utils import *


##
# Minions

class UNG_022:
	"""Mirage Caller"""
	play = Summon(CONTROLLER, Buff(ExactCopy(TARGET), "UNG_022e"))


class UNG_022e:
	atk = SET(1)
	max_health = SET(1)


class UNG_032:
	"""Crystalline Oracle"""
	deathrattle = Give(CONTROLLER, Copy(RANDOM(ENEMY_DECK)))


class UNG_034:
	"""Radiant Elemental"""
	update = Refresh(FRIENDLY_HAND + SPELL, {GameTag.COST: -1})


class UNG_035:
	"""Curious Glimmerroot"""
	play = Glimmerroot()


class UNG_037:
	"""Tortollan Shellraiser"""
	deathrattle = Buff(FRIENDLY_MINIONS, "UNG_037e")


UNG_037e = buff(+1, +1)


class UNG_963:
	"""Lyra the Sunshard"""
	events = OWN_SPELL_PLAY.on(Give(CONTROLLER, RandomSpell(card_class=CardClass.PRIEST)))


##
# Spells

class UNG_029:
	"""Shadow Visions"""
	play = DISCOVER(Copy(RANDOM(FRIENDLY_DECK + SPELL)))


class UNG_030:
	"""Binding Heal"""
	play = Heal(TARGET | FRIENDLY_HERO, 5)


class UNG_854:
	"""Free From Amber"""
	play = DISCOVER(CONTROLLER, RandomMinion(cost=[8, 9, 10, 11, 12, 20, 25]))


class UNG_940:
	"""Awaken the Makers"""
	events = Summon(CONTROLLER, DEATHRATTLE).after(CompleteQuest(SELF))
	reward = Destroy(SELF), Give(CONTROLLER, "UNG_940t8")


class UNG_940t8:
	play = SetCurrentHealth(FRIENDLY_HERO, 15)
