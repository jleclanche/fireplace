from ..utils import *


class UNG_999t10e:
	"""Shrouding Mist"""
	tags = {GameTag.STEALTH: True}
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


UNG_999t7e = buff(windfury=True)


class UNG_999t8e:
	"""Crackling Shield"""
	def apply(self, target):
		self.game.trigger(self, (GiveDivineShield(target), ), None)


class UNG_999t10:
	play = Buff(TARGET, "UNG_999t10e")


class UNG_999t2:
	play = Buff(TARGET, "UNG_999t2e")


class UNG_999t3:
	play = Buff(TARGET, "UNG_999t3e")


class UNG_999t4:
	play = Buff(TARGET, "UNG_999t4e")


class UNG_999t5:
	play = Buff(TARGET, "UNG_999t5e")


class UNG_999t6:
	play = Buff(TARGET, "UNG_999t6e")


class UNG_999t7:
	play = Buff(TARGET, "UNG_999t7e")


class UNG_999t8:
	play = Buff(TARGET, "UNG_999t8e")


class UNG_999t13:
	play = Buff(TARGET, "UNG_999t13e")


class UNG_999t14:
	play = Buff(TARGET, "UNG_999t14e")
