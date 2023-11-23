from ..utils import *


class UNG_999t10e:
	"""Shrouding Mist"""
	events = OWN_TURN_BEGIN.on(Unstealth(OWNER), Destroy(SELF))


# Poison Spit
UNG_999t13e = buff(poisonous=True)


# Volcanic Might
UNG_999t14e = buff(+1, +1)


class UNG_999t2e:
	"""Living Spores"""
	deathrattle = Summon(CONTROLLER, "UNG_999t2t1") * 2


# Flaming Claws
UNG_999t3e = buff(atk=3)


# Rocky Carapace
UNG_999t4e = buff(health=3)


# Liquid Membrane
UNG_999t5e = buff(
	cant_be_targeted_by_spells=True,
	cant_be_targeted_by_hero_powers=True
)


# Massive
UNG_999t6e = buff(taunt=True)


class UNG_999t7e:
	"""Lightning Speed"""
	windfury = SET(1)


class UNG_999t8e:
	"""Crackling Shield"""
	def apply(self, target):
		self.game.trigger(self, (GiveDivineShield(target), ), None)
