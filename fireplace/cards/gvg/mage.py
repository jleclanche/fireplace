from ..utils import *


##
# Minions

class GVG_002:
	"""Snowchugger"""
	events = Damage(CHARACTER, None, SELF).on(Freeze(Damage.TARGET))


class GVG_004:
	"""Goblin Blastmage"""
	powered_up = Find(FRIENDLY_MINIONS + MECH)
	play = powered_up & Hit(RANDOM_ENEMY_CHARACTER, 1) * 4


class GVG_007:
	"""Flame Leviathan"""
	draw = Hit(ALL_CHARACTERS, 2)


##
# Spells

class GVG_001:
	"""Flamecannon"""
	requirements = {PlayReq.REQ_MINIMUM_ENEMY_MINIONS: 1}
	play = Hit(RANDOM_ENEMY_MINION, 4)


class GVG_003:
	"""Unstable Portal"""
	play = Give(CONTROLLER, RandomMinion()).then(Buff(Give.CARD, "GVG_003e"))


@custom_card
class GVG_003e:
	tags = {
		GameTag.CARDNAME: "Unstable Portal Buff",
		GameTag.CARDTYPE: CardType.ENCHANTMENT,
		GameTag.COST: -3,
	}

	events = REMOVED_IN_PLAY


class GVG_005:
	"""Echo of Medivh"""
	play = Give(CONTROLLER, Copy(FRIENDLY_MINIONS))
