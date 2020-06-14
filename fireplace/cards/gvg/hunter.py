from ..utils import *


##
# Minions

class GVG_046:
	"""King of Beasts"""
	play = Buff(SELF, "GVG_046e") * Count(FRIENDLY_MINIONS + BEAST)


GVG_046e = buff(atk=1)


class GVG_048:
	"""Metaltooth Leaper"""
	play = Buff(RANDOM(FRIENDLY_MINIONS + MECH - SELF), "GVG_048e")


GVG_048e = buff(atk=2)


class GVG_049:
	"""Gahz'rilla"""
	events = SELF_DAMAGE.on(Buff(SELF, "GVG_049e"))


class GVG_049e:
	atk = lambda self, i: i * 2


class GVG_087:
	"""Steamwheedle Sniper"""
	update = Refresh(CONTROLLER, {GameTag.STEADY_SHOT_CAN_TARGET: True})


##
# Spells

class GVG_017:
	"""Call Pet"""
	play = Draw(CONTROLLER).then(
		Find(BEAST + Draw.CARD) & Buff(Draw.CARD, "GVG_017e")
	)


@custom_card
class GVG_017e:
	tags = {
		GameTag.CARDNAME: "Call Pet Buff",
		GameTag.CARDTYPE: CardType.ENCHANTMENT,
		GameTag.COST: -4,
	}


class GVG_026:
	"""Feign Death"""
	play = Deathrattle(FRIENDLY_MINIONS)


class GVG_073:
	"""Cobra Shot"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Hit(TARGET | ENEMY_HERO, 3)


##
# Weapons

class GVG_043:
	"""Glaivezooka"""
	play = Buff(RANDOM_FRIENDLY_MINION, "GVG_043e")


GVG_043e = buff(atk=1)
