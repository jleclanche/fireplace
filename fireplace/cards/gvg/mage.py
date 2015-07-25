from ..utils import *


##
# Minions

# Snowchugger
class GVG_002:
	events = Damage().on(
		lambda self, target, amount, source: source is self and Freeze(target)
	)


# Goblin Blastmage
class GVG_004:
	play = Find(FRIENDLY_MINIONS + MECH) & Hit(RANDOM_ENEMY_CHARACTER, 1) * 4


# Flame Leviathan
class GVG_007:
	events = Draw(CONTROLLER, SELF).on(Hit(ALL_CHARACTERS, 2))


# Illuminator
class GVG_089:
	events = OWN_TURN_END.on(Find(FRIENDLY_SECRETS) & Heal(FRIENDLY_HERO, 4))


##
# Spells

# Flamecannon
class GVG_001:
	play = Hit(RANDOM_ENEMY_MINION, 4)


# Unstable Portal
class GVG_003:
	play = Buff(Give(CONTROLLER, RandomMinion()), "GVG_003e")


# Echo of Medivh
class GVG_005:
	play = Give(CONTROLLER, Copy(FRIENDLY_MINIONS))
