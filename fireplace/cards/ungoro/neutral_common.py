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
	deathrattle = Summon(CONTROLLER, "UNG_201t") * 3


class UNG_073:
	"""Rockpool Hunter"""
	requirements = {
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
		PlayReq.REQ_TARGET_WITH_RACE: 14}
	play = Buff(TARGET, "UNG_073e")


UNG_073e = buff(+1, +1)


class UNG_076:
	"""Eggnapper"""
	deathrattle = Summon(CONTROLLER, "UNG_076t1") * 2


class UNG_082:
	"""Thunder Lizard"""
	play = ELEMENTAL_PLAYED_LAST_TURN & Adapt(SELF)


class UNG_084:
	"""Fire Plume Phoenix"""
	requirements = {PlayReq.REQ_NONSELF_TARGET: 0, PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
	play = Hit(TARGET, 2)


class UNG_205:
	"""Glacial Shard"""
	requirements = {PlayReq.REQ_ENEMY_TARGET: 0, PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
	play = Freeze(TARGET)


class UNG_801:
	"""Nesting Roc"""
	play = (Count(FRIENDLY_MINIONS - SELF) >= 2) & Buff(SELF, "UNG_801e")


UNG_801e = buff(taunt=True)


class UNG_803:
	"""Emerald Reaver"""
	play = Hit(ALL_HEROES, 1)


class UNG_809:
	"""Fire Fly"""
	play = Give(CONTROLLER, "UNG_809t1")


class UNG_818:
	"""Volatile Elemental"""
	deathrattle = Hit(RANDOM_ENEMY_MINION, 3)


class UNG_845:
	"""Igneous Elemental"""
	deathrattle = Give(CONTROLLER, "UNG_809t1") * 2


class UNG_928:
	"""Tar Creeper"""
	update = CurrentPlayer(OPPONENT) & Refresh(SELF, {GameTag.ATK: +2})


class UNG_937:
	"""Primalfin Lookout"""
	play = Find(FRIENDLY_MINIONS + MURLOC - SELF) & DISCOVER(RandomMurloc())
