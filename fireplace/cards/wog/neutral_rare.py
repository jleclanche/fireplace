from ..utils import *


##
# Minions

class OG_162:
	"""Disciple of C'Thun"""
	requirements = {PlayReq.REQ_NONSELF_TARGET: 0, PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
	play = Hit(TARGET, 2), Buff(CTHUN, "OG_281e", atk=2, max_health=2)


class OG_255:
	"""Doomcaller"""
	play = (
		Buff(CTHUN, "OG_281e", atk=2, max_health=2),
		Find(FRIENDLY + KILLED + CTHUN) & Shuffle(CONTROLLER, "OG_280")
	)


class OG_034:
	"""Silithid Swarmer"""
	update = (NUM_ATTACKS_THIS_TURN(FRIENDLY_HERO) == 0) & (
		Refresh(SELF, {GameTag.CANT_ATTACK: True})
	)


class OG_339:
	"""Skeram Cultist"""
	play = Buff(CTHUN, "OG_281e", atk=2, max_health=2)


class OG_147:
	"""Corrupted Healbot"""
	deathrattle = Heal(ENEMY_HERO, 8)


class OG_161:
	"""Corrupted Seer"""
	play = Hit(ALL_MINIONS - MURLOC, 2)


class OG_254:
	"""Eater of Secrets"""
	play = (
		Buff(SELF, "OG_254e") * Count(ENEMY_SECRETS),
		Destroy(ENEMY_SECRETS)
	)


OG_254e = buff(+1, +1)


class OG_320:
	"""Midnight Drake"""
	play = Buff(SELF, "OG_320e") * Count(FRIENDLY_HAND)


OG_320e = buff(atk=1)


class OG_322:
	"""Blackwater Pirate"""
	update = Refresh(FRIENDLY_HAND + WEAPON, {GameTag.COST: -2})
