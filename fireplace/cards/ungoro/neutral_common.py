from ..utils import *


##
# Minions

class UNG_001:
	"""Pterrordax Hatchling"""
	play = Adapt(SELF)


class UNG_009:
	"""Ravasaur Runt"""
	play = (Count(FRIENDLY_MINIONS - SELF) >= 2) & Adapt(SELF)


class UNG_010:
	"""Sated Threshadon"""
	deathrattle = Summon("UNG_201t") * 3


class UNG_073:
	"""Rockpool Hunter"""
	play = Buff(TARGET, "UNG_073e")


UNG_073e = buff(+1, +1)


class UNG_076:
	"""Eggnapper"""
	deathrattle = Summon(CONTROLLER, "UNG_076t1") * 3


class UNG_082:
	"""Thunder Lizard"""
	play = PLAYED_ELEMENTAL_LAST_TURN(CONTROLLER) & Adapt(SELF)


class UNG_084:
	"""Fire Plume Phoenix"""
	play = Hit(TARGET, 2)


class UNG_205:
	"""Glacial Shard"""
	play = Freeze(TARGET)


class UNG_801:
	"""Nesting Roc"""
	play = (Count(FRIENDLY_MINIONS - SELF) >= 2) & Taunt(SELF)


class UNG_803:
	"""Emerald Reaver"""
	play = Hit(ALL_HEROES, 1)


class UNG_809:
	"""Fire Fly"""
	play = Give(CONTROLLER, "UNG_809t1")


class UNG_818:
	"""Volatile Elemental"""
	dealthrattle = Hit(RANDOM_ENEMY_MINION, 3)


class UNG_845:
	"""Igneous Elemental"""
	deathrattle = Give(CONTROLLER, "UNG_809t1") * 2


class UNG_928:
	"""Tar Creeper"""
	update = Find(CURRENT_PLAYER + CONTROLLER) | Refresh(SELF, {GameTag.ATK: +2})


class UNG_937:
	"""Primalfin Lookout"""
	play = Find(FRIENDLY_MINIONS - SELF + MURLOC) & DISCOVER(RandomMurloc())
