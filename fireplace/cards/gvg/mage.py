from ..utils import *


##
# Minions

# Snowchugger
class GVG_002:
	events = [
		Damage().on(
			lambda self, target, amount, source: source is self and [Freeze(target)] or []
		)
	]


# Goblin Blastmage
class GVG_004:
	action = [Find(FRIENDLY_MINIONS + MECH) & Hit(RANDOM_ENEMY_CHARACTER, 1) * 4]


# Illuminator
class GVG_089:
	events = [
		OWN_TURN_END.on(
			lambda self, player: player.secrets and [Heal(FRIENDLY_HERO, 4)] or []
		)
	]


##
# Spells

# Flamecannon
class GVG_001:
	action = [Hit(RANDOM_ENEMY_MINION, 4)]


# Unstable Portal
class GVG_003:
	action = [Buff(Give(CONTROLLER, RandomMinion()), "GVG_003e")]


# Echo of Medivh
class GVG_005:
	action = [Give(CONTROLLER, Copy(FRIENDLY_MINIONS))]
