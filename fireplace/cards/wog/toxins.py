"""
Xaril's Toxins
"""

from ..utils import *


class OG_080b:
	"""Kingsblood Toxin"""
	play = Draw(CONTROLLER)


class OG_080c:
	"""Bloodthistle Toxin"""
	requirements = {
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Bounce(TARGET), Buff(TARGET, "EX1_144e")


class OG_080ae:
	tags = {
		GameTag.CARDNAME: "Bloodthistle",
		GameTag.CARDTYPE: CardType.ENCHANTMENT,
		GameTag.COST: -2,
	}
	events = REMOVED_IN_PLAY


class OG_080d:
	"""Briarthorn Toxin"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Buff(TARGET, "OG_080ee")


OG_080ee = buff(atk=3)


class OG_080e:
	"""Fadeleaf Toxin"""
	requirements = {
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = (
		Buff(TARGET - STEALTH, "OG_080de"),
		Stealth(TARGET)
	)


class OG_080de:
	"""Fadeleaf"""
	events = OWN_TURN_BEGIN.on(Unstealth(OWNER), Destroy(SELF))


class OG_080f:
	"""Firebloom Toxin"""
	requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Hit(TARGET, 2)
