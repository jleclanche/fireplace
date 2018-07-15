from ..utils import *


##
# Minions

class GVG_006:
	"""Mechwarper"""
	update = Refresh(FRIENDLY_HAND + MECH, {GameTag.COST: -1})


class GVG_013:
	"""Cogmaster"""
	update = Find(FRIENDLY_MINIONS + MECH) & Refresh(SELF, {GameTag.ATK: +2})


class GVG_065:
	"""Ogre Brute"""
	events = FORGETFUL


class GVG_067:
	"""Stonesplinter Trogg"""
	events = Play(OPPONENT, SPELL).on(Buff(SELF, "GVG_067a"))


GVG_067a = buff(atk=1)


class GVG_068:
	"""Burly Rockjaw Trogg"""
	events = Play(OPPONENT, SPELL).on(Buff(SELF, "GVG_068a"))


GVG_068a = buff(atk=2)


class GVG_069:
	"""Antique Healbot"""
	play = Heal(FRIENDLY_HERO, 8)


class GVG_075:
	"""Ship's Cannon"""
	events = Summon(CONTROLLER, PIRATE).on(Hit(RANDOM_ENEMY_CHARACTER, 2))


class GVG_076:
	"""Explosive Sheep"""
	deathrattle = Hit(ALL_MINIONS, 2)


class GVG_078:
	"""Mechanical Yeti"""
	deathrattle = Give(ALL_PLAYERS, RandomSparePart())


class GVG_082:
	"""Clockwork Gnome"""
	deathrattle = Give(CONTROLLER, RandomSparePart())


class GVG_090:
	"""Madder Bomber"""
	play = Hit(RANDOM_OTHER_CHARACTER, 1) * 6


class GVG_096:
	"""Piloted Shredder"""
	deathrattle = Summon(CONTROLLER, RandomMinion(cost=2))


class GVG_102:
	"""Tinkertown Technician"""
	powered_up = Find(FRIENDLY_MINIONS + MECH)
	play = powered_up & (Buff(SELF, "GVG_102e"), Give(CONTROLLER, RandomSparePart()))


GVG_102e = buff(+1, +1)


class GVG_103:
	"""Micro Machine"""
	# That card ID is not a mistake
	events = TURN_BEGIN.on(Buff(SELF, "GVG_076a"))


GVG_076a = buff(atk=1)
