from ..utils import *


##
# Minions

class GVG_110:
	"""Dr. Boom"""
	play = Summon(CONTROLLER, "GVG_110t") * 2


class GVG_110t:
	"""Boom Bot"""
	deathrattle = Hit(RANDOM_ENEMY_CHARACTER, RandomNumber(1, 2, 3, 4))


class GVG_111:
	"""Mimiron's Head"""
	events = OWN_TURN_BEGIN.on(
		(Count(FRIENDLY_MINIONS + MECH) >= 3) &
		(Destroy(FRIENDLY_MINIONS + MECH), Deaths(), Summon(CONTROLLER, "GVG_111t"))
	)


class GVG_111t:
	tags = {GameTag.WINDFURY: 3}


class GVG_112:
	"""Mogor the Ogre"""
	events = Attack(MINION).on(
		COINFLIP & Retarget(
			Attack.ATTACKER,
			RANDOM(ALL_CHARACTERS - Attack.DEFENDER - CONTROLLED_BY(Attack.ATTACKER))
		)
	)


class GVG_113:
	"""Foe Reaper 4000"""
	events = Attack(SELF).on(CLEAVE)


class GVG_114:
	"""Sneed's Old Shredder"""
	deathrattle = Summon(CONTROLLER, RandomLegendaryMinion())


class GVG_115:
	"""Toshley"""
	play = deathrattle = Give(CONTROLLER, RandomSparePart())


class GVG_116:
	"""Mekgineer Thermaplugg"""
	events = Death(ENEMY + MINION).on(Summon(CONTROLLER, "EX1_029"))


class GVG_117:
	"""Gazlowe"""
	events = Play(CONTROLLER, SPELL + (COST == 1)).on(
		Give(Play.PLAYER, RandomMech())
	)


class GVG_118:
	"""Troggzor the Earthinator"""
	events = Play(OPPONENT, SPELL).on(Summon(CONTROLLER, "GVG_068"))


class GVG_119:
	"""Blingtron 3000"""
	play = Summon(ALL_PLAYERS, RandomWeapon())


class GVG_120:
	"""Hemet Nesingwary"""
	requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0, PlayReq.REQ_TARGET_WITH_RACE: 20}
	play = Destroy(TARGET)
