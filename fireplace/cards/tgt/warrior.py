from ..utils import *


##
# Minions

class AT_066:
	"""Orgrimmar Aspirant"""
	inspire = Buff(FRIENDLY_WEAPON, "AT_066e")


AT_066e = buff(atk=1)


class AT_067:
	"""Magnataur Alpha"""
	events = Attack(SELF).on(CLEAVE)


class AT_069:
	"""Sparring Partner"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
	play = Taunt(TARGET)


class AT_071:
	"""Alexstrasza's Champion"""
	powered_up = HOLDING_DRAGON
	play = powered_up & Buff(SELF, "AT_071e")


AT_071e = buff(atk=1, charge=True)


class AT_072:
	"""Varian Wrynn"""
	play = (Draw(CONTROLLER) * 3).then(
		Find(MINION + Draw.CARD) & Summon(CONTROLLER, Draw.CARD)
	)


class AT_130:
	"""Sea Reaver"""
	draw = Hit(FRIENDLY_MINIONS, 1)


##
# Spells

class AT_064:
	"""Bash"""
	requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Hit(TARGET, 3), GainArmor(FRIENDLY_HERO, 3)


class AT_068:
	"""Bolster"""
	play = Buff(FRIENDLY_MINIONS + TAUNT, "AT_068e")


AT_068e = buff(+2, +2)


##
# Weapons

class AT_065:
	"""King's Defender"""
	play = Find(FRIENDLY_MINIONS + TAUNT) & Buff(SELF, "AT_065e")


AT_065e = buff(health=1)
