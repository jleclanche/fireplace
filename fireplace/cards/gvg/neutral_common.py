from ..utils import *


##
# Minions

# Mechwarper
class GVG_006:
	update = Refresh(FRIENDLY + MECH + IN_HAND, {GameTag.COST: -1})


# Cogmaster
class GVG_013:
	update = Find(FRIENDLY_MINIONS + MECH) & Refresh(SELF, {GameTag.ATK: +2})


# Stonesplinter Trogg
class GVG_067:
	events = Play(OPPONENT, SPELL).on(Buff(SELF, "GVG_067a"))


# Burly Rockjaw Trogg
class GVG_068:
	events = Play(OPPONENT, SPELL).on(Buff(SELF, "GVG_068a"))


# Antique Healbot
class GVG_069:
	play = Heal(FRIENDLY_HERO, 8)


# Ship's Cannon
class GVG_075:
	events = Summon(CONTROLLER, PIRATE).on(Hit(RANDOM_ENEMY_CHARACTER, 2))


# Explosive Sheep
class GVG_076:
	deathrattle = Hit(ALL_MINIONS, 2)


# Mechanical Yeti
class GVG_078:
	deathrattle = Give(ALL_PLAYERS, RandomSparePart())


# Clockwork Gnome
class GVG_082:
	deathrattle = Give(CONTROLLER, RandomSparePart())


# Madder Bomber
class GVG_090:
	play = Hit(RANDOM_CHARACTER, 1) * 6


# Piloted Shredder
class GVG_096:
	deathrattle = Summon(CONTROLLER, RandomMinion(cost=2))


# Tinkertown Technician
class GVG_102:
	powered_up = Find(FRIENDLY_MINIONS + MECH)
	play = powered_up & (Buff(SELF, "GVG_102e"), Give(CONTROLLER, RandomSparePart()))


# Micro Machine
class GVG_103:
	# That card ID is not a mistake
	events = TURN_BEGIN.on(Buff(SELF, "GVG_076a"))
