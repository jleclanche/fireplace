from ..utils import *


##
# Minions

class AT_011:
	"""Holy Champion"""
	events = Heal().on(Buff(SELF, "AT_011e"))


AT_011e = buff(atk=2)


class AT_012:
	"""Spawn of Shadows"""
	inspire = Hit(ALL_HEROES, 4)


class AT_014:
	"""Shadowfiend"""
	events = Draw(CONTROLLER).on(Buff(Draw.CARD, "AT_014e"))


AT_014e = buff(cost=-1)


class AT_018:
	"""Confessor Paletress"""
	inspire = Summon(CONTROLLER, RandomMinion(rarity=Rarity.LEGENDARY))


class AT_116:
	"""Wyrmrest Agent"""
	powered_up = HOLDING_DRAGON
	play = powered_up & Buff(SELF, "AT_116e")


AT_116e = buff(atk=1, taunt=True)


##
# Spells

class AT_013:
	"""Power Word: Glory"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Buff(TARGET, "AT_013e")


class AT_013e:
	events = Attack(OWNER).on(Heal(FRIENDLY_HERO, 4))


class AT_015:
	"""Convert"""
	requirements = {
		PlayReq.REQ_ENEMY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Give(CONTROLLER, Copy(TARGET))


class AT_016:
	"""Confuse"""
	play = Buff(ALL_MINIONS, "AT_016e")


AT_016e = AttackHealthSwapBuff()


class AT_055:
	"""Flash Heal"""
	requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Heal(TARGET, 5)
