from ..utils import *


##
# Minions

# Dr. Boom
class GVG_110:
	play = Summon(CONTROLLER, "GVG_110t") * 2

# Boom Bot
class GVG_110t:
	deathrattle = Hit(RANDOM_ENEMY_CHARACTER, RandomNumber(1, 2, 3, 4))


# Mimiron's Head
class GVG_111:
	events = OWN_TURN_BEGIN.on(
		(Count(FRIENDLY_MINIONS + MECH) >= 4) &
		Destroy(FRIENDLY_MINIONS + MECH), Deaths(), Summon(CONTROLLER, "GVG_111t")
	)


# Mogor the Ogre
class GVG_112:
	events = Attack(MINION).on(COINFLIP & Retarget(Attack.ATTACKER, RANDOM(ALL_CHARACTERS - Attack.DEFENDER - CONTROLLED_BY(Attack.ATTACKER))))


# Foe Reaper 4000
class GVG_113:
	events = Attack(SELF).on(CLEAVE)


# Sneed's Old Shredder
class GVG_114:
	deathrattle = Summon(CONTROLLER, RandomLegendaryMinion())


# Toshley
class GVG_115:
	play = deathrattle = Give(CONTROLLER, RandomSparePart())


# Mekgineer Thermaplugg
class GVG_116:
	events = Death(ENEMY + MINION).on(Summon(CONTROLLER, "EX1_029"))


# Gazlowe
class GVG_117:
	events = Play(CONTROLLER, SPELL + (COST == 1)).on(
		Give(Play.PLAYER, RandomMech())
	)


# Troggzor the Earthinator
class GVG_118:
	events = Play(OPPONENT, SPELL).on(Summon(CONTROLLER, "GVG_068"))


# Blingtron 3000
class GVG_119:
	play = Summon(ALL_PLAYERS, RandomWeapon())


# Hemet Nesingwary
class GVG_120:
	play = Destroy(TARGET)
