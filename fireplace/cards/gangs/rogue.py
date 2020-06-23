from ..utils import *


##
# Minions

class CFM_342:
	"""Luckydo Buccaneer"""
	powered_up = Find(FRIENDLY_WEAPON + (ATK >= 3))
	play = powered_up & Buff(SELF, "CFM_342e")


CFM_342e = buff(+4, +4)


class CFM_634:
	"""Lotus Assassin"""
	events = Attack(SELF, ALL_MINIONS).after(
		Dead(ALL_MINIONS + Attack.DEFENDER) & Stealth(SELF)
	)


class CFM_691:
	"""Jade Swarmer"""
	deathrattle = SummonJadeGolem(CONTROLLER)


class CFM_693:
	"""Gadgetzan Ferryman"""
	requirements = {
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_FOR_COMBO: 0}
	play = Bounce(TARGET)


class CFM_694:
	"""Shadow Sensei"""
	requirements = {
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_STEALTHED_TARGET: 0,
		PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
	play = Buff(TARGET, "CFM_694e")


CFM_694e = buff(+2, +2)


class CFM_781:
	"""Shaku, the Collector"""
	events = Attack(SELF).on(Give(CONTROLLER, RandomCollectible(card_class=ENEMY_CLASS)))


##
# Spells

class CFM_630:
	"""Counterfeit Coin"""
	play = ManaThisTurn(CONTROLLER, 1)


class CFM_690:
	"""Jade Shuriken"""
	requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Hit(TARGET, 2)
	combo = Hit(TARGET, 2), SummonJadeGolem(CONTROLLER)
