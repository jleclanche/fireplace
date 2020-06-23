from ..utils import *


##
# Minions

class CFM_020:
	"""Raza the Chained"""
	play = Buff(CONTROLLER, "CFM_020e")


class CFM_020e:
	update = Refresh(FRIENDLY_HERO_POWER, {GameTag.COST: SET(0)})


class CFM_605:
	"""Drakonid Operative"""
	powered_up = HOLDING_DRAGON

	def play(self):
		decklist = [i.id for i in self.controller.opponent.deck]
		if decklist:
			yield HOLDING_DRAGON & DISCOVER(RandomID(*decklist))


class CFM_606:
	"""Mana Geode"""
	events = Heal(SELF).on(Summon(CONTROLLER, "CFM_606t"))


class CFM_626:
	"""Kabal Talonpriest"""
	requirements = {
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
	play = Buff(TARGET, "CFM_626e")


CFM_626e = buff(health=3)


class CFM_657:
	"""Kabal Songstealer"""
	requirements = {
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_NONSELF_TARGET: 0,
		PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
	play = Silence(TARGET)


##
# Spells

class CFM_603:
	"""Potion of Madness"""
	requirements = {
		PlayReq.REQ_ENEMY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_NUM_MINION_SLOTS: 1,
		PlayReq.REQ_TARGET_MAX_ATTACK: 2,
		PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Steal(TARGET), Buff(TARGET, "CFM_603e")


class CFM_603e:
	events = [
		TURN_END.on(Destroy(SELF), Steal(OWNER, OPPONENT)),
		Silence(OWNER).on(Steal(OWNER, OPPONENT))
	]
	tags = {GameTag.CHARGE: True}


class CFM_604:
	"""Greater Healing Potion"""
	requirements = {PlayReq.REQ_FRIENDLY_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Heal(TARGET, 12)


class CFM_661:
	"""Pint-Size Potion"""
	play = Buff(ENEMY_MINIONS, "CFM_661e")


CFM_661e = buff(atk=-3)


class CFM_662:
	"""Dragonfire Potion"""
	play = Hit(ALL_MINIONS - DRAGON, 5)
