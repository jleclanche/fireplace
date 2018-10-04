from ..utils import *


##
# Minions

class UNG_201:
	"""Primalfin Totem"""
	events = OWN_TURN_END.on(Summon(CONTROLLER, "UNG_201t"))


class UNG_202:
	"""Fire Plume Harbinger"""
	play = Buff(FRIENDLY_HAND + ELEMENTAL, "UNG_202e")


class UNG_202e:
	events = REMOVED_IN_PLAY
	tags = {GameTag.COST: -1}


class UNG_208:
	"""Stone Sentinel"""
	play = PLAYED_ELEMENTAL_LAST_TURN(CONTROLLER) & (Summon(CONTROLLER, "UNG_208t") * 2)


class UNG_211:
	"""Kalimos, Primal Lord"""
	play = (
		PLAYED_ELEMENTAL_LAST_TURN(CONTROLLER) &
		DISCOVER(["UNG_211a", "UNG_211b", "UNG_211c", "UNG_211d"])
	)


class UNG_938:
	"""Hot Spring Guardian"""
	play = Heal(TARGET, 3)


##
# Spells

class UNG_025:
	"""Volcano"""
	def play(self):
		count = self.controller.get_spell_damage(15)
		yield Hit(ALL_MINIONS, 1) * count


class UNG_817:
	"""Tidal Surge"""
	play = Hit(TARGET, 4), Heal(FRIENDLY_HERO, 4)


class UNG_942:
	"""Unite the Murlocs"""
	events = Summon(CONTROLLER, MURLOC).after(CompleteQuest(SELF))
	reward = Destroy(SELF), Give(CONTROLLER, "UNG_942t")


class UNG_942t:
	play = Give(CONTROLLER, RandomMurloc()) * 10


class UNG_956:
	"""Spirit Echo"""
	play = Buff(FRIENDLY_MINIONS, "UNG_956e")


class UNG_956e:
	deathrattle = Give(CONTROLLER, Copy(SELF))
	tags = {GameTag.DEATHRATTLE: True}
