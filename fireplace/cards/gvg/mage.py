from ..utils import *


##
# Minions

# Snowchugger
class GVG_002:
	events = Damage(CHARACTER, None, SELF).on(Freeze(Damage.TARGET))


# Goblin Blastmage
class GVG_004:
	powered_up = Find(FRIENDLY_MINIONS + MECH)
	play = powered_up & Hit(RANDOM_ENEMY_CHARACTER, 1) * 4


# Flame Leviathan
class GVG_007:
	draw = Hit(ALL_CHARACTERS, 2)


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
	play = Give(CONTROLLER, RandomMinion()).then(Buff(Give.CARD, "GVG_003e"))

@custom_card
class GVG_003e:
	tags = {
		GameTag.CARDNAME: "Unstable Portal Buff",
		GameTag.CARDTYPE: CardType.ENCHANTMENT,
		GameTag.COST: -3,
	}


# Echo of Medivh
class GVG_005:
	play = Give(CONTROLLER, Copy(FRIENDLY_MINIONS))
